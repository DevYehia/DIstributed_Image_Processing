import socket



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1234))
server.listen(5)

client, addr = server.accept()
payload = client.recv(1024).decode("utf-8")

operation = payload.split(" ")[0]
print("Operation Selected is: ",operation)
img_name = payload.split(" ")[1]
print("Image Name is: ",img_name)
img_size = int(payload.split(" ")[2])
print("Image Size is: ",img_size)

img = open(img_name,"wb")
img_data = b""

done = False
for i in range(img_size):
    data = client.recv(1)
    img_data += data
img.write(img_data)

img.close()
client.close()
server.close()