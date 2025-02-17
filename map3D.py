# Reading and writing map data
import numpy as np
import time
# Structure of the map
# Hier: Stellen innerhalb einer binären Zahl(-enfolge) (r. -> l.)
# 0: north
# 1: east
# 2: south
# 3: west
# 4: blue
# 5: ramp
# 6: seen
# 7: unknown
# following bytes: ramp: z coord to which ramp leads

# variables
sizeOfMap = 33
sizeOfMapHalf = sizeOfMap//2
height = 20
halfHeight = height // 2

#Array deklariert
posLastCheckpoint = np.array([halfHeight, sizeOfMapHalf, sizeOfMapHalf])

#3D Array deklariert und initialisiert mit dem Wert 143 (= 10001111), heißt alle sind unbekannt und alle Richtungen treffen zu. Nutzt 16 bit unsigned integer 
map = np.full((height, sizeOfMap, sizeOfMap), 143, dtype='u2')

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

currentPosition = np.array([halfHeight, sizeOfMapHalf, sizeOfMapHalf], dtype='u1')
currentRotation = NORTH


## Getter Functions ##

def getBlack(z, y, x):
    if getWalls(z, y, x) == (True,True,True,True) and getUnknown(z, y, x) == False:
        print(f"z: {z}y: {y} x: {x} map[z, y, x]: bin: {bin(map[z, y, x])} map[z, y, x]: {map[z, y, x]}")
        return True
    return False

#Returns the walls of a tile as multiple variables according to the given coordinates
def getWalls(z, y, x):
    val = map[z, y, x]
    north = val & 1
    if north != 0:
        north = True
    east = val & 2
    if east != 0:
        east = True
    south = val & 4
    if south != 0:
        south = True
    west = val & 8
    if west != 0:
        west = True
    return north,east,south,west

#Returns the blue value of a tile with the given coordinates
def getBlue(z, y, x):
    val = map[z, y, x]
    blue = val & 16
    return blue

#s.o.
def getRamp(z, y, x):
    val = map[z, y, x]
    ramp = val & 32
    return ramp

#seen but not visited tile
def getSeen(z, y, x):
    val = map[z, y, x]
    seen = val & 64
    return seen

def getUnknown(z, y, x):
    val = map[z, y, x]
    unknown = val & 128
    return unknown

def getVisited(z, y, x):
    if getSeen(z, y, x) == 0 and getUnknown(z, y, x) == 0:
        return True
    return False

def getTargetZ(z,y,x):
    if map[z,y,x] & 32:
        return map[z,y,x] >> 8
    else:
        return z 

def RelativeToAbsolutWalls(north, east, south, west):
    if currentRotation == NORTH:
        return north, east, south, west
    elif currentRotation == EAST:
        return west, north, east, south
    elif currentRotation == SOUTH:
        return south, west, north, east
    elif currentRotation == WEST:
        return east, south, west, north
    
    
## Setter Functions ##

def setBlue(z, y, x,blue):
    if map[z, y, x] & 16:
        if blue == False:
            map[z, y, x] -= 16
    else:
        if blue == True:
            map[z, y, x] += 16
    
def setSeen(z, y, x,seen):
    if map[z, y, x] & 64:
        if seen == False:
            map[z, y, x] -= 64
    else:
        if seen == True and getUnknown(z, y, x):
            map[z, y, x] += 64

def setUnknown(z, y, x,unknown):
    if map[z, y, x] & 128:
        if unknown == False:
            map[z, y, x] -= 128
    else:
        if unknown == True:
            map[z, y, x] += 128

def setLastCheckpoint(pos):
    global posLastCheckpoint
    posLastCheckpoint = np.copy(pos) 

def goToLastCheckpoint():
    global currentPosition
    currentPosition = np.copy(posLastCheckpoint)
    print(f" set back to last checkpoint currentPosition: {currentPosition}")

def setBlack(z, y, x):
    if currentRotation == NORTH:
        setWalls(z,y + 1,x,True,True,True,True)
    elif currentRotation == EAST:
        setWalls(z,y,x + 1,True,True,True,True)
    elif currentRotation == SOUTH:
        setWalls(z,y - 1,x,True,True,True,True)
    elif currentRotation == WEST:
        setWalls(z,y,x - 1,True,True,True,True)


maxAngle = 25
angleCoefficient = 1 #quick and dirty PID for angle
heightDifferenceMaxAngleRamp = 3

#should work 3d: possible pitfall: tile ends not correctly identified on ramp
def setRamp(z, y, x, angle, sign):
    if angle > maxAngle:
        angleCoefficient = 25 / angle
    angle = angle * angleCoefficient #see above, quick and dirty PID
    if sign == 255:
        angle = angle * (-1)#printing only displays positive values, possibility that angle is never negative...
    differenceZ = ceil(angle * (heightDifferenceMaxAngleRamp / maxAngle))

    #on the "level" from which the robot came, only the side from which the robot came is declared "open" (no wall)
    #on the "level" to which the ramp leads, the side on which the robot "left" the ramp is declared
    setWalls(z,y,x,True,True,False,True)
    setWalls(z + differenceZ,y,x,False,True,True,True)
    if map[z,y,x] & 32 or map[z + differenceZ,y,x] & 32:
        map[z,y,x] -= 32
        map[z + differenceZ,y,x] -= 32
    else:
        map[z,y,x] += 32 + (differenZ + z) * (2**8)
        map[z + differenceZ,y,x] += 32 + z * (2**8)

    # if currentRotation == NORTH:
    #     setWalls(z,y-1,x,True,True,False,True)
    #     setWalls(z + differenceZ,y-1,x,False,True,True,True)
    #     if map[z,y - 1,x] & 32 or map[z + differenceZ,y - 1,x] & 32:
    #         map[z,y - 1,x] -= 32
    #         map[z + differenceZ,y - 1,x] -= 32
    #     else:
    #         map[z,y - 1,x] += 32 + (differenZ + z) * (2**8)
    #         map[z + differenceZ,y - 1,x] += 32 + z * (2**8)
    # elif currentRotation == EAST:
    #     setWalls(z,y,x - 1, True,True,False,True)
    #     setWalls(z + differenceZ,y,x - 1, False,True,True,True)
    #     if map[z,y,x - 1] & 32 or map[z + differenceZ,y,x - 1] & 32:
    #         map[z,y,x - 1] -= 32
    #         map[z + differenceZ,y,x -1] -= 32
    #     else:
    #         map[z,y,x - 1] += 32 + (differenZ + z) * (2**8)
    #         map[z + differenceZ,y,x -1] += 32 + z * (2**8)
    # elif currentRotation == SOUTH:
    #     setWalls(z,y + 1,x, True, True, False, True)
    #     setWalls(z + differenceZ,y + 1,x, False, True, True, True)
    #     if map[z,y + 1,x] & 32 or map[z + differenceZ, y + 1,x] & 32:
    #         map[z,y + 1,x] -= 32
    #         map[z + differenceZ, y + 1, x] -= 32
    #     else:
    #         map[z, y + 1, x] += 32 + (differenZ + z) * (2**8)
    #         map[z + differenceZ, y + 1, x] += 32 + z * (2**8)
    # elif currentRotation == WEST:
    #     setWalls(z,y, x + 1, True, True, False , True)
    #     setWalls(z + differenceZ,y, x + 1, False, True, True , True)
    #     if map[z,y,x + 1] & 32 or map[z + differenceZ, y, x + 1]:
    #         map[z,y, x + 1] -= 32
    #         map[z + differenceZ, y, x + 1] -= 32
    #     else:
    #         map[z,y,x + 1] += 32 + (differenZ + z) * (2**8)
    #         map[z + differenceZ, y, x + 1] += 32 + z * (2**8)

#should work 3d
def setWalls(z, y, x,north,east,south,west):
    setSeen(z, y, x,False)
    setUnknown(z, y, x,False)

    north, east, south, west = RelativeToAbsolutWalls(north, east, south, west)

    if getBlack(currentPosition[0], currentPosition[1] + 1 , currentPosition[2]):
        north = True
    if getBlack(currentPosition[0], currentPosition[1], currentPosition[2] + 1):
        east = True
    if getBlack(currentPosition[0], currentPosition[1] - 1, currentPosition[2]):
        south = True
    if getBlack(currentPosition[0], currentPosition[1], currentPosition[2] - 1):
        west = True

    print(f"translated: {north}, {east}, {south}, {west}")
    for i in range(4):
        if i == 0:
            neighbourX = 0
            neighbourY = 1
            wall = north
        elif i == 1:
            neighbourX = 1
            neighbourY = 0
            wall = east * 2
        elif i == 2:
            neighbourX = 0
            neighbourY = -1
            wall = south * 4
        elif i == 3:
            neighbourX = -1
            neighbourY = 0
            wall = west * 8
        
        if map[z, y, x] & (2**i) != wall:
            if wall:
                map[z, y, x] += wall
            else:
                map[z, y, x] -= 2**i

        if map[z,y+neighbourY,x+neighbourX] & (2**((i + 2) % 4)) != (2**((i + 2) % 4)) * bool(wall):
            print(f"y: {y} x: {x} i: {i} neighbourY: {neighbourY} neighbourX: {neighbourX} wall: {wall} map[z,y+neighbourY,x+neighbourX]: {bin(map[z,y+neighbourY,x+neighbourX])} calc: {map[z,y+neighbourY,x+neighbourX] & (2**((i + 2) % 4))} calc2: {2**i * (not bool(wall))}")
            if wall:
                map[z,y+neighbourY,x+neighbourX] += 2**((i + 2) % 4)
            else:
                map[z,y+neighbourY,x+neighbourX] -= 2**((i + 2) % 4)

        if not wall and not getBlack(z,y+neighbourY,x+neighbourX):
            setSeen(z,y+neighbourY, x+neighbourX, True)
            setUnknown(z,y+neighbourY, x+neighbourX, False)
    
#######################
# Interface:
#######################    

#3D
def getRotationFromPath(path): 
    #path[n, 1] is y coord, path[n, 2] x coord
    if path[0,1] < path[1,1]:
        gotoTile = NORTH
    elif path[0,1] > path[1,1]:
        gotoTile = SOUTH
    elif path[0,2] < path[1,2]:
        gotoTile = EAST
    elif path[0,2] > path[1,2]:
        gotoTile = WEST
    
    gotoTile -= currentRotation
    if gotoTile <= -3:
        gotoTile += 4
    elif gotoTile >= 3:
        gotoTile -= 4
    return gotoTile

#3D
def moveForward():
    global currentPosition
    global currentRotation
    if(getRamp(currentPosition[0], currentPosition[1], currentPosition[2])):
        currentPosition[0] = (map[currentPosition[0], currentPosition[1], currentPosition[2]] >> 8)
        usedZLayers[currentPosition] = True
    if currentRotation == NORTH:
        currentPosition[1] += 1
    elif currentRotation == EAST:
        currentPosition[2] += 1
    elif currentRotation == SOUTH:
        currentPosition[1] -= 1
    elif currentRotation == WEST:
        currentPosition[2] -= 1

def turnLeft():
    global currentRotation
    currentRotation -= 1
    if currentRotation < NORTH:
        currentRotation = WEST

def turnRight():
    global currentRotation
    currentRotation += 1
    if currentRotation > WEST:
        currentRotation = NORTH
        