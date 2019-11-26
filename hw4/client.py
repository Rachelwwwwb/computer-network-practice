import sys
import socket
import threading
from _thread import *
import threading

registered = False

class sendThread (threading.Thread):   
    def __init__(self, sock, clientName ,server_address,f):
        threading.Thread.__init__(self)
        self.sock = sock
        self.clientName = clientName
        self.server_address = server_address
        self.f = f
    def run(self): 
        send_msg(self.sock, self.clientName, self.server_address,self.f)

class receiveThread (threading.Thread):   
    def __init__(self, sock, f):
        threading.Thread.__init__(self)
        self.sock = sock
        self.f = f
    def run(self): 
        recv_msg(self.sock,self.f)


def recv_msg (sock,f):
    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode().upper() == "WELCOME":
            pass
        else:
            name = str(addr[0]) + "," + str(addr[1])
            f.write("recvfrom " + name + " received")
            f.flush()
            print("recvfrom " + name + " received")

def send_msg (s, name, addr, f):
    while True:
        try: 
            text = input("")
            message = "".join(text.split()[1:])
            f.write("sending " + message + "\n")
            f.flush()
            print ("sending " + message + "\n")
            s.sendto(text.encode(), addr)
            
        except EOFError:
            continue
        except KeyboardInterrupt:
            sys.exit()

def main():
    if len(sys.argv) < 5:
        print("missing parameters")
        sys.exit()

    for x in range(len(sys.argv)):
        if sys.argv[x] == "-p":
            x += 1
            port = sys.argv[x]
        elif sys.argv[x] == "-l":
            x += 1
            logfile = sys.argv[x]
        elif sys.argv[x] == "-d":
            x += 1
            destIP = sys.argv[x]
        elif sys.argv[x] == "-n":
            x += 1
            clientName = sys.argv[x]

    f = open(logfile, "w+")
    f.write("connecting to the server "+ destIP + " at port "+ port + "\n")
    f.flush()   
    print ("connecting to the server "+ destIP + " at port "+ port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (destIP, int(port))
    
    #only send once: register some time
    registerMessage = "register "+ clientName
    sock.sendto(registerMessage.encode(encoding="utf-8"), server_address)
    f.write("sending register message " + str(clientName) + "\n")
    f.flush()
    print ("sending register message " + str(clientName))

    thread_send = sendThread(sock,clientName,server_address,f)
    thread_receive = receiveThread(sock, f)
    thread_receive.start()
    thread_send.start()

if __name__ == "__main__":
    main()