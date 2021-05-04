import requests
import threading
import time
import queue
import curses

class terminal(threading.Thread):
    def __init__(self,pairs,queue,end):
        threading.Thread.__init__(self)
        self.pairs = pairs
        self.queue = queue
        self.end = end

    def run(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        line = ""
        space = " "
        stdscr.addstr("SEMBOL   SON FİYAT   DEĞİŞİM%\n",curses.A_BLINK)

        while(self.end == False):
            try:

                curses.curs_set(1)
                
                stdscr.addstr(0,0,"SEMBOL   SON FİYAT   DEĞİŞİM%\n",curses.A_UNDERLINE)
                for i in range(4):
                    data = self.queue.get()
                    if(data[0:6] == "BTCUSD"):
                        stdscr.addstr(1,0,data,curses.A_STANDOUT)
                    if(data[0:6] == "ETHUSD"):
                        stdscr.addstr(2,0,data)
                    if(data[0:6] == "EOSUSD"):
                        stdscr.addstr(3,0,data)            
                    if(data[0:6] == "LTCBTC"):
                        stdscr.addstr(4,0,data)                                                            
                i = 0
                stdscr.addstr(5,0,"Çıkmak için CTRL+Z tuşlarına basınız.")

                stdscr.refresh()
                time.sleep(1)

                stdscr.clear()
                
                '''window.getch(6,0)
                if c == ord('q'):
                    curses.echo()
                    #curse.nocbreak()
                    stdscr.keypad(False)
                    curses.endwin()'''
            except:
                pass                

class getter_thread(threading.Thread):
    def __init__(self,pair,queue,end):
        threading.Thread.__init__(self)
        self.pair = pair
        self.queue = queue
        self.end = end
    def run(self):
        url = "https://api-pub.bitfinex.com/v2/ticker/" + 't' +  self.pair
        while(self.end == False):
            response = requests.request("GET", url)
            values = response.text[1:-1].split(",")
            if len(values) < 5:
                pass
            else:
                DAILY_CHANGE = float('{:.6f}'.format(float(values[4])))
                DAILY_CHANGE_RELATIVE = float('{:.6f}'.format(float(values[5])))
                LAST_PRICE = float('{:.6f}'.format(float(values[6])))

                string = self.pair + "   " + str(LAST_PRICE) + "     " + str(DAILY_CHANGE_RELATIVE)

                to_send = string
                self.queue.put(to_send)
            
            time.sleep(5)
        print('Terminating getter_thread\n')

if __name__ == '__main__':
    ciftler = ['BTCUSD','ETHUSD','EOSUSD','LTCBTC']
    n_ciftler = len(ciftler)
    end = False

    kuyruk = queue.Queue()
    threads = []

    terminal = terminal(ciftler,kuyruk,end)
    terminal.start()

    for cift in ciftler:
        thread = getter_thread(cift, kuyruk, end)
        threads.append(thread)
        thread.start()

    for i in threads:
        i.join()
