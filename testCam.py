import time
import os.path
import shutil

import socket
import sys
import commands
import math

#added by ziv - a websocket class
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

#added by ziv - a geo helper class
import geopy
from geopy.distance import VincentyDistance,vincenty

import cv2

CAMERA = True
server_up = True
TIMEOUT=10

        
if CAMERA:
    import picamera	
    camera = picamera.PiCamera()
    camera.ISO = 100
    camera.exposure = "snow"


isFound = False
for x in range(0, 4): #try 4 times
    camera.capture('/tmp/image.jpg')
    output = commands.getstatusoutput('~/aruco-1.3.0/build/utils/aruco_test /tmp/image.jpg ' + data[1])
    if output[0] == 0:
        if output[1] == data[1]:
            isFound = True
            break
if isFound:
    print 'FOUND'
elif output[1] == "WRONGQR":
    print 'WRONGQR'
else:
    print 'NOQR'

shutil.copy2('/tmp/image.jpg', '/var/www/html/image.jpg')
 