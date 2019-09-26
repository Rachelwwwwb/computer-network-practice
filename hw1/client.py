import sys
import socket
from _thread import *
import threading

port = ""
logfile = ""
serverIP = ""
clientName = ""

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

if not port or not logfile or not serverIP or not clientName:
    print("missing parameters")
    sys.exit()

f = open(logfile, "w+")
f.write("connecting to the server "+ serverIP + " at port "+ port + "\n")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (serverIP, int(port))
    #register some time
    registerMessage = "register "+clientName
    sock.sendto(registerMessage.encode(encoding="utf-8"), server_address)
    f.write("sending register message " + str(clientName) + "\n")

    try:
        hasInput = True
        while(hasInput):
            # contantly receive message from others
            data, server_detail = sock.recvfrom(1024)
            data = data.decode(encoding='utf-8')
            #print out the data for debug
            #print (data)
            #if receive from the server
            if str(data) == "WELCOME " + clientName.upper():
                f.write("received welcome\n")

            #constantly waiting for an input to send to others
            answer = str(input())
            #if exit
            if answer.upper() == "EXIT":
                hasInput = False
            elif answer[:6].upper() == "SENDTO":
                user_input = str(clientName) + answer[7:]
                data = user_input.encode(encoding="utf-8") 
                sock.sendto(data, server_address)

    # except:
    #     print ("Something went wrong while connecting to server")
    finally:
        f.write("terminating client...\n")
        data = "exit".encode(encoding="utf-8")
        sock.sendto(data, server_address) 
        sock.close()