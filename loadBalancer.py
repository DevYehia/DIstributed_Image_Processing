import socket
import threading
import time
import errno
import numpy as np
import cv2
import atexit


slavesNum = 3  # Max number of servers the load balancer can communicate to
timeoutPorts = [1234,1234,1234]  # Ports for each timeout 
dataPorts = [2000,2000,2000]    
slavesIPs = ["16.171.133.158","51.20.2.218","13.60.64.240"]

#Status of each Machine
'''
None ---> Machine is Down
False ---> Machine took too long to respond
True ---> Machine is up and running

'''
slaveStatus = [None,None,None]  
timeoutSockets= list()
dataSockets = list()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1237)) #socket that the client will connect to

imagesReceived = []  #Array that will store list of [img_name,img_bytes]

#Timeout Function that will continously check on the health of the servers
def timeout():
    print("I\'m Here")
    while True:
        #print("Slaves Statuses:",slaveStatus)
        for sock in range(len(timeoutSockets)):
            if slaveStatus[sock] == None:  #No Connection Exists between load balancer and server
                try:
                    timeoutSockets[sock].connect((slavesIPs[sock],timeoutPorts[sock])) #Try to connect
                    dataSockets[sock].connect((slavesIPs[sock],dataPorts[sock]))                    
                    slaveStatus[sock] = True
                except:
                    continue
            try:
                data = timeoutSockets[sock].recv(4096)
                timeoutSockets[sock].send(b"K")
                if not data:  #Socket Closed
                    slaveStatus[sock] = None  
                else:
                    slaveStatus[sock] = True
            except TimeoutError as e:
                slaveStatus[sock] = False
            except IOError as e:
                if e.errno == errno.EPIPE:
                    slaveStatus[sock] = None
        #time.sleep(2)

#the main function that gets called when the client uploads his images
def process_request():

    global imagesReceived
    imagesNo = int(client.recv(1024).decode())
    client.send(b"K")
    print("Images No is ",imagesNo)
    op = client.recv(1024).decode()
    print("Operation is",op)
    client.send(b"K") 
    for i in range(imagesNo):
        imgSize = int(client.recv(1024).decode())
        print("For Image No.",i,":\nSize =",imgSize)
        imgData = b""
        client.send(b"K")
        imgName = client.recv(1024).decode()
        print("Name is",imgName)
        client.send(b"K")
        while imgSize:
            data = client.recv(min(imgSize,4096))
            imgSize -= len(data)
            imgData+=data
        imagesReceived.append([imgName, imgData])
    origImagesNo =imagesNo
    serverTaskSize = imagesNo // 3  #Will be distributed to each server available
    extraTasks = imagesNo % 3       #Will be handled by one available server
    currImageIndex = 0              #Current image being processed
    isOneImage = False 
    print("----------Sending to Server-----------")

    if extraTasks == 1 and serverTaskSize == 0: #One image case: Divide image into three fragments

        isOneImage = True

        #Convert to cv2 image to split it
        image_array = np.frombuffer(imagesReceived[0][1], dtype=np.uint8)
        org_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        h, w, channels = org_img.shape
        third = w // 3
        imageName = imagesReceived[0][0]
        extension = imageName.split(".")[1]
        nameNoExt = imageName.split(".")[0]

        #Save the each splitted image
        imageFragmentsData = [org_img[:,:third],org_img[:,third:third*2],org_img[:,third*2:]]
        imagesReceived = []

        #Now we have three images not one
        extraTasks = 0
        serverTaskSize = 1
        imagesNo = 3 

        #Put the three fragments now as three seperate images
        #Each one will have a name: original_name + fragmentIndex
        for fragmentIndex in range(len(imageFragmentsData)):
            _, encoded = cv2.imencode("." +extension,imageFragmentsData[fragmentIndex])
            imagesReceived.append([nameNoExt+str(fragmentIndex)+"."+extension,encoded.tobytes()])
        

    
    while extraTasks != 0:
        i = -1
        for j in range(slavesNum):  #Find a working server
            if slaveStatus[j] == True:
                i = j
                break
        if i == -1:  #All Servers Down
            #print("All Servers are down, go somewhere else")
            continue
        print("Found Server No",i)

        try:
            dataSockets[i].send(str(extraTasks).encode())
            dataSockets[i].recv(1024)
            dataSockets[i].send(op.encode())
            dataSockets[i].recv(1024)
        #print("Passed")
            for j in range(extraTasks): 
                send_image(currImageIndex + j,dataSockets[i],i,isOneImage)
                
            #dataSockets[i].send(b"OK")
            for j in range(extraTasks):
                recv_image(dataSockets[i],isOneImage)
        except:  #Something Wrong happened, Declare server status as None and try with another server
            print("Server ",i,"Failed")
            slaveStatus[i] = None
            continue
        currImageIndex+=extraTasks
        imagesNo -= extraTasks
        extraTasks = 0

    while imagesNo != 0:
        for i in range(slavesNum):
            if slaveStatus[i] == True:  #Working server found
                try:
                    dataSockets[i].send(str(serverTaskSize).encode())
                    dataSockets[i].recv(1024)
                    dataSockets[i].send(op.encode())
                    dataSockets[i].recv(1024)
                    for j in range(serverTaskSize): 
                        send_image(currImageIndex + j,dataSockets[i],i,isOneImage)
                        

                    for j in range(serverTaskSize):
                        recv_image(dataSockets[i],isOneImage)
                except: #Something Wrong happened, Declare server status as None and try with another server
                    #print(e)
                    print("Server",i,"Failed")
                    slaveStatus[i] = None
                    continue
                currImageIndex+=serverTaskSize
                imagesNo -= serverTaskSize
            if(imagesNo == 0):
                break

    #Send Confirmation to client that processing is done, and now images will be sent
    client.send("Done 0 0".encode())
    client.recv(1024)

    print("-------------Finished Receiving from server------------")


    if isOneImage: #One image case : Merge Image Parts

        #Convert first third to cv2 image to merge it
        img_in_bytes = imagesReceived[0][1] # Get First Third Of the Image
        image_array = np.frombuffer(img_in_bytes, dtype=np.uint8)
        new_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)


        for i in range(1,3):

            #Convert the fragment to cv2
            image_array = np.frombuffer(imagesReceived[i][1], dtype=np.uint8)
            imageFragment = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            #Merge the Image
            if op == "Rotate 90°":
                new_img = cv2.vconcat([new_img,imageFragment])
            elif op == "Reflect":
                new_img = cv2.hconcat([imageFragment,new_img])        
            else:   
                new_img = cv2.hconcat([new_img,imageFragment])

        imageName = imagesReceived[0][0]
        extension = imageName.split(".")[1]
        nameNoExt = imageName.split(".")[0]

        #Convert Merged Image back to bytes and save it
        _ , encoded = cv2.imencode("." + extension,new_img)
        imagesReceived = [[nameNoExt[:len(nameNoExt) - 1]+"."+extension,encoded.tobytes()]]

    #Send images to client by the order they were received in
    for _,image in imagesReceived:
        client.send(str(len(image)).encode())
        client.recv(1024)
        client.sendall(image)
        print("Sent An Image to client")

    
oneImageStartUpdate = False
def send_image(index,server,serverNo,isOneImage):
    global oneImageStartUpdate
    server.send(str(index).encode())
    server.recv(1024)
    
    if not isOneImage:
        client.send(("Start "+ str(serverNo) + " " + str(index)).encode())
        client.recv(1024)
    else:
        if not oneImageStartUpdate:
            client.send(("Start "+ str(serverNo) + " 0").encode())        
            client.recv(1024)
            oneImageStartUpdate = True

    server.send(imagesReceived[index][0].encode())
    server.recv(1024)
    server.send(str(len(imagesReceived[index][1])).encode())
    server.recv(1024)
    server.sendall(imagesReceived[index][1])
  
    
oneImageEndUpdate = False
def recv_image(server,isOneImage):
    global oneImageEndUpdate
    img_ID = server.recv(1024).decode()
    print("ID Recieved is",img_ID)
    server.send(b"K")
    img_name = server.recv(1024).decode()
    print("Name Recieved is",img_name)
    server.send(b"K")
    new_img_size = int(server.recv(1024).decode())
    print("New Image Size is",new_img_size)
    server.send(b"K")
    newImgData = b""
    while new_img_size:
        data = server.recv(min(new_img_size,4096))
        new_img_size -= len(data)
        newImgData+=data
    if not isOneImage:
        client.send(("End 0 "+str(img_ID)).encode())
        client.recv(1024)
    else:
        if not oneImageEndUpdate:
            client.send(("End 0 0").encode())  
            client.recv(1024)
            oneImageEndUpdate = True
    imagesReceived[int(img_ID)][1] = newImgData

#Close Socket When Crashing
def close_socket():
    client.close()
atexit.register(close_socket)

#Create Timeout Sockets
for i in range(slavesNum):
    newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newSock.settimeout(3)
    try:
        newSock.connect((slavesIPs[i],timeoutPorts[i]))
        slaveStatus[i] = True
    except:
        pass
    timeoutSockets.append(newSock)

print("Slaves Statuses:",slaveStatus)

#Create Data Sockets
for i in range(slavesNum):
    #print("At i =",i)
    newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        newSock.connect((slavesIPs[i],dataPorts[i]))

    except:
        pass
    dataSockets.append(newSock)

server.listen(5)
client, addr = server.accept()
timeoutThread = threading.Thread(target = timeout)
timeoutThread.start()
while True:
    
    clientThread  = threading.Thread(target = process_request)
    clientThread.start()
    clientThread.join()
    imagesReceived.clear()
    oneImageStartUpdate = False
    oneImageEndUpdate = False
