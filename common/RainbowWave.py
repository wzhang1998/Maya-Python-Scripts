import maya.cmds as mc
import math
import random

#convert number range of (-1,1) to (0,1)
def reRange(val):
    OldRange = (1 - (-1))
    NewRange = (1 - 0)
    NewValue = (((val - (-1)) * NewRange) / OldRange) + 0
    
    return NewValue
    
#take numeric input, use it to generate rgb value    
def sphereColor(timeVal):
    rVal = reRange(math.sin(math.radians(timeVal)))
    gVal = reRange(math.sin(math.radians(timeVal + 120)))
    bVal = reRange(math.sin(math.radians(timeVal + 240)))
    
    return [rVal, gVal , bVal]

#for loop for grid
for i in range(20):
    for j in range(20):
    
        #create sphere name
        sphereName =  ('sphere' + '_' + str(i) + '_' + str(j))
        
        #delete existing groups
        if(mc.objExists(sphereName + '_group')):
            mc.select(sphereName + '_group', r = True)
            mc.delete()
            
        #create group name
        sphereNameGroup = sphereName + '_group'
        
        #random radius
        if (j%4 == 0):
            randomRadius = random.uniform(.1, .2)
        else:
            randomRadius = random.uniform(.2, .5)
        
        #create sphere
        mc.polySphere(name = sphereName, sx = 7, sy = 7, r = randomRadius)
        mc.polySoftEdge(a = 180, ch = 0)
        
        #group itself
        mc.group(name = sphereNameGroup)
        mc.select(sphereName, r = True)
        
        #move the sphere
        mc.move(.5,0,0, a = True)
        mc.select(sphereNameGroup, r = True)
        
        #move to grid location
        mc.move(i, 0, j, a = True)
        
        #rotation variation
        rotationVariation = random.uniform(0,2)
        
        #rotation offset
        offset = i + j + rotationVariation
        
        #rotation expression
        mc.expression( s = (sphereNameGroup + '.rotateY = (time + ' + str(offset) + ' ) * 30'), ae =True, uc = 'all')
        
        #rotate the smaller shpere in z
        if (j%4 == 0):
            mc.expression( s = (sphereNameGroup + '.rotateZ = (time + ' + str(offset) + ' ) * -50'), ae =True, uc = 'all')    
        
        #speedup every 4th one    
        if (j%4 == 0):
            #scale expression
            mc.expression( s = (sphereName + '.scaleX = abs(sin( time + ' + str(offset) + '/ 2))'), ae =True, uc = 'all')
            mc.expression( s = (sphereName + '.scaleY = abs(sin( time + ' + str(offset) + '/ 2))'), ae =True, uc = 'all')
            mc.expression( s = (sphereName + '.scaleZ = abs(sin( time + ' + str(offset) + '/ 2))'), ae =True, uc = 'all')
            
        else:     
            #scale expression
            mc.expression( s = (sphereName + '.scaleX = abs(sin( time + ' + str(offset) + '/ 1.5))'), ae =True, uc = 'all')
            mc.expression( s = (sphereName + '.scaleY = abs(sin( time + ' + str(offset) + '/ 1.5))'), ae =True, uc = 'all')
            mc.expression( s = (sphereName + '.scaleZ = abs(sin( time + ' + str(offset) + '/ 1.5))'), ae =True, uc = 'all')
        
        #take j val and use it ganerate degree val
        colorVariantion = 10 * (random.uniform(1,1.5))
        
        if (j%4 == 0):
            col = sphereColor( j * 1.5 * colorVariantion)
            
        else:
            col = sphereColor( j * colorVariantion)
       
        mc.select(sphereName, r = True)
        vertCount = mc.polyEvaluate(v = True)
       
       #select the vertex
        mc.select(sphereName + '.vtx[0:' + str(vertCount - 1) + ']', r = True)
        mc.polyColorPerVertex(rgb = (col[0], col[1], col[2]), cdo = True)
        
        mc.select(clear = True)