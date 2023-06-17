## L-System Garden 1.0.0


### How to use?
1. Windows / Linux:<br/>
Move the scripts to: Documents\maya\YEAR\scripts
Move the images to: Documents\maya\YEAR\prefs\icons
2. OSX:<br/>
Move the scripts to: /Users/YOUR_USERNAME/Library/Preferences/Autodesk/Maya/YEAR/scripts
<br/>Move the images to: /Users/YOUR_USERNAME/Library/Preferences/Autodesk/Maya/YEAR/prefs/icons

3. Copy and Paste this section of code to launch the UI. Make sure you set it to Python.
```python
{
import importlib
import maya.cmds as cmds
import gui_LGarden
importlib.reload(gui_LGarden)
}
```

### More
- This script is based on Zeno Pelgrims - www.graffik.be - NCCA 2014 - fractalGenerator. I modified the original scripts from 2D L-system to 3D, added 4 more rotation operations: <, >, ^, &.
- The iteration time can influence the running time significantly, be careful if when iterations > 4.
- If the L-system start to be drawn incorrectly, please restart Maya, clear inputs and try again. There still is a small bug hiding itself...
- try F ==> F[+F][-F[-F]F[+F][-F]
- ref1:http://algorithmicbotany.org/papers/#abop
- ref2:http://paulbourke.net/fractals/lsys/