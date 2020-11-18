import sys
import socket
import random

def start_game(conn):
    while True:
        mess = conn.recv(1024).decode()
        mess_stripped = mess.strip()
        if len(mess_stripped) > 3:
            mess1 = mess.split(" ")
            command = str(mess1[0]).strip()
            number = str(mess1[1]).strip()
            if command == "TRY" and number.isdigit():
                conn.send("GRR\n".encode())

        if mess_stripped == "TIC":
            conn.send("TOC\n".encode())
        if mess_stripped == "QUI":
            conn.send("BYE\n".encode())
            conn.close()
            break

        if mess_stripped == "STA":
            n = random.randint(0, 100)
            print(n)
            conn.send("RDY\n".encode())
            while True:
                data = str(conn.recv(1024).decode())
                data_stripped = data.strip()
                tahmin = data.split(" ")
                if len(data_stripped) < 4:
                    if data_stripped == "TIC":
                        conn.send("TOC\n".encode())
                    if data_stripped == "QUI":
                        conn.send("BYE\n".encode())
                        conn.close()
                        break
                if len(data_stripped) > 4:
                    sayi = int(tahmin[1])
                    #if sayi is not int
                        #conn.send("PRR".encode())
                    if sayi > n:
                        conn.send("GTH\n".encode())
                    if sayi < n:
                        conn.send("LTH\n".encode())          
                    if sayi == n:
                        conn.send("WIN\n".encode())
                        break
                    #if data == "STA":
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

    start_game(c,)

server_socket.close()
