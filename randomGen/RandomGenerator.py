from maya import cmds
import random
import math

#------------------------------------------------------------------------------------------------------------------------------------------------#
# This script generates a random colorful animated scene using three hided meshes in the Maya scene: 'cartoon_controller', 'soda_can', 'lollipop'#
# Don't forget to play the animation ;)                                                                                                          #
#------------------------------------------------------------------------------------------------------------------------------------------------#

# Random Numbers
randNum = random.uniform(50, 70)
randInt = int(randNum)


# Convert number range of (-1,1) to (0,1)
def reRange(val):
    OldRange = (1 - (-1))
    NewRange = (1 - 0)
    NewValue = (((val - (-1)) * NewRange) / OldRange) + 0
    
    return NewValue
    
# Take numeric input, use it to generate rgb value    
def sphereColor(timeVal):
    rVal = reRange(math.sin(math.radians(timeVal)))
    gVal = reRange(math.sin(math.radians(timeVal + 120)))
    bVal = reRange(math.sin(math.radians(timeVal + 240)))
    
    return [rVal, gVal , bVal]
    
# Lets create something!
for i in range(randInt):
    
    # Scene variables
    limitSize = 4
    limitTrans = 50
        
    randSizeX = random.uniform(0.7, limitSize)
    # use varibales below if needed
    # randSizeY = random.uniform(1, limitSize)
    # randSizeZ = random.uniform(1, limitSize)
        
    randTransX = random.triangular(-limitTrans, limitTrans, 0)
    randTransY = random.triangular(-limitTrans, limitTrans, 0)
    randTransZ = random.triangular(-limitTrans, limitTrans, 0)
    
    # pick your things here
    if i%2 == 0:
        # Create the fist shape
        # obj = cmds.polyCube()
        thing = 'cartoon_controller'
        
    elif i%3 == 0:
        # Create the other shape
        thing = 'soda_can'

    else:
        # Create the other shape
        # obj = cmds.polyPipe()
        thing = 'lollipop'
        
    # Duplicate things and add them to a list     
    obj = cmds.duplicate(thing)
    geo = obj[0]

    # Place the cube at random location
    cmds.setAttr(geo+".translateX", randTransX)
    cmds.setAttr(geo+".translateY", randTransY)
    cmds.setAttr(geo+".translateZ", randTransZ)
    
    # Size the cube at random size
    cmds.setAttr(geo+".scaleX", randSizeX)
    cmds.setAttr(geo+".scaleY", randSizeX)
    cmds.setAttr(geo+".scaleZ", randSizeX)
    
    # Make things visible
    cmds.setAttr(thing + '1.visibility', 1)
    # Rename things so them can be animated and colored
    cmds.rename( thing + '1', 'obj_' + str(i) )
    
    # Rotation variation
    rotationVariation = random.uniform(0,3)
        
    # Rotation offset
    offset = i + rotationVariation
        
    # Rotation expression
    cmds.expression( s = ('obj_' + str(i) + '.rotateY = (time + ' + str(offset) + ' ) * 40'), ae =True, uc = 'all')
    cmds.expression( s = ('obj_' + str(i) + '.rotateX = (time + ' + str(offset) + ' ) * 20'), ae =True, uc = 'all')
        
    # Rotate the smaller obj in z
    if (i%4 == 0):
        cmds.expression( s = ('obj_' + str(i) + '.rotateZ = (time + ' + str(offset) + ' ) * -50'), ae =True, uc = 'all')   
    
    # Assign vertex color
    colorVariantion = 15 * (random.uniform(1,1.5))
        
    if (i%2 == 0):
        col = sphereColor( i * 2 * colorVariantion)
            
    else:
        col = sphereColor( i * colorVariantion)
    
    cmds.select('obj_' + str(i), r = True)
    vertCount = cmds.polyEvaluate(v = True)
       
    # Select the vertex
    cmds.select('obj_' + str(i) + '.vtx[0:' + str(vertCount - 1) + ']', r = True)
    cmds.polyColorPerVertex(rgb = (col[0], col[1], col[2]), cdo = True)
        
    cmds.select(clear = True)


