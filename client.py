# import os
# import socket

# #Operation, Image name with extension, file size, stopping condition
# client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# client.connect(("13.51.158.159",1234))

# operation = "resize"  # Change this to the desired operation


# file=open("image.jpeg","rb")
# file_size=os.path.getsize("image.jpeg")


# # Send operation, image name, and file size to the server
# client.send(operation.encode())
# client.send("received_image.jpeg".encode())
# client.send(str(file_size).encode())

# data = file.read()
# client.sendall(data)
# client.send(b"<END>")

# file.close()
# client.close()


import os
import socket

# Operation, Image name with extension, file size, stopping condition
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("13.51.158.159", 1234))

# Specify the operation and image file details
operation = "resize"  # Change this to the desired operation
image_name = "image.jpeg"
file_size = os.path.getsize(image_name)
print(file_size)
# Send operation, image name, and file size to the server
#client.send(operation.encode("utf-8")+" ".encode())
#client.send(image_name.encode("utf-8")+" ".encode())
client.send(operation.encode("utf-8")+" ".encode()+image_name.encode("utf-8")+" ".encode()+str(file_size).encode("utf-8")+" ".encode())


# Send the image data to the server
with open(image_name, "rb") as file:
    data = file.read()
    client.sendall(data)

# Send the end signal to indicate the end of data transmission
client.send(b"<END>")

client.close()