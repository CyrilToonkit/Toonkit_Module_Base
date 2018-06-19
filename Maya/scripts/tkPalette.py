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

"""
    Geometry colors manager
"""
import os

import maya.cmds as mc
import maya.mel as mel

import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

SHADERTYPES = mc.listNodeTypes('shader')

PREVIZ_COLORS = {}

def to0_255(inColor):
    return (int(inColor[0] * 255), int(inColor[1] * 255), int(inColor[2] * 255))

def to0_1(inColor):
    return (inColor[0] / 255.0, inColor[1] / 255.0, inColor[2] / 255.0)

def assignShader(inMaterial, inObj, inSG=None):
    #print "assignShader(%s, %s, %s, %s)" % (str(inMaterial), str(inObj), str(inSG), str(inMultiUVs))
    #return None
    shape = inObj
    if mc.nodeType(inObj) == "transform":
        shapes = mc.listRelatives(inObj, shapes=True)
        if len(shapes) > 0:
            shape = shapes[0]
        else:
            mc.warning("Can't find any shapes on object %s" % inObj)

    shadingGroup = None

    if inSG != None:
        shadingGroup = inSG
    else:
        nodes = mc.listHistory(inMaterial, future=True, levels=1)
        
        for node in nodes:
            nodeType = mc.nodeType(node)
            if not "initialParticleSE" in node and (nodeType == "shadingEngine" or nodeType == "materialFacade"):
                shadingGroup = node
                break

        #No shading group ?
        if shadingGroup == None:
            shadingGroup = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=inMaterial+"SG")
            mc.connectAttr(inMaterial + ".outColor", shadingGroup + ".surfaceShader", force=True)

    mel.eval("sets -forceElement " + shadingGroup + " " + shape)

    return shadingGroup

def getShaders(inObj, inFirstOnly=True):
    shaders = []
    shapes = [inObj]
    if mc.nodeType(inObj) == "transform":
        shapes = mc.listRelatives(inObj, shapes=True)

    for shape in shapes:
        shadingGroups = mc.listConnections(shape, type="shadingEngine")
        if shadingGroups != None:
            for sGroup in shadingGroups:
                if "initialParticleSE" in sGroup:
                    continue
                cons = mc.listConnections(sGroup, destination=False)
                for con in cons:
                    if mc.nodeType(con) in SHADERTYPES:
                        shaders.append(con)
                        if inFirstOnly:
                            return shaders
                        break
    
    return shaders

def roundColor(inColor):
    return (round(inColor[0], 2), round(inColor[1], 2), round(inColor[2], 2))

def getShaderName(inColor):
    return "pre_lambert_{0}_{1}_{2}".format(inColor[0], inColor[1], inColor[2])

def assignColor(inMesh, inColor):
    shaderName = getShaderName(inColor)

    if not mc.objExists(shaderName):
        mc.shadingNode("lambert", asShader=True, name=shaderName)
        mc.setAttr(shaderName + ".color", *[i / 255.0 for i in inColor])

    assignShader(shaderName, inMesh)

def addColor(rgb, sel):
    global PREVIZ_COLORS

    if not rgb in PREVIZ_COLORS:
        PREVIZ_COLORS[rgb] = []

    for selObj in sel:
        shortName = selObj.split(":")[-1]
        if not shortName in PREVIZ_COLORS[rgb]:
            PREVIZ_COLORS[rgb].append(shortName)

        assignColor(selObj, rgb)

        emptyKeys = []
        for key, value in PREVIZ_COLORS.iteritems():
            if key != rgb and shortName in value:
                value.remove(shortName)
                if len(value) == 0:
                    emptyKeys.append(key)
        for key in emptyKeys:
            del PREVIZ_COLORS[key]

def setColors():
    notFound = []
    for shd_color, meshes in PREVIZ_COLORS.iteritems():
        for mesh in meshes:
            meshName = mesh
            if not mc.objExists(meshName):
                results = mc.ls("*:"+meshName)
                if len(results) > 0:
                    meshName = results[0]
            if mc.objExists(meshName):
                assignColor(meshName, shd_color)
            else:
                notFound.append(mesh)
                mc.warning(mesh + " not found !")
                
    if len(notFound) > 0:
        mc.warning("Some meshes were not found :\n" + ",".join(notFound))

def colorCommand(inColor):
    global PREVIZ_COLORS
    selection = mc.ls(sl=True)

    if len(selection) == 0:
        mc.warning("Please select some objects to color")
        return

    opaqueColor = (inColor[1], inColor[2], inColor[3])
    opaqueColor = to0_255(roundColor(to0_1(opaqueColor)))

    addColor(opaqueColor, selection)
    initUI()

    mc.select(selection)

def palNewClick(*args):
    sel = mc.ls(sl=True)

    if len(sel) == 0:
        mc.warning("Please select some objects to color")
        return

    mc.colorEditor()
    if mc.colorEditor(query=True, result=True):
        values = roundColor(mc.colorEditor(query=True, rgb=True))
        
        rgb = to0_255(values)

        addColor(rgb, sel)
        initUI()

    mc.select(sel)

def palEditClick(*args):
    global PREVIZ_COLORS

    sel = mc.textScrollList("tkPalManagedLB", query=True, selectItem=True)

    if sel == None:
        mc.warning("Please select a color set in the list")
        return

    oldColor = eval("("+sel[0].split(" : ")[0]+")")

    values = to0_1(oldColor)

    mc.colorEditor(rgb=values)

    if mc.colorEditor(query=True, result=True):
        values = roundColor(mc.colorEditor(query=True, rgb=True))
        
        rgb = to0_255(values)

        objects = PREVIZ_COLORS[oldColor]
        del PREVIZ_COLORS[oldColor]
        PREVIZ_COLORS[rgb] = objects

        for obj in objects:
            meshName = obj
            if not mc.objExists(meshName):
                results = mc.ls("*:"+meshName)
                if len(results) > 0:
                    meshName = results[0]
            assignColor(meshName, rgb)

        initUI()

def palApplyClick(*args):
    global PREVIZ_COLORS

    selection = mc.ls(sl=True)

    if len(selection) == 0:
        mc.warning("Please select some objects to color")
        return

    sel = mc.textScrollList("tkPalManagedLB", query=True, selectItem=True)

    if sel == None:
        mc.warning("Please select a color set in the list")
        return

    color = eval("("+sel[0].split(" : ")[0]+")")
    objects = sel[0].split(" : ")[1].split(",")

    for selObj in selection:
        assignColor(selObj, color)
        shortName = selObj.split(":")[-1]
        if not shortName in objects:
            PREVIZ_COLORS[color].append(shortName)
        emptyKeys = []
        for key, value in PREVIZ_COLORS.iteritems():
            if key != color and shortName in value:
                value.remove(shortName)
                if len(value) == 0:
                    emptyKeys.append(key)
        for key in emptyKeys:
            del PREVIZ_COLORS[key]
    initUI()

def palTodoChanged(*args):
    sel = mc.textScrollList("tkPalTodoLB", query=True, selectItem=True)
    mc.select(sel)

def palManagedChanged(*args):
    sync = mc.checkBox("tkPalAutoSelectCB", query=True, value=True)

    if sync:
        sel = []
        rawSel = mc.textScrollList("tkPalManagedLB", query=True, selectItem=True)
        
        for selPatterns in rawSel:
            selPatterns = selPatterns.split(" : ")[1].split(",")
            for selPattern in selPatterns:
                objs = mc.ls(["*:"+selPattern, selPattern], transforms=True)
                sel.extend(objs)

        if len(sel) == 0:
            mc.select(clear=True)
        else: 
            mc.select(sel)

def palLoadClick(*args):
    global PREVIZ_COLORS

    choosenFile = mc.fileDialog2(caption="Select your palette file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=1)

    if choosenFile != None and len(choosenFile) > 0:
        choosenFile = choosenFile[0]

        content = None

        with open(choosenFile) as f:
            content = f.read()

        if content != None:
            PREVIZ_COLORS = eval(content)
            initUI()

def palSaveClick(*args):
    choosenFile = mc.fileDialog2(caption="Save your palette file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

    if choosenFile != None and len(choosenFile) > 0:
        choosenFile = choosenFile[0]

        with open(choosenFile, "w") as f:
            f.write(str(PREVIZ_COLORS))

def palApplyAllClick(*args):
    setColors()
    tkc.deleteUnusedNodes()

def palGetFromSceneClick(*args):
    global PREVIZ_COLORS

    PREVIZ_COLORS = {}

    meshes = mc.ls(type="mesh")

    for mesh in meshes:
        if not mc.getAttr(mesh + ".intermediateObject"):
            parents = mc.listRelatives(mesh, parent=True)
            if parents != None and len(parents) > 0:
                shaders = getShaders(mesh)
                if len(shaders) > 0:
                    shader = shaders[0]
                    color = to0_255(mc.getAttr(shader + ".color")[0])
                    if not color in PREVIZ_COLORS:
                        PREVIZ_COLORS[color] = []

                    PREVIZ_COLORS[color].append(parents[0].split(":")[-1])

    initUI()
    setColors()
    tkc.deleteUnusedNodes()

def palRefreshClick(*args):
    initUI()

def connectControls():
    mc.button("tkPalLoadBT", edit=True, c=palLoadClick)
    mc.button("tkPalSaveBT", edit=True, c=palSaveClick)
    mc.button("tkPalApplyAllBT", edit=True, c=palApplyAllClick)

    mc.button("tkPalGetFromSceneBT", edit=True, c=palGetFromSceneClick)
    mc.button("tkPalRefreshBT", edit=True, c=palRefreshClick)

    mc.button("tkPalNewBT", edit=True, c=palNewClick)
    mc.button("tkPalEditBT", edit=True, c=palEditClick)
    mc.button("tkPalApplyBT", edit=True, c=palApplyClick)

    mc.textScrollList("tkPalManagedLB", edit=True, sc=palManagedChanged)
    mc.textScrollList("tkPalTodoLB", edit=True, sc=palTodoChanged)

def initUI(*args):
    meshesT=[]
    meshes = mc.ls(type="mesh")

    for mesh in meshes:
        if not mc.getAttr(mesh + ".intermediateObject"):
            parents = mc.listRelatives(mesh, parent=True)
            if parents != None and len(parents) > 0 and not (parents[0] in meshesT):
                meshesT.append(parents[0])

    managedMeshes = []
    mc.textScrollList("tkPalManagedLB", edit=True, removeAll=True)

    for shd_color, meshes in PREVIZ_COLORS.iteritems():
        mc.textScrollList("tkPalManagedLB", edit=True, append="{0},{1},{2} : {3}".format(shd_color[0], shd_color[1], shd_color[2], ",".join(meshes)))
        for mesh in meshes:
            for meshT in meshesT:
                if meshT.split(":")[-1] == mesh:
                    managedMeshes.append(meshT.split(":")[-1])
                    break

    mc.textScrollList("tkPalTodoLB", edit=True, removeAll=True)
    for meshT in meshesT:
        if not meshT.split(":")[-1] in managedMeshes:
            mc.textScrollList("tkPalTodoLB", edit=True, append=meshT)

def showUI():
    if (mc.window('tkPaletteUI', q=True, exists=True)):
        mc.deleteUI('tkPaletteUI')

    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = mc.loadUI(uiFile=dirname + "\\UI\\tkPalette.ui")

    mc.showWindow(ui)

    #add menu

    connectControls()

    initUI()

    mc.control("palProgressBar", edit=True, visible=False)