import socket
import threading
import time
import errno

maxSlaveCapacity = 3
slavesNum = 3
timeoutPorts = [1234,1235,1236]
dataPorts = [2000,2001,2002]
slavesIPs = ["16.171.133.158","ip2","ip3"]
slaveStatus = [None,None,None]
timeoutSockets= list()
dataSockets = list()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1237))

imagesReceived = []


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
                if not data:
                    #print("Client closed")
                    slaveStatus[sock] = None
                else:
                    slaveStatus[sock] = True
            except TimeoutError as e:
                #print("Timed Out: ",e)
                slaveStatus[sock] = False
            except IOError as e:
                if e.errno == errno.EPIPE:
                    slaveStatus[sock] = None
        #time.sleep(2)

def process_request():
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
    serverTaskSize = imagesNo // 3
    extraTasks = imagesNo % 3
    currImageIndex = 0

    while extraTasks != 0:
        i = -1
        for j in range(slavesNum):
            if slaveStatus[j] == True:
                i = j
                break
        if i == -1:
            #print("All Servers are down, go somewhere else")
            continue
        print("Found Server No",i)

        try:

            dataSockets[i].send(str(extraTasks).encode())
            dataSockets[i].recv(1024)
            dataSockets[i].send(op.encode())
            dataSockets[i].recv(1024)
            print("Passed")
            for j in range(extraTasks): 
                send_image(currImageIndex,dataSockets[i],i)
                currImageIndex+=1
            #dataSockets[i].send(b"OK")
            for j in range(extraTasks):
                recv_image(dataSockets[i])
        except:
            print("Server ",i,"Failed")
            slaveStatus[i] = None
            continue
        imagesNo -= extraTasks
        extraTasks = 0
    while imagesNo:
        for i in range(slavesNum):
            if slaveStatus[i] == True:
                try:
                    dataSockets[i].send(str(serverTaskSize).encode())
                    dataSockets[i].recv(1024)
                    dataSockets[i].send(op.encode())
                    dataSockets[i].recv(1024)
                    for j in range(serverTaskSize): 
                        send_image(currImageIndex,dataSockets[i],i)
                        currImageIndex+=1

                    for j in range(serverTaskSize):
                        recv_image(dataSockets[i])
                except:
                    print("Server",i,"Failed")
                    slaveStatus[i] = None
                    continue
                imagesNo -= serverTaskSize
    client.send("Done 0 0".encode())
    client.recv(1024)
    for i in range(origImagesNo):
        file = open(imagesReceived[i][0],"wb")
        file.write(imagesReceived[i][1])

    for _,image in imagesReceived:
        client.send(str(len(image)).encode())
        client.recv(1024)
        client.sendall(image)
        print("Sent An Image to client")

    

def send_image(index,server,serverNo):
    server.send(str(index).encode())
    server.recv(1024)
    
    client.send(("Start "+ str(serverNo) + " " + str(index)).encode())
    #print("Sent Change to client")
    client.recv(1024)
    server.send(imagesReceived[index][0].encode())
    server.recv(1024)
    server.send(str(len(imagesReceived[index][1])).encode())
    server.recv(1024)
    server.sendall(imagesReceived[index][1])
  
    

def recv_image(server):
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
    client.send(("End 0 "+str(img_ID)).encode())
    client.recv(1024)
    imagesReceived[int(img_ID)][1] = newImgData





for i in range(3):
    newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newSock.settimeout(3)
    try:
        newSock.connect((slavesIPs[i],timeoutPorts[i]))
        slaveStatus[i] = True
    except:
        pass
    timeoutSockets.append(newSock)

print("Slaves Statuses:",slaveStatus)

for i in range(3):
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
