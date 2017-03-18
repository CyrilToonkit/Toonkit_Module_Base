import tkMayaCore as tkc
import pymel.core as pc

UINAME = "gatorOptionWD"

def gator(*args):#I'll take strictCopy:bool, matchMatrices:bool
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        strictCopy = False
        if len(args) > 1:
            strictCopy = args[1]
        copyMatrices = False
        if len(args) > 2:
            copyMatrices = args[2]

        tkc.gator(sel[:-1], sel[-1], copyMatrices, strictCopy)
    else:
        pc.warning("Please select at least two objects (any number of meshes to receive weights, then a \"Reference\" mesh) !")

def gatorClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    gator(True, pc.checkBox("gatorOptionStrict",query=True, value=True), pc.checkBox("gatorOptionMatch",query=True, value=True))

def gatorOption(*args):
    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("gatorOptionWD", title='Gator')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select any number of meshes to match first, then the ref mesh')

    pc.checkBox("gatorOptionStrict", label='Strict copy (weights array)', value=False)
    pc.checkBox("gatorOptionMatch", label='Match bind poses', value=False)
    pc.button(label='Apply', c=gatorClick, width=177)

    pc.showWindow(UINAME)

gatorOption()