
import socket      
import sys       

natTable = {}
assignPort = 10000

if len(sys.argv) < 3:
        print("missing parameters")
        sys.exit()

for x in range(len(sys.argv)):
    if sys.argv[x] == "-p":
        x += 1
        destPort = sys.argv[x]
    elif sys.argv[x] == "-l":
        x += 1
        logfile = sys.argv[x]
    elif sys.argv[x] == "-m":
        x += 1
        myport = sys.argv[x]
    elif sys.argv[x] == "-d":
        x += 1
        destIP = sys.argv[x]
    elif sys.argv[x] == "-i":
        x += 1
        IP = sys.argv[x]

f = open(logfile, "w+")

server_address = (destIP, int(destPort))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
s.bind(("localhost", int(myport)))        							# Bind to the port
print (" Binding completed  ! !")

while True:
    data, client_address = s.recvfrom(1024)
    # print (" Received connection from : ", client_address)
    if (data):
        # register the the client name and assign a new port
        print (data.decode())
        if data.decode().split()[0].upper() == "REGISTER":
            newport = assignPort
            assignPort += 1
            natTable[client_address] = newport
            welcomemsg = "WELCOME"
            name = "".join(data.decode().split()[1:])
            writeMsg = name + " | " + str(client_address[0]) + "," + str(client_address[1]) + " | " + IP + "," + str(newport)
            f.write(writeMsg)
            f.flush()
            print (writeMsg)
            s.sendto(welcomemsg.upper().encode(), client_address)
        elif data.decode().split()[0].upper() == "SENDTO":
            msg = data.decode().split()[1:]
            msg1 = "".join(msg)
            prepend = IP + " " + str(newport)

            msg1 = prepend + " " + msg1
            print (msg1)
            s.sendto(msg1.encode(),server_address)
        # receive back from the server 
        elif data.decode().split()[0] == IP:
            newport = int(data.decode().split()[1])
            for address in natTable:
                if natTable[address] == newport:
                    s.sendto(data,address)
