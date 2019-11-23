
import socket      
import sys         							
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

f = open(logfile, "w+")
f.write("server started on localhost at port "+ port + "...\n")
f.flush()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
s.bind(('localhost', int(port)))        							# Bind to the port
print (" Binding completed  ! !")

while True:
    data, client_address = s.recvfrom(1024)
    if (data):
        if data.decode().split()[0].upper() == "REGISTER":
            welcomemsg = "WELCOME"
            print ("register successfully")
            s.sendto(welcomemsg.upper().encode(), client_address) 
        elif data.decode().split()[0].upper() == "SENDTO":
            s.sendto(data,client_address)
            
        prepend = data.decode().split()
        welcomemsg = "WELCOME"
        s.sendto(welcomemsg.upper().encode(), client_address)
