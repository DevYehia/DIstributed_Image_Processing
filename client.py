
import os
import socket



# Specify the operation and image file details
def send_image(operation,image_path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("13.51.158.159", 1234))
    image_name = image_path.split("/")[-1]
    # Send operation, image name, and file size to the server
    client.send(operation.encode("utf-8")+";".encode()+image_name.encode("utf-8")+";".encode())
    client.recv(1)

    # Send the image data to the server
    with open(image_path, "rb") as file:
        data = file.read()
        client.sendall(data)

    client.close()