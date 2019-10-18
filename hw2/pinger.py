import sys
import socket
import os
import struct
import select
import time

ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket.getprotobyname('icmp')
message = ""
packageNum = 10
destIP = ""

def checksum(msg):
    sum = 0
    countTo = (len(msg)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(msg[count + 1])*256 + ord(msg[count])
        sum += thisVal
        sum = sum & 0xffffffff # Necessary?
        count = count + 2
 
    if countTo<len(msg):
        sum = sum + ord(msg[len(msg) - 1])
        sum = sum & 0xffffffff # Necessary?
 
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
 
    answer = answer >> 8 | (answer << 8 & 0xff00)
 
    return answer
    

 
def receive_one_ping(my_socket, ID, timeout, message, dest_ip):

    timeLeft = timeout
    while True:
        startedSelect = time.time()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return
 
        timeReceived = time.time()
        recPacket, addr = my_socket.recvfrom(1024)
        TTL = ord(recPacket[8:9])
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
        if packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            delay = 1000*(timeReceived - timeSent)
            print ("Reply from " + dest_ip + ": bytes=" + str(packageNum) +" ddl=" + str(TTL) + " time=%0.4fms" % delay)
            return delay
            
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return


def send_one_ping(my_socket, dest_addr, ID, message):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr  =  socket.gethostbyname(dest_addr)
 
    my_checksum = 0
 
    # Make a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", time.time()) + data
 
    my_checksum = checksum(header + data)
 
    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
    )
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1
 

def do_one(dest_addr, timeout, message):
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error as msg:
        msg = msg + (
            " - Note that ICMP messages can only be sent from processes"
            " running as root."
        )
        raise socket.error(msg)
 
    my_ID = os.getpid() & 0xFFFF
 
    send_one_ping(my_socket, dest_addr, my_ID, message)
    delay = receive_one_ping(my_socket, my_ID, timeout, message, dest_addr)
 
    my_socket.close()
    return delay
 

if __name__ == '__main__':

    logfile = ""
    if len(sys.argv) < 7:
        print ("missing paramter")
        sys.exit()

    logfile = ""

    for x in range (len(sys.argv)):
        if sys.argv[x] == "-p":
            message = sys.argv[x+1]
            x += 1
        elif sys.argv[x] == "-c":
            packageNum = int(sys.argv[x+1])
            x += 1
        elif sys.argv[x] == "-d":
            destIP = sys.argv[x+1]
            x += 1
        elif sys.argv[x] == "-l":
            logfile = sys.argv[x+1]
            x+=1
        

    if logfile != "":
        f = open(logfile, "w+")
        f.write("\n")
        f.flush()

    source_ip = '192.168.1.101'
    dest_ip = destIP

    print ("Ping " + dest_ip + " with " + str(packageNum) + " bytes of data \"" + message + "\"")

    for i in range(packageNum):
        try:
            delay  =  do_one(dest_ip, 2, message)
        except socket.gaierror as e:
            print ("failed. (socket error: '%s')" % e[1])
            break
 
        if delay  ==  None:
            print ("failed. (timeout within %ssec.)" % 2)
