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
        self.flag = False           #NIC yazmadan önce GLS PRV GNL'nin kullanımını engellemek icin
        self.flag2 = False          #aynı isimdi kullanıcı kaydını engllemek için
        self.banned = []
        
    def run(self):

        print(self.name, "Starting.")
        self.loggerQueue.put(self.name + " Starting.\n")
        while True:
            data = self.connection.recv(1024)

            strip = (data.decode()).strip()
            self.loggerQueue.put(self.name+": "+strip+"\n")

            self.incoming_parser(data.decode())

            if not data and self.flag2 == True: #client rumuz aldıktan sonra QUI yazmazdan çıkarsa
                lobby.pop(self.name)
                self.connection.close()
                break
            if not data and self.flag2 == False:
                self.connection.close()
                break
            if strip == "QUI":
                print(self.name, "Exiting.")
                self.loggerQueue.put(self.name + " Exiting.\n")

        #self.connection.close()

    def incoming_parser(self, data):
        msg = data.strip().split(" ")
        print("Client:", msg)

        if msg[0] == "":
            pass

        elif msg[0] == "REG" and len(msg) == 3:                                               #registration
            user = msg[1]
            password = msg[2]
            if user in registered:
                self.queue.put("REF\n")                                     #registration failed
                self.loggerQueue.put("Sunucu: "+"REF\n")
            elif user not in registered and not password.isdigit():         #password not numeric
                self.queue.put("PSW\n")                                     
                self.loggerQueue.put("Sunucu: "+"PSW\n")
            else:                                                           #registration succesful.
                self.queue.put("RES "+ user +"\n")
                self.loggerQueue.put("Sunucu: "+"RES "+ msg[1]+"\n")
                registered[user] = password                                 #added to registered dictionary

        elif msg[0] == "CHA":                                               #change password
            if msg[1] not in registered:
                self.queue.put("USR\n")                                     #user not found
                self.loggerQueue.put("Sunucu: "+"USR\n")
            elif msg[1] in registered and not msg[2].isdigit():        
                self.queue.put("PSW\n")                                     #password not numeric
                self.loggerQueue.put("Sunucu: "+"PSW\n")
            else:                                                           
                self.queue.put("CHS\n")                                     #password changed succesfully.
                self.loggerQueue.put("Sunucu: "+"CHS\n")
                registered[msg[1]] = msg[2]                                 

        elif msg[0] == "NIC" and len(msg) == 3 and self.flag2 == False and msg[1] not in lobby:
            user = msg[1]
            password = msg[2]
            if user not in registered.keys() or not registered:                              #user not found
                self.queue.put("USR\n")
                self.loggerQueue.put("USR\n")    

            elif password != registered[user]:                                #NIC password not match
                self.queue.put("PSW\n")
                self.loggerQueue.put("Sunucu: "+"PSW\n")

            else:
                self.queue.put("WEL "+ user +"\n")
                self.loggerQueue.put("WEL "+ user +"\n")

                lobby[user] = self.queue
                self.name = user
                self.flag = True
                self.flag2 = True

                uye[self.name] = []
                yonetici[self.name] = [] 
                banned[self.name] = []

                self.loggerQueue.put("WRN: "+self.name+" Kullanıcısı gruba katıldı.\n")

                for client in lobby:
                    lobby[client].put("WRN: "+self.name+" Kullanıcısı gruba katıldı.\n")

        elif msg[0] == "QUI" and len(msg) == 1:
            self.queue.put("BYE "+self.name+"\n")
            self.loggerQueue.put("Sunucu: "+"BYE "+self.name+"\n")
            for client in lobby:
                lobby[client].put("User named "+self.name+" has left the group.\n")
            self.loggerQueue.put(("User named "+self.name+" has left the group.\n"))
            if self.flag == True:
                lobby.pop(self.name)
                self.flag = False
                self.flag2 = False
                #self.name = "Read Thread"

        elif msg[0] == "PIN" and len(msg) == 1:
            self.queue.put("PON\n")
            self.loggerQueue.put("Sunucu: "+"PON\n")
            
        elif self.flag == True and (msg[0] == "GLS" or msg[0] == "GNL" or msg[0] == "PRV"  or msg[0] == "OKW" or msg[0] == "OKP" or msg[0] == "OKG" or msg[0] == "TIN" or msg[0] =="OPG"
        or msg[0] == "SHW" or msg[0] =="ENT" or msg[0] == "EXI" or msg[0] == "WHR" or msg[0] == "KCK" or msg[0] == "CLO" or msg[0] == "BAN" or msg[0] == "PRO"):
            if msg[0] == "GLS" and len(msg) == 2:                           
                room = msg[1]
                if room == "lobby":
                    lobby_list = []
                    for key in lobby:
                        lobby_list.append(key)
                    str2 = ":"
                    str2 = str2.join(lobby_list)
                    self.queue.put("LST "+str2+"\n")
                    self.loggerQueue.put("LST "+str2+"\n")
                else:        
                    if room not in rooms:                                           #room not exists
                        self.queue.put("ONE\n")
                        self.loggerQueue.put("ONE\n")  
                    elif not rooms[room]:                                           #room is empty
                        self.queue.put("NOU\n")
                        self.loggerQueue.put("NOU\n")
                    else:                                                           #show users in the room
                        str1 = ":"
                        str1 = str1.join(rooms[room])
                        self.queue.put("LST "+str1+"\n")
                        self.loggerQueue.put("Sunucu: "+"LST "+str1+"\n")


            elif msg[0] == "GNL":
                room = msg[1]
                if room not in rooms:                                           #room not exists
                    self.queue.put("ONE\n")
                    self.loggerQueue.put("ONE\n")  
                else:                                                           #message sent
                    self.queue.put("OKG\n")
                    self.loggerQueue.put("Sunucu: "+"OKG\n")

                    seperator = " "
                    message = seperator.join(msg[2:])

                    for client in rooms[room]:
                        lobby[client].put(self.name+":"+message+"\n")
                        self.loggerQueue.put("Sunucu: "+self.name+":"+message+"\n")

            elif msg[0] == "PRV":
                data = str(msg[1]).split(":")
                receiver = data[0]
                
                seperator = " "
                message = seperator.join(msg[1:])

                if receiver not in lobby:                                       #user not found
                    self.queue.put("USR "+receiver+"\n")
                    self.loggerQueue.put("Sunucu: "+"USR "+receiver+"\n")
                    
                else:                                                           #private message sent
                    self.queue.put("OKP\n")
                    self.loggerQueue.put("Sunucu: "+"OKP\n")
                    
                    lobby[receiver].put(self.name+":"+message+"\n")
                    self.loggerQueue.put("Sunucu: "+self.name+":"+receiver+" "+message+"\n")

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

            elif msg[0] == "OPG" and len(msg) == 2:
                room = msg[1]
                
                if room in rooms:                                                 #room already exists
                    self.queue.put("ODE\n")                                       
                    self.loggerQueue.put("ODE\n")
                else:
                    rooms[room] = []
                    self.queue.put("WEC\n")
                    self.loggerQueue.put("WEC\n")
                    rooms[room].append(self.name)                                 #add user to the room
                    yonetici[self.name].append(room)                              #add user to the yoneticiler dictionary
                    print(yonetici)
            elif msg[0] == "SHW":
                if rooms:                                                         #show rooms
                    str1 = ":"
                    str1 = str1.join(rooms.keys())
                    self.queue.put("LST: "+str1+"\n")
                    self.loggerQueue.put("Sunucu: "+"LST: "+str1+"\n") 
                else:
                    self.queue.put("NOO\n")                                       #user not in any room
                    self.loggerQueue.put("NOO\n") 

            elif msg[0] == "ENT":
                room = msg[1]
                if room in rooms and room not in banned[self.name]:                     #room exists and not banned
                    self.queue.put("WEU "+self.name+"\n")       
                    self.loggerQueue.put("WEU "+self.name+"\n") 
                    rooms[room].append(self.name)
                    uye[self.name].append(room)
                    
                    self.loggerQueue.put("INC: "+self.name+" Kullanıcısı odaya girdi.\n")
                    for client in rooms[room]:
                        lobby[client].put("INC: "+self.name+" Kullanıcısı odaya girdi.\n")

                elif room in rooms and room in banned[self.name]:                       #room exists and banned
                    self.queue.put("BNN\n")
                    self.loggerQueue.put("BNN\n")
                else:
                    self.queue.put("NOO\n")                                       #no rooms                     
                    self.loggerQueue.put("NOO\n") 

            elif msg[0] == "EXI":
                room = msg[1]
                if room in rooms and room in uye[self.name]:                    #exit room #list #.values()
                    rooms[room].remove(self.name)
                    uye[self.name].remove(room)
                    self.queue.put("BYE\n")
                    self.loggerQueue.put("BYE\n")    

                    self.loggerQueue.put("ONG: "+self.name+" Kullanıcısı odadan çıktı.\n")
                    for client in rooms[room]:
                        lobby[client].put("ONG: "+self.name+" Kullanıcısı odadan çıktı.\n")                
                if room not in rooms:                                             #room not exists
                    self.queue.put("ONE\n")
                    self.loggerQueue.put("ONE\n")

            elif msg[0] == "KCK" and len(msg) == 3:
                room = msg[1]
                user = msg[2] 
                value = False
                if room not in rooms:                                            #room does not exists
                    self.queue.put("ONE\n")                                    
                    self.loggerQueue.put("ONE\n")         
                elif user not in registered:                                         #user not found
                    self.queue.put("USR\n")
                    self.loggerQueue.put("USR\n")                     
                else:
                    users_in_room = rooms[room]                             
                    if user in users_in_room:                                   
                        for key,val in yonetici.items():
                            if key == self.name and room in val:                #user kicked from the room
                                rooms[room].remove(user)
                                if user in uye[user]:
                                    uye[user].remove(room)
                                else:
                                    yonetici[user].remove(room)     
                                self.queue.put("KCD\n")
                                self.loggerQueue.put("KCD\n")
                                lobby[user].put("KLK You have been kicked from "+room+"\n")
                                self.loggerQueue.put("KLK You have been kicked from "+room+"\n")
                                for client in rooms[room]:
                                    lobby[client].put("KLG "+user+" has been kicked from the room.\n")
                                self.loggerQueue.put("KLG "+user+" has been kicked from the room.\n")
                                value = True
                        if value == False:
                            self.queue.put("YET\n")
                            self.loggerQueue.put("YET\n")                            
                    else:
                        self.queue.put("USR\n")
                        self.loggerQueue.put("USR\n")

            elif msg[0] == "CLO" and len(msg) == 2:
                value = False
                room = msg[1]
                if room not in rooms:                                           #room does not exists
                    self.queue.put("ONE\n")
                    self.loggerQueue.put("ONE\n")
                else:
                    for key,val in yonetici.items():                                #kick users
                        if key == self.name and room in val:
                            value = True
                            for client in rooms[room]:
                                lobby[client].put("The room "+room+" has been closed.\n")
                            self.loggerQueue.put("The room "+room+" has been closed.\n")                                                    
                            for user in lobby:
                                if room in uye[user]:
                                    uye[user].remove(room)
                            rooms.pop(room)
                            self.queue.put("OKS "+msg[1]+"\n")
                            self.loggerQueue.put("OKS "+msg[1]+"\n")
                    
                    if value == True:
                        self.queue.put("YET\n")
                        self.loggerQueue.put("YET\n")                    
            
            elif msg[0] == "BAN" and len(msg) == 3:
                room = msg[1]
                user = msg[2]
                value = False
                if room not in rooms:                                            #room does not exists
                    self.queue.put("ONE\n")                                    
                    self.loggerQueue.put("ONE\n")         
                elif user not in registered:                                         #user not found
                    self.queue.put("USR\n")
                    self.loggerQueue.put("USR\n")
                else:
                    for key,val in yonetici.items():
                        if key == self.name and room in val:                #user banned from the room
                            banned[user].append(room)
                            self.queue.put("BND\n")
                            self.loggerQueue.put("BND\n")    
                            lobby[user].put("You have been banned from the room "+room+"\n")
                            self.loggerQueue.put("You have been banned from the room "+room+"\n")              
                            users_in_room = rooms[room]
                            if user in users_in_room:
                                rooms[room].remove(user)
                                uye[user].remove(room)                          
                                self.queue.put("KCD\n")
                                self.loggerQueue.put("KCD\n")  
                                value = True
                    if value == False:
                        self.queue.put("YET\n")
                        self.loggerQueue.put("YET\n")  
                             
            elif msg[0] == "WHR" and len(msg) == 1:                             #show the rooms in which user participates
                rooms_user_in = []
                for key,val in uye.items():
                    if key == self.name:
                        for room in val:
                            rooms_user_in.append(room)

                for key,val in yonetici.items():
                    if key == self.name:
                        for room in val:
                            rooms_user_in.append(room)
                str1 = ":"
                str1 = str1.join(rooms_user_in)
                if rooms_user_in:
                    self.queue.put("LSI "+str1+"\n")
                    self.loggerQueue.put("LSI "+str1+"\n")
                    
                else:                                                           #not in a room
                    self.queue.put("NOI\n")                                     
                    self.loggerQueue.put("NOI\n")

            elif msg[0] == "PRO" and len(msg) == 3:
                room = msg[1]
                user = msg[2]
                value = False
                if not room in rooms:                                       #room does not exists
                    self.queue.put("ONE\n")                                    
                    self.loggerQueue.put("ONE\n")         
                elif user not in rooms[room]:                                     #user not found
                    self.queue.put("USR\n")
                    self.loggerQueue.put("USR\n")                
                else:                                                       
                    for key,val in yonetici.items():                        
                        if key == self.name and room in val:                                                       
                            yonetici[user].append(room)                           #user added to yonetici dictionary
                            self.queue.put("PRM\n")
                            self.loggerQueue.put("PRM\n")
                            for client in rooms[room]:
                                lobby[client].put("YON\n")
                            self.loggerQueue.put("YON\n")
                            value = True
                    if value == False:
                        self.queue.put("YET\n")
                        self.loggerQueue.put("YET\n")
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

server_socket = socket.socket()

host = sys.argv[1]
port = int(sys.argv[2])
server_socket.bind((host, port))
print("socket binded to port", port)
server_socket.listen(5)
print("socket is listening")

registered = {}          #kisi-sifre
lobby ={}                #kisi ve queue
rooms = {}               #oda ve icindeki kisiler
yonetici = {}            #kisi-oda ikilisi
uye = {}                 #kisi-oda ikilisi
banned = {}

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
