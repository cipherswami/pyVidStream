############################################################
# Author:       Aravind Potluri <aravindswami135@gmail.com>
# Description:  A simple python based video streaming app.
############################################################

# Libraries
import cv2
import socket
import pickle
import struct

# Set up the client socket
try:
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    targetIP = input("[#] Enter Streamer's IP: ")  # Replace with the server's IP address
    targetPort = int(input("[#] Enetr Port: "))
    clientSock.connect((targetIP, targetPort))
except KeyboardInterrupt:
    clientSock.close()
    exit()

data = b""
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        packet = clientSock.recv(4 * 1024)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += clientSock.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize the frame and display it
    frame = pickle.loads(frame_data)
    cv2.imshow("Received", frame)
    cv2.waitKey(1)
