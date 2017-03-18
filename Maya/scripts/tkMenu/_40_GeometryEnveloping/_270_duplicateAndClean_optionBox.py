import tkBlendShapes
import pymel.core as pc

UINAME = "duplicateCleanOptionWD"

def duplicateClean(*args):#I'll take muteDeformers:bool
    muteDeformers = False

    if len(args) > 1:
        muteDeformers = args[1]

    selObjs = pc.ls(sl=True)

    for selObj in selObjs:
        tkBlendShapes.duplicateAndClean(selObj.name(), "$REF_dupe", muteDeformers)

def duplicateCleanClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    duplicateClean(True, pc.checkBox("duplicateCleanOptionMute",query=True, value=True))

def duplicateCleanOption(*args):
    global UINAME

    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("duplicateCleanOptionWD", title='Duplicate Clean')
        
    colLayout = pc.columnLayout()

    pc.checkBox("duplicateCleanOptionMute", label='Mute Deformers', value=False)
    pc.button(label='Apply', c=duplicateCleanClick, width=177)

    pc.showWindow(UINAME)

duplicateCleanOption()