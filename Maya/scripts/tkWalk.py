"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD - Toonkit
    Copyright (C) 2014-2017 Toonkit
    http://toonkit-studio.com/

    Toonkit Module Lite is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Toonkit Module Lite is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Toonkit Module Lite.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""

import os

import pymel.core as pc

import tkMayaCore as tkc
import tkRig
try:basestring
except:basestring = str

__author__ = "Cyril GIBAUD - Toonkit"

#################################################################################
#   Projection
#################################################################################

def getProjectNodes(inNamespace=None):
    projectNodes = []
    if inNamespace is None:
        projectNodes = pc.ls(type="tkProject")
    else:
        if isinstance(inNamespace, basestring):
            inNamespace = [inNamespace]

        projectNodes = pc.ls([ns + ":*" for ns in inNamespace], type="tkProject")

    return projectNodes

def getTargets(inProjectNode, connections=False):
    if connections:
        return pc.listConnections(inProjectNode.targets, connections=True, plugs=True)

    return [c[1].node() for c in pc.listConnections(inProjectNode.targets, connections=True, plugs=True)]

def addGround(inProjectNode, inGround):
    targets = getTargets(inProjectNode)

    if not inGround in targets:
        freeIndex = tkc.get_next_free_multi_index(inProjectNode.targets.name())
        inGround.worldMesh[0] >> inProjectNode.attr("targets[{0}]".format(freeIndex))

def removeGround(inProjectNode, inGround=None):
    if inGround is None:
        inProjectNode.targets.disconnect()
        return

    targets = getTargets(inProjectNode, connections=True)

    for inputAttr, targetAttr in targets:
        if targetAttr.node() == inGround:
            inputAttr.disconnect()

#################################################################################
#   Baking
#################################################################################

def getBakeables(inNamespace=None):
    bakeables = []
    if inNamespace is None:
        bakeables = pc.ls("*{0}".format(tkRig.CONST_BAKERSUFFIX), transforms=True)
    else:
        if isinstance(inNamespace, basestring):
            inNamespace = [inNamespace]
        bakeables = pc.ls(["{0}:*{1}".format(ns, tkRig.CONST_BAKERSUFFIX) for ns in inNamespace], transforms=True)

    return bakeables

def bake(inStart, inEnd, inNamespace=None, inUnbake=True):
    if inUnbake:
        unbake(inNamespace=inNamespace)

    bakeables = getBakeables(inNamespace=inNamespace)
    sources = []
    toBake = []
    cns = []
    bakeAttrs = []

    for bakeable in bakeables:
        sourceName = bakeable.name()[:-len(tkRig.CONST_BAKERSUFFIX)]
        if not pc.objExists(sourceName):
            pc.warning("Source object {0} not found for baking !".format(sourceName))
            continue

        source = pc.PyNode(sourceName)
        sources.append(source)
        cns.append(tkc.constrain(bakeable, source, inOffset=False))
        toBake.append(bakeable)

        attr = tkc.getRealAttr(source.baked.name())
        if not attr in bakeAttrs:
            bakeAttrs.append(attr)

    if len(toBake) == 0:
        pc.warning("Nothing to bake, skipping...")
        return

    timerMessage = "Baking {0} transforms on {1} frames".format(len(toBake), inEnd-inStart+1)

    try:
        pc.mel.eval("paneLayout -e -manage false $gMainPane")

        tkc.startTimer(timerMessage, inReset=True)
        pc.bakeResults(toBake, simulation=True, sampleBy=1, t=(inStart,inEnd), disableImplicitControl=False, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=False, controlPoints=False, shape=False)
        pc.delete(cns)
        tkc.stopTimer(timerMessage, inLog=True)
    except Exception as e:
        pc.warning("Unmanaged exception in baking ({0})".format(e))
    finally:
        pc.mel.eval("paneLayout -e -manage true $gMainPane") 

    for bakeAttr in bakeAttrs:
        pc.setAttr(bakeAttr, 1)

"""DEPRECATED
def unbake(inNamespace=None):
    bakeables = getBakeables(inNamespace=inNamespace)

    bakeAttrs = []

    for bakeable in bakeables:
        sourceName = bakeable.name()[:-len(tkRig.CONST_BAKERSUFFIX)]
        if not pc.objExists(sourceName):
            pc.warning("Source object {0} not found for baking !".format(sourceName))
            continue

        pc.cutKey(bakeable, clear=True)
        tkc.resetTRS(bakeable)

        source = pc.PyNode(sourceName)
        attr = tkc.getRealAttr(source.baked.name())

        if not attr in bakeAttrs:
            bakeAttrs.append(attr)

    for bakeAttr in bakeAttrs:
        pc.setAttr(bakeAttr, 0)
"""
#################################################################################
#   UI
#################################################################################

def UIVisChanged(args):
    #Defer the execution in case hidiung is temporary (docking/undocking)
    pc.evalDeferred(cleanIfHidden)

def cleanIfHidden(*args):
    if pc.window('walkDockControl', query=True, exists=True):
        if not pc.window('walkDockControl', query=True, visible=True):
            pc.deleteUI('walkDockControl')


def getNamespaces():
    return None if pc.checkBox("walkAllCB", query=True, value=True) else [ns for ns in pc.textField("walkNsLE", query=True, text=True).replace(",", ";").split(";") if ns]

def refreshGrounds():
    pc.textScrollList("walkGroundsLB", edit=True, removeAll=True)

    ns = getNamespaces()

    if not ns is None and len(ns) == 0:
        return

    projectNodes = getProjectNodes(getNamespaces())

    if len(projectNodes) == 0:
        pc.warning("No projection nodes found !")
        return

    allGrounds = []

    for projectNode in projectNodes:
        grounds = getTargets(projectNode)

        for ground in grounds:
            if not ground in allGrounds:
                allGrounds.append(ground)

    for ground in allGrounds:
        pc.textScrollList("walkGroundsLB", edit=True, append=ground.name())

def refreshAll():
    refreshGrounds()

#CALLBACKS
###########################################################################

def walkAllChanged(*args):
    if pc.checkBox("walkAllCB", query=True, value=True):
        pc.textField("walkNsLE", edit=True, text=";".join([str(n.namespace()) for n in tkc.getAssets()]))
        pc.textField("walkNsLE", edit=True, enable=False)
    else:
        pc.textField("walkNsLE", edit=True, enable=True)
    
    refreshGrounds()

def walkNsChanged(*args):
    refreshGrounds()

def walkFromSelClick(*args):
    nss = list(set([str(n.namespace()) for n in pc.selected()]))
    if len(nss) == 0:
        pc.warning("Please select any object from your assets")
        return

    pc.checkBox("walkAllCB", edit=True, value=False)
    pc.textField("walkNsLE", edit=True, text=";".join(nss))
    walkAllChanged()

def walkSelectClick(*args):
    nss = getNamespaces()
    if nss is None:
        nss = [str(n.namespace()) for n in tkc.getAssets()]

    pc.select([ns + "Global_SRT" for ns in nss])

def walkGroundAddClick(*args):
    sel = pc.selected()

    shapes = []

    for selObj in sel:
        shape = selObj
        if selObj.type() == "transform":
            shape = shape.getShape()
            if not shape is None and shape.type() == "mesh":
                shapes.append(shape)

    if len(shapes) == 0:
        pc.warning("No meshes selected !")
        return

    projectNodes = getProjectNodes(getNamespaces())
    for projectNode in projectNodes:
        for shape in shapes:
            addGround(projectNode, shape)

    refreshGrounds()

def walkGroundRemClick(*args):
    selGrounds = pc.textScrollList("walkGroundsLB", query=True, allItems=True)

    if len(selGrounds) == 0:
        pc.warning("Please select one or more grounds to remove")
        return

    projectNodes = getProjectNodes(getNamespaces())

    for selGround in selGrounds:
        for projectNode in projectNodes:
            removeGround(projectNode, pc.PyNode(selGround))

    refreshGrounds()

def walkGroundClearClick(*args):
    projectNodes = getProjectNodes(getNamespaces())
    for projectNode in projectNodes:
        removeGround(projectNode)

    refreshGrounds()

def walkBakeClick(*args):
    start = float(pc.textField("walkStartFrameLE", query=True, text=True))
    end = float(pc.textField("walkEndFrameLE", query=True, text=True))

    PostSetAttrs = {"Autowalk_ParamHolder.Autowalk":0}
    skipControls = ["Left_Leg_01_IK_Parent","Left_Leg_02_IK_Parent", "Left_Leg_03_IK_Parent", "Left_Leg_04_IK_Parent", "Right_Leg_01_IK_Parent","Right_Leg_02_IK_Parent", "Right_Leg_03_IK_Parent", "Right_Leg_04_IK_Parent"]

    nss = getNamespaces()
    if nss is None:
        nss = [str(n.namespace()) for n in tkc.getAssets()]

    tkRig.bakeAutomatedCtrls([ns.rstrip(":") for ns in nss], inStart=start, inEnd=end, inPostSetAttrs=PostSetAttrs, inSkipControls=skipControls)


"""DEPRECATED
def walkUnbakeClick(*args):
    unbake(getNamespaces())
"""

def walkGetFromSceneClick(*args):
    start = pc.playbackOptions(query=True, minTime=True)
    end = pc.playbackOptions(query=True, maxTime=True)

    pc.textField("walkStartFrameLE", edit=True, text=str(start))
    pc.textField("walkEndFrameLE", edit=True, text=str(end))

#INIT
###########################################################################

def connectControls():
    pc.checkBox("walkAllCB", edit=True, cc=walkAllChanged)
    pc.textField("walkNsLE", edit=True, cc=walkNsChanged)

    pc.button("walkFromSelBT", edit=True, c=walkFromSelClick)
    pc.button("walkSelectBT", edit=True, c=walkSelectClick)

    pc.button("walkGroundAddBT", edit=True, c=walkGroundAddClick)
    pc.button("walkGroundRemBT", edit=True, c=walkGroundRemClick)
    pc.button("walkGroundClearBT", edit=True, c=walkGroundClearClick)
    pc.button("walkGetFromSceneBT", edit=True, c=walkGetFromSceneClick)
    pc.button("walkBakeBT", edit=True, c=walkBakeClick)
    
    #pc.button("walkUnbakeBT", edit=True, c=walkUnbakeClick)

def showUI(*inArgs):
    walkUIMayaWindow = "tkWalkWindow"
    walkUIDockLayout = "tkWalkLayout"
    walkUIDockWindow = "walkDockControl"

    if not pc.window(walkUIMayaWindow, q=True, exists=True):
        mayaWindow = pc.window(walkUIMayaWindow, title = "TK Sym")
        dirname, filename = os.path.split(os.path.abspath(__file__))
        walkUIWindow = pc.loadUI(uiFile=os.path.join(dirname, "UI", "tkWalk.ui"))
        pc.control(walkUIWindow, e=True, parent=mayaWindow)
        
    mainWindow = pc.mel.eval("$tmp = $gMainPane")
    if not pc.paneLayout(walkUIDockLayout, q=True, exists=True):
        pc.paneLayout(walkUIDockLayout, configuration='single', parent=mainWindow)
    if not pc.dockControl(walkUIDockWindow, q=True, exists=True):
        pc.dockControl(walkUIDockWindow, allowedArea='all', area='right', floating=False, content=walkUIDockLayout, label='TK Sym', vcc=UIVisChanged)
        pc.control(mayaWindow, e=True, parent= walkUIDockLayout)
    if not pc.dockControl(walkUIDockWindow, q=True, visible=True):
        pc.dockControl(walkUIDockWindow,e=True, visible=True)

    connectControls()

    refreshAll()

    walkGetFromSceneClick()
    walkAllChanged()

    pc.control("walkProgressBar", edit=True, visible=False)