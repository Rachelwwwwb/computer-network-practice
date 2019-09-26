import sys
import socket

logfile = ""
port = ""

for x in range(len(sys.argv)):
    if sys.argv[x] == "-p":
        x += 1
        port = sys.argv[x]
    elif sys.argv[x] == "-l":
        x += 1
        logfile = sys.argv[x]
if not logfile or not port :
    print ("missing inputs")
    sys.exit()
    
f = open(logfile, "w+")
# declare a register dict
register = None
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
s.bind(('localhost', int(port)))    							# Bind to the port
f.write("server started on "+s.getsockname()[0]+ " at port "+ port + "...\n")

while True:
    data, client_address = s.recvfrom(1024)
    data = str(data.decode(encoding='utf-8').upper())

    #if it is a register message
    if str(data)[:8] == "REGISTER":
        f.write("client connection from host port\n")
        userName = str(data)[9:].upper()
        #the register dic has not created yet
        if register is None:
            register = {userName : client_address}
        elif userName not in register:
            register.update({userName : client_address})
        else:
            # has registered
            break
        f.write("received register " + userName + " from host port" + "\n")
        print (client_address)
        s.sendto(str("WELCOME "+ userName).encode(encoding='utf-8'), client_address)

    elif data == "EXIT":
        f.write("terminating server...\n")
    elif data[:6].upper() == "SENDTO":
        print (data)
        print (register.get(data.split()[2]))
        # if register is None?
        s.sendto(data.encode(encoding='utf-8'), register.get(data.split()[2]))
