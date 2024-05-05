import socket
import threading
import time
import errno

maxSlaveCapacity = 3
slavesNum = 3
slavesPorts = [1234,1235,1236]
slavesIPs = ["13.60.34.246","ip2","ip3"]
slaveStatus = [None,None,None]
slaveCapacity = [slaveCapacity, slaveCapacity, slaveCapacity]
timeoutSockets= list()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1234))

imagesReceived = []




def timeout():
    print("I\'m Here")
    while True:
        print("Slaves Statuses:",slaveStatus)
        for sock in range(len(timeoutSockets)):
            if slaveStatus[sock] == None:
                try:
                    timeoutSockets[sock].connect((slavesIPs[sock],slavesPorts[sock]))
                    slaveStatus[sock] = True
                except:
                    print("Couldn\'t Connect")
                    continue
            try:
                data = timeoutSockets[sock].recv(4096)
                timeoutSockets[sock].send(b"K")
                if not data:
                    print("Client closed")
                    slaveStatus[sock] = None
                else:
                    slaveStatus[sock] = True
            except TimeoutError as e:
                print("Timed Out: ",e)
                slaveStatus[sock] = False
            except IOError as e:
                if e.errno == errno.EPIPE:
                    slaveStatus[sock] = None
        time.sleep(2)

def process_request():
    imagesNo = client.recv(1024)
    client.send(b"K")
    op = client.recv(1024)
    client.send("K") 
    for i in range(imagesNo):
        imgSize = client.recv(1024)
        imgData = b""
        client.send(b"K")
        while imgSize:
            data = client.recv(min(imgSize,4096))
            imgSize -= len(data)
            imgData+=data
        imagesReceived.append(imgData)
    currImageIndex = 0
    for slaveIndex in range(len(slaveStatus)):
        if slaveStatus[slaveIndex] == True and slaveCapacity[slaveIndex] == maxSlaveCapacity:
            slaveCapacity[slaveIndex] = 0
            client.send(maxSlaveCapacity)
            client.recv(1024)
            client.send(op)
            client.send("K") 
            for i in range(maxSlaveCapacity):
                client.send(currImageIndex)
                client.recv(1024)
                client.send(len(imagesReceived[currImageIndex]))
                client.recv(1024)
                client.sendall(imagesReceived[currImageIndex])
                currImageIndex+=1
            for i in range(maxSlaveCapacity):
                img_ID = client.recv(1024)
                client.send(b"K")
                new_img_size = client.recv(1024)
                client.send(b"K")
                newImgData = b""
                while new_img_size:
                    data = client.recv(min(new_img_size,4096))
                    imgSize -= len(data)
                    newImgData+=data
                imagesReceived[img_ID] = newImgData
            slaveCapacity[slaveIndex] = maxSlaveCapacity
    






for i in range(3):
    newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newSock.settimeout(3)
    try:
        newSock.connect((slavesIPs[i],slavesPorts[i]))
        slaveStatus[i] = True
    except:
        pass
    timeoutSockets.append(newSock)


server.listen(5)
client, addr = server.accept()
print("Connection Arrived From",addr)
timeoutThread = threading.Thread(target = timeout)
clientThread  = threading.Thread(target = process_request)
clientThread.start()
timeoutThread.start()
clientThread.join()
timeoutThread.join()