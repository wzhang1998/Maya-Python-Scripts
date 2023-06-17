import maya.cmds as mc
import random

def makePlanets():
    
    numPlanets = mc.intField( 'numPlanets', query = True, value = True )
    numMoons = mc.intField( 'numMoons', query = True, value = True )
    
    
    for i in range (0,numPlanets):
        #planet variables
        planetRadius = random.uniform(3,8)
        numberOfmoons = numMoons
        planetRotationOffset = random.uniform(0,360)
        planetGroupSpeed = random.uniform(1,9)
    
        mc.polySphere(name = 'planet_' + str(i), radius = planetRadius)
        
        for j in range (0,numberOfmoons):
            
            #moon variables
            randomMoonRotationX = random.uniform(0,360)
            randomMoonRotationY = random.uniform(0,360)
            randomMoonRotationZ = random.uniform(0,360)
            
            randomMoonOrbit = (planetRadius) + random.uniform(1,10)
            moonRadius = random.uniform(planetRadius/15, planetRadius/5)
             
            mc.polySphere(name = '_moon_' + str(i) + '_' + str(j), radius = moonRadius)
            mc.move(randomMoonOrbit + 2, 0, 0, r = True)
            mc.move( -(randomMoonOrbit) - 2, 0, 0, '_moon_' + str(i) + '_' + str(j) + '.scalePivot', '_moon_' + str(i) + '_' + str(j) + '.rotatePivot', relative = True)
            mc.rotate (randomMoonRotationX, randomMoonRotationY, randomMoonRotationZ, r =True, os = True)
            mc.expression ( string = ( '_moon_' + str(i) + '_' + str(j) + '.rotateY = time * 20'), object = '_moon_' + str(i) + '_' + str(j), ae = True, uc = 'all' )
            
            mc.select('planet_' + str(i), tgl = True)
            mc.parent()
        
        #planet rotation    
        mc.expression ( string = ('planet_' + str(i) + '.rotateY = time * 5'), object = 'planet_' + str(i), ae = True, uc = 'all' )
    
        #move planets away from origin
        mc.select('planet_' + str(i), replace = True)
        mc.move(20 * i, 0, 0, relative = True)
        
         #create empty groups for each planet
        mc.group( em=True, name='planetGroup_' + str(i))
        
        mc.select('planet_' + str(i), replace = True)
        mc.select('planetGroup_' + str(i), tgl = True)
        
        mc.parent()
        
        mc.expression ( string = ('planetGroup_' + str(i) + '.rotateY = (time + ' + str(planetRotationOffset) + ') *' + str(planetGroupSpeed)), object = 'planetGroup_' + str(i), ae = True, uc = 'all' )
        
def makeUI():
    if (mc.window('planetWindow', exists=True)):
        mc.deleteUI('planetWindow')
		
    window = mc.window( 'planetWindow', title="make some planets", widthHeight=(100, 55) )
    mc.columnLayout( adjustableColumn=True )
    
    mc.text( label='Mumber of Planets' )
    mc.intField( 'numPlanets', minValue=1, maxValue=100, value=5 )
    
    mc.text( label='Mumber of Moons' )
    mc.intField( 'numMoons', minValue=1, maxValue=100, value=5 )
    
    mc.button(label = 'Make Planets', command = 'makePlanets()')
    mc.showWindow( window )

makeUI()