from math import sqrt, radians, sin, cos
import maya.cmds as cmds


### LSystem
class LSystem(object):

	### create empty rule dictionary
	rule = {}

	### replace axiom rule function
	def replaceRule(self, initial, replacement):
		self.rule[initial] = replacement

	### repeat function 
	def repeat(self, axiom, iterations):

		### reset var
		replacement = ""

		if iterations > 0:
			for i in axiom:
				replacement += self.rule.get(i, i)
			axiom = replacement
			return self.repeat(axiom, iterations-1)
		else:
			print (axiom)
			return axiom

### add rule function: add new rule to dictionary
def addRule(replacementA, replacementA_2, replacementB, replacementB_2, replacementC, replacementC_2):

	LSystem().replaceRule(replacementA, replacementA_2)
	LSystem().replaceRule(replacementB, replacementB_2)
	LSystem().replaceRule(replacementC, replacementC_2)


### draw L-system function
def drawLsystem(instructions, angle, distance, radius, presetName, scale):
	### parent cylinders
	if len(presetName) > 0 and presetName != "None":
		parent = cmds.createNode("transform", n=str(presetName))
	else:
		parent = cmds.createNode("transform", n="L_Root_#")
	saved=[]

	for act in instructions:
		if act == 'F':
			cyl = cmds.cylinder(r=radius, ax=[0,1,0], hr=distance/radius)
			cyl = cmds.parent( cyl[0], parent, r=1)
			cmds.move(0, (distance/2.0), 0, cyl[0], os=1)   
			parent = cmds.createNode("transform", p=parent)
			cmds.move(0, (distance), 0, parent, os=1) 
		if act == '-':
			parent = cmds.createNode("transform", p=parent)
			cmds.rotate(angle, 0, 0, parent, os=1) 
		if act == '+':
			parent = cmds.createNode("transform", p=parent)
			cmds.rotate(-angle, 0, 0, parent, os=1) 
		if act == '>':
			parent = cmds.createNode("transform", p=parent)
			cmds.rotate(0, angle, 0, parent, os=1) 
		if act == '<':
			parent = cmds.createNode("transform", p=parent)
			cmds.rotate(0, -angle, 0, parent, os=1) 
		if act == '^':
			parent = cmds.createNode("transform", p=parent)
			cmds.rotate(0, 0, angle, parent, os=1) 
		if act == '&':
			parent = cmds.createNode("transform", p=parent)
			cmds.rotate(0, 0, -angle, parent, os=1) 
		if act == '[':
			saved.append(parent)
		if act == ']':
			parent = saved.pop()  
		if act == '|':
			parent = cmds.createNode("transform", p=parent)
			cmds.rotate(180, 0, 0, parent, os=1) 
		if act == '@':
			parent = cmds.createNode("transform", p=parent)
			cmds.scale(scale, scale, scale, parent) 

	### flush undo history to remove ram usage
	cmds.flushUndo()
		


