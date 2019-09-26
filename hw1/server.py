import sys
import socket
import os

def register (s, registered, userName, client_address):
    if registered is None:
        registered = {userName : client_address}
    elif userName not in registered:
        print ("line 10: " + userName + " ")
        print (client_address)
        registered[userName] = client_address
        print (registered)
    
def recv_msg(s, receiver, registered, name, message):
    print("line 12: " + message)
    data = name + ": " + message
    print ("registered list: ")
    print(registered)
    s.sendto(data.encode(), registered.get(receiver))

def leave (registered, name):
    del registered[name]

def parent_thread(s):
    registered = {}
    registered["unused"] = ("0.0.0.0" , 1)
    while True:
        data, client_address = s.recvfrom(1024)
        dataList = data.decode().split(' ')
        #for debug use
        print("line 26: ")
        print(dataList)


        if dataList[0] == 'REGISTER':  # L为请求登录
            register(s, registered, dataList[1], client_address)
        elif dataList[0].upper() == 'SENDTO':
            recv_msg(s, dataList[1], registered, dataList[1], ' '.join(dataList[2:]))
        elif dataList[0] == 'EXIT':
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
    # declare a register dict
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', int(port)))    							# Bind to the port

    f.write("server started on "+s.getsockname()[0]+ " at port "+ port + "...\n")

    pid = os.fork()
    if pid < 0:
        sys.exit("fail")
    else:
        parent_thread(s)

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
