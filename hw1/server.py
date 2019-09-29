import sys
import socket
import os
import time
import queue
from _thread import *
import threading


connectionList = []
registered = {}

class dummy(threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            pass

class parentThread(threading.Thread):
    def __init__ (self, s, f):
        threading.Thread.__init__(self)
        self.s = s
        self.f = f
    def run(self):
        parent_thread(self.s,self.f)
        

class myThread (threading.Thread):   
    def __init__(self, threadID, s_send, f, s ,addr,s_UDP):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.s_send = s_send
        self.f = f
        self.s = s
        self.addr = addr
        self.s_UDP = s_UDP
    def run(self): 
        try: 
            global connectionList
            if self.threadID == 1:
                receiveConnection (self.s_send,self.f, self.s_UDP, self.addr)
            elif self.threadID == 2:
                sendConnection (self.s_send,self.f, self.s,  self.addr)
        except KeyboardInterrupt:
            print ("exiting")
            sys.exit()

def register (s, registered, userName, client_address, f):
    if registered is None:
        registered = {userName : client_address}
    elif userName not in registered:
        registered[userName] = client_address
        f.write("received register " + userName +" from host port\n")
        f.flush()
        print (registered)
    #welcome 
    s.sendto(str("welcome").encode(),client_address)
    
def recv_msg(s, receiver, registered, name, message,f):
    data = receiver + ": " + message
    f.write("receivefrom " + name + " to " + receiver + " " + message+"\n")
    f.flush()
    if (receiver not in registered):
        #call another function that forwards to another server
        forward_message(s, receiver, name, message)
        return
    s.sendto(data.encode(), registered.get(receiver))

def forward_message(s, receiver, name, message):
    global connectionList
    data = name + " sendto " + receiver + " " + message
    print (data)
    if len(connectionList) > 0:
        con = connectionList[0]
        print (con)
        con.send(data.encode()) 
    # else:
    #     print (s)
    #     print (s.getsockname())
    #     addr = (str(s.getsockname()[0]),int(str(s.getsockname()[1])))
    #     s.sendto(data.encode(),addr)

def leave (s, registered, name):
    s.sendto(str("EXIT").encode(), registered.get(name))
    del registered[name]

def parent_thread(s,f):
    global connectionList
    registered["unused"] = ("0.0.0.0" , 1)
    f.write("client connection from host port\n")
    f.flush()
    try:    
        while True:
            data, client_address = s.recvfrom(1024)
            dataList = data.decode().split(' ')

            print (dataList)

            if dataList[0] == 'REGISTER':  
                print ("register")
                register(s, registered, dataList[1], client_address, f)
                dataList = []
            elif dataList[1].upper() == 'SENDTO':
                print("here")
                f.write("sendto " + dataList[2] + " from " + dataList[0] + " " + dataList[3]+"\n")
                f.flush()
                recv_msg(s, dataList[2], registered, dataList[0], ' '.join(dataList[3:]),f)
                dataList = []
            elif dataList[0] == 'EXIT':
                leave(s, registered, dataList[1])
                dataList = []
    except KeyboardInterrupt:
        f.write("terminating server...")
        print ("line 95 terminating")
        f.flush()
        f.close()
        sys.exit()

# send the message only; don't need to listen
def receiveConnection(s,f, s_UDP, localAdress):
    global connectionList

    s.listen(5)
    while True: 
        print ("line 62: try to connect")
        connection, overlay_address = s.accept()     # Establish connection with other server.
        if connection:
            print ("connected")
            f.write("server joined overlay from host port\n")
            f.flush()
            connectionList.append(connection)
            readData(connection, s_UDP, localAdress)
   

#listen only;
# check if in the registered; if yes, send to udp
def sendConnection (s_listen, f, s_UDP, addr): 
    readData (s_listen, s_UDP, addr)

def readData(s_listen ,s_UDP, localAdress):
    while True:
        if len(connectionList) > 0:
            data =  s_listen.recv(1024)
            data = str(data.decode().strip())
            if (len(data) > 0):
                if str(data.split(" ")[0]) not in registered:
                    s_UDP.sendto(data.encode(),localAdress)
                # if user exists
                # snedto UDP


def main():
    global connectionList
    if len(sys.argv) < 3:
        print("missing parameters")
        sys.exit()

    overlayIP, overlayPort, serveroverlayport = "" ,"",  ""

    for x in range(len(sys.argv)):
        if sys.argv[x] == "-p":
            x += 1
            port = sys.argv[x]
        elif sys.argv[x] == "-l":
            x += 1
            logfile = sys.argv[x]
        elif sys.argv[x] == "-s":
            x += 1
            overlayIP = sys.argv[x]
        elif sys.argv[x] == "-t":
            x += 1
            serveroverlayport = sys.argv[x]
        elif sys.argv[x] == "-o":
            x += 1
            overlayPort = sys.argv[x]

    f = open(logfile, "w+")
    f.write("server started on localhost at port "+ port + "...\n")
    f.flush()
    localAdress = ("localhost", int(port))

    # connect to the client via UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', int(port)))    							# Bind to the port
    parent = parentThread(s, f)

    try:
        parent.start()
    except KeyboardInterrupt:
        f.write("terminating server...")
        print ("exiting")
        f.flush()
        f.close()
        sys.exit()


    # try connect to the overlay service through TCP
    if overlayPort is not "":
        s_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
        if overlayIP == "":
            overlayIP = "localhost"
        s_send.bind((overlayIP, int(overlayPort)))                         # Bind to the port
        f.write("server overlay started at port " + str(overlayPort) + "\n")
        f.flush()
        thread_send_1 = myThread(1,s_send,f,s,localAdress,s)
        thread_send_1.start()
    
    # bind to the serveroverlay port if necessary
    if serveroverlayport is not "":
        s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_listen.connect(("localhost", int(serveroverlayport) ))
        connectionList.append(s_listen)
        
        # thread_listen_1 = myThread(1,s_listen,f,s,localAdress)
        thread_listen_2 = myThread(2,s_listen,f,s,localAdress, s)
        # thread_listen_1.start()
        thread_listen_2.start()
        

    thread_dummy = dummy()
    try:
        thread_dummy.start()
        while True: time.sleep(100)
    except KeyboardInterrupt:
            print ("exiting")
            f.write("terminating server...")
            f.flush()
            sys.exit()


if __name__ == '__main__':
    main()