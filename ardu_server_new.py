import picamera
import time
import os.path

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
from geopy.distance import VincentyDistance
"""
Connecting to Quadcopter
"""
#api = local_connect()
#vehicle = api.get_vehicles()[0] 
#cmds = vehicle.commands

vehicle = connect('127.0.0.1:1244', wait_ready=True)

CAMERA = False
server_up = True
TIMEOUT=10

    
    
if CAMERA:	
	camera = picamera.PiCamera()
#added by ziv to culculate movment along vehicle axis
def getLocation_byDistanceAndBearing (lat, lon,distanceInKM, bearing):

    origin = geopy.Point(lat, lon)
    destination = VincentyDistance(kilometers=distanceInKM).destination(origin, bearing)
    return destination.latitude, destination.longitude

#def send_data(data):
#    print "Sending: " + data
#    client.sendall(data)


def arm():
    print "Basic pre-arm checks"
    # Don't let the user try to arm until autopilot is ready
    #while not vehicle.is_armable:
    #    print " Waiting for vehicle to initialise..."
    #    time.sleep(1)

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

def disarm():
    print "Disarming vehicle"
    
    if not vehicle.armed:
        vehicle.armed = False
        
def set_home_location(location):
    print "Setting home location"
    vehicle.home_location=location
    
def set_current_location_as_home():
    print "Setting current location as home"
    set_home_location(vehicle.location.global_frame)
    
    
def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    arm()
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    count = 0
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print "Reached target altitude"
            break
        if count > TIMEOUT:
            break
        time.sleep(1)
        count = count+1






"""
Convenience functions for sending immediate/guided mode commands to control the Copter.

The set of commands demonstrated here include:
* MAV_CMD_CONDITION_YAW - set direction of the front of the Copter (latitude, longitude)
* MAV_CMD_DO_SET_ROI - set direction where the camera gimbal is aimed (latitude, longitude, altitude)
* MAV_CMD_DO_CHANGE_SPEED - set target speed in metres/second.


"""

def condition_yaw(heading, relative=False):
    """
    Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).

    This method sets an absolute heading by default, but you can set the `relative` parameter
    to `True` to set yaw relative to the current yaw heading.

    By default the yaw of the vehicle will follow the direction of travel. After setting 
    the yaw using this function there is no way to return to the default yaw.

    """
    if relative:
        is_relative = 1 #yaw relative to direction of travel
    else:
        is_relative = 0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        10,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)




"""
Functions to make it easy to convert between the different frames-of-reference. In particular these
make it easy to navigate in terms of "metres from the current position" when using commands that take 
absolute positions in decimal degrees.

The methods are approximations only, and may be less accurate over longer distances, and when close 
to the Earth's poles.

Specifically, it provides:
* get_location_metres - Get LocationGlobal (decimal degrees) at distance (m) North & East of a given LocationGlobal.
* get_distance_metres - Get the distance between two LocationGlobal objects in metres
* get_bearing - Get the bearing in degrees to a LocationGlobal
"""

def get_location_metres(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned LocationGlobal has the same `alt` value
    as `original_location`.

    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.

    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.

    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius = 6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
        
    return targetlocation;


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. 
    """
    
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def get_bearing(aLocation1, aLocation2):
    """
    Returns the bearing between the two LocationGlobal objects passed as parameters.

    This method is an approximation, and may not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """	
    
    off_x = aLocation2.lon - aLocation1.lon
    off_y = aLocation2.lat - aLocation1.lat
    bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795
    if bearing < 0:
        bearing += 360.00
    return bearing;



"""
Functions to move the vehicle to a specified position (as opposed to controlling movement by setting velocity components).

The methods include:
* goto_position_target_global_int - Sets position using SET_POSITION_TARGET_GLOBAL_INT command in 
    MAV_FRAME_GLOBAL_RELATIVE_ALT_INT frame
* goto_position_target_local_ned - Sets position using SET_POSITION_TARGET_LOCAL_NED command in 
    MAV_FRAME_BODY_NED frame
* goto - A convenience function that can use Vehicle.simple_goto (default) or 
    goto_position_target_global_int to travel to a specific position in metres 
    North and East from the current location. 
    This method reports distance to the destination.
"""

def climb_to_altitude(altitude):
    loc = Location(vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon,vehicle.location.global_relative_frame.alt+altitude)
    goto_position_target_global_int(loc)
    count = 0
    targetAlt = vehicle.location.global_relative_frame.alt+altitude;
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt    
        if altitude > 0 and vehicle.location.global_relative_frame.alt>=targetAlt*0.95:

            print "Reached target altitude"
            break
        elif  altitude <=0 and vehicle.location.global_relative_frame.alt <= targetAlt*1.05 :
            print "Reached target altitude"
            break
        if count > TIMEOUT:
            break
        time.sleep(1)
        count = count+1
    
    
def goto_position_target_global_int(aLocation):
    """
    Send SET_POSITION_TARGET_GLOBAL_INT command to request the vehicle fly to a specified LocationGlobal.

    For more information see: https://pixhawk.ethz.ch/mavlink/#SET_POSITION_TARGET_GLOBAL_INT

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111111000, # type_mask (only speeds enabled)
        aLocation.lat*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
        aLocation.lon*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        aLocation.alt, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
        0, # X velocity in NED frame in m/s
        0, # Y velocity in NED frame in m/s
        0, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)

    currentLocation = vehicle.location.global_relative_frame
    targetLocation = aLocation
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    
    count = 0
    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        #print "DEBUG: mode: %s" % vehicle.mode.name
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        print "Distance to target: ", remainingDistance
        if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
            print "Reached target"
            break;
        if count > TIMEOUT:
            break
        count+=2
        time.sleep(2)    



def goto_position_target_local_ned(north, east, down):
    """	
    
    
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified 
    location in the North, East, Down frame.

    It is important to remember that in this frame, positive altitudes are entered as negative 
    "Down" values. So if down is "10", this will be 10 metres below the home altitude.

    Starting from AC3.3 the method respects the frame setting. Prior to that the frame was
    ignored. For more information see: 
    http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.

    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down, # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)
    
    

def goto_position_target_offset_ned(north, east, down):
    """	
    
    
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified 
    location in the North, East, Down frame.

    It is important to remember that in this frame, positive altitudes are entered as negative 
    "Down" values. So if down is "10", this will be 10 metres below the home altitude.

    Starting from AC3.3 the method respects the frame setting. Prior to that the frame was
    ignored. For more information see: 
    http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.

    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down, # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    vehicle.groundspeed = 5
    # send command to vehicle
    vehicle.send_mavlink(msg)
    
    #added by ziv - find new target location based on current heading
    currentLocation = vehicle.location.global_relative_frame
    currentBearing = vehicle.heading
    newlat,newlon = getLocation_byDistanceAndBearing (currentLocation.lat,currentLocation.lon,north/1000,currentBearing)
    newlat,newlon = getLocation_byDistanceAndBearing (newlat,newlon,east/1000,currentBearing + 90)    
    targetLocation=LocationGlobalRelative(newlat, newlon,currentLocation.alt)

    #targetLocation = get_location_metres(currentLocation, north, east)
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    print "DEBUG: targetLocation: %s" % targetLocation
    print "DEBUG: targetLocation: %s" % targetDistance
    count = 0
    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        #print "DEBUG: mode: %s" % vehicle.mode.name
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        print "Distance to target: ", remainingDistance
        if remainingDistance<=targetDistance*0.1: #Just below target, in case of undershoot.
            print "Reached target"
            break;
        if count > TIMEOUT:
            break
        count+=1
        time.sleep(1)    


def goto(dNorth, dEast, gotoFunction=vehicle.simple_goto):
    """
    Moves the vehicle to a position dNorth metres North and dEast metres East of the current position.

    The method takes a function pointer argument with a single `dronekit.lib.LocationGlobal` parameter for 
    the target position. This allows it to be called with different position-setting commands. 
    By default it uses the standard method: dronekit.lib.Vehicle.simple_goto().

    The method reports the distance to target every second.
    """
    
    
    currentLocation = vehicle.location.global_relative_frame
    targetLocation = get_location_metres(currentLocation, dNorth, dEast)
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    gotoFunction(targetLocation)
    
    print "DEBUG: targetLocation: %s" % targetLocation
    print "DEBUG: targetLocation: %s" % targetDistance
    count = 0
    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        #print "DEBUG: mode: %s" % vehicle.mode.name
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        print "Distance to target: ", remainingDistance
        if remainingDistance<=targetDistance*0.1: #Just below target, in case of undershoot.
            print "Reached target"
            break;
        if count > TIMEOUT:
            break
        count+=1

        time.sleep(1)



"""
Functions that move the vehicle by specifying the velocity components in each direction.
The two functions use different MAVLink commands. The main difference is
that depending on the frame used, the NED velocity can be relative to the vehicle
orientation.

The methods include:
* send_ned_velocity - Sets velocity components using SET_POSITION_TARGET_LOCAL_NED command
* send_global_velocity - Sets velocity components using SET_POSITION_TARGET_GLOBAL_INT command
"""

def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors and
    for the specified duration.

    This uses the SET_POSITION_TARGET_LOCAL_NED command with a type mask enabling only 
    velocity components 
    (http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned).
    
    Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
    with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
    velocity persists until it is canceled. The code below should work on either version 
    (sending the message multiple times does not cause problems).
    
    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)
    
    


def send_global_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.

    This uses the SET_POSITION_TARGET_GLOBAL_INT command with type mask enabling only 
    velocity components 
    (http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_global_int).
    
    Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
    with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
    velocity persists until it is canceled. The code below should work on either version 
    (sending the message multiple times does not cause problems).
    
    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, # lat_int - X Position in WGS84 frame in 1e7 * meters
        0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
        velocity_x, # X velocity in NED frame in m/s
        velocity_y, # Y velocity in NED frame in m/s
        velocity_z, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)    





#while not vehicle.is_armable:
   # print " Waiting for vehicle to initialise..."
  #  time.sleep(1)

"""       
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c.bind(('', 1234))
c.listen(1)
"""
class droneCommands(WebSocket):

    def handleMessage(self):
        # echo message back to client
        line = self.data
	data = line.split(":")
    	cmd_id = int(data[0])
    	if cmd_id == -1:
        	send_data("test\n")

    	elif cmd_id ==0:
        	arm()

    	elif cmd_id == 1:
        	disarm()

    	elif cmd_id ==2:

        	set_current_location_as_home()

        elif cmd_id ==3:

        	alt = float(data[1])
        	arm_and_takeoff(alt)

        elif cmd_id ==4:
            targetLocation = LocationGlobal(float(data[1]), float(data[2]),float(data[3]))
            goto_position_target_global_int(targetLocation)

        elif cmd_id ==5:
            camera.capture('/tmp/image.jpg')
            time.sleep(1)
            output = commands.getstatusoutput('~/aruco-1.3.0/build/utils/aruco_test_board /tmp/image.jpg ~/aruco-1.3.0/build/utils/board.yml camera.yml 0.5 | grep Position')
            print output
            if output[0] == 0:
                x,y,z = output[1].split(":")[1].split(",")
                print "Found: " + x + "," + y + "," + z
                goto_position_target_offset_ned(float(y)*100, -float(x)*100, 0)
           
            else:
                print "No QR found"

        elif cmd_id ==6:
            print "Flying to qr"
        
        elif cmd_id ==7:
            print "Setting altitude"
            climb_to_altitude(float(data[1]))   

        elif cmd_id ==8:
            print "Returning to launch"
            vehicle.mode = VehicleMode("RTL")

        elif cmd_id ==9:
            print "Landing"
            vehicle.mode = VehicleMode("LAND")
        
        elif cmd_id ==10:
            print "Changing mode to: " + data[1].strip()
            vehicle.mode = VehicleMode(data[1].strip())
    
        elif cmd_id ==11:
            goto_position_target_offset_ned(float(data[1]), float(data[2]), -float(data[3]))
    
        elif cmd_id == 12:
            condition_yaw(float(data[1]))
    
        elif cmd_id == 13:
            condition_yaw(float(data[1]),True)

            
        elif cmd_id == 22:
            forward = float(data[1]) 
#            currentLocation = vehicle.location.global_relative_frame
#            currentBearing = vehicle.heading
#            print currentBearing
#            newlat,newlon = getLocation_byDistanceAndBearing (currentLocation.lat,currentLocation.lon,forward/1000,currentBearing)
#            print currentLocation.lat,currentLocation.lon
#            print newlat,newlon
            goto(forward,0);

        elif cmd_id == 23:
            forward = float(data[1]) 
#            currentLocation = vehicle.location.global_relative_frame
#            currentBearing = vehicle.heading
#            print currentBearing
#            newlat,newlon = getLocation_byDistanceAndBearing (currentLocation.lat,currentLocation.lon,forward/1000,currentBearing)
#            print currentLocation.lat,currentLocation.lon
#            print newlat,newlon
            goto(-forward,0);

        elif cmd_id == 24:
            forward = float(data[1]) 
#            currentLocation = vehicle.location.global_relative_frame
#            currentBearing = vehicle.heading
#            print currentBearing
#            newlat,newlon = getLocation_byDistanceAndBearing (currentLocation.lat,currentLocation.lon,forward/1000,currentBearing)
#            print currentLocation.lat,currentLocation.lon
#            print newlat,newlon
            goto(0,forward);
        elif cmd_id == 25:
            forward = float(data[1]) 
#            currentLocation = vehicle.location.global_relative_frame
#            currentBearing = vehicle.heading
#            print currentBearing
#            newlat,newlon = getLocation_byDistanceAndBearing (currentLocation.lat,currentLocation.lon,forward/1000,currentBearing)
#            print currentLocation.lat,currentLocation.lon
#            print newlat,newlon
            goto(0,-forward);    


	self.sendMessage('ACK')
	vehicle.flush() 
    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'


#added by ziv - establish a web socket server
server = SimpleWebSocketServer('', 8000, droneCommands)
print "Server is up - waiting for client connection"
server.serveforever()
quad_commands = {0: "ARM", 1: "DISARM", 2:"SETHOME",3: "TAKEOFF", 4:"FLYTO",5:"CHECKIFQRAVAILABLE",6:"DETECTQRANDFLY",7:"SETALTITUDE8",8:"RETURNTOLAUNCH",9:"LAND",10:"SETFLIGHTMODE",11:"GOTO",12:"SETHEADINGABS",13:"SETHEADINGREL"}


"""
Accepting 1 client only, there couldn't be more than 1 ground station
"""
#client, client_address = c.accept()


#fd = client.makefile()
#for line in client.makefile('r'):

"""
    print line
    data = line.split(":")
    cmd_id = int(data[0])
    if cmd_id == -1:
        send_data("test\n")
        
    elif cmd_id ==0:
        arm()
    
    elif cmd_id == 1:
        disarm()
    
    elif cmd_id ==2:
	
        set_current_location_as_home()

    elif cmd_id ==3:
    
        alt = float(data[1])
        arm_and_takeoff(alt)

    elif cmd_id ==4:
        targetLocation = LocationGlobal(float(data[1]), float(data[2]),float(data[3]))

        goto_position_target_global_int(targetLocation)
	
    
    elif cmd_id ==5:
        camera.capture('/tmp/image.jpg')
        time.sleep(1)
	output = commands.getstatusoutput('~/aruco-1.3.0/build/utils/aruco_test_board /tmp/image.jpg ~/aruco-1.3.0/build/utils/board.yml camera.yml 0.5 | grep Position')
        print output
	if output[0] == 0:
            x,y,z = output[1].split(":")[1].split(",")
            print "Found: " + x + "," + y + "," + z
            goto_position_target_offset_ned(float(y)*100, -float(x)*100, 0)
           
        else:
            print "No QR found"
        
    
    elif cmd_id ==6:
	    print "Flying to qr"
    
    elif cmd_id ==7:
	    print "Setting altitude"
	    climb_to_altitude(float(data[1]))   
   
    elif cmd_id ==8:
        print "Returning to launch"
        vehicle.mode = VehicleMode("RTL")
    elif cmd_id ==9:
        print "Landing"
        vehicle.mode = VehicleMode("LAND")
        
    elif cmd_id ==10:
        print "Changing mode to: " + data[1].strip()
        vehicle.mode = VehicleMode(data[1].strip())
    
    elif cmd_id ==11:
    
        goto_position_target_offset_ned(float(data[1]), float(data[2]), -float(data[3]))
    
    elif cmd_id == 12:
        condition_yaw(float(data[1]))
    
    elif cmd_id == 13:
        condition_yaw(float(data[1]),True)
        
        
    send_data("ACK\n")
   """
# vehicle.flush()
   
    
print "Done"        
