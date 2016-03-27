import os,time
import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        while True:
        	time.sleep(0.001)
        print "Exiting " + self.name


filename = 'test.txt'
last = t  = 0
print t




class droneCommands(WebSocket):
    isAck = False
    def handleMessage(self):
        # echo message back to client
        print "message"
        
    def handleConnected(self):
        print self.address, 'connected'
        

    def handleClose(self):
        print self.address, 'closed'

    def file_monitor():
        global t,last
        while 1:
            if os.path.isfile(filename) :
                t = os.path.getmtime(filename)
                if t > last:
                    last = t
                    ##place your function here
                    print "change"
                    self.sendMessage("change")
                    time.sleep(1)   


thread1 = myThread(1, "Thread-1", 1)
thread1.start()

server = SimpleWebSocketServer('', 8001, droneCommands)
print "Server is up - waiting for client connection"
server.serveforever()
