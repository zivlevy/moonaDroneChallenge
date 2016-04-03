import os,time
import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import zmq,base64,json

clients = []
class droneCommands(WebSocket):

    def handleMessage(self):
        global clients
        # echo message back to client
        print self.data
        

        
    def handleConnected(self):
        clients.append(self)
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'
        clients.remove(self)
    
def file_monitor():
    global clients
    if len(clients) == 0:
        print "return"
        threading.Timer(1, file_monitor).start()
        return
    global t,last
     
    path = os.path.dirname(os.path.abspath(__file__))
    filename = path + '/text.txt'
    if os.path.isfile(filename):
        t = os.path.getmtime(filename)
        if t > last:
            last = t
            print "change"
            clients[0].sendMessage("change")
            time.sleep(1)
    threading.Timer(1, file_monitor).start()
     

def sub():
    
    msg = socket.recv()
    print msg
    if msg=="newpicture":
        for client in clients:
            with open("/tmp/image.jpg", "rb") as imageFile:
                str = base64.b64encode(imageFile.read())
                msg = json.dumps({'type':'picture','data':str})
                client.sendMessage(msg)
    else:
        for client in clients:
            msg = json.dumps({'type':'message','data':msg})
            client.sendMessage(msg)
                
    threading.Timer(0.01, sub).start()

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, '')
socket.connect("tcp://127.0.0.1:4999")


last = t  = 0
server = SimpleWebSocketServer('', 8001, droneCommands)
threading.Timer(1, sub).start()
print "Server is up - on port 8001"
server.serveforever()

