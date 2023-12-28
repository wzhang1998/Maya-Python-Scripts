# Maya-Python-Scripts
Python plugins for Maya

## L-SystemGarden
![](/LSystemGarden/LSystemGardenDemo01.gif)
<img src='/LSystemGarden/preview02.png' width='518'>
### How to use?
1. Windows / Linux:<br/>
Move the scripts to: Documents\maya\YEAR\scripts
Move the images to: Documents\maya\YEAR\prefs\icons
2. OSX:<br/>
Move the scripts to: /Users/YOUR_USERNAME/Library/Preferences/Autodesk/Maya/YEAR/scripts
<br/>Move the images to: /Users/YOUR_USERNAME/Library/Preferences/Autodesk/Maya/YEAR/prefs/icons

3. Copy and Paste this section of code to launch the UI. Make sure you set it to Python.
```python

import importlib
import maya.cmds as cmds
import gui_LGarden
importlib.reload(gui_LGarden)

```
### More
- This script is based on Zeno Pelgrims - www.graffik.be - NCCA 2014 - fractalGenerator. I modified the original scripts from 2D L-system to 3D, added 4 more rotation operations: <, >, ^, &.
- The iteration time can influence the running time significantly, be careful if when iterations > 4.
- If the L-system start to be drawn incorrectly, please restart Maya, clear inputs and try again. There still is a small bug hiding itself...
- try F ==> F[+F][-F[-F]F[+F][-F]
- ref1:http://algorithmicbotany.org/papers/#abop
- ref2:http://paulbourke.net/fractals/lsys/

## RandomGen
<img src="https://github.com/wzhang1998/Maya-Python-Scripts/assets/67906283/c45cb706-a09d-42b1-9b61-6022b5dbdc1d" width='518'>\
This script generates a random colorful animated scene using three hided meshes in the Maya scene: 'cartoon_controller', 'soda_can', 'lollipop'
Don't forget to play the animation ;)       

### How to use?
1. open 10_8_script_RandomGen.ma in Maya
2. copy and paste RandomGenerator.py into script editor


## StoneCirclePlugin
<img src="https://github.com/wzhang1998/Maya-Python-Scripts/assets/67906283/6f0da355-6de7-4f96-9f9a-4df74a854180" width='518'>\
This is a plug-in to make rings of standing stones.

### How to use?
1. move all the files in this folder into your Maya plug-in folder
2. open Plug-in Manager Window, search stoneGui.py, and check 'Loaded'
3. then you can start creating customize stone circles!

### More
- still have some issue with deleting overlapping, I've tried to use the bounding box command.
