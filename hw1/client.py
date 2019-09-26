import sys
import socket
import threading
import os

def recv_msg (sock):
    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode())

def send_msg (s, name, addr, f):
    while True:
        try: 
            text = input("")
            if text.upper() == "EXIT":
                # exit the chatroom
                # not sure if send anything to somebody else
                data = "EXIT " + name
                s.sendto(data, addr)
                f.write("terminating client...\n")
                sys.exit()
            #elif text[:6].upper() == "SENDTO":
            text = name + " " + text
            s.sendto(text.encode(), addr)
            
        except EOFError:
            continue

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
    registerMessage = "REGISTER "+clientName
    sock.sendto(registerMessage.encode(encoding="utf-8"), server_address)
    f.write("sending register message " + str(clientName) + "\n")

    pid = os.fork()
    if pid < 0:
        sys.exit("fail to create a new thread")
    elif pid == 0:
        send_msg(sock, clientName, server_address,f)
    else:
        recv_msg(sock)

if __name__ == "__main__":
    main()

    # try:
    #     hasInput = True
    #     while(hasInput):
    #         # contantly receive message from others
    #         data, server_detail = sock.recvfrom(1024)
    #         data = str(data.decode(encoding='utf-8'))
    #         #if receive from the server
    #         print ("line 47: " + data)
    #         if str(data) == "WELCOME " + clientName.upper():
    #             f.write("received welcome\n")
    #         else:
    #             print (data)

    #         #constantly waiting for an input to send to others
    #         answer = str(input())
    #         print ("to test if input is a blocking line")
    #         #if exit
    #         if answer.upper() == "EXIT":
    #             hasInput = False
    #         elif answer[:6].upper() == "SENDTO":
    #             user_input = "SENDTO" + " " + str(clientName) + " " + answer[7:]
    #             data = user_input.encode(encoding="utf-8") 
    #             sock.sendto(data, server_address)
    #         else:
    #             print ("here")
    #             continue

    # # except:
    # #     print ("Something went wrong while connecting to server")
    # finally:
    #     f.write("terminating client...\n")
    #     data = "exit".encode(encoding="utf-8")
    #     sock.sendto(data, server_address) 
    #     sock.close()