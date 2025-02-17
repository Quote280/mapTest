# import serial
# import time

# import pathfinder3D
# from pathfinder3D import map3D

# try:
#     # Open the serial port that your arduino is connected to.
#     if __name__ == "__main__":
#         import random
#         test_mode = True
#     ser = serial.Serial('/dev/ttyUSB0', 230400)  # Change '/dev/ttyACM0' to your serial port
#     print("Serial port opened succesfully")
#     activeCom = True
# except:
#     print("Please check the port and connection to the arduino")
#     activeCom = False

# def decodeCam():
#     if activeCom:
#         left = False
#         right = False
#         timeBeginning = time.time()
#         while time.time() - timeBeginning < 0.5:
#             if ser.in_waiting > 0:
#                 incoming = ser.read()
#                 incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
#                 mask = 1
#                 if incomingInt & mask:
#                     left = True
#                 if incomingInt & (mask << 1):
#                     right = True  
#                 print(f"received: {incoming} to int: {bin(incomingInt)} left: {left} right: {right}")
#                 return left, right  
#         print("no data and error in activeCom")
#     else:
        # return True, True

# def camSendToArduino(amountLeft=0, amountRight=0): 
#     if activeCom:
#         ser.write(amountLeft.to_bytes(1, 'big'))
#         ser.write(amountRight.to_bytes(1, 'big'))
#         ser.flush()
#         print(f"sent: byte l+r ({amountLeft}, {amountRight})")

# def serialMonitor():
#     timeBeginning = time.time()
#     incoming = None
#     incoming_str = "monitor: "
#     while time.time() - timeBeginning < 0.1 and incoming != b'\n':
#         if ser.in_waiting > 0:
#             incoming = ser.read()
#             incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
#             incoming_str += incoming.decode('utf-8')
#             #incomingString = incoming.decode("utf-8")
#             if isinstance(incoming, bytes):
#                 pass
#                 #print(f"Monitor: {incoming} to int: {bin(incomingInt)} als string: {incoming.decode('utf-8')}")
#             else:
#                 print("error in decoding for monitor")
#                 # print(f"Monitor: {incoming} to int: {bin(incomingInt)}")
#             #print("Monitor: to int: " + bin(incomingInt))
#     print(incoming_str)

# def sendRotationToArduino():
#     if activeCom:
#         print("finding Path")
#         print(f"getWalls: {map3D.getWalls(map3D.currentPosition[0],map3D.currentPosition[1],map3D.currentPosition[2])}")
#         path = pathfinder3D.findWayNextBestTile()
#         print(f"found path: {path}")
#         print("done caluclating path")
#         rotation = map3D.getRotationFromPath(path)
#         print(f"rotation of the robot will be: {rotation}")
#         if rotation == -1:
#             rotation = 3
#         print(f"rotation is: {rotation}")
#         ser.write(rotation.to_bytes(1, 'big'))
#         ser.flush()
                    
# def receiveInput():
#     if activeCom:
#         identifier = ser.read()
#         identifierInt = int.from_bytes(identifier, byteorder="big", signed=False)
#         if identifierInt != 32:
#             print(f"identifier: {identifierInt}")
#         # cam
#         if identifierInt == 1: 
#             print("getting asked for recue kits")
#             left, right = decodeCam()
#             print(f"get asked for kits: {left} r: {right}")
#             if test_mode:
#                 camSendToArduino(random.randint(0, 4), random.randint(0, 4))
#             else:
#                 return left, right
#         # set Walls
#         elif identifierInt == 2:
#             print("setting walls")
#             incoming = ser.read()
#             incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
#             mask = 1
#             if incomingInt & mask:
#                 top = True
#             else:
#                 top = False
#             if incomingInt & (mask << 1):
#                 right = True
#             else:
#                 right = False
#             if incomingInt & (mask << 2):
#                 bottom = True
#             else:
#                 bottom = False
#             if incomingInt & (mask << 3):
#                 left = True
#             else:
#                 left = False
#             print(f"top, right, bottom, right: {top}, {right}, {bottom}, {right}")
#             map3D.setWalls(map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPostition[2], top, right, bottom, left)
#         # robot interaction
#         elif identifierInt == 3:
#             incoming = ser.read()
#             incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
#             if incomingInt == 1:
#                 print("forward")
#                 map3D.moveForward()
#             elif incomingInt == 2:
#                 print("turn left")
#                 map3D.turnLeft()
#             elif incomingInt == 3:
#                 print("turn right")
#                 map3D.turnRight()
#             elif incomingInt == 4:
#                 print("setBlack")
#                 map3D.setBlack(map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPosition[2])
#             elif incomingInt == 5:
#                 print("set checkpoint")
#                 map3D.setLastCheckpoint(map3D.currentPosition)
#             elif incomingInt == 6:
#                 # get to last checkpoint
#                 print("going to last checkpoint on map")
#                 map3D.goToLastCheckpoint()
#             elif incomingInt == 7:
#                 # send path
#                 print("sending rotation to Arduino")
#                 sendRotationToArduino()
#             elif incomingInt == 8:
#                 print("set start position")
#                 map3D.setBlue(map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPosition[2])
#         #ramp
#         elif identifierInt == 4:
#             sign = ser.read() #might have to be passed through a from_bytes()
#             incoming = ser.read()
#             incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
#             print("set Ramp incline to {incomingInt}")
#             map3D.setRamp(map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPosition[2], incomingInt, sign)
#         # monitor
#         elif identifierInt == 32:
#             serialMonitor()
#         else:
#             print("invalid identifier")
#     return False, False     

# if __name__ == "__main__":
#     while True:
#         if(ser.in_waiting >= 1):
#             receiveInput()




from picamera2 import Picamera2, Preview
import cv2 as cv
import time

import algorithm_detector as ad
from picamera2 import Picamera2, Preview

show_images = True


picam2_left = Picamera2(0)
print(picam2_left.sensor_modes)
config = picam2_left.create_preview_configuration(main={"size": (728,544), "format": 'XRGB8888'},
                                             sensor={'output_size': (1456, 1088)} )

picam2_right = Picamera2(1)
print(picam2_right.sensor_modes)
config = picam2_right.create_preview_configuration(main={"size": (728,544), "format": 'XRGB8888'},
                                             sensor={'output_size': (1456, 1088)} )

picam2_left.configure(config)
picam2_right.configure(config)
# picam2.start_preview(Preview.QTGL)
picam2_left.start()
picam2_right.start()

while True:
    # Capture frame-by-frame
    frame_left = picam2_left.capture_array()
    frame_right = picam2_right.capture_array()
    # Our operations on the frame come here
    # letter_left, frame_left = ad.run_letter_detection(frame_left, show_images, "left")
    # print(letter_left)
    
    # letter_right, frame_right = ad.run_letter_detection(frame_right, show_images, "right")
    # print(letter_right)
    cv.imshow('orginial left', frame_left)
    cv.imshow('original right', frame_right)
    frame_left = ad.convertToBW(frame_left)
    frame_right = ad.convertToBW(frame_right)
    frame_left = cv.resize(frame_left, (1456, 1088))
    frame_right = cv.resize(frame_right, (1456, 1088))
    cv.imshow('result detection_left', frame_left)
    cv.imshow('result detection_right', frame_right)
    
    if cv.waitKey(1) == ord('q'):
        break
