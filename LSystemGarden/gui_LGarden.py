import maya.cmds as cmds
import maya.mel as mel
from L_system_create import *

### clear scene fuction
def clearScene(*args):
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

### create shader function
def create_shader(*args):
	
	### select objs
	selected = cmds.ls(sl=True, long=True)

	### Create a blinn material
	surfaceMat = cmds.shadingNode('surfaceShader', asShader=1)
	### query color from color slider group
	cmds.colorSliderGrp( 'csg', e=True, query=True, vis=True)
	rgb = cmds.colorSliderGrp( 'csg', query=True, rgb=True)
	cmds.setAttr ((surfaceMat + '.outColor'), rgb[0],rgb[1],rgb[2], type = 'double3' ) 
	cmds.setAttr ((surfaceMat + '.outTransparency'), 0.89,0.89,0.89, type = 'double3') 

	#Create a shading group
	shadingGroup = cmds.sets(renderable=1, noSurfaceShader=1, empty=1)
	#Connect the material to the shading group
	cmds.connectAttr((surfaceMat+'.outColor'),(shadingGroup+'.surfaceShader'),f=1)
	#Assign the material using sets
	cmds.sets(selected, e=1, forceElement=shadingGroup)

def windowUI(*args):

	### Window
	if cmds.window("windowUI", exists=True):
		cmds.deleteUI("windowUI")
		
	cmds.window("windowUI", title="L-System Garden", resizeToFitChildren=True, sizeable=False)

	### Header image
	cmds.rowColumnLayout(w=380)
	cmds.image(image="fractalGenerator_header.png", w=380)
	cmds.setParent("..")

	### Frame
	cmds.frameLayout(label="L-Garden Options", collapsable=False, mw=5, mh=5)

	### Preset drop down menu
	cmds.rowColumnLayout(cw=[(1, 370)])
	cmds.optionMenu("presetDropDown", label='Preset: ', cc=changeOptions, ann='please choose a preset')
	cmds.menuItem(label='None')
	cmds.menuItem(label="Tree structure")
	cmds.menuItem(label="Tree structure 2")
	cmds.menuItem(label="Tree structure 3")
	cmds.menuItem(label="Stochastic Plant")
	cmds.menuItem(label='Hilbert curve')
	cmds.menuItem(label='Hilbert II curve 3D')
	cmds.menuItem(label='Terdragon curve')
	### cmds.menuItem(label="Pythagorean Tree")
	cmds.menuItem(label='Moore curve')
	cmds.menuItem(label='Sierpinski triangle')
	cmds.menuItem(label='Sierpinski arrowhead curve')
	cmds.menuItem(label='Sierpinski curve')
	cmds.menuItem(label='Koch curve')
	### cmds.menuItem(label='Quadratic Koch curve')
	cmds.menuItem(label='Koch snowflake')
	cmds.menuItem(label='Koch antisnowflake')
	cmds.menuItem(label='Quadratic Koch island')
	cmds.menuItem(label='Cross stitch curve')
	cmds.menuItem(label='Box fractal')
	cmds.menuItem(label='Harter Heighway dragon curve')
	cmds.menuItem(label='Peano Gosper curve')
	cmds.menuItem(label='Quadratic Gosper curve')
	cmds.menuItem(label='Minkowski sausage')
	cmds.menuItem(label='Levy curve')
	cmds.menuItem(label="cmdsWorter's Pentigree")
	

	cmds.text(l='', w=370, h=10, ww=True)
	cmds.separator(h=10, st='in')

	### Axiom
	cmds.rowColumnLayout(nc=2, cal=[(1, "left")], cw=[(1,105),(2,260)])
	cmds.text(l="Axiom: ", ann='define the starting word')
	cmds.textField("axiom")
	cmds.setParent("..")

	### Iterations
	cmds.rowColumnLayout(nc=1, w=380)
	cmds.intSliderGrp("iterations", l="Iterations: ", ann='define the number of the replacement operation', v=3, cw3=[102,50,210], min=1, max=5, fmx=10, f=True, cal=[(1, "left")])
	cmds.setParent("..")

	### Angle
	cmds.rowColumnLayout(nc=1, w=380)
	cmds.floatSliderGrp("angle", l="Angle: ",  ann='define the rotating angle when + - < > ^ & are used', v=90, cw3=[102,50,210], min=0, max=180, fmx=360, f=True, cal=[(1, "left")])
	cmds.setParent("..")

	### radius
	cmds.rowColumnLayout(nc=1, w=380)
	cmds.floatSliderGrp("radius", l="Radius: ", ann='define the width of branches', v=0.2, cw3=[102,50,210], min=0.1, max=2, fmx=360, f=True, cal=[(1, "left")])
	cmds.setParent("..")
	
	### Length
	cmds.rowColumnLayout(nc=1, w=380)
	cmds.intSliderGrp("distance", l="Length: ", ann='define the length of branches',v=10, cw3=[102,50,210], min=0, max=20, f=True, cal=[(1, "left")])
	cmds.setParent("..")

	### Scale
	cmds.rowColumnLayout(nc=1, w=380)
	cmds.floatSliderGrp("scale", l="Scale: ", ann='define the scale variable when @ is used', v=0.75, cw3=[102,50,210], min=0.1, max=2, f=True, cal=[(1, "left")])
	cmds.setParent("..")

	### Replacements
	cmds.text(l='', w=370, h=2, ww=True)
	cmds.rowColumnLayout(nc=1, cal=[(1, "left")], cw=[(1,150)])
	cmds.text(l="Replacement rules: ", h=30, ann='define the replacement rules')
	
	### Rules info
	cmds.scrollField( editable=False, wordWrap=False, w=370, h=40, text='F  :  Move forward by line length drawing a line \n+  :  Turn left by angle\n-  :  Turn right by angle \n[  :  Push current drawing state onto stack\n]  :  Pop current drawing state from the stack\n<  :  Roll left by angle\n>  :  Roll right by angle\n^  :  Tilt up by angle\n&  :  Tilt down by angle\n|  :  Flip 180 degree\n@  :  Scale the line', fn="smallPlainLabelFont" )

	cmds.setParent("..")
	cmds.text(l='', w=370, h=10, ww=True)
	### Create rule text field
	cmds.rowColumnLayout(nc=3, cal=[(1, "left")], cw=[(1,30), (2,50), (3,290)])
	cmds.textField("replacementA")
	cmds.text(l="==>")
	cmds.textField("replacementA_2")
	cmds.setParent("..")

	cmds.rowColumnLayout(nc=3, cal=[(1, "left")], cw=[(1,30), (2,50), (3,290)])
	cmds.textField("replacementB")
	cmds.text(l="==>")
	cmds.textField("replacementB_2")
	cmds.setParent("..")

	cmds.rowColumnLayout(nc=3, cal=[(1, "left")], cw=[(1,30), (2,50), (3,290)])
	cmds.textField("replacementC")
	cmds.text(l="==>")
	cmds.textField("replacementC_2")
	cmds.setParent("..")
	cmds.text(l='', w=370, h=10, ww=True)

	### Buttons
	cmds.rowColumnLayout(nc=3, cw=[(1,123),(2,123), (3,123)],cs=[(2,5),(3,5)])
	cmds.button("createFractalButton", l="Create", al="center", c=createFractalButton)
	cmds.button("resetButton", l="Reset", al="center", c=windowUI)
	cmds.button("cleanButton", l="Clear Scene", al="center", c=clearScene)
	cmds.setParent("..")

	cmds.rowColumnLayout(nc=1, w=380)
	cmds.text(l='', w=370, h=10, ww=True)
	cmds.colorSliderGrp( 'csg', label='Color', rgb=(0, 0.616, 0.594), cal=[(1,'left')])
	cmds.text(l='', w=370, h=10, ww=True)
	cmds.button("addColor", l="Add Color", al="center", c=create_shader)
	cmds.setParent("..")
	cmds.text(l='', w=370, h=10, ww=True)
	cmds.separator(h=10, st='in')

	### Text
	cmds.text(l='', w=370, h=5, ww=True)
	cmds.text(l='Wenyi Zhang - 2022', w=370, h=30, ww=True, fn="smallPlainLabelFont")
	cmds.text(l='If you are not familiar with Lindenmayer Systems, please check http://algorithmicbotany.org/papers/#abop and Twitter@LSystemBot for reference', w=370, h=30, ww=True, fn="smallPlainLabelFont")
	cmds.text(l='', w=370, h=5, ww=True)

	### show window
	cmds.showWindow("windowUI")


def createFractalButton(*args):

	### variables
	iterations = cmds.intSliderGrp("iterations", query=True, v=True)
	angle = cmds.floatSliderGrp("angle", query=True, v=True)
	presetName = cmds.optionMenu("presetDropDown", q=True, v=True)
	axiom = cmds.textField("axiom", query=True, tx=True)
	radius = cmds.floatSliderGrp("radius", query=True, v=True)
	distance = cmds.intSliderGrp("distance", query=True, v=True)
	scale = cmds.floatSliderGrp("scale", query=True, v=True)
	replacementA = str(cmds.textField("replacementA", query=True, tx=True))
	replacementA_2 = str(cmds.textField("replacementA_2", query=True, tx=True))
	replacementB = str(cmds.textField("replacementB", query=True, tx=True))
	replacementB_2 = str(cmds.textField("replacementB_2", query=True, tx=True))
	replacementC = str(cmds.textField("replacementC", query=True, tx=True))
	replacementC_2 = str(cmds.textField("replacementC_2", query=True, tx=True))

	### call functions
	addRule(replacementA, replacementA_2, replacementB, replacementB_2, replacementC, replacementC_2)

	### show error if no rule to apply
	if len(replacementA) == 0 | len(replacementA_2) == 0:
		errorWindow = cmds.window(title="Error", sizeable=False)
		cmds.rowColumnLayout(nc=3, cw=[(1,123),(2,123), (3,123)])
		cmds.text(l='Please create at least one rule!', w=370, h=50, ww=True, fn='boldLabelFont')
		cmds.setParent("..")
		cmds.showWindow( errorWindow )
	else:
		drawLsystem(LSystem().repeat(axiom, iterations), angle, distance, radius, presetName, scale)


def changeOptions(*args):

	presetName = cmds.optionMenu("presetDropDown", q=True, v=True)
	print ("presetName: ", presetName)

	if presetName == "None":
		cmds.textField("axiom", e=True, tx="", en=True)
		cmds.floatSliderGrp("angle", e=True, v=30, en=True)
		cmds.floatSliderGrp("radius", e=True, v=0.1, en=True)
		cmds.textField("replacementA", e=True, tx="", en=True)
		cmds.textField("replacementA_2", e=True, tx="", en=True)
		cmds.textField("replacementB", e=True, tx="", en=True)
		cmds.textField("replacementB_2", e=True, tx="", en=True)
		cmds.textField("replacementC", e=True, tx="", en=True)
		cmds.textField("replacementC_2", e=True, tx="", en=True)

	if presetName == "Hilbert curve":
		cmds.textField("axiom", e=True, tx="L")
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.textField("replacementA", e=True, tx="L")
		cmds.textField("replacementA_2", e=True, tx="+RF-LFL-FR+")
		cmds.textField("replacementB", e=True, tx="R")
		cmds.textField("replacementB_2", e=True, tx="-LF+RFR+FL-")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == 'Terdragon curve':
		cmds.textField("axiom", e=True, tx="F")
		cmds.floatSliderGrp("angle", e=True, v=120, en=True)
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F+F-F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == 'Pythagorean Tree':
		cmds.textField("axiom", e=True, tx="", en=False)
		cmds.floatSliderGrp("radius", e=True, v=0.2)
		cmds.intSliderGrp("angle", e=True, en=False)
		cmds.textField("replacementA", e=True, tx="", en=False)
		cmds.textField("replacementA_2", e=True, tx="", en=False)
		cmds.textField("replacementB", e=True, tx="", en=False)
		cmds.textField("replacementB_2", e=True, tx="", en=False)
		cmds.textField("replacementC", e=True, tx="", en=False)
		cmds.textField("replacementC_2", e=True, tx="", en=False)

	if presetName == "Hilbert II curve 3D":
		cmds.textField("axiom", e=True, tx="X")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="X")
		cmds.textField("replacementA_2", e=True, tx="^<XF^<XFX-F^>>XFX&F+>>XFX-F>X->")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Moore curve":
		cmds.textField("axiom", e=True, tx="LFL-F-LFL")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="L")
		cmds.textField("replacementA_2", e=True, tx="+RF-LFL-FR+")
		cmds.textField("replacementB", e=True, tx="R")
		cmds.textField("replacementB_2", e=True, tx="-LF+RFR+FL-")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Sierpinski arrowhead curve":
		cmds.textField("axiom", e=True, tx="YF")
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.floatSliderGrp("angle", e=True, v=60, en=True)
		cmds.textField("replacementA", e=True, tx="X")
		cmds.textField("replacementA_2", e=True, tx="YF+XF+Y")
		cmds.textField("replacementB", e=True, tx="Y")
		cmds.textField("replacementB_2", e=True, tx="XF-YF-X")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Sierpinski curve":
		cmds.textField("axiom", e=True, tx="F+XF+F+XF")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="X")
		cmds.textField("replacementA_2", e=True, tx="XF-F+F-XF+F+XF-F+F-X")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Koch curve":
		cmds.textField("axiom", e=True, tx="F")
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.floatSliderGrp("angle", e=True, v=60, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F+F--F+F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Quadratic Koch curve":
		cmds.textField("axiom", e=True, tx="F")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F+F-F-F+F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Koch snowflake":
		cmds.textField("axiom", e=True, tx="F--F--F")
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.floatSliderGrp("angle", e=True, v=60, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F+F--F+F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Koch antisnowflake":
		cmds.textField("axiom", e=True, tx="F++F++F")
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.floatSliderGrp("angle", e=True, v=60, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F+F--F+F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Cross stitch curve":
		cmds.textField("axiom", e=True, tx="F+F+F+F")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F-F+F+F-F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Box fractal":
		cmds.textField("axiom", e=True, tx="F-F-F-F")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F-F+F+F-F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Quadratic Koch island":
		cmds.textField("axiom", e=True, tx="F+F+F+F")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F+F-F-FF+F+F-F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Harter Heighway dragon curve":
		cmds.textField("axiom", e=True, tx="FX")
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.floatSliderGrp("angle", e=True, v=45, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="Z")
		cmds.textField("replacementB", e=True, tx="X")
		cmds.textField("replacementB_2", e=True, tx="+FX--FY+")
		cmds.textField("replacementC", e=True, tx="Y")
		cmds.textField("replacementC_2", e=True, tx="-FX++FY-")

	if presetName == "Peano Gosper curve":
		cmds.textField("axiom", e=True, tx="FX")
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.floatSliderGrp("angle", e=True, v=60, en=True)
		cmds.textField("replacementA", e=True, tx="X")
		cmds.textField("replacementA_2", e=True, tx="X+YF++YF-FX--FXFX-YF+")
		cmds.textField("replacementB", e=True, tx="Y")
		cmds.textField("replacementB_2", e=True, tx="-FX+YFYF++YF+FX--FX-Y")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Minkowski sausage":
		cmds.textField("axiom", e=True, tx="F")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F+F-F-FF+F+F-F")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Levy curve":
		cmds.textField("axiom", e=True, tx="F")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="+F--F+")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Quadratic Gosper curve":
		cmds.textField("axiom", e=True, tx="-YF")
		cmds.floatSliderGrp("radius", e=True, v=0.5, en=True)
		cmds.floatSliderGrp("angle", e=True, v=90, en=True)
		cmds.textField("replacementA", e=True, tx="X")
		cmds.textField("replacementA_2", e=True, tx="XFX-YF-YF+FX+FX-YF-YFFX+YF+FXFXYF-FX+YF+FXFX+YF-FXYF-YF-FX+FX+YFYF-")
		cmds.textField("replacementB", e=True, tx="Y")
		cmds.textField("replacementB_2", e=True, tx="+FXFX-YF-YF+FX+FXYF+FX-YFYF-FX-YF+FXYFYF-FX-YFFX+FX+YF-YF-FX+FX+YFY")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "cmdsWorter's Pentigree":
		cmds.textField("axiom", e=True, tx="F")
		cmds.floatSliderGrp("radius", e=True, v=0.5)
		cmds.floatSliderGrp("angle", e=True, v=36, en=True)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="+F++F----F--F++F++F-")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Tree structure":
		cmds.textField("axiom", e=True, tx="F")
		cmds.floatSliderGrp("radius", e=True, en=True, v=0.4)
		cmds.floatSliderGrp("angle", e=True, en=True, v=22.5)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="FF-[<<<<-F+F+F]+[>>>>+F-F-F]")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Tree structure 2":
		cmds.textField("axiom", e=True, tx="F")
		cmds.intSliderGrp("iterations", e=True,  en=True, v=5)
		cmds.floatSliderGrp("radius", e=True, en=True, v=0.4)
		cmds.floatSliderGrp("angle", e=True, en=True, v=30)
		cmds.textField("replacementA", e=True, tx="F")
		cmds.textField("replacementA_2", e=True, tx="F[+@F][<<<<+@F][>>>>+@F]")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

	if presetName == "Tree structure 3":
		cmds.textField("axiom", e=True, tx="FFFA")
		cmds.floatSliderGrp("radius", e=True, en=True, v=0.8)
		cmds.floatSliderGrp("angle", e=True, en=True, v=40)
		### cmds.intSliderGrp("iterations", e=True,  en=True, v=4)
		cmds.textField("replacementA", e=True, tx="A")
		cmds.textField("replacementA_2", e=True, tx="@[&FFFA]<<<<<<[&FFFA]<<<<<<[&FFFA]")
		cmds.textField("replacementB", e=True, tx="")
		cmds.textField("replacementB_2", e=True, tx="")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")
		
	if presetName == "Stochastic Plant":
		cmds.textField("axiom", e=True, tx="YYY")
		cmds.floatSliderGrp("radius", e=True, en=True, v=0.2)
		cmds.floatSliderGrp("angle", e=True, en=True, v=30)
		cmds.textField("replacementA", e=True, tx="X")
		cmds.textField("replacementA_2", e=True, tx="X[-FFF][+FFF]>>FX ")
		cmds.textField("replacementB", e=True, tx="Y")
		cmds.textField("replacementB_2", e=True, tx="YFX<[+Y]<[-Y] ")
		cmds.textField("replacementC", e=True, tx="")
		cmds.textField("replacementC_2", e=True, tx="")

windowUI()
