import tkBlendShapes
import pymel.core as pc

UINAME = "copyBSOptionWD"

def copyBS(*args):#I'll take strictCopy:bool, matchMatrices:bool
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        source = sel[-1]
        targets = sel[:-1]
        sources = pc.ls(pc.listHistory(source, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
        if len(sources) == 0:
            pc.warning("Cannot find BlendShape node on {0}".format(source))
            return
        for target in targets:
            for source in sources:
                tkBlendShapes.copyBS(source.name(), target.name())
    else:
        pc.warning("Please select at least two objects (any number of meshes to receive blendShapes, then a \"Reference\" mesh) !")

def copyBSClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    copyBS(True, )

def copyBSOption(*args):
    print ("NOT IMPLEMENTED")
    return

    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("copyBSOptionWD", title='Gator')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select any number of meshes to match first, then the ref mesh')

    pc.checkBox("gatorOptionStrict", label='Strict copy (weights array)', value=False)
    pc.checkBox("gatorOptionMatch", label='Match bind poses', value=False)
    pc.button(label='Apply', c=gatorClick, width=177)

    pc.showWindow(UINAME)

copyBSOption()