import socket
from operations import *
import os
import threading
# Receive image data from client
images = dict()
threads = []
image_data = bytearray()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
timeOutSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def timeoutRespond():
    while True:
        timeOutResponseSocket.send(b"I am Online")
        timeOutResponseSocket.recv(1024)

def getImage(img_size):
    img_data = b""
    while img_size:
        data = client.recv(min(img_size,4096))
        #print("Counter=,counter")
        img_size -= len(data)
        img_data+=data
    return img_data


def getImageNo():
    imagesNo = client.recv(1024).decode()
    client.send(b"OK")
    return int(imagesNo)

def getOperation():
    operation = client.recv(1024).decode()
    client.send(b"OK")
    return operation

def edit_image(operation, img_name, img_data):
    
    img = open(img_name,"wb")

    img_size_orig = img_size

    counter = 0
    
    img.write(img_data)
    print("Passes Downloading")
    # Convert received data back to bytes
    image_bytes = bytes(img_data)

    # Convert image bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)

    # Decode numpy array to image
    org_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)


    if operation == "Edge Detection":
        new_img = edges(org_img)
    elif operation == "GrayScale":
        new_img = gray(org_img)
    elif operation == "Invert":  
        new_img = invert_photo(org_img)
    elif operation == "Rotate 90°":
        new_img = rotate(org_img)
    elif operation == "Edge Detection":
        new_img = edges(org_img)

    cv2.imwrite("new" + img_name, new_img)

def send_image(img_name):
    new_img_length = os.path.getsize("new"+img_name) #len(open("new"+img_name).read())
    print("New File Size",new_img_length)  
    # Send encoded image data back to client
    client.send(str(new_img_length).encode())
    client.recv(1024)
    client.sendall(open("new" + img_name , "rb").read())

timeOutSocket.bind(("0.0.0.0", 1234))
timeOutSocket.listen(1)
timeOutResponseSocket , _ = timeOutSocket.accept() 
timeoutThread = threading.Thread(target = timeoutRespond)
timeoutThread.start()
server.bind(("0.0.0.0", 2000))


server.listen(5)
client, addr = server.accept()
while True:
    #client, addr = server.accept()
    #print("Connection Arrived")
    imgNo = getImageNo()
    print("No of images is",imgNo)
    op = getOperation()
    print("Operation is",op)
    for i in range(imgNo):
        id = client.recv(1024).decode()
        print("At i =",i," ID is",id)
        client.send(b"OK")
        img_name = client.recv(1024).decode()
        client.send(b"OK")
        print("Name is",img_name)
        img_size = int(client.recv(1024).decode())
        print("Image Size is",img_size)
        client.send(b"OK")
        img_data = getImage(img_size)
        #client.send(b"OK")
        images[id] = (img_name,img_data)
        threads.append(threading.Thread(target = edit_image,args=(op,img_name,img_data)))
    #client.recv(1024)
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for key,value in images.items():
        client.send(key.encode())
        client.recv(1024)    
        client.send(value[0].encode())
        client.recv(1024)
        send_image(value[0])
        #client.recv(1024)
    threads.clear()
    images.clear()

