
import os
import socket
from PIL import Image
import cv2
names = ["Kalsen.png","smallKalsen.png"]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
client.connect(("51.20.85.5", 1234))
imagesReceived = []
imagesReceived.append(open("Kalsen.png","rb").read())
imagesReceived.append(open("smallKalsen.png","rb").read())
op = "Invert"
imagesNo = 2
client.send(str(imagesNo).encode())
client.recv(1024)
client.send(op.encode())
client.recv(1024) 
for i in range(imagesNo):
    client.send(str(i).encode())
    client.recv(1024)
    client.send(names[i].encode())
    client.recv(1024)
    client.send(str(len(imagesReceived[i])).encode())
    client.recv(1024)
    client.sendall(imagesReceived[i])
    client.recv(1024)
client.send(b"K")
for i in range(imagesNo):
    img_ID = client.recv(1024).decode()
    client.send(b"K")
    img_name = client.recv(1024).decode()
    client.send(b"K")
    new_img_size = int(client.recv(1024).decode())
    client.send(b"K")
    newImgData = b""
    while new_img_size:
        data = client.recv(min(new_img_size,4096))
        new_img_size -= len(data)
        newImgData+=data
    client.send(b"K")
    file = open(img_name,"wb")
    file.write(newImgData)