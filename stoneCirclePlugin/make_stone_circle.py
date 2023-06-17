from distutils.command.check import check
import maya.cmds as cmds
import math
import random

# create function of assigning random material to each geometry
def material():

        shapeList = cmds.ls(g=True)
        list = cmds.listRelatives(shapeList, p=True)
        sel=list
        
        if sel!=[]:

            for obj in sel:

                myShade = cmds.shadingNode('lambert', asShader=True)
                myShadeSG=cmds.sets( renderable=True,noSurfaceShader=True, name=(myShade+"SG"))
                cmds.connectAttr ((myShade+".outColor"),(myShadeSG+".surfaceShader"))
                cmds.select(obj)
                cmds.sets (forceElement=myShadeSG)

                colorR1=random.random()
                colorG1=random.random()
                colorB1=random.random()

                cmds.setAttr ((myShade+".color"),colorR1,colorG1,colorB1,type="double3" )

        else:
            cmds.inViewMessage( amg='please select object!', pos='midCenter', fade=True )

# stone circle function
def arrayCircle(innerSize = 15, circleNum = 4, stoneNum = 7, stoneHeight = 5, stoneWidth = 2, structureWidth = 4):
    stoneSub = 2
    stoneGroup = []
    # create circle 
    for i in range(0,circleNum):
        # define circlesize
        circleSize = innerSize + i * 5
        # create circle groups
        cmds.group(em=True,n='circleGroup_' + str(i))
    
        # create stones
        for n in range(0,stoneNum):

            # define random values
            randomRotate = random.uniform(0,360)
            randomRotateOffsetT = random.uniform(-10,10)
            randomRotateOffsetR = random.uniform(-16,16)
            randomRotateOffsetL = random.uniform(-20,20)
            randomScaleX = random.uniform(0.6,1.2)
            randomScaleY = random.uniform(0.4,1.2)
            randomScaleZ = random.uniform(0.6,1.2)
            randomBevelL = random.uniform(0.1,1)
            randomBevelR = random.uniform(0.1,1)
            randomBevelT = random.uniform(0.1,1)

            # create stone groups
            cmds.group(em=True,name='stoneGroup_' + str(n) + str(i))
            stoneGroup.append('stoneGroup_' + str(n) + str(i))

            # build stone parts and parent them to group
            # check the strucure parameter
            if structureWidth <= stoneWidth*2 :
                structureWidth = stoneWidth + 1

            num=str(n) + str(i)
            cmds.polyCube(name='part'+ num + 'L',h = stoneHeight, w = stoneWidth, d = stoneWidth/2, sx=stoneSub, sy=stoneSub, sz=stoneSub)
            cmds.polyBevel(f=randomBevelL, oaf=1)
            cmds.move(stoneHeight/2, moveY = True)
            cmds.move(structureWidth/2, moveX = True)
            cmds.rotate(0,randomRotateOffsetR,0,t= True)
            cmds.parent('part'+ num + 'L', 'stoneGroup_' + str(n) + str(i))

            cmds.polyCube(name='part'+ num + 'R',h = stoneHeight, w = stoneWidth, d = stoneWidth/2, sx=stoneSub, sy=stoneSub, sz=stoneSub)
            cmds.polyBevel(f=randomBevelR, oaf=1)
            cmds.move(stoneHeight/2, moveY = True)
            cmds.move(-structureWidth/2, moveX = True)
            cmds.rotate(0,randomRotateOffsetL,0,t= True)
            cmds.parent('part'+ num + 'R','stoneGroup_' + str(n) + str(i))

            # skip head stone when n%3 == 0
            if n%3 == 0:
                pass
            else:
                cmds.polyCube(name='part'+ num + 'T',h=stoneWidth/2, w=structureWidth + stoneWidth*2, d=stoneWidth*randomScaleX, sx=stoneSub, sy=stoneSub, sz=stoneSub)
                cmds.polyBevel(f=randomBevelT, oaf=1)
                cmds.move(stoneHeight , moveY=True)
                cmds.rotate(randomRotateOffsetT,randomRotateOffsetT,0,t= True)
                cmds.parent('part'+ num + 'T','stoneGroup_' + str(n) + str(i))
            
            # give group random scale and apply it
            cmds.scale( randomScaleX, randomScaleY, randomScaleZ, 'stoneGroup_' + str(n) + str(i) ,r=True )
            cmds.makeIdentity('stoneGroup_' + str(n) + str(i), s=True )
            # move the stone group according to circle size
            cmds.move(0,0,circleSize,'stoneGroup_' + str(n) + str(i), r=True)
            # move the pivot point to back to origin
            cmds.move(0,0,-circleSize,'stoneGroup_' + str(n) + str(i) + '.scalePivot', 'stoneGroup_' + str(n) + str(i) + '.rotatePivot', relative = True)
            # rotate stone group random value along Y axis
            cmds.rotate(0,randomRotate,0, 'stoneGroup_' + str(n) + str(i), r=True)

            # check each stoneGroup's bounding boxes
            if len(stoneGroup) > 1:
                check = len(stoneGroup)-1
                while check != 0:  
                    for b in range(0,len(stoneGroup)-1):
                        bbox1 = cmds.exactWorldBoundingBox('stoneGroup_' + str(n) + str(i))
                        bbox2 = cmds.exactWorldBoundingBox(stoneGroup[b])
                        xminA, yminA, zminA, xmaxA, ymaxA, zmaxA = bbox1[0], bbox1[1], bbox1[2], bbox1[3], bbox1[4],  bbox1[5]
                        xminB, yminB, zminB, xmaxB, ymaxB, zmaxB = bbox2[0], bbox2[1], bbox2[2], bbox2[3], bbox2[4],  bbox2[5]
                        
                        intersect_true = (((xminB > xminA) & (xminB < xmaxA)) & ((yminB > yminA) & (yminB < ymaxA)) & ((zminB > zminA) & (zminB < zmaxA)) | 
                            ((xminB >= xminA) & (xminB <= xmaxA)) & ((yminB >= yminA) & (yminB <= ymaxA)) & ((zmaxB >= zminA) & (zmaxB <= zmaxA)) |
                            ((xmaxB >= xminA) & (xmaxB <= xmaxA)) & ((yminB >= yminA) & (yminB <= ymaxA)) & ((zminB >= zminA) & (zminB <= zmaxA)) |
                            ((xmaxB >= xminA) & (xmaxB <= xmaxA)) & ((yminB >= yminA) & (yminB <= ymaxA)) & ((zmaxB >= zminA) & (zmaxB <= zmaxA)) |
                            ((xminB >= xminA) & (xminB <= xmaxA)) & ((ymaxB >= yminA) & (ymaxB <= ymaxA)) & ((zminB >= zminA) & (zminB <= zmaxA)) |
                            ((xminB >= xminA) & (xminB <= xmaxA)) & ((ymaxB >= yminA) & (ymaxB <= ymaxA)) & ((zmaxB >= zminA) & (zmaxB <= zmaxA)) |
                            ((xmaxB >= xminA) & (xmaxB <= xmaxA)) & ((ymaxB >= yminA) & (ymaxB <= ymaxA)) & ((zminB >= zminA) & (zminB <= zmaxA)) |
                            ((xmaxB >= xminA) & (xmaxB <= xmaxA)) & ((ymaxB >= yminA) & (ymaxB <= ymaxA)) & ((zmaxB >= zminA) & (zmaxB <= zmaxA)))

                        if intersect_true:  
                            print('overlapping!')
                            randomFix = random.uniform(0,360)
                            cmds.rotate(0,randomFix,0, 'stoneGroup_' + str(n) + str(i), r=True) 
                            check = len(stoneGroup)-1
                            break

                        else:
                            check = check - 1 
          

            # group stoneGroup into circleGroup
            cmds.parent('stoneGroup_' + str(n) + str(i),'circleGroup_' + str(i))

    
