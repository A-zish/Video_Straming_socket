import socket
import cv2
import pickle
import struct


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 1234

socket_address = ( host_ip ,port)
print("Socket Created")

server_socket.bind(socket_address)
print("Socket Binded")

server_socket.listen(5)
print("LISTENING AT:",socket_address)

print("Socket Accepted")

while True:
    #accept() - accept a connection request from a client. 

    client_socket,addr = server_socket.accept()
    print('GET CONNECTION FROM:',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        
        while(vid.isOpened()):
            img,frame = vid.read()
            a = pickle.dumps(frame) #Object Serialization
            
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            
            cv2.imshow('Server',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_s.close()


print("Thank u")
