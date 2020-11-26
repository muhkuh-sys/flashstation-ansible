# How to use this

First copy the 64bit Ubuntu Raspberry image from [here](https://ubuntu.com/download/raspberry-pi) to a memory card.
There are simple GUI tools for this task:

* [Ubuntu tutorial](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#2-prepare-the-sd-card)
* [balenaEtcher](https://www.balena.io/etcher/)

If you would like to use the command line, make sure that any partitions on the card are ummounted before writing the image.
Replace /dev/SDCARD with the device of the memory card.

```bash
xzcat ubuntu-20.04-preinstalled-server-arm64+raspi.img.xz | sudo dd bs=4M of=/dev/SDCARD
```

Example after inserting the card:

```bash
huhn@asteroid:~# dmesg | tail
[  398.923366] sd 3:0:0:3: [sdf] 15286272 512-byte logical blocks: (7.83 GB/7.29 GiB)
[  398.924362] sd 3:0:0:3: [sdf] Write Protect is off
[  398.924370] sd 3:0:0:3: [sdf] Mode Sense: 21 00 00 00
[  398.925139] sd 3:0:0:3: [sdf] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
[  398.929437] sd 3:0:0:1: [sdd] Attached SCSI removable disk
[  398.935507] sd 3:0:0:2: [sde] Attached SCSI removable disk
[  398.936209] sd 3:0:0:0: [sdc] Attached SCSI removable disk
[  398.949968]  sdf: sdf1 sdf2
[  398.952600] sd 3:0:0:3: [sdf] Attached SCSI removable disk
[  399.974403] EXT4-fs (sdf2): mounted filesystem with ordered data mode. Opts: (null)
huhn@asteroid:~# umount /dev/sdf1
huhn@asteroid:~# umount /dev/sdf2
huhn@asteroid:~# xzcat ubuntu-20.04-preinstalled-server-arm64+raspi.img.xz | sudo dd bs=4M of=/dev/sdf
```

When the card ist written, replace the file ```user-data``` in the first partition with the following lines.
This creates a muhkuh user with a ready-to-use password, installs avahi and reads the IP of the board with espeak-ng.

```
#cloud-config

# Set the hostname.
hostname: muhkuh-teststation-set-me-up

# Enable password authentication with the SSH daemon
ssh_pwauth: true

## Add the empty group "muhkuh" to the system. The user will be created later.
groups:
- muhkuh

## Create a new user with the name "muhkuh". It has access rights like the
#  default "ubuntu" user. The password is set to "muhkuh65536".
users:
- name: muhkuh
  gecos: Muhkuh
  primary_group: muhkuh
  groups: [adm, audio, cdrom, dialout, dip, floppy, lxd, netdev, plugdev, sudo, video]
  lock_passwd: false
  passwd: $1$DYDIC3M5$HJ2lA8xrKXcS3Xw6WfqwC/
  sudo: ["ALL=(ALL) NOPASSWD:ALL"]
  shell: /bin/bash

## Update apt database and upgrade packages on first boot
package_update: true

## Install additional packages on first boot
packages:
- avahi-daemon
- espeak-ng

write_files:
- encoding: b64
  content: IyEgL2Jpbi9iYXNoCndoaWxlIFsgdHJ1ZSBdOyBkbyBpcCAtNCAtbyBhZGRyZXNzIHNob3cgZGV2IGV0aDAgfCBncmVwIC1vUCAnKD88PWluZXRccylcZCsoXC5cZCspezN9JyB8IHNlZCAtZSAncy9cLi8gcG9pbnQgL2cnIHwgZXNwZWFrLW5nIC1zIDEyNTsgc2xlZXAgMjsgZG9uZTsK
  owner: root:root
  path: /opt/announce_ip
  permissions: '0755'
- encoding: b64
  content: W1VuaXRdCkRlc2NyaXB0aW9uPUFubm91bmNlIHRoZSBJUCB3aXRoIGVzcGVhay1uZwpBZnRlcj1uZXR3b3JrLnRhcmdldAoKW1NlcnZpY2VdClR5cGU9c2ltcGxlCkV4ZWNTdGFydD0vb3B0L2Fubm91bmNlX2lwCgpbSW5zdGFsbF0KV2FudGVkQnk9bXVsdGktdXNlci50YXJnZXQK
  owner: root:root
  path: /lib/systemd/system/announce_ip.service
  permissions: '0644'

## Remove unattended upgrades. It blocks the package list at random times so
#  access with management tools like ansible fails.
runcmd:
- [ "/bin/systemctl", "enable", "announce_ip.service" ]
- [ "/bin/systemctl", "start", "announce_ip.service" ]
- [ "/usr/bin/apt", "purge", "unattended-upgrades" ]
```


Then insert the card into the Raspberry, connect it to the network and plug in the power. After a few seconds the green activity led starts going on and off.
The first boot will take a while. Either connect a speaker and wait until the IP is read aloud be epeak-ng.
An alternative is to use avahi to find the board. The initial hostname of the board is "muhkuh-teststation-set-me-up.local":

```bash
huhn@asteroid:~# avahi-resolve-host-name -4 muhkuh-teststation-set-me-up.local
muhkuh-teststation-set-me-up.local      10.11.5.59
```

Write the IP to the hosts file:

```ini
[FreshlyInstalledBoards]                                                                                                                                                                                   10.11.5.59                                                                                                                                                                                                 
10.11.5.59
```

Build the flashstation APP from here https://github.com/muhkuh-sys/org.muhkuh.tools-flashstation_app and copy it to ```data/var/lib/tftpboot/flashapp_netx4000.img```.

Then run the playbook:

```bash
huhn@asteroid:~# ansible-playbook flash-station-setup.yml
```

The script asks for the hostname of the new flash station and the SWFP file to install.
At the end it powers down the board.

# TODO

* Automate download and install of the flashstation APP.
* Powerdown cuts the connection to ansible immediately which results in an error.
