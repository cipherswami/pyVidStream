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
payloadSize = struct.calcsize("L")

while True:
    try:
        # Data Processing
        while len(data) < payloadSize:
            packet = clientSock.recv(4 * 1024)
            if not packet:
                break
            data += packet
        packedMsgSize = data[:payloadSize]
        data = data[payloadSize:]
        msgSize = struct.unpack("L", packedMsgSize)[0]
        while len(data) < msgSize:
            data += clientSock.recv(4 * 1024)
        frameData = data[:msgSize]
        data = data[msgSize:]

        # Deserialize the frame and display it
        frame = pickle.loads(frameData)
        cv2.imshow("Received", frame)
        cv2.waitKey(1)
    except KeyboardInterrupt:
        break
    except struct.error:
        break

clientSock.close()
