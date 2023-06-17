import maya.cmds as cmds
import random, math
import commonS

#clear Scene
commonS.clearScene()


#define global variables
sizePlane = 50
posList = []
maxTries = 20

#### Functions ####

#def distance(x2, z2, x1, z1):
    
#    return math.squareroot()

def findUniqueXZ(minD):
    
    newNumsNeeded = True
    tries = maxTries
    
    # Loop until we have a point that is far enough spaced
    while newNumsNeeded == True and tries > 0:
        
        ranX = random.uniform(-sizePlane/2,sizePlane/2)
        ranZ = random.uniform(-sizePlane/2,sizePlane/2)
    
        # if first object, just return numbers
        if len(posList) == 0:
            return ranX, ranZ
            
        for usedSpot in posList:
        
            distance = math.dist((ranX, ranZ), usedSpot)
            
            if distance < minD:
                newNumsNeeded = True
                tries -= 1
                break
            else:
                newNumsNeeded = False
                

            
        
    # return a tuple of two values
    if tries > 0:
        return ranX, ranZ


def sample(numObjects = 20, minDistance = 5):
    
    for i in range(numObjects):
        ## get random x&z
        ranTuple = findUniqueXZ(minDistance)
        
        if ranTuple is not None:
            ## add tuple to the list of points
            posList.append(ranTuple)
    
            
            cube = cmds.polyCube()[0]
            cmds.move(ranTuple[0], 0, ranTuple[1])
        
        



# Run code that DRIVES everything        
        
cmds.polyPlane(w = sizePlane, h=sizePlane)
sample(300, 2)