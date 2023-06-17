from maya import cmds
import random
import math

# Random Numbers
randNum = random.uniform(10, 50)
randInt = int(randNum)


# convert number range of (-1,1) to (0,1)
def reRange(val):
    OldRange = (1 - (-1))
    NewRange = (1 - 0)
    NewValue = (((val - (-1)) * NewRange) / OldRange) + 0
    
    return NewValue
    
# take numeric input, use it to generate rgb value    
def sphereColor(timeVal):
    rVal = reRange(math.sin(math.radians(timeVal)))
    gVal = reRange(math.sin(math.radians(timeVal + 120)))
    bVal = reRange(math.sin(math.radians(timeVal + 240)))
    
    return [rVal, gVal , bVal]
    
# Create some cubes!
for i in range(randInt):
    
    # Random variables
    limitSize = 4
    limitTrans = 20
        
    randSizeX = random.uniform(1, limitSize)
    randSizeY = random.uniform(1, limitSize)
    randSizeZ = random.uniform(1, limitSize)
        
    randTransX = random.uniform(-limitTrans, limitTrans)
    randTransY = random.uniform(-limitTrans, limitTrans)
    randTransZ = random.uniform(-limitTrans, limitTrans)
    
    if i%2 == 0:
        # Create the cube
        obj = cmds.polyCube()
        geo = obj[0]

    else:
        # Create the other shape
        obj = cmds.polyPipe()
        geo = obj[0]

    # Place the cube at random
    cmds.setAttr(geo+".translateX", randTransX)
    cmds.setAttr(geo+".translateY", randTransY)
    cmds.setAttr(geo+".translateZ", randTransZ)
    
    # Size the cube at random
    cmds.setAttr(geo+".scaleX", randSizeX)
    cmds.setAttr(geo+".scaleY", randSizeY)
    cmds.setAttr(geo+".scaleZ", randSizeZ)
    
    cmds.rename( 'obj_' + str(i) )
    
    # rotation variation
    rotationVariation = random.uniform(0,2)
        
    # rotation offset
    offset = i + rotationVariation
        
    # rotation expression
    cmds.expression( s = ('obj_' + str(i) + '.rotateY = (time + ' + str(offset) + ' ) * 40'), ae =True, uc = 'all')
    cmds.expression( s = ('obj_' + str(i) + '.rotateX = (time + ' + str(offset) + ' ) * 20'), ae =True, uc = 'all')
        
    # rotate the smaller obj in z
    if (i%4 == 0):
        cmds.expression( s = ('obj_' + str(i) + '.rotateZ = (time + ' + str(offset) + ' ) * -50'), ae =True, uc = 'all')   
    
    # assign vertex color
    colorVariantion = 15 * (random.uniform(1,1.5))
        
    if (i%2 == 0):
        col = sphereColor( i * 1.5 * colorVariantion)
            
    else:
        col = sphereColor( i * colorVariantion)
    
    cmds.select('obj_' + str(i), r = True)
    vertCount = cmds.polyEvaluate(v = True)
       
    # select the vertex
    cmds.select('obj_' + str(i) + '.vtx[0:' + str(vertCount - 1) + ']', r = True)
    cmds.polyColorPerVertex(rgb = (col[0], col[1], col[2]), cdo = True)
        
    cmds.select(clear = True)


