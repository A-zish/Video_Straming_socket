import socket
import cv2
import pickle
import struct

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.53.28'
port = 1234
print("Socket Created")

#Client Socket will use connect() to connect with Server Socket after the socket is created.
client_socket.connect((host_ip,port))

#Empty string defined size - 1 byte
data = b"" 

payload_size = struct.calcsize("Q")
print(payload_size)
print("Socket Accepted")

while True:
    while len(data) < payload_size: #1 byte < 8 bytes
        packet = client_socket.recv(2160)
        if not packet: break
        data += packet #Appending serial data that come from server (stored in loc var message on in Server.ipynb)
    dynamicSerializedMsg = data[:payload_size] #Data of first 8 bytes.
    data = data[payload_size:]

    # Unpacks only 8 bytes of data dynamically stored in packed message.
    # [0] refers to element at first index
    msg_size = struct.unpack("Q",dynamicSerializedMsg)[0] 
    
    # len(data) - (One of them: 2152 (max); Defined by strlen passed as an arguement in .recv function)
    # msg_size (One of them:  9044780001777646981; Type - int)
    while len(data) < msg_size:
        data += client_socket.recv(2160)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data) #Object Deserialization
    cv2.imshow("Client",frame)
    key = cv2.waitKey(1) & 0xFF

    #ord () function accepts a string of unit length as an argument and returns the Unicode equivalence of the passed argument.
    if key  == ord('q'): # 113
        break
client_socket.close()
