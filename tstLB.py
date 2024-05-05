import socket
import threading
import time
import errno

slavesNum = 3
slavesPorts = [1234,1235,1236]
slavesIPs = ["13.60.34.246","ip2","ip3"]
slaveStatus = [None,None,None]
timeoutSockets= list()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1234))




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


for i in range(3):
    newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newSock.settimeout(3)
    try:
        newSock.connect((slavesIPs[i],slavesPorts[i]))
        slaveStatus[i] = True
    except:
        pass
    timeoutSockets.append(newSock)

thread = threading.Thread(target = timeout)
thread.start()
server.listen(5)
client, addr = server.accept()
print("Connection Arrived From",addr)
thread = threading.Thread(target = timeout)
thread.start()
thread.join()
