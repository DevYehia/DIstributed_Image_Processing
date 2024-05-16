import socket
from operations import *
import os
import threading
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
lock = threading.Lock()
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
    
    
    #l1 = l[:int(len(l)/2)]
    #l2 = l[len(l1):]
    


    # Convert received data back to bytes
    image_bytes = bytes(img_data)

    # Convert image bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)

    # Decode numpy array to image
    org_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    h, w, channels = org_img.shape

    half = w // 2

    img_first_half = org_img[:,:half]
    #b,g,r = cv2.split(org_img)
    
    #Crtitical Section of sending to process 1 
    lock.acquire()
    comm.send(operation,1,11)
    comm.send(org_img[:,half:],1,11)
    lock.release()
    #end of critical section
    org_img = img_first_half

    if operation == "Edge Detection":
        new_img = edges(org_img)
    elif operation == "GrayScale":
        new_img = gray(org_img)
    elif operation == "Invert":  
        new_img = invert_photo(org_img)
    elif operation == "Rotate 90°":
        new_img = rotate(org_img)
    elif operation == "Corners":
        new_img = corners(org_img)
    elif operation == "Reflect":  
        new_img = reflect(org_img)
    elif operation == "Brighten":
        new_img = brighten(org_img)
    elif operation == "Darken":
        new_img = darken(org_img)

    new_img_second_half = comm.recv(source=1,tag=11)

    if operation == "Rotate 90°":
        new_img = cv2.vconcat([new_img,new_img_second_half])
    elif operation == "Reflect":
        new_img = cv2.hconcat([new_img_second_half,new_img])        
    else:   
        new_img = cv2.hconcat([new_img,new_img_second_half])

    #cv2.imwrite("new" + img_name.split(".")[0] + "1." + img_name.split(".")[1], new_img)
    #cv2.imwrite("new" + img_name.split(".")[0] + "2." + img_name.split(".")[1], new_img_second_half)
    cv2.imwrite("new" +img_name, new_img)

def send_image(img_name):
    first_img_name = "new" + img_name.split(".")[0] + "1." + img_name.split(".")[1]
    second_img_name = "new" + img_name.split(".")[0] + "2." + img_name.split(".")[1]
    new_img_length = os.path.getsize("new" + img_name)
    print("New File Size",new_img_length)  
    # Send encoded image data back to client
    client.send(str(new_img_length).encode())
    client.recv(1024)
    #client.sendall(open(first_img_name , "rb").read())
    client.sendall(open("new" + img_name , "rb").read())

if rank == 0:
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
    
        threads.clear()
        images.clear()

elif rank == 1:
    while True:
        operation = comm.recv(source=0,tag = 11)
        org_img = comm.recv(source = 0, tag =11)



        if operation == "Edge Detection":
            new_img = edges(org_img)
        elif operation == "GrayScale":
            new_img = gray(org_img)
        elif operation == "Invert":  
            new_img = invert_photo(org_img)
        elif operation == "Rotate 90°":
            new_img = rotate(org_img)
        elif operation == "Corners":
            new_img = corners(org_img)
        elif operation == "Reflect":  
            new_img = reflect(org_img)
        elif operation == "Brighten":
            new_img = brighten(org_img)
        elif operation == "Darken":
            new_img = darken(org_img)
        comm.send(new_img,dest=0,tag=11)

