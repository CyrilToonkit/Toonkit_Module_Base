import maya.cmds as cmds
import maya.mel as mel

import tkRig

SPACES_ATTRS = ["Parent_Space", "ParentSpace", "Orient_Space", "OrientSpace"]

UINAME = "SpaceSwitcherUI"
JOBID = None

def getFirstExistingAttr(inObj, inAttrs):
    for attr in inAttrs:
        if cmds.attributeQuery(attr, n=inObj, ex=True):
            return attr

    return None

def getEnumIndex(inObj, inAttrName, inValue):
    enums = pc.attributeQuery(inAttrName, node=inObj, listEnum=True)[0].split(":")
    try:
        return enums.index(inValue)
    except:
        return None

def optionChanged(item):
    print(item)
    
    for obj in cmds.ls(sl=True):
        attr = getFirstExistingAttr(obj, SPACES_ATTRS)
        if attr is None:
            continue

        idx = getEnumIndex(obj, attr, item)
        if idx is None:
            continue

        tkRig.setSpace("{}.{}".format(obj, attr), idx)

    buildUI()

def selectionChanged():
    print("selectionChanged")
    buildUI()

def UIVisChanged(*args):
    cmds.evalDeferred(cleanIfHidden)

def isObjectValid(inObj):
    for attr in SPACES_ATTRS:
        if cmds.attributeQuery(attr, n=inObj, ex=True):
            return True

    return False

def buildUI():
    
    objs = [n for n in cmds.ls(selection=True) if isObjectValid(n)]
    text = "No valid objects selected !" if len(objs) == 0 else "Selected objects : " + ",".join(objs)
    
    cmds.text(UINAME + "_label", edit=True, label=text)
    
    items = cmds.optionMenu(UINAME + "_optMenu", query=True, itemListLong=True)
    for item in items or []:
        cmds.deleteUI(item)
    
    if len(objs) == 0:
        cmds.optionMenu(UINAME + "_optMenu", edit=True, enable=False)
    else:
        spaceAttr = getFirstExistingAttr(objs[0], SPACES_ATTRS)
        
        enums = pc.attributeQuery(spaceAttr, node=objs[0], listEnum=True)[0].split(":")
        currentIndex = pc.getAttr("{}.{}".format(objs[0], spaceAttr))
        
        cmds.setParent(UINAME + "_optMenu", menu=True)

        for i, enum in enumerate(enums):
            cmds.menuItem( label=enum , enable= i != currentIndex)

        cmds.optionMenu(UINAME + "_optMenu", edit=True, enable=True, label=spaceAttr, select=currentIndex+1)

def cleanUI():
    if cmds.control(UINAME, query=True, exists=True):
        cmds.deleteUI(UINAME, control=True)
        
    if not JOBID is None:
        cmds.evalDeferred("import maya.cmds as cmds;cmds.scriptJob(kill=" + str(JOBID) + ", force=True)")

def cleanIfHidden():
    if not cmds.control(UINAME, query=True, exists=True) or not cmds.control(UINAME, query=True, visible=True):
        cmds.evalDeferred(cleanUI)

def showUI():
    global JOBID

    if cmds.window(UINAME, query=True, exists=True):
        cmds.deleteUI(UINAME)
    
    window = cmds.window(UINAME, title="Space switcher")
    
    JOBID = cmds.scriptJob(event=["SelectionChanged", selectionChanged])

    cmds.columnLayout()
    cmds.text(UINAME + "_label", label="")
    cmds.optionMenu(UINAME + "_optMenu", label='Spaces', changeCommand=optionChanged , vcc=UIVisChanged)
    
    buildUI()
    
    cmds.showWindow( window )
    
showUI()