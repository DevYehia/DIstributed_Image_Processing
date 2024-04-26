import socket
from operations import *
import os
# Receive image data from client
image_data = bytearray()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1234))
server.listen(5)
client, addr = server.accept()
while True:
    payload = client.recv(1024).decode("utf-8")
    #print(payload)
    client.send(b"1")
    operation = payload.split(";")[0]
    print("Operation Selected is: ",operation)
    img_name = payload.split(";")[1]
    print("Image Name is: ",img_name)
    img_size = int(payload.split(";")[2])
    print("Image Size is",img_size)
    img = open(img_name,"wb")
    img_data = b""

    img_size_orig = img_size

    counter = 0
    while img_size:
        data = client.recv(min(img_size,4096))
        #print("Counter=,counter")
        img_size -= len(data)
        img_data+=data

    
    img.write(img_data)
    print("Passes Downloading")
    # Convert received data back to bytes
    image_bytes = bytes(img_data)

    # Convert image bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)

    # Decode numpy array to image
    org_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)


    if operation == "Blur":
        new_img = blur(org_img)
    elif operation == "GrayScale":
        new_img = gray(org_img)
    elif operation == "Invert":  
        new_img = invert_photo(org_img)
    elif operation == "Rotate 90°":
        new_img = rotate(org_img)
    elif operation == "Increase Brightness":
        new_img = incerase_brightness(org_img)

    cv2.imwrite("new" + img_name, new_img)
    new_img_length = os.path.getsize("new"+img_name) #len(open("new"+img_name).read())
    print("New File Size",new_img_length)  
    # Send encoded image data back to client
    client.send(new_img_length.to_bytes(4,'big'))
    client.sendall(open("new" + img_name , "rb").read())

    img.close()
    #client.close()
    #server.close()

