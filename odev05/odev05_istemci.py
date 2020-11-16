import socket
import sys

address = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket()

s.connect((address,port))

while True:
    user = str(input("Please enter your command: "))
    s.send(user.encode())
    print("N:",s.recv(1024).decode())    
    if(user == "Kapan"):
        break

s.close()
