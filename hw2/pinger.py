import sys

message = ""
packageNum = 10
destIP = ""
logfile = ""
if len(sys.argv) < 9:
    print ("missing paramter")
    sys.exit()

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
    elif sys.argv[x] == "-l"
        logfile = sys.argv[x+1]
        x+=1
    

    