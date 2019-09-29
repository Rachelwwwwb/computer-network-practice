
import socket               								# Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
port = 12345                								# Reserve a port for your service.
s.bind(('localhost', port))        							# Bind to the port
print (" Binding completed  ! !")

while True:
    data, client_address = s.recvfrom(1024)
    print (" Received connection from : ", client_address)
    if (data):
        print (" Data received from client : ", str(data))
        print (" Sending data back to client : ", data.upper())
        s.sendto(data.upper(), client_address)
