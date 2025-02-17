import serial
import time

import pathfinder3D
from pathfinder3D import map3D

if __name__ == "__main__":
    import random
    test_mode = True

try:
    # Open the serial port that your arduino is connected to.
    ser = serial.Serial('/dev/ttyUSB0', 230400)  # Change '/dev/ttyACM0' to your serial port
    activeCom = True
except:
    print("Please check the port and connection to the arduino")
    activeCom = False

def decodeCam():
    if activeCom:
        left = False
        right = False
        timeBeginning = time.time()
        while time.time() - timeBeginning < 0.5:
            if ser.in_waiting > 0:
                incoming = ser.read()
                incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
                mask = 1
                if incomingInt & mask:
                    left = True
                if incomingInt & (mask << 1):
                    right = True  
                print(f"received: {incoming} to int: {bin(incomingInt)} left: {left} right: {right}")
                return left, right  
        print("no data and error in activeCom")
    else:
        return True, True

def camSendToArduino(amountLeft=0, amountRight=0): #why no interaction with camera? A: The cameras should be implemented here
    if activeCom:
        ser.write(amountLeft.to_bytes(1, 'big'))
        ser.write(amountRight.to_bytes(1, 'big'))
        ser.flush()
        print(f"sent: byte l+r ({amountLeft}, {amountRight})")

def serialMonitor():
    timeBeginning = time.time()
    incoming = None
    incoming_str = "monitor: "
    while time.time() - timeBeginning < 0.1 and incoming != b'\n':
        if ser.in_waiting > 0:
            incoming = ser.read()
            incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
            incoming_str += incoming.decode('utf-8')
            #incomingString = incoming.decode("utf-8")
            if isinstance(incoming, bytes):
                pass
                #print(f"Monitor: {incoming} to int: {bin(incomingInt)} als string: {incoming.decode('utf-8')}")
            else:
                print("error in decoding for monitor")
                # print(f"Monitor: {incoming} to int: {bin(incomingInt)}")
            #print("Monitor: to int: " + bin(incomingInt))
    print(incoming_str)

def sendRotationToArduino():
    if activeCom:
        print("finding Path")
        print(f"getWalls: {map3D.getWalls(map3D.currentPosition[0],map3D.currentPosition[1],map3D.currentPosition[2])}")
        path = pathfinder3D.findWayNextBestTile()
        print(f"found path: {path}")
        print("done caluclating path")
        rotation = map3D.getRotationFromPath(path)
        print(f"rotation of the robot will be: {rotation}")
        if rotation == -1:
            rotation = 3
        print(f"rotation is: {rotation}")
        ser.write(rotation.to_bytes(1, 'big'))
        ser.flush()
                    
def receiveInput():
    if activeCom:
        identifier = ser.read()
        identifierInt = int.from_bytes(identifier, byteorder="big", signed=False)
        if identifierInt != 32:
            print(f"identifier: {identifierInt}")
        # cam
        if identifierInt == 1: #why no interaction with camera? A: This was just for testing purposes. Yes, this should be changed
            print("getting asked for recue kits")#???????????????????????????????????????????????????????????????????????????????
            left, right = decodeCam()#???????????????????????????????????????????????????????????????????????????????
            print(f"get asked for kits: {left} r: {right}")#???????????????????????????????????????????????????????????????????????????????
            if test_mode:#???????????????????????????????????????????????????????????????????????????????
                camSendToArduino(random.randint(0, 4), random.randint(0, 4))#???????????????????????????????????????????????????????????????????????????????
            else:#???????????????????????????????????????????????????????????????????????????????
                return left, right#??????????????????????????????????????????????????????????????????????????????
        # set Walls
        elif identifierInt == 2:
            print("setting walls")
            incoming = ser.read()
            incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
            mask = 1
            if incomingInt & mask:
                top = True
            else:
                top = False
            if incomingInt & (mask << 1):
                right = True
            else:
                right = False
            if incomingInt & (mask << 2):
                bottom = True
            else:
                bottom = False
            if incomingInt & (mask << 3):
                left = True
            else:
                left = False
            print(f"top, right, bottom, right: {top}, {right}, {bottom}, {right}")
            map3D.setWalls(map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPostition[2], top, right, bottom, left)
        # robot interaction
        elif identifierInt == 3:
            incoming = ser.read()
            incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
            if incomingInt == 1:
                print("forward")
                map3D.moveForward()
            elif incomingInt == 2:
                print("turn left")
                map3D.turnLeft()
            elif incomingInt == 3:
                print("turn right")
                map3D.turnRight()
            elif incomingInt == 4:
                print("setBlack")
                map3D.setBlack()
            elif incomingInt == 5:
                print("set checkpoint")
                map3D.setLastCheckpoint(map3D.currentPosition)
            elif incomingInt == 6:
                # get to last checkpoint
                print("going to last checkpoint on map")
                map3D.goToLastCheckpoint()
            elif incomingInt == 7:
                # send path
                print("sending rotation to Arduino")
                sendRotationToArduino()
            elif incomingInt == 8:
                print("set start position")
                map3D.setBlue()
        #ramp
        elif identifierInt == 4:
            incoming = ser.read()
            incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
            print("set Ramp incline to {incomingInt}")
            map3D.setRamp(incomingInt)
        # monitor
        elif identifierInt == 32:
            serialMonitor()
        else:
            print("invalid identifier")
    return False, False     

if __name__ == "__main__": #why multiple loops?
    while True:
        if(ser.in_waiting >= 2):
            receiveInput()
    # while False:
    #     outgoing = 64 
    #     ser.write(outgoing.to_bytes(1, 'little'))
    #     print(f"sending: {outgoing.to_bytes(1, 'little')}")
    #     time.sleep(2)
    # while False:
    #     if ser.in_waiting > 0:
    #         incoming = int.from_bytes(ser.read(), byteorder='big')
    #         print(f"received: {incoming}")
    #         ser.write(incoming)
    #     time.sleep(0.1)
    while activeCom:
        one = 1
        ser.write(b'0')
        #ser.write(one.to_bytes(1, 'little'))
        if ser.in_waiting:
           print(str(ser.read()))
        print("none")
        time.sleep(0.1)
            
    while True:
        if activeCom:
            if ser.in_waiting > 0:
                identifier = ser.read()
                identifierInt = int.from_bytes(identifier, byteorder="big", signed=False)
                print(f"received: {identifier} to int: {bin(identifierInt)}")
                # cam
                if identifierInt == 1:
                    print("getting asked for recue kits")
                    left, right = decodeCam()
                    
                    camSendToArduino(left, right)
                # set Walls
                elif identifierInt == 2:
                    print("setting walls")
                    incoming = ser.read()
                    incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
                    mask = 1
                    if incomingInt & mask:
                        top = True
                    else:
                        top = False
                    if incomingInt & (mask << 1):
                        right = True
                    else:
                        right = False
                    if incomingInt & (mask << 2):
                        bottom = True
                    else:
                        bottom = False
                    if incomingInt & (mask << 3):
                        left = True
                    else:
                        left = False
                    print(f"top, right, bottom, right: {top}, {right}, {bottom}, {right}")
                    map3D.setWalls(map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPosition[2], top, right, bottom, left)
                # robot interaction
                elif identifierInt == 3:
                    incoming = ser.read()
                    incomingInt = int.from_bytes(incoming, byteorder="big", signed=False)
                    if incomingInt == 1:
                        print("forward")
                        map3D.moveForward()
                    elif incomingInt == 2:
                        print("turn left")
                        map3D.turnLeft()
                    elif incomingInt == 3:
                        print("turn right")
                        map3D.turnRight()
                    elif incomingInt == 4:
                        print("setBlack")
                        map3D.setBlack()
                    elif incomingInt == 5:
                        print("set checkpoint")
                        map3D.setLastCheckpoint(map3D.currentPosition)
                    elif incomingInt == 6:
                        # get to last checkpoint
                        print("going to last checkpoint on map")
                        map3D.goToLastCheckpoint()
                    elif incomingInt == 7:
                        # send path
                        print("sending rotation to Arduino")
                        sendRotationToArduino()
                # monitor
                elif identifierInt == 32:
                    serialMonitor()
                        


                    

                
                
        
        # left, right = checkForData()
        # if left or right:
        #     sendToArduino(random.randint(0,3), random.randint(0,3))
        #     if activeCom:
        #         #while(ser.in_waiting > 0):
        #         #    answer = int.from_bytes(ser.read(), byteorder="big", signed=False)
        #         #    print(f"received: {answer} and bitwise: {bin(answer)}")
        #         #    time.sleep(0.1)
        #         pass
        #     else:
        #         print("com seems to be not properly working")
        #         time.sleep(1)