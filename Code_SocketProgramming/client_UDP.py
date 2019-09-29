import socket               # Import socket module

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)

    try:
        input = True
        while(input):
            user_input=str(raw_input('>Enter string you would like capitalize : '))
            sock.sendto(user_input, server_address)
            data, server_detail = sock.recvfrom(1024)
            print (" Received message from server : ", data)
            
            input = str(raw_input('>Do you want to send more message ? (Y/y/N/n/any character) : '))
            input = True if input in ['Y', 'y'] else False
    except:
        print ("Something went wrong while connecting to server")
    finally:
        sock.close()





