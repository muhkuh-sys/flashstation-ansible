# How to use this

First copy the 64bit Ubuntu 20.04 Raspberry image from [here](https://ubuntu.com/download/raspberry-pi) to a memory card.
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

When the card ist written, replace the file ```user-data``` in the first partition with the file in the
```cloud_init``` subfolder of this repository. This creates a muhkuh user with a ready-to-use password,
and installs avahi.

Then insert the card into the Raspberry, connect it to the network and plug in the power. It is important that the raspberry can connect to the internet.
After a few seconds the green activity led starts going on and off.
The first boot will take a while. Either connect a UART and login with user "muhkuh" and password "muhkuh65536" to find out the IP address.
An alternative is to use avahi to find the board. The initial hostname of the board is "muhkuh-teststation-set-me-up.local".

Example with UART:
```bash
huhn@asteroid:~$ tio /dev/ttyUSB0 
[tio 09:20:53] tio v1.32
[tio 09:20:53] Press ctrl-t q to quit
[tio 09:20:53] Connected

muhkuh-teststation-set-me-up login: muhkuh
Password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-1042-raspi aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed Sep 21 07:21:04 UTC 2022

  System load:  0.08               Swap usage:  0%       Users logged in: 0
  Usage of /:   11.8% of 14.30GB   Temperature: 37.5 C
  Memory usage: 13%                Processes:   126

199 updates can be applied immediately.
129 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable



The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

muhkuh@muhkuh-teststation-set-me-up:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether e4:5f:01:b0:97:ef brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.73/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86396sec preferred_lft 86396sec
    inet6 2a00:6020:15dc:d200:e65f:1ff:feb0:97ef/64 scope global dynamic mngtmpaddr noprefixroute 
       valid_lft 3597sec preferred_lft 2247sec
    inet6 fdaa:bbcc:ddee:0:e65f:1ff:feb0:97ef/64 scope global dynamic mngtmpaddr noprefixroute 
       valid_lft 7197sec preferred_lft 3597sec
    inet6 fe80::e65f:1ff:feb0:97ef/64 scope link 
       valid_lft forever preferred_lft forever
3: wlan0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether e4:5f:01:b0:97:f0 brd ff:ff:ff:ff:ff:ff
```

Example with avahi:
```bash
huhn@asteroid:~# avahi-resolve-host-name -4 muhkuh-teststation-set-me-up.local
muhkuh-teststation-set-me-up.local      10.11.5.59
```

Write the IP to the hosts file:

```ini
[FreshlyInstalledBoards]
10.11.5.59
```

Then run the playbook:

```bash
huhn@asteroid:~# ansible-playbook flash-station-setup.yml
```

The script sets up the flash station. At the end it powers down the board.

Please note that the device is now configured to the IP 192.168.64.1 . Connect it to a 

Here is a guide how to setup Ansible on Windows: https://phoenixnap.com/kb/install-ansible-on-windows
