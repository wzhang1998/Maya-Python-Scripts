#in maya script editor

#import aligner
#import importlib
#importlib.reload(aligner)

#aligner.Aligner()

from maya import cmds
from functools import partial

def align(nodes=None, axis='x', mode='mid'):
    #default node to selection if not nothing is provided
    if not nodes:
        nodes = cmds.ls(sl=True)

    if not nodes:
        cmds.error('Nothing selected or provided')

    _nodes = []
    for node in nodes:
        #check if nodes are faces
        if '.f[' in node:
            node = cmds.polyListComponentConversion(node, fromFace = True, toVertex = True)
        #check if nodes are edges
        elif '.e[' in node:
            node = cmds.polyListComponentConversion(node, fromEdge = True, toVertex = True)

        cmds.select(node)
        node = cmds.ls(sl = True, fl = True)

        _nodes.extend(node)

    #changed the selection, set it back to the nodes list
    cmds.select(nodes)
    #replace nodes with the _nodes temp list that we made
    nodes = _nodes
    #check
    print(nodes)

    minMode = mode == 'min'
    maxMode = mode == 'max'
    midMode = mode == 'mid'

    if axis == 'x':
        start = 0
    elif axis == 'y':
        start = 1
    elif axis == 'z':
        start = 2
    else:
        #error out
        cmds.error('Unknown Axis')

    #store the values and bounding boxes
    bboxes = {}    
    values = []

    #gets the dimention of objects(boundingbox)
    for node in nodes:
        if '.vtx[' in node:
            ws = cmds.xform(node, q = True, t = True, ws = True)
            minValue = midValue = maxValue = ws[start]

        else:
            bbox = cmds.exactWorldBoundingBox(node)

            minValue = bbox[start]
            maxValue = bbox[start+3]
            midValue = (maxValue+minValue)/2

        bboxes[node] = (minValue, midValue, maxValue)

        if minMode:
            values.append(minValue)
        elif maxMode:
            values.append(maxValue)
        else:
            values.append(midValue)

    #caculate the alignment point
    if minMode:
        target = min(values)
    elif maxMode:
        target = max(values)
    else:
        target = sum(values)/len(values)

    #figure out the distance to the target
    for node in nodes:
        bbox = bboxes[node]
        minValue, midValue, maxValue = bbox

        ws = cmds.xform(node, query=True, translation=True, ws=True)

        width = maxValue - minValue
        
        if minMode:
            distance = minValue - target
            ws[start] = (minValue - distance) + width/2
        elif maxMode:
            distance = target - maxValue
            ws[start] = (maxValue + distance) - width/2
        else:
            distance = target - midValue
            ws[start] = midValue + distance

        #move object to target(xform([translation=[linear, linear, linear]]))
        cmds.xform(node, translation = ws, ws = True)

class Aligner(object):

    def __init__(self):
        name = 'Aligner'
        if cmds.window(name, exists = True):
            cmds.deleteUI(name)
        
        window = cmds.window(name)
        self.buildUI()
        cmds.showWindow()
        cmds.window(window, e=True, resizeToFitChildren = True)

    def buildUI(self):
        column = cmds.columnLayout()
        #add buttons for axis
        cmds.frameLayout(label = "Choose an axis")

        cmds.gridLayout(numberOfColumns = 3, cellWidth=50)

        cmds.radioCollection()
        self.xAxis = cmds.radioButton(label = 'x', select = True)
        self.yAxis = cmds.radioButton(label = 'y')
        self.zAxis = cmds.radioButton(label = 'z')

        createIconButton('XAxis.png', command = partial(self.onOptionClick, self.xAxis))
        createIconButton('YAxis.png', command = partial(self.onOptionClick, self.yAxis))
        createIconButton('ZAxis.png', command = partial(self.onOptionClick, self.zAxis))

        #add buttons for mode
        cmds.setParent(column)

        cmds.frameLayout(label = "Choose where to align")

        cmds.gridLayout(numberOfColumns = 3, cellWidth=50)

        cmds.radioCollection()
        self.minMode = cmds.radioButton(label = 'min')
        self.midMode = cmds.radioButton(label = 'mid', select = True)
        self.maxMode = cmds.radioButton(label = 'max')

        createIconButton('MinAxis.png', command = partial(self.onOptionClick, self.minMode))
        createIconButton('MidAxis.png', command = partial(self.onOptionClick, self.midMode))
        createIconButton('MaxAxis.png', command = partial(self.onOptionClick, self.maxMode))

        #add apply button
        cmds.setParent(column)
        cmds.button(label = 'Align', command = self.onApplyClick, bgc = (0.2, 0.5, 0.2))
    
    def onOptionClick(self, opt):
        cmds.radioButton(opt, edit = True, select = True)

    def onApplyClick(self, *args):
        #get the sxis
        if cmds.radioButton(self.xAxis, q=True, select=True):
            axis = 'x'
        elif cmds.radioButton(self.yAxis, q=True, select=True):
            axis = 'y'
        elif cmds.radioButton(self.zAxis, q=True, select=True):
            axis = 'z'

        #get the mode
        if cmds.radioButton(self.minMode, q=True, select=True):
            mode = 'min'
        elif cmds.radioButton(self.midMode, q=True, select=True):
            mode = 'mid'
        elif cmds.radioButton(self.maxMode, q=True, select=True):
            mode = 'max'

        #call the align function
        align(axis = axis, mode = mode)

#get icon file
def getIcon(icon):
    import os
    scripts = os.path.dirname(__file__)
    icons = os.path.join(scripts, 'icons')

    icon = os.path.join(icons, icon)
    return icon

def createIconButton(icon, command=None):
    if command:
        cmds.iconTextButton(image1 = getIcon(icon), width = 50, height = 50, command = command)
    else:
        cmds.iconTextButton(image1 = getIcon(icon), width = 50, height = 50)
