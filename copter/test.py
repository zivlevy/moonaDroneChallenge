
import picamera
import time
import os.path
import shutil

from droneapi.lib import VehicleMode, Location, Command
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative

from pymavlink import mavutil
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
"""
Connecting to Quadcopter
"""

#added by ziv - establish a web socket server
print "start"
camera = picamera.PiCamera()
camera.ISO = 100
camera.exposure = "snow" 
camera.capture('/tmp/image.jpg')
print "read1"
id="129"
output = commands.getstatusoutput('~/aruco-1.3.0/build/utils/aruco_test /tmp/image.jpg '+ id)
shutil.copy2('/tmp/image.jpg', '/var/www/html/image.jpg')
print output
if output[0] == 0:
#    self.frag_type = 0x1
    print "the id " + output[1]
    if output[1] == "WRONGQR":
        print "wrong"
 #       self.sendMessage('WRONGQR')
    elif output[1] == id:
        print "found"
  #      self.sendMessage('FOUND')
    else:
   #     self.sendMessage('NOQR')
        print "NOQR"

   
    
print "Done"        
