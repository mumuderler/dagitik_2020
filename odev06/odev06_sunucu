import socket
import threading
import queue
import datetime
import os
import sys

class lThread(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        print(self.name,"starting")

    def run(self):
        f = open("./text.txt","w", buffering = 1)
        while True:
            data = self.queue.get()
            now = datetime.datetime.now()
            f.write(str(now)+" ")
            f.write(data)            

class rThread(threading.Thread):
    def __init__(self, name, connection, queue, quits, loggerQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.connection = connection
        self.queue = queue
        self.quits = quits
        self.loggerQueue = loggerQueue

    def run(self):
        self.flag = False
        self.flag2 = False
        print(self.name, "Starting.")
        self.loggerQueue.put(self.name + " Starting.\n")
        while True:
            if self.quits == True:
                print(self.name, "Exiting.")
                self.loggerQueue.put(self.name + " Exiting.\n")
                self.connection.close()
                break         
            data = self.connection.recv(1024)

            strip = (data.decode()).strip()
            self.loggerQueue.put(self.name+": "+strip+"\n")

            self.incoming_parser(data.decode())

            if strip == "QUI":
                self.quits = True 


        #self.connection.close()

    def incoming_parser(self, data):
        msg = data.strip().split(" ")
        print("Kullanıcı:", msg)
        if msg[0] == "":
            pass

        elif msg[0] == "NIC" and len(msg) == 2 and self.flag2 == False:
            if msg[1] in sozluk:
                self.queue.put("REJ\n")
                self.loggerQueue.put("Sunucu: "+"REJ\n")

            else:
                self.queue.put("WEL\n")
                self.loggerQueue.put("Sunucu: "+"WEL\n")

                sozluk[msg[1]] = self.queue
                self.name = msg[1]
                self.flag = True
                self.flag2 = True

                self.loggerQueue.put("WRN: "+self.name+" Kullanıcısı gruba katıldı.\n")

                for client in sozluk:
                    sozluk[client].put("WRN: "+self.name+" Kullanıcısı gruba katıldı.\n")

        elif msg[0] == "QUI" and len(msg) == 1:
            self.queue.put("BYE "+self.name+"\n")
            self.loggerQueue.put("Sunucu: "+"BYE "+self.name+"\n")

            if self.flag == True:
                sozluk.pop(self.name)

        elif msg[0] == "PIN" and len(msg) == 1:
            self.queue.put("PON\n")
            self.loggerQueue.put("Sunucu: "+"PON\n")
            
        elif self.flag == True and (msg[0] == "GLS" or msg[0] == "GNL" or msg[0] == "PRV"  or msg[0] == "OKW" or msg[0] == "OKP" or msg[0] == "OKG" or msg[0] == "TIN"):
            if msg[0] == "GLS" and len(msg) == 1:
                str1 = ":"
                str1 = str1.join(sozluk.keys())
                self.queue.put("LST "+str1+"\n")
                self.loggerQueue.put("Sunucu: "+"LST "+str1+"\n")

            elif msg[0] == "GNL":
                self.queue.put("OKG\n")
                self.loggerQueue.put("Sunucu: "+"OKG\n")

                str1 = " "
                str1 = str1.join(msg[1:])

                for client in sozluk:
                    sozluk[client].put(self.name+":"+str1+"\n")
                    self.loggerQueue.put("Sunucu: "+self.name+":"+str1+"\n")

            elif msg[0] == "PRV":
                data = str(msg[1]).split(":")
                receiver = data[0]
                
                str2 = " "
                str2 = str2.join(msg[1:])
                #mesaj = data[1:]

                if receiver not in sozluk:
                    self.queue.put("NOP "+receiver+"\n")
                    self.loggerQueue.put("Sunucu: "+"NOP "+receiver+"\n")
                    
                else:
                    self.queue.put("OKP\n")
                    self.loggerQueue.put("Sunucu: "+"OKP\n")
                    
                    sozluk[receiver].put(self.name+":"+str2+"\n")
                    self.loggerQueue.put("Sunucu: "+self.name+":"+receiver+" "+str2+"\n")

            elif msg[0] == "OKW":
                print("OKW")
                self.loggerQueue.put("Sunucu: OKW\n")

            elif msg[0] == "OKP":
                print("OKP")
                self.loggerQueue.put("Sunucu: OKP\n")

            elif msg[0] == "OKG":
                print("OKG")
                self.loggerQueue.put("Sunucu: OKG\n")

            elif msg[0] == "TIN":
                print("TON")
                self.loggerQueue.put("Sunucu: TON\n")                    

            else:
                self.queue.put("ERR\n")
                self.loggerQueue.put("Sunucu: "+"ERR\n")
                
            
        elif self.flag == False and (msg[0] == "GLS" or msg[0] == "GNL" or msg[0] == "PRV"):
            self.queue.put("LRR\n")
            self.loggerQueue.put("Sunucu: "+"LRR\n")

        else:
            self.queue.put("ERR\n") 
            self.loggerQueue.put("Sunucu: "+"ERR\n")

class wThread(threading.Thread):
    def __init__(self, name, connection, queue, quits):
        threading.Thread.__init__(self)
        self.connection = connection
        self.queue = queue
        self.name = name
        self.quits = quits

    def run(self):
        print(self.name, "Starting.")
        while True:     
            data = self.queue.get()
            self.connection.send(data.encode())
            print("Istemci", data)
            if self.quits == True:
                print(self.name, "Exiting.")
                #self.connection.close()
                break                

server_socket = socket.socket()

host = sys.argv[1]
port = int(sys.argv[2])
server_socket.bind((host, port))
print("socket binded to port", port)
server_socket.listen(5)
print("socket is listening")

sozluk = {}
a = False

LoggerQueue = queue.Queue()
loggerThread = lThread("Logger Thread",LoggerQueue)
loggerThread.start()

while True:
    conn_socket, addr = server_socket.accept()
    print("Connected to :", addr[0],":",addr[1])

    queue1 = queue.Queue()
    readThread = rThread("Read Thread", conn_socket, queue1, a, LoggerQueue)
    writeThread = wThread("Write Thread", conn_socket, queue1, a)

    readThread.start()
    writeThread.start()
