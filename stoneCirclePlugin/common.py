import maya.cmds as cmds

def clearScene():
    matList = cmds.ls(mat=True)
    cmds.delete(matList)
    shapeList = cmds.ls(g=True)
    list = cmds.listRelatives(shapeList, p=True)

    check = 1
    while check == 1:
        parentList = cmds.listRelatives(list, p=True)
        if parentList is not None:
            list.append(parentList)
            list = parentList
        else:
            check = 0

    if list is not None:
        cmds.delete(list)
        
    