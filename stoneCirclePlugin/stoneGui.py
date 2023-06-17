import importlib
import maya.cmds as cmds
import maya.api.OpenMaya as om
import inspect, os.path
import common
importlib.reload(common)
import make_stone_circle
importlib.reload(make_stone_circle)



def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

def initializePlugin(plugin):
    """
    Entry point for a plugin. It is called once -- immediately after the plugin is loaded.
    This function registers all of the commands, nodes, contexts, etc... associated with the plugin.

    It is required by all plugins.

    :param plugin: MObject used to register the plugin using an MFnPlugin function set
    """
    vendor = "Wenyi Zhang"
    version = "1.0.0"

    om.MFnPlugin(plugin, vendor, version)

		#your plugin code below
    def clearSc(*args):
        common.clearScene()

    def colorMat(*args):
        make_stone_circle.material()

    def build(*args):
        innerSize = cmds.intSliderGrp( innerSizeSlider, query =True, value = True)
        circleNum = cmds.intSliderGrp( circleNumSlider, query =True, value = True)
        stoneNum = cmds.intSliderGrp( stoneNumSlider, query =True, value = True)
        stoneHeight = cmds.floatSliderGrp( heightSlider, query =True, value = True)
        stoneWidth = cmds.floatSliderGrp( widthSlider, query =True, value = True)
        structureWidth = cmds.floatSliderGrp( structureSlider, query =True, value = True)
        make_stone_circle.arrayCircle(innerSize, circleNum, stoneNum, stoneHeight, stoneWidth, structureWidth)
    
    def getIcon(icon):
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        icons = os.path.join(path, 'icons')

        icon = os.path.join(icons, icon)
        return icon

    # Make a new window
    stoneWindow = cmds.window( title="Make Stone Circles", iconName='MSC', widthHeight=(500, 440) )
    cmds.columnLayout(adj=True, cat=('both', 5))
    cmds.image( image=(getIcon('preview.png')))
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='in')
    cmds.text( label='Circle Attributes', font = 'boldLabelFont' )
    cmds.separator(h=10, style='in')
    cmds.separator(h=10, style='none')
    # create sliders for each parameter
    innerSizeSlider = cmds.intSliderGrp( label='Inner Circle', min=12, max=50, value=15, field = True)
    circleNumSlider = cmds.intSliderGrp( label='Circle Number', min=4, max=20, value=5, field = True)
    stoneNumSlider = cmds.intSliderGrp( label='Stone Number', min=4, max=9, value=5, field = True)
    heightSlider = cmds.floatSliderGrp( label='Stone Height', min=0.1, max=50,value= 5, step=1, field = True)
    widthSlider = cmds.floatSliderGrp( label='Stone Width', min=0.1, max=5,value= 2, step=1, field = True)
    structureSlider = cmds.floatSliderGrp( label='Structure Width', min=0.1, max=10,value= 5, step=1, field = True)

    cmds.separator(h=20, style='none')
    #create buttons
    cmds.button( label='Make Circles',command=build, bgc=(197/255, 116/255, 232/255))
    cmds.separator(h=10, style='none')
    cmds.button( label='Make Circles Colorful',command=colorMat, bgc=(197/255, 116/255, 232/255))
    cmds.separator(h=10, style='none')
    cmds.button( label='Clear Scene', command=clearSc,bgc=(178/255, 235/255, 102/255))
    cmds.separator(h=10, style='none')
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + stoneWindow + '\", window=True)'))
    cmds.separator(h=20, style='none')
    cmds.setParent( '..' )
    # draw winow
    cmds.showWindow( stoneWindow )

def uninitializePlugin(plugin):
    """
    Exit point for a plugin. It is called once -- when the plugin is unloaded.
    This function de-registers everything that was registered in the initializePlugin function.

    It is required by all plugins.

    :param plugin: MObject used to de-register the plugin using an MFnPlugin function set
    """
    pass


if __name__ == "__main__":
    """
    For Development Only

    Specialized code that can be executed through the script editor to speed up the development process.

    For example: scene cleanup, reloading the plugin, loading a test scene
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)


    # Reload the plugin
    plugin_name = "stoneGui.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))


    # Any setup code to help speed up testing (e.g. loading a test scene)