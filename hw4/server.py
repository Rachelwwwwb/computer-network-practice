
import socket      
import sys         							
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
f.flush()
print ("server started on localhost at port " + port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
s.bind(('localhost', int(port)))        							# Bind to the port

while True:
    data, client_address = s.recvfrom(1024)
    if (data):
        if data.decode().split()[0].upper() == "REGISTER":
            f.write("client connection from " + str(client_address[0]) + "," + str(client_address[1])+"\n")
            f.write("received register " + str(data.decode().split()[0])+ " from " + str(client_address[0]) + "," + str(client_address[1]))
            welcomemsg = "WELCOME"
            s.sendto(welcomemsg.upper().encode(), client_address) 
        elif data.decode().split()[0].upper() == "SENDTO":
            f.write("recvfrom " + str(client_address[0]) + "," + str(client_address[1]) + " " + "".join(data.decode().split()[1:])+"\n")
            f.flush()
            s.sendto(data,client_address)
        else:
            print ("here")
            msg = "".join(data.decode().split()[2:])
            f.write("recvfrom " + str(data.decode().split()[0]) + "," + str(data.decode().split()[1]) + " " + msg + "\n")
            f.flush()
            print ("recvfrom " + str(data.decode().split()[0]) + "," + str(data.decode().split()[1]) + " " + msg)
            s.sendto(data,client_address)
