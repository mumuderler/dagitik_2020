from multiprocessing import Queue, Process, Lock, current_process
import sys

#mumuderler

def encrypt(key, harf):
    if len(harf) > 1:
        return
        
    encrypted = ""
    c = harf
    c = c.lower()
    #print(c)
	
    if c.isalpha():
        c_index = ord(c) - ord('a')
        c_shifted = (c_index + key) % 26 + ord('a')
        c_new = chr(c_shifted).upper()
        encrypted += c_new
    else:
        encrypted += c

    return encrypted
    
def process(key, block_len, work_queue, lock):

    for letter in iter(work_queue.get, "DUR"):
      
        lock.acquire()
        for i in range(block_len):
        	book_enc.append(encrypt(key, work_queue.get()))
        lock.release()       
    #print("AAAA")  
    return True

      
key = int(sys.argv[1])
nmProcess = int(sys.argv[2])
block_len = int(sys.argv[3])

process_list = []
book_enc = []

l = Lock()

f = open("edgardoe.txt", "r")
book = []
while 1:
    char = f.read(1)
    book.append(char)
    if not char:
    	break
f.close()

work_queue = Queue(len(book))

for letter in book:
   work_queue.put(letter)

for p in range(nmProcess):
    p = Process(target=process, args=(key,block_len,work_queue,l))
    p.start()
    process_list.append(p)
    work_queue.put("DUR")
        
#print("asdas")

#processlerin sonlanma konusunda sikintisi var

for process in process_list:
    print("aaa")
    process.join()
        
#print("asdas")
print(book_enc)

g = open('sample2.txt', 'w')
for element in book_enc:
    g.write(element)
g.close()
