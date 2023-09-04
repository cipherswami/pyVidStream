############################################################
# Author:       Aravind Potluri <aravindswami135@gmail.com>
# Description:  A simple python based video streaming app.
############################################################

# Librarires
import cv2
import socket
import pickle
import struct

# Set up the server socket
try:
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nodeIP = "0.0.0.0"  # Replace with your server's IP address
    nodePort = int("[#] Enter stream port: ")
    serverSock.bind((nodeIP, nodePort))
    serverSock.listen(5)
    clientSock, ClientAddr = serverSock.accept()
except Exception as err:
    print(f"[!] {str(err)}")
    serverSock.close()
    exit()

print(f"[#] Listening at {nodeIP}:{nodePort}")

# Accept a connection from a client
print("[#] Received connection from:", ClientAddr)

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Serialize the frame
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))

    # Send the frame size and frame data to the client
    clientSock.sendall(message_size + data)

