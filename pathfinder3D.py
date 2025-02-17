import numpy as np
import map3D
import time

#globally needed variables
pathfinder = np.full((map3D.height,map3D.sizeOfMap,map3D.sizeOfMap), 143,dtype='u1')
pathfinderDirection = np.full((map3D.height,map3D.sizeOfMap,map3D.sizeOfMap), 5,dtype='u1')
delay = 0
usedZLayers = np.full(map3D.height, 0, dtype=u1)
usedZLayers[map3D.halfheight] = 1 
#nextTravelTile = np.full([[0,0]])
#currentTravelTile = np.full([0, 0, 0])

def pathfinderIncomplete(): # checks if there are still Fields left that havent been treated by the pathfinder
    for z in range(len(pathfinder)):
        if usedZLayers[z] == 1:
            for y in range(len(pathfinder[z])):
                for x in range(len(pathfinder[z,y])):
                    if pathfinder[z,y,x] == 64: #every tile that hasnt been assigned a distance from the current tile is 64
                        return True
    return False

def mapIncomplete():
    #if there are no tiles that have been seen but not visited, all tiles must have been visited, so the robot can return to the start
    for z in range(len(map3D.map)):
        if usedZLayers[z] == 1:
            for y in range(len(map3D.map[z])):
                for x in range(len(map3D.map[z,y])):
                    if (map3D.getSeen(z,y,x)):
                        return True
    return False

#rewriting this probably wouldnt hurt
def assignDistance(): # assigns every visited Field the value of the distance from the current tile: basically a dijkstra(not optimized)
    currentNumber = 0 #not tile id, but distance to current tile
    while(pathfinderIncomplete()):
        print(f"pathfidner still incomplete {currentNumber}")
        #first loops through all neighbours of all tiles with distance  (i.e. current tile), then through all
        #neighbours of all tiles with distance 1, etc., always assigning the treated tiles the distance from the current tile
        for z in range(len(pathfinder)):
            if usedZLayers[z] == 1:
                for y in range(len(pathfinder[z])):
                    for x in range(len(pathfinder[z,y])):
                        if pathfinder[z,y,x] == currentNumber:
                            print(f"pathfinder is currentNumber : {currentNumber} at {z} {y} {x} ")
                            print(f"map[z,y,x] {bin(map3D.map[z,y,x])}")
                            time.sleep(delay)
                            if (not(map3D.map[z,y,x] & 1)) and pathfinder[z,y + 1,x] == 64: #checks wether the Tile North is accessable and wasn't treated by the pathfinder yet
                                pathfinder[z,y + 1,x] = currentNumber + 1
                                print("TileNorth is accessable and wasn't treated by the pathfinder yet")
                                time.sleep(delay)
                                if (map3D.map[z,y + 1,x] & 16): #checks wether a accessible Tile North is Blue
                                    pathfinder[z,y + 1,x] += 5
                                if (map3D.map[z,y + 1,x] & 32): #checks wether a accessible Tile North is a ramp
                                    pathfinder[z,y + 1,x] += 6
                                    pathfinder[(map3D.getTargetZ(map3D.map[z, y + 1, x])), y + 1, x] += 7 #incremented by 1 since it hadnt been incremented by one like original z
                                    if (map3D.map[z,y + 1,x] & 16):
                                        pathfinder[(map3D.getTargetZ(map3D.map[z, y + 1, x])), y + 1, x] += 6
                            if (not(map3D.map[z,y,x] & 2)) and pathfinder[z,y,x + 1] == 64: #checks wether the Tile East is accessable and wasn't treated by the pathfinder yet
                                pathfinder[z,y,x + 1] = currentNumber +1
                                print("TileEast is accessable and wasn't treated by the pathfinder yet")
                                time.sleep(delay)
                                if (map3D.map[z,y,x + 1] & 16): #checks wether a accessible Tile East is Blue
                                    pathfinder[z,y,x + 1] += 5
                                if (map3D.map[z,y,x + 1] & 32): #checks wether a accessible Tile East is a ramp
                                    pathfinder[z,y,x + 1] += 6
                                    pathfinder[(map3D.getTargetZ(map3D.map[z, y, x + 1])), y, x + 1] += 7 #incremented by 1 since it hadnt been incremented by one like original z
                                    if (map3D.map[z, y, x] & 16):
                                        pathfinder[(map3D.getTargetZ(map3D.map[z, y, x + 1])), y, x + 1] += 6
                            if (not(map3D.map[z,y,x] & 4)) and pathfinder[z,y - 1,x] == 64: #checks wether the Tile South is accessable and wasn't treated by the pathfinder yet
                                pathfinder[z,y - 1,x] = currentNumber +1
                                print("TileSouth is accessable and wasn't treated by the pathfinder yet")
                                time.sleep(delay)
                                if (map3D.map[z,y - 1,x] & 16): #checks wether a accessible Tile South is Blue
                                    pathfinder[z,y - 1,x] += 5
                                if (map3D.map[z,y - 1,x] & 32): #checks wether a accessible Tile South is a Ramp
                                    pathfinder[z,y - 1,x] += 6
                                    pathfinder[(map3D.getTargetZ(map3D.map[z,y - 1,x])), y - 1, x] += 7 #incremented by 1 since it hadnt been incremented by one like original z
                                    if (map3D.map[z, y - 1, x] & 16):
                                        pathfinder[(map3D.getTargetZ(map3D.map[z, y - 1, x])), y - 1, x] += 6
                            if (not(map3D.map[z,y,x] & 8)) and pathfinder[z, y, x - 1] == 64: #checks wether the Tile West is accessable and wasn't treated by the pathfinder yet
                                pathfinder[z,y,x - 1] = currentNumber +1
                                print("TileWest is accessable and wasn't treated by the pathfinder yet")
                                time.sleep(delay) 
                                if (map3D.map[z,y,x - 1] & 16): #checks wether a accessible Tile West is Blue
                                    pathfinder[z,y,x - 1] += 5
                                if (map3D.map[z,y,x - 1] & 32): #checks wether a accessible Tile West is a ramp
                                    pathfinder[z,y,x - 1] += 6
                                    pathfinder[(map3D.getTargetZ(map3D.map[z, y, x - 1])), y, x - 1] += 7 #incremented by 1 since it hadnt been incremented by one like original z
                                    if (map3D.map[z, y, x - 1] & 16):
                                        pathfinder[(map3D.getTargetZ(map3D.map[z, y, x - 1])), y + 1, x - 1] += 6
        currentNumber += 1
        print(pathfinder)
        time.sleep(delay)


def getNextBestTile(): # searches for the nearest tile that was seen but not visited
    #set every unknown ot black tiles to 128, known Tiles to 64, current Tile to 0, prepares the assignment
    for z in range(len(map3D.map)):
        if usedZLayers[z] == 1:
            for y in range(len(map3D.map[z])):
                for x in range(len(map3D.map[z,y])):
                    if map3D.map[z,y,x] & 128 or map3D.map[z,y,x] == 15:
                        pathfinder[z,y,x] = 128
                    else:
                        pathfinder[z,y,x] = 64
    pathfinder[map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPosition[2]] = 0
    print(f"pathfinder intiialised {pathfinder}")
    assignDistance()
    currentNextBestTile = np.array([128, 128, 128, 128])
    for z in range(len(map3D.map)):
        if usedZLayers[z] == 1:
            for y in range(len(map3D.map[z])):
                for x in range(len(map3D.map[z, y])):
                    if (map3D.map[z,y,x] & 64) and pathfinder[z,y,x] < currentNextBestTile[3]:
                        currentNextBestTile = np.array([z,y,x,pathfinder[z,y,x]])
    nextBestTile = currentNextBestTile
    print(f"next best tile is: {nextBestTile}")
    return nextBestTile

def findPossibleTiles(z,y,x): # finds every Tile the robot can go from the Tile currently under observation, return optimal tiles
    lowestDistance = 128
    #positions 0 to 2: coords, position 3: distance
    possibleTiles = np.array([[128,128,128,128],[128,128,128,128],[128,128,128,128],[128,128,128,128]])
    print(f"possibleTiles: {possibleTiles}")
    # finds which Fileds cam be directly accessed
    if not(map3D.map[z,y,x] & 1):
        possibleTiles[0] = np.array([z,y + 1,x,pathfinder[z,y + 1,x]])
    if not(map3D.map[z,y,x] & 2):
        possibleTiles[1] = np.array([z,y,x + 1,pathfinder[z,y,x + 1]])
    if not(map3D.map[z,y,x] & 4):
        possibleTiles[2] = np.array([z,y - 1,x,pathfinder[z,y - 1,x]])
    if not(map3D.map[z,y,x] & 8):
        possibleTiles[3] = np.array([z,y,x - 1,pathfinder[z,y,x - 1]])
    #find the neighboring Tile with the lowest Value
    for i in range (len(possibleTiles)):
        if possibleTiles[i,3] < lowestDistance:
            lowestDistance = possibleTiles[i,3]
    #check for Multiple solutions
    bestTiles = np.array([[128,128,128]])#coords
    print(bestTiles)
    print("best tiles and tile to add on its own and then concatenated")
    #Stores the Tiles with the lowest distance in an array
    for i in range (len(possibleTiles)):
        if possibleTiles[i,3] == lowestDistance:
            tileToAdd = np.array([[possibleTiles[i,0],possibleTiles[i,1],possibleTiles[i,2]]])
            # if first tile has no value yet
            if bestTiles[0,0] == 128 and bestTiles[0,1] == 128 and bestTiles[0,2]:
                bestTiles = tileToAdd
                print(bestTiles)
            else:
            #if there are already tiles stored
                bestTiles = np.concatenate((bestTiles, tileToAdd), axis=0)
    print(tileToAdd)
    print(bestTiles)
    return bestTiles
        

def findShortestWay(targetZ, targetY,targetX):
    #set every unknown, seen, or black tile to 128, known Tiles to 64, nextBestTile to 0, prepares the assignment
    for z in range(len(map3D.map)):
        if usedZLayers[z] == 1:
            for y in range(len(map3D.map[z])):
                for x in range(len(map3D.map[z, y])):
                    if map3D.map[z,y,x] & 128 or map3D.map[z,y,x] & 64 or map3D.map[z,y,x] ==  15:
                        pathfinder[z,y,x] = 128
                    else:
                        pathfinder[z,y,x] = 64
    pathfinder[targetZ,targetY,targetX] = 0
    print(f"pathfinder intiialised for shortest way {pathfinder}")
    assignDistance()
    #longestWay = pathfinder[map.currentPosition[0],map.currentPosition[1]] + 2
    currentTravelTile = np.array([map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPosition[2], pathfinder[map3D.currentPosition[0], map3D.currentPosition[1], map3D.currentPosition[2]]])
    # write down one found path
    wayFound = np.array([[currentTravelTile[0],currentTravelTile[1], currentTravelTile[2]]], dtype='u1')
    while (not (currentTravelTile[3] == 0)):
        #find nextBestTile
        bestTiles = findPossibleTiles(currentTravelTile[0], currentTravelTile[1], currentTravelTile[2])
        newArr = np.array([[bestTiles[0,0], bestTiles[0,1], bestTiles[0,2]]], dtype='u1')
        print(newArr)
        print("gerade new jetzt way:")
        print(wayFound)
        print("and bestTiles")
        print(bestTiles)
        wayFound = np.concatenate((wayFound, newArr), axis=0)
        currentTravelTile[0] = newArr[0,0].copy()
        currentTravelTile[1] = newArr[0,1].copy()
        currnetTravelTile[2] = newArr[0,2].copy()
        currentTravelTile[3] = pathfinder[currentTravelTile[0], currentTravelTile[1], currentTravelTile[2]]
    print(F"Found Path :{wayFound}")
    return wayFound #next tile to move to

def findWayNextBestTile():
    if mapIncomplete():
        print("finding way to next best tile")
        nextBestTile = getNextBestTile()
        print("found nextBestTile")
        return findShortestWay(nextBestTile[0], nextBestTile[1], nextBestTile[2]) #next tile to go to
    else:
        print("finding way to starting tile")
        if map3D.currentPosition[0] == map3D.halfHeight and map3D.currentPosition[1] == map3D.sizeOfMapHalf and map3D.currentPosition[2] == map3D.sizeOfMapHalf:
            print("already at starting position")
            return False
        else:
            return findShortestWay(map3D.halfHeight, map3D.sizeOfMapHalf, map3D.sizeOfMapHalf) #find shortest path to starting tile
