import threading
import sys

letter_index = 0

def encrypt(kitap,key):
    encrypted = ""
    global letter_index
    c = kitap[letter_index]
    c = c.lower()
    if c.isalpha():
        c_index = ord(c) - ord('a')
        c_shifted = (c_index + key) % 26 + ord('a')
        c_new = chr(c_shifted).upper()
        encrypted += c_new
    else:
        encrypted += c
    
    letter_index += 1
    return encrypted
    

class myThread(threading.Thread):
    def __init__(self, threadID, name, key, block_len, Tlock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.key = key
        self.block_len = block_len
        self.Tlock = Tlock
    def run(self):
        while letter_index + block_len*4 < len(book):
            for i in range(block_len):
                print("starting" + self.name)
                self.Tlock.acquire()
                book_enc.append(encrypt(book,key))
                self.Tlock.release()
                print("exiting" + self.name)


def createThread(nmThread,key,block_len,Tlock):
    for i in range(nmThread):
        thread = myThread(i, "thread"+str(i), key, block_len, Tlock)
        threads.append(thread)

f = open("edgardoe.txt", "r")
book = []
while 1:
    char = f.read(1)
    book.append(char)
    if not char:
        break
f.close()

book_enc = []
threads = []

exitFlag = 0

key = int(sys.argv[1])
nmThread = int(sys.argv[2])
block_len = int(sys.argv[3])
threadLock = threading.Lock()

createThread(nmThread, key, block_len, threadLock)
for t in threads:
    t.start()
for t in threads:
    t.join()

print(book_enc)
g = open('sample.txt', 'w')
for element in book_enc:
    g.write(element)
g.close()
