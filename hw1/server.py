import sys
import socket
import os

def register (s, registered, userName, client_address, f):
    if registered is None:
        registered = {userName : client_address}
    elif userName not in registered:
        registered[userName] = client_address
        f.write("received register " + userName +" from host port\n")
        print (registered)
    #welcome 
    s.sendto(str("welcome").encode(),client_address)
    
def recv_msg(s, receiver, registered, name, message,f):
    data = receiver + ": " + message
    f.write("receivefrom " + name + " to " + receiver + " " + message+"\n")
    s.sendto(data.encode(), registered.get(receiver))

def leave (registered, name):
    del registered[name]

def parent_thread(s,f):
    registered = {}
    registered["unused"] = ("0.0.0.0" , 1)
    while True:
        data, client_address = s.recvfrom(1024)
        f.write("client connection from host port")
        dataList = data.decode().split(' ')

        print (dataList)

        if dataList[0] == 'REGISTER':  
            print ("register")
            register(s, registered, dataList[1], client_address, f)
        elif dataList[1].upper() == 'SENDTO':
            print("here")
            f.write("sendto " + dataList[2] + " from " + dataList[0] + " " + dataList[3]+"\n")
            recv_msg(s, dataList[2], registered, dataList[0], ' '.join(dataList[3:]),f)
        elif dataList[1] == 'EXIT':
            leave(registered, dataList[1])
    
def main():

    if len(sys.argv) < 3:
        print("missing parameters")
        sys.exit()
    
    for x in range(len(sys.argv)):
        if sys.argv[x] == "-p":
            x += 1
            port = sys.argv[x]
        elif sys.argv[x] == "-l":
            x += 1
            logfile = sys.argv[x]
    
    f = open(logfile, "w+")
    f.write("server started on localhost at port "+ port + "...\n")

    # declare a register dict
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', int(port)))    							# Bind to the port


    pid = os.fork()
    if pid < 0:
        sys.exit("fail")
    elif pid is not 0:
        parent_thread(s,f)

if __name__ == '__main__':
    main()


# while True:
#     data, client_address = s.recvfrom(1024)
#     data = str(data.decode(encoding='utf-8').upper())

#     #if it is a register message
#     if str(data)[:8] == "REGISTER":
#         f.write("client connection from host port\n")
#         userName = str(data)[9:].upper()
#         #the register dic has not created yet
#         if register is None:
#             register = {userName : client_address}
#         elif userName not in register:
#             register.update({userName : client_address})
#         else:
#             # has registered
#             break
#         f.write("received register " + userName + " from host port" + "\n")
#         print (client_address)
#         s.sendto(str("WELCOME "+ userName).encode(encoding='utf-8'), client_address)

#     elif data == "EXIT":
#         f.write("terminating server...\n")
#     elif data[:6].upper() == "SENDTO":
#         print (data)
#         print (register.get(data.split()[2]))
#         # if register is None?
#         s.sendto(data.encode(encoding='utf-8'), register.get(data.split()[2]))
