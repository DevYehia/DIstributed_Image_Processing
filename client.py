
import os
import socket
from PIL import Image
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False


def connectToLB():
    global connected
    if not connected:
        connected = True
        client.connect(("51.20.85.5", 1234))   

def send_images_number(imagesNo):
    client.send(imagesNo)
    client.recv(1)

def applyImageOp(imagesNo,img_paths,operation):
    connectToLB()
    send_images_number(imagesNo)
    images = []
    for i in range(imagesNo):
        images.append(send_and_recieve_image())
    return images

# Specify the operation and image file details
def send_and_recieve_image(operation,image_path):

    image_name = image_path.split("/")[-1]

    file_size = os.path.getsize(image_path)
    # Send operation, image name, and file size to the server
    
    client.send(operation.encode("utf-8")+
                ";".encode()+image_name.encode("utf-8")+
                ";".encode()+str(file_size).encode("utf-8")+";".encode())
    print("Sent Data")
    client.recv(1)
    print("Recieved ACK")
    # Send the image data to the server
    with open(image_path, "rb") as file:
        data = file.read()
        client.sendall(data)

    img = open("new" + image_name,"wb")
    new_img_size = int.from_bytes(client.recv(4),'big')
    print("New Size is",new_img_size)
    img_data = b""
    while new_img_size:
        data = client.recv(min(4096,new_img_size))
        new_img_size -= len(data)
        img_data += data
    img.write(img_data)
    img.close()
    return Image.open("new" + image_name)
