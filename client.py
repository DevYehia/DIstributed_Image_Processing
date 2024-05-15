
import os
import socket
from PIL import Image
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False


def connectToLB():
    global connected
    if not connected:
        connected = True
        client.connect(("51.20.8.142", 1237))   

def send_images_number(imagesNo):
    client.send(str(imagesNo).encode())
    client.recv(1024)

def send_operation(op):
    client.send(op.encode())
    client.recv(1024)

def applyImageOp(img_paths,operation):
    imagesNo = len(img_paths)
    img_names = [img_paths[i].split("/")[-1] for i in range(len(img_paths))]
    connectToLB()
    send_images_number(imagesNo)
    send_operation(operation)
    images = []
    for i in range(imagesNo):
        send_image(img_paths[i])
    for i in range(imagesNo):
        images.append(recv_image(img_names[i]))
    return images

# Specify the operation and image file details
def send_image(image_path):

    image_name = image_path.split("/")[-1]

    file_size = os.path.getsize(image_path)
    # Send operation, image name, and file size to the server
    print(file_size)
    client.send(str(file_size).encode())
    client.recv(1024)
    client.send(image_name.encode())
    client.recv(1024)


    with open(image_path, "rb") as file:
        data = file.read()
        client.sendall(data)
    #End Of Send

def recv_image(image_name):
    img = open("new" + image_name,"wb")
    new_img_size = int(client.recv(1024).decode())
    client.send(b"OK")
    print("New Size is",new_img_size)
    img_data = b""
    while new_img_size:
        data = client.recv(min(4096,new_img_size))
        new_img_size -= len(data)
        img_data += data
    img.write(img_data)
    img.close()
    return "new" + image_name

if __name__ == '__main__':
    op = "Invert"

    applyImageOp(["Kalsen.png","smallKalsen.png"],op)