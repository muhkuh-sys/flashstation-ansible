import socket

# Create a TCP socket.
tSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
tServerAddress = ('192.168.64.1', 5555)
print('Starting server on %s port %s' % tServerAddress, flush=True)
tSocket.bind(tServerAddress)

# Listen for incoming connections
tSocket.listen(256)

while True:
    # Wait for a connection
    tConnection, tClientAddress = tSocket.accept()
    try:
        aucData = tConnection.recv(4096)
        strData = aucData.decode(
            "utf-8",
            "replace"
        )

        # Split the string by comma.
        astrData = list(map(lambda s: s.strip(' \t\r\n'), strData.split(',')))
        print('Received from %s: %s' % (tClientAddress[0], ','.join(astrData)), flush=True)

    finally:
        # Clean up the connection
        tConnection.close()
