import os,time
import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []
class droneCommands(WebSocket):

    def handleMessage(self):
        # echo message back to client
        print "message"
        
    def handleConnected(self):
        global clients
        print self.address, 'connected'
        self.sendMessage("connected")
        clients.append(self)
        threading.Timer(1, self.file_monitor).start() 

        
        

    def handleClose(self):
        print self.address, 'closed'
    
    def file_monitor(self):
        global t,last
         
        path = os.path.dirname(os.path.abspath(__file__))
        
        filename = path + '/text.txt'
        if os.path.isfile(filename):
            t = os.path.getmtime(filename)
            if t > last:
                last = t
                print "change"
                clients[0].sendMessage("change")
                clients[0].sendMessage("change1")
                clients[0].sendMessage('/n')

                print "change after"
        threading.Timer(1, self.file_monitor).start() 




last = t  = 0
server = SimpleWebSocketServer('', 8001, droneCommands)
print "Server is up - waiting for client connection on port 8001"
server.serveforever()

