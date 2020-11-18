import sys
import socket
import random
from _thread import *
import threading

def threaded(conn):

    print("Sayi bulmaca oyununa hosgeldiniz!\n")

    while True:
        mess = conn.recv(1024).decode()
        mess_stripped = mess.strip()

        mess1 = mess.split(" ")
        if len(mess1) > 1:
            command1 = str(mess1[0]).strip()
            number1 = str(mess1[1]).strip()
            if command1 == "TRY" and number1.isdigit():
                conn.send("GRR\n".encode())
            else:
                conn.send("ERR\n".encode())
                
        else:    
            if mess_stripped != "QUI" and mess_stripped != "TIC" and mess_stripped != "STA":
                conn.send("ERR\n".encode())

        if mess_stripped == "TIC":
            conn.send("TOC\n".encode())
        if mess_stripped == "QUI":
            conn.send("BYE\n".encode())
            #conn.close()
            break

        if mess_stripped == "STA":
            n = random.randint(1, 99)
            #print(n)
            conn.send("RDY\n".encode())
            while True:                                         #oyuna baslangic
                data = str(conn.recv(1024).decode())
                data_stripped = data.strip()
                tahmin = data.split(" ")

                if len(tahmin) < 2:
                    if data_stripped == "TIC":
                        conn.send("TOC\n".encode())
                    elif data_stripped == "QUI":
                        conn.send("BYE\n".encode())
                        conn.close()
                        break
                    elif data_stripped == "STA":
                        n = random.randint(1,99)
                        conn.send("RDY\n".encode())
                        #print(n)
                    else:
                        conn.send("ERR\n".encode())
                    
                elif len(tahmin) == 2:
                    if tahmin[0].strip() == "TRY" and tahmin[1].strip().isdigit():
                        sayi = int(tahmin[1])
                        if sayi > n:
                            conn.send("GTH\n".encode())
                        if sayi < n:
                            conn.send("LTH\n".encode())          
                        if sayi == n:
                            conn.send("WIN\n".encode())
                            #conn.close()
                            break
                    elif False == (tahmin[1].strip().isdigit()) and tahmin[0].strip() == "TRY":
                        conn.send("PRR\n".encode())
                    else:
                        conn.send("ERR\n".encode())
                else:
                        conn.send("ERR\n".encode())
            break
    conn.close()
           
server_socket = socket.socket()

host = "0.0.0.0"

port = int(sys.argv[1])

server_socket.bind((host, port))
print("socket binded to port", port)

server_socket.listen(5)
print("socket is listening")

while True:
    c, addr = server_socket.accept()

    print("Connected to :", addr[0],":",addr[1])

    start_new_thread(threaded, (c,))

server_socket.close()
