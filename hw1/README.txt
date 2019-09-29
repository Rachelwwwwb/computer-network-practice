USC ID: 3692163617
Compiling instructions: follow the hw instructions
additional notes: 
    1. To terminate the server, you may need to hit control c twice
    2. Sometimes the compiler will stop you from running saying "Address already in use". In this case,
    you could either change the overlayport, or wait for some time (less than 1 min usually), or kill the process manually by doing:
    sudo lsof -i:8080   //where 8080 is the port num
    kill xxxx   //use the provided pid
    3. The user name IS case sensitive
