import socket
from _thread import *
import threading
from datetime import datetime

print_lock = threading.Lock()

def threaded(c):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current time is ",current_time)

    while True:
        
        data = c.recv(1024).decode()
        data = str(data).strip()
        if not data:
            #print("GG")
            #print_lock.release()
            break
        #print(data)
        if(data == "Selam"):
            r = "Selam\n"
            c.send(r.encode())

        elif(data == "Naber"):
            r = "Iyiyim, sagol\n"
            c.send(r.encode())
            
        elif(data == 'Hava'):
            r = "Yagmurlu\n"
            c.send(r.encode()) 

        elif(data == "Haber"):
            r = "Korona\n"
            c.send(r.encode())    

        elif(data == "Kapan"):
            r = "Gule gule\n"
            c.send(r.encode())
            break

        else:
            c.send("Anlamadim\n".encode())
    #print_lock.release()
    c.close()
        

server_socket = socket.socket()

host = "0.0.0.0"

port = 12335


server_socket.bind((host, port))
print("socket binded to port", port)

server_socket.listen(5)
print("socket is listening")

while True:
    c, addr = server_socket.accept()

    #print_lock.acquire()
    print("Connected to :", addr[0],":",addr[1])

    start_new_thread(threaded, (c,))

server_socket.close()
