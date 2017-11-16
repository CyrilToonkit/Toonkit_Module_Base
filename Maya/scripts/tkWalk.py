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

__author__ = "Cyril GIBAUD - Toonkit"

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

    for inputAttr, target in targets:
        if target == inGround:
            inputAttr.disconnect()

#################################################################################
#   UI
#################################################################################

def UIVisChanged(args):
    #Defer the execution in case hidiung is temporary (docking/undocking)
    pc.evalDeferred(cleanIfHidden)

def cleanIfHidden(*args):
   if not pc.control("walkDockControl", query=True, visible=True):
        if pc.window('walkUI', q=True, exists=True):
            pc.deleteUI('walkUI')
        pc.deleteUI('walkDockControl')

def getNamespaces():
    return None if pc.checkBox("walkAllCB", query=True, value=True) else [ns for ns in pc.textField("walkNsLE", query=True, text=True).replace(",", ";").split(";") if ns]

def refreshGrounds():
    pc.textScrollList("walkGroundsLB", edit=True, removeAll=True)

    ns = getNamespaces()

    print "ns",ns

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
    pc.textField("walkNsLE", edit=True, enable=not pc.checkBox("walkAllCB", query=True, value=True))
    refreshGrounds()

def walkNsChanged(*args):
    refreshGrounds()

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

#INIT
###########################################################################

def connectControls():
    pc.checkBox("walkAllCB", edit=True, cc=walkAllChanged)
    pc.textField("walkNsLE", edit=True, cc=walkNsChanged)

    pc.button("walkGroundAddBT", edit=True, c=walkGroundAddClick)
    pc.button("walkGroundRemBT", edit=True, c=walkGroundRemClick)
    pc.button("walkGroundClearBT", edit=True, c=walkGroundClearClick)

def showUI(*inArgs):
    if (pc.window('walkUI', q=True, exists=True)):
        pc.deleteUI('walkUI')

    mainWindow = pc.mel.eval("$tmp = $gMainPane")
    dockLayout = pc.paneLayout(configuration='single', parent=mainWindow)
    dockName = pc.dockControl("walkDockControl", allowedArea='all', area='right', floating=True, content=dockLayout, label="Autowalk", vcc=UIVisChanged)
 
    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = pc.loadUI(uiFile=dirname + "\\UI\\tkWalk.ui")
    pc.showWindow(ui)

    pc.control(ui, e=True, parent=dockLayout)

    connectControls()

    refreshAll()

    pc.control("walkProgressBar", edit=True, visible=False)