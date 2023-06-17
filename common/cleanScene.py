import maya.cmds as cmds

def clean():

    list = cmds.ls(geometry = True)
    transformList = cmds.listRelatives(list, parent = True)

    if transformList != None:
        cmds.delete(transformList)