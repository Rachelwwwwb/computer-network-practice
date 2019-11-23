
import socket      
import sys       

natTable = {}

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
f.write("server started on " + IP + " at port "+ myport + "...\n")
f.flush()

server_address = (destIP, int(destPort))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
s.bind((IP, int(myport)))        							# Bind to the port
print (" Binding completed  ! !")

while True:
    data, client_address = s.recvfrom(1024)
    # print (" Received connection from : ", client_address)
    if (data):
        # register the the client name and assign a new port
        print (data.decode())
        if data.decode().split()[0].upper() == "REGISTER":
            newport = 5555
            natTable[client_address] = newport
            welcomemsg = "WELCOME"
            print ("register successfully")
            s.sendto(welcomemsg.upper().encode(), client_address)
        elif data.decode().split()[0].upper() == "SENDTO":
            msg = data.decode().split()[1:]
            msg1 = "".join(msg)
            prepend = IP + " " + str(newport)

            msg1 = prepend + " " + msg1
            print (msg1)
            s.sendto(msg1.encode(),server_address)