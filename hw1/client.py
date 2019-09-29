import sys
import socket
import threading
from _thread import *
import threading


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
        if data.decode() == 'EXIT':
            sys.exit(0)
        elif data.decode().upper() == "WELCOME":
            f.write("received welcome \n")
        print(data.decode())

def send_msg (s, name, addr, f):
    while True:
        try: 
            text = input("")
            if text.upper() == "EXIT":
                # exit the chatroom
                # not sure if send anything to somebody else
                data = "EXIT " + name
                s.sendto(data.encode(), addr)
                f.write("terminating client...\n")
                sys.exit()
                del s
            else:
                dataList = text.split(" ")
                f.write("sendto " + str(dataList[1]) + " " + str(dataList[2:]) + "\n")
                text = name + " " + text
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
        elif sys.argv[x] == "-s":
            x += 1
            serverIP = sys.argv[x]
        elif sys.argv[x] == "-n":
            x += 1
            clientName = sys.argv[x]

    f = open(logfile, "w+")
    f.write("connecting to the server "+ serverIP + " at port "+ port + "\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (serverIP, int(port))
    
    #only send once: register some time
    registerMessage = "REGISTER "+ clientName
    sock.sendto(registerMessage.encode(encoding="utf-8"), server_address)
    f.write("sending register message " + str(clientName) + "\n")

    
    thread_send = sendThread(sock,clientName,server_address,f)
    thread_receive = receiveThread(sock, f)
    thread_send.start()
    thread_receive.start()

if __name__ == "__main__":
    main()