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
    Topological symmetry tool
"""
import time
import os
from itertools import permutations
import time

import pymel.core as pc
import maya.cmds as mc

import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

WAVETIME = 0.1

"""
Number of max theoretical waves per point (edges would be a much better estimate)

tests:
2981 pts = Wave 25 (0,00838)
1863 pts = Wave 19 (0,01019)
5231 pts = Wave 42 (0,00802)
"""
MAXITERRATIO = 0.08

MAXWAVELENGTH = 8

MINITER = 10

CENTERTOL = 0.02
DOTTOL = 0.25

SYMMAP = "symMap"
LOCMAP = "locMap"

SYMCTRLS = [
                "symSymSelBT",
                "symAddSelCB",
                "symSymMeshBT",
                "symRuleDD",
                "symSelRealRightBT",
                "symSelRealCenterBT",
                "symSelRealLeftBT"
            ]

MESHEXISTSCTRLS = [
                "symSelCenterBT",
                "symCheckBT",
                "symShowwCB",
                "symResetBaseBT"
            ]

TABLE = []
VERBOSE=False

UIJOBID = None
JOBID = None
OLDPREF = False

def logVerbose(inString):
    if VERBOSE:
        print inString

def sortCurWaves(posRef, curPosWave, negRef, curNegWave, posInfo, negInfo):
    global TABLE

    split = 0
    if posInfo[0][0].name() != negInfo[0][0].name():
        split = 1

    #print "sortCurWaves(", curPosWave,", ",curNegWave,", ", posInfo, ", ", negInfo,")"
    nbComps = len(curPosWave)
    rangeNbComps = range(nbComps)
    if nbComps > 1:
        if VERBOSE:
            print "Waves longer than 1, arrangement required !! (",posRef, ":", curPosWave, negRef, ":", curNegWave, ")"

        if nbComps > MAXWAVELENGTH:
            #Fill table ?
            """
            for i in range(len(curPosWave)):
                TABLE[curPosWave[i]] = curNegWave[i]
                TABLE[curNegWave[i]] = curPosWave[i]
            """
            return False

        #find all permutations of negative list of vetors to see wich arrangement fits
        negWavesArrangements = tuple(permutations(curNegWave))

        #precalculate localized vectors
        posLocalized = {}
        negLocalized = {}
        for i in rangeNbComps:
            vec = posInfo[posRef][1] - posInfo[curPosWave[i]][1]
            vec.normalize()
            posLocalized[curPosWave[i]] = vec

            negVec = negInfo[negRef][1] - negInfo[curNegWave[i]][1]
            negVec.normalize()
            if not split:
                negVec[0]*=-1
            negLocalized[curNegWave[i]] = negVec

        bestScore = 0
        bestArrangement = None

        for negWavesArrangement in negWavesArrangements:
            #print "Arrangement",negWavesArrangement
            score = 0.0
            for i in rangeNbComps:
                score += posLocalized[curPosWave[i]]*negLocalized[negWavesArrangement[i]]
            #print "score",score
            if score > bestScore:
                bestArrangement = negWavesArrangement
                bestScore = score


        #We really have to rearrange curNegWave, it will sort it for topology parsing
        #... and Fill table
        for i in rangeNbComps:
            curNegWave[i]=bestArrangement[i]
            TABLE[curPosWave[i]] = curNegWave[i]
            TABLE[curNegWave[i] + (split*len(posInfo))] = curPosWave[i]
        #print "curPosWave",curPosWave
        #print "curNegWave",curNegWave
    else:
        #Fill table
        TABLE[curPosWave[0]] = curNegWave[0]
        TABLE[curNegWave[0] + (split*len(posInfo))] = curPosWave[0]

    return True

def writeMaps(nodes, symTable, locTable, numVertices):
    offset = 0
    managed = []
    for nodeItem in nodes:
        if nodeItem in managed:
            continue
        managed.append(nodeItem)
        tkc.addPerPointData(nodeItem, SYMMAP, symTable[offset:offset+numVertices])
        tkc.addPerPointData(nodeItem, LOCMAP, locTable[offset:offset+numVertices])
        offset = numVertices

def getTable(inMesh, inCenterIDs=None, inAxis=0, inShowWavesTime=WAVETIME, inCenterTol=CENTERTOL):
    global TABLE

    if VERBOSE:
        print "getTable({0}, inCenterIDs={1}, inAxis={2}, inShowWavesTime={3}, inCenterTol={4})".format(inMesh, inCenterIDs, inAxis, inShowWavesTime, inCenterTol)

    #inMesh should become "inMeshes"
    #initial selection should ba able to be considered "split" (on different meshes, or on different places of the same mesh)

    lenMeshes = 1

    nodes = []
    #We'll take PyNodes or strings
    if isinstance(inMesh, list):
        lenMeshes = len(inMesh)
        for mesh in inMesh:
            nodes.append(pc.Pynode(mesh) if isinstance(mesh, basestring) else mesh)
    else:
        nodes.append(pc.Pynode(inMesh) if isinstance(inMesh, basestring) else inMesh)

    node = nodes[0]

    numVertices = node.numVertices()

    maxIter = max(MINITER, numVertices * MAXITERRATIO) 

    if VERBOSE:
        print "{0} have {1} vertices, topology parsing should be complete in max {2} iterations...".format(node.name(), numVertices, maxIter)

    if pc.control("symProgressBar", exists=True):
        pc.control("symProgressBar", edit=True, visible=True)
        gMainProgressBar = "symProgressBar"
    else:
        gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

    pc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Parsing topology",
    maxValue=numVertices)

    isSplit = inCenterIDs != None and isinstance(inCenterIDs[0], list)

    if isSplit:
        if VERBOSE:
            print "Working split with {0}({1}) and {2}({3})".format(nodes[0], inCenterIDs[0], nodes[1], inCenterIDs[1])

    #TABLE : -2 = Not managed, -1 = Managed (not matched yet or know asymmetrical), i=i = Center, i>=0 = Symmetric
    TABLE = []
    locTable = []

    for nodeItem in nodes:
        symMap = tkc.getPerPointData(nodeItem, inName=SYMMAP)
        TABLE.extend(symMap if symMap != None else [-2 for i in range(numVertices)])
        locMap = tkc.getPerPointData(nodeItem, inName=LOCMAP)
        locTable.extend(locMap if locMap != None else [-2 for i in range(numVertices)])

    managedCount = 0

    #First arrange Positive|Center|Negative vertices by position
    centerIds = []
    posIds = []
    negIds = []

    vertsInfos = []

    for nodeItem in nodes:
        vertInfo = {}
        points = nodeItem.getPoints()

        for i in range(numVertices):
            pos = points[i]
            idx = i
            vertInfo[idx] = (nodeItem.vtx[i], pos)

            if inCenterIDs == None:#strict position based strategy only
                if pos[0] > inCenterTol:
                    posIds.append(idx)
                    #posInfo[idx] = (vertex, pos)
                elif pos[0] < -inCenterTol:
                    negIds.append(idx)
                    #negInfo[idx] = (vertex, pos)
                else:
                    centerIds.append(idx)
                    #centerInfo[idx] = (vertex, pos)
                    TABLE[idx] = idx
        vertsInfos.append(vertInfo)

    if VERBOSE and inCenterIDs == None:
        print "strict position based strategy"
        print "centerIds",centerIds
        print "posIds",posIds
        print "negIds",negIds

    if not isSplit:
        if inCenterIDs != None:
            centerIds = inCenterIDs

            for centerID in centerIds:
                TABLE[centerID] = centerID

            if VERBOSE:
                print "most offseted based strategy"
                print "nb Center points", len(centerIds)
                print "centerIds",centerIds

    managedCount += len(centerIds)
    pc.progressBar(gMainProgressBar, edit=True, step=len(centerIds))

    if pc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        pc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        pc.warning("GetTable cancelled !")
        return None

    posWave = []
    negWave = []

    if isSplit:
        for i in range(len(inCenterIDs[0])):
            TABLE[inCenterIDs[0][i]] = inCenterIDs[1][i]
            TABLE[inCenterIDs[1][i] + numVertices] = inCenterIDs[0][i]
            locTable[inCenterIDs[0][i]] = 1
            locTable[inCenterIDs[1][i] + numVertices] = -1

        posWave = inCenterIDs[0]
        negWave = inCenterIDs[1]
    else:
        nodes.append(nodes[0])
        vertsInfos.append(vertsInfos[0])

        #Loop over center vertices and build first positive and negative "waves"
        for centerID in centerIds:
            locTable[centerID] = 0
            centerVert, centerPos = vertsInfos[0][centerID]

            #t0 = time.clock()
            connecteds = centerVert.connectedVertices()
            #t1 = time.clock()
            #print "getting", centerID, "connected Vertices took", (t1-t0) * 1000, "ms"

            curPosWave = []
            curNegWave = []

            offsetsList = []

            for connected in connecteds:
                idx = connected.indices()[0]
                if TABLE[idx] > -2:#centered, already sym or know assymmetrical
                    continue
                if inCenterIDs == None: #strict position based strategy
                    if idx in posIds:
                        curPosWave.append(idx)
                        locTable[idx] = 1
                    else:
                        curNegWave.append(idx)
                        locTable[idx] = -1
                else:                   #most offseted based strategy, will need post process
                    offset = centerPos - vertsInfos[0][idx][1]
                    offsetsList.append((offset[0], idx))

            if inCenterIDs != None:
                offsetsList.sort(key=lambda x: x[0])

                for i in range(len(offsetsList)):
                    #print i / (len(offsetsList)/2.0)
                    if i / (len(offsetsList)/2.0) < 1:
                        curPosWave.append(offsetsList[i][1])
                        locTable[offsetsList[i][1]] = 1
                    else:
                        curNegWave.append(offsetsList[i][1])
                        locTable[offsetsList[i][1]] = -1

            if len(curPosWave) != len(curNegWave):
                vertIDs = curPosWave[:]
                vertIDs.extend(curNegWave)
                verts = [node.vtx[i] for i in vertIDs]
                pc.select(verts)

                writeMaps(nodes, TABLE, locTable, numVertices)

                pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

                if gMainProgressBar == "symProgressBar":
                    pc.control("symProgressBar", edit=True, visible=False)

                pc.error("Topology not symmetrical around vertex {0} !".format(centerID))

            if len(curPosWave) > 0:
                if not sortCurWaves(centerID, curPosWave, centerID, curNegWave, vertsInfos[0], vertsInfos[1]):
                    pc.warning("Vertices around vertex {0} have not been paired, it would have taken too long and used too much memory (too much connected vertices : more than {1} for a reasonnable maximum of {2}), there's a chance you're topology is symmetrical but will not be considered so  !".format(centerID, 2 * len(curPosWave), 2 * MAXWAVELENGTH))
                else:
                    posWave.extend(curPosWave)
                    negWave.extend(curNegWave)

            if pc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
                pc.progressBar(gMainProgressBar, edit=True, endProgress=True)
                pc.warning("GetTable cancelled !")
                return None

    managedCount += len(posWave) + len(negWave)
    pc.progressBar(gMainProgressBar, edit=True, step=len(posWave) + len(negWave))

    if VERBOSE:
        print "posWave",posWave
        print "negWave",negWave
        print "Wave 1 reached"
        print "Nodes",nodes

    if inShowWavesTime > 0:
        verts = []
        verts.extend([nodes[0].vtx[i] for i in posWave])
        verts.extend([nodes[1].vtx[i] for i in negWave])
        pc.select(verts)
        pc.refresh()
        time.sleep(inShowWavesTime)

    count = 0
    while len(posWave) + len(negWave) > 0:
        if count >= maxIter:
            print "maxIter reached : ", count, " iterations !!"
            break

        posNextWave = []
        negNextWave = []

        for i in range(len(posWave)):
            posVert, posPos = vertsInfos[0][posWave[i]]
            negVert, negPos = vertsInfos[1][negWave[i]]

            curPosWave = []
            curNegWave = []

            connecteds = posVert.connectedVertices()
            for connected in connecteds:
                idx = connected.indices()[0]
                if TABLE[idx] > -2:#centered, already sym or know assymmetrical
                    continue
                curPosWave.append(idx)
                locTable[idx] = 1

            connecteds = negVert.connectedVertices()
            for connected in connecteds:
                idx = connected.indices()[0]
                if TABLE[idx+(numVertices * (lenMeshes-1))] > -2:#centered, already sym or know assymmetrical
                    continue
                curNegWave.append(idx)
                locTable[idx+(numVertices * (lenMeshes-1))] = -1

            if len(curPosWave) != len(curNegWave):
                verts = [nodes[0].vtx[j] for j in curPosWave]
                verts.extend([nodes[1].vtx[j] for j in curNegWave])
                pc.select(verts)

                writeMaps(nodes, TABLE, locTable, numVertices)

                pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

                if gMainProgressBar == "symProgressBar":
                    pc.control("symProgressBar", edit=True, visible=False)

                pc.error("Topology not symmetrical around vertices {0}, {1} !".format(posWave[i], negWave[i]))

            if len(curPosWave) > 0:
                if not sortCurWaves(posWave[i], curPosWave, negWave[i], curNegWave, vertsInfos[0], vertsInfos[1]):
                    pc.warning("Vertices around vertex {0} have not been paired, it would have taken too long and used too much memory (too much connected vertices : more than {1} for a reasonnable maximum of {2}), there's a chance you're topology is symmetrical but will not be considered so !".format(posWave[i], len(curPosWave), MAXWAVELENGTH))
                else:
                    posNextWave.extend(curPosWave)
                    negNextWave.extend(curNegWave)

        posWave = posNextWave[:]
        negWave = negNextWave[:]

        if inShowWavesTime > 0:
            verts = []
            verts.extend([nodes[0].vtx[i] for i in posWave])
            verts.extend([nodes[1].vtx[i] for i in negWave])
            pc.select(verts)
            pc.refresh()
            time.sleep(inShowWavesTime)

        managedCount += len(posWave) + len(negWave)

        if pc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
            pc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            pc.warning("GetTable cancelled !")
            return None

        pc.progressBar(gMainProgressBar, edit=True, step=len(posWave) + len(negWave))
    
        #Count number of iterations to spot for endless parsing (which should never happen...)
        count += 1

        if VERBOSE:
            print "Wave {0} reached".format(count+1)

    if VERBOSE:
        print "TABLE",TABLE

    pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    if gMainProgressBar == "symProgressBar":
        pc.control("symProgressBar", edit=True, visible=False)
        
    print "Successfully parsed {0} in {1} iterations.".format(node.name(), count+1)

    #Store symMap on mesh
    writeMaps(nodes, TABLE, locTable, numVertices)

    return TABLE

def guessCenter(inMesh, inAxis=0, inCenterTol=CENTERTOL):
    centerIds = []
    #We'll take a PyNode or a string
    node = pc.Pynode(inMesh) if isinstance(inMesh, basestring) else inMesh

    points = node.getPoints()

    for i in range(len(points)):
        pos = points[i]
        if pos[inAxis] < inCenterTol and pos[inAxis] > -inCenterTol:
            centerIds.append(i)

    return centerIds

def getCenter():
    obj = pc.textField("symMeshLE", query=True, text=True)
    node = pc.PyNode(obj) if pc.objExists(obj) else None

    if node == None:
        pc.warning("Can't get mesh from '{0}'".format(obj))
        return []

    symMap = tkc.getPerPointData(inMeshT, inName=SYMMAP)

    if symMap == None:
        pc.warning("Can't get symMap on mesh '{0}'".format(obj))
        return []

    centerIds = []

    for curId in range(len(symMap)):
        if symMap[curId] == curId:
            centerIds.append(curId)

    return centerIds

"""
def getOpposite():
    curVert = pc.selected()[0]
    curIdx = curVert.indices()[0]
    if TABLE[curIdx] < 0:
        return None
    if TABLE[curIdx] == curIdx:#center loop point
        return curVert
    else:
        return curVert.node().vtx[TABLE[curIdx]]
"""

def getSelectedIndices(node=None):
    vertSel = pc.ls(orderedSelection=True)
    if node == None:
        node = vertSel[0].node()
    else:
        if node.type() == "transform":
            node = node.getShape()

    selIndices = []

    for curVertSel in vertSel:
        if curVertSel.node() == node:
            for curIdx in curVertSel.indices():
                selIndices.append(curIdx)

    return (node, selIndices)

def selectVertices(inMeshName, inIndicesList):
    if len(inIndicesList) == 0:
        mc.select(clear=True)
        return

    selList = []
    for i in inIndicesList:
        selList.append(inMeshName+".vtx["+str(i)+"]")
    mc.select(*selList)

def symSelection(inAdd=False, inKeepCenter=True):
    mesh, indices = getSelectedIndices()

    otherMesh = None

    for selObj in pc.selected():
        if not isinstance(selObj, pc.general.MeshVertex) and selObj.type() == "transform" and selObj != mesh:
            otherMesh = selObj
            break

    if mesh == None:
        pc.warning("Please select some vertices on a mesh with a SymMap built")
        return

    obj = mesh.getParent()

    symMap = tkc.getPerPointData(obj, inName=SYMMAP)

    if symMap == None:
        pc.warning("Can't get symMap on mesh '{0}'".format(obj))
        return []

    newIndices = [] if (otherMesh != None or not inAdd) else indices[:]

    for index in indices:
        if symMap[index] >= 0 and (otherMesh != None or inKeepCenter or symMap[index] != index):
            newIndices.append(symMap[index])

    selectVertices(mesh.name() if otherMesh == None else otherMesh.name(), newIndices)

"""
    STARTEGIES = 1:Pos To neg, 2:Neg To ^=pos, 3:Average, 4:Swap
"""
strategiesTexts = { "Pos to neg":1,
                    "Neg to pos":2,
                    "Average":3,
                    "Swap":4}
strategiesLocs = [None, -1, 1]
def symMesh(inMeshName, inIndicesList=None, strategy=1, affectCenter=True):
    inMeshes = inMeshName.split(",")

    nodes = [pc.PyNode(n) for n in inMeshes]
    node = nodes[0]
    otherNode = nodes[-1]

    symMap = tkc.getPerPointData(node, inName=SYMMAP)
    locMap = None

    if symMap == None:
        pc.warning("Can't get symMap on mesh '{0}'".format(node))
        return

    if strategy < 3:
        locMap = tkc.getPerPointData(node, inName=LOCMAP)
        if locMap == None:
            pc.warning("Can't get locMap on mesh '{0}'".format(node))
            return

    origMap = tkc.getPerPointData(otherNode, inName=tkc.BASEMAP)
    if origMap == None:
        tkc.createBaseMap(otherNode)

    points = node.getPoints()
    otherPoints = otherNode.getPoints() if otherNode != node else points
    newPoints = [pc.datatypes.Vector(p[0], p[1], p[2]) for p in otherPoints]

    if otherNode != node:
        for i in range(len(symMap)):
            if symMap[i] >= 0:
                newPoints[symMap[i]] = points[i]
    else:
        if inIndicesList == None:#Sym whole mesh using strategy
            #todo Strategy !!!
            for i in range(len(symMap)):
                if symMap[i] == i and affectCenter:
                    if strategy == 3: #Average
                        newPoints[i][0] = 0.0 #todo AXIS, todo Average ?
                    else:
                        newPoints[i][0] = 0.0 #todo AXIS
                elif symMap[i] >= 0:
                    if strategy < 3: #todo AXIS Pos To Neg 
                        if locMap[i] == strategiesLocs[strategy]:
                            newPoints[i] = points[symMap[i]]
                            newPoints[i][0] *= -1
                    if strategy == 3: #todo AXIS Average
                        newPoints[i][0] = (newPoints[i][0] - newPoints[symMap[i]][0]) / 2.0
                        newPoints[symMap[i]][0] = -newPoints[i][0]

                        newPoints[i][1] = newPoints[symMap[i]][1] = (newPoints[i][1] + newPoints[symMap[i]][1]) / 2.0
                        newPoints[i][2] = newPoints[symMap[i]][2] = (newPoints[i][2] + newPoints[symMap[i]][2]) / 2.0

                    elif strategy == 4: #Swap
                        newPoints[i] = points[symMap[i]]
                        newPoints[i][0] *= -1 #todo AXIS !!!

        else:#Sym selected vertices
            for curIdx in inIndicesList: 
                pos = points[curIdx]
                if symMap[curIdx] < 0:
                    #print "curIdx", curIdx, "NO MATCH"
                    continue

                if symMap[curIdx] == curIdx and affectCenter:#center loop point
                    newPoints[curIdx][0] = 0.0 #todo AXIS !!!
                    #print "curIdx", curIdx, "CENTER MATCH"
                elif symMap[curIdx] >= 0:#symmetric point:
                    newPoints[symMap[curIdx]] = points[curIdx]
                    newPoints[symMap[curIdx]][0] *= -1 #todo AXIS !!!
                else:
                    pc.warning("Cannot symmetrize index {0}".format(curIdx))

    otherNode.setPoints(newPoints)
    otherNode.updateSurface()

def getAxis():
    val = pc.optionMenu("symAxisDD", query=True, value=True)

    return 0 if val == "X" else (1 if val == "Y" else 2)

def getTolerance():
    val = pc.textField("symTolLE", query=True, text=True)
    try:
        return float(val)
    except:
        print val

    return None

def resetMapOnSelection():
    selMesh, selIndices = getSelectedIndices()
    selMesh = selMesh.getParent()
    
    symMap = tkc.getPerPointData(selMesh, inName=SYMMAP)
    locMap = tkc.getPerPointData(selMesh, inName=LOCMAP)
    for selIndex in selIndices:
        symMap[selIndex] = -2
        locMap[selIndex] = -2

    prop = tkc.getProperty(selMesh, SYMMAP)
    pc.setAttr(prop.name() + ".data", symMap)
    
    prop = tkc.getProperty(selMesh, LOCMAP)
    pc.setAttr(prop.name() + ".data", locMap)

def symCheckClick(*args):
    tkc.storeSelection()

    objs = pc.textField("symMeshLE", query=True, text=True)
    nodes = []
    for obj in objs.split(","):
        if pc.objExists(obj):
            nodes.append(pc.PyNode(obj))

    sel = pc.ls(orderedSelection=True)
    if len(nodes) == 0 and len(sel) == 0:
        pc.warning("Please select a mesh or all the center vertices of a mesh")
        return

    showWaves = pc.checkBox("symShowwCB", query=True, value=True)

    axis = getAxis()
    if axis == None:
        pc.warning("Can't get axis value !")
        return

    table = []
    if isinstance(sel[0], pc.general.MeshVertex):
        if len(nodes) > 1:
            indices=[]
            for sel in nodes:
                node, selected = getSelectedIndices(sel)
                #print "node",node
                #print "selected", selected
                indices.append(selected)

            table = getTable(nodes, indices, inAxis=axis, inShowWavesTime=WAVETIME if showWaves else 0)
        else:
            node, selected = getSelectedIndices()
            table = getTable(nodes[0], selected, inAxis=axis, inShowWavesTime=WAVETIME if showWaves else 0)
    else:
        tol = getTolerance()
        if tol == None:
            pc.warning("Can't get tolerance value !")
            return

        table = getTable(nodes[0], inAxis=axis, inShowWavesTime=WAVETIME if showWaves else 0, inCenterTol=tol)

    tkc.loadSelection()

    initUI()

def symSelCenterClick(*args):
    obj = pc.textField("symMeshLE", query=True, text=True)
    node = pc.PyNode(obj) if pc.objExists(obj) else None

    sel = pc.ls(orderedSelection=True)
    if node == None and len(sel) == 0:
        pc.warning("Please select a mesh")
        return

    if isinstance(sel[0], pc.general.MeshVertex):
        node = sel[0].node()

    axis = getAxis()
    if axis == None:
        pc.warning("Can't get axis value !")
        return

    tol = getTolerance()
    if tol == None:
        pc.warning("Can't get tolerance value !")
        return

    indices = guessCenter(node, axis, tol)

    selectVertices(node.name(), indices)


def symSymMeshBTClick(*args):
    indices = None

    sel = pc.ls(orderedSelection=True)
    if len(sel) > 0 and isinstance(sel[0], pc.general.MeshVertex):
        mesh, indices = getSelectedIndices()

    name = pc.textField("symMeshLE", query=True, text=True)
    affectCenter = pc.checkBox("symAffectCenterCB", query=True, value=True)
    
    strategy = 1
    strategyText = pc.optionMenu("symRuleDD", query=True, value=True)

    print "strategyText",strategyText
    if strategyText in strategiesTexts:
        strategy=strategiesTexts[strategyText]
    
        symMesh(name, indices, strategy, affectCenter)
    else:
        pc.warning('Unknown symmetry strategy : "{0}", valid values are {1}'.format(strategyText, ",".join('"{0}"'.format(s) for s in strategiesTexts.keys())))

def symSymSelBTClick(*args):
    sel = pc.ls(orderedSelection=True)
    if len(sel) == 0 or not isinstance(sel[0], pc.general.MeshVertex):
        pc.warning("Please select  some vertices")
        return

    symSelection(pc.checkBox("symAddSelCB", query=True, value=True))

def symVerboseChanged(*args):
    global VERBOSE
    VERBOSE = pc.checkBox("symVerboseCB", query=True, value=True)

def symSelRealLeftClick(*args):
    obj = pc.textField("symMeshLE", query=True, text=True)
    node = pc.PyNode(obj) if pc.objExists(obj) else None

    locMap = tkc.getPerPointData(node, inName=LOCMAP)
    if locMap == None:
        pc.warning("Can't get symMap on mesh '{0}'".format(obj))
        return

    indices = []
    for i in range(len(locMap)):
        if locMap[i] == 1:
            indices.append(i)

    selectVertices(node.name(), indices)

def symSelRealCenterClick(*args):
    obj = pc.textField("symMeshLE", query=True, text=True)
    node = pc.PyNode(obj) if pc.objExists(obj) else None

    locMap = tkc.getPerPointData(node, inName=LOCMAP)
    if locMap == None:
        pc.warning("Can't get symMap on mesh '{0}'".format(obj))
        return

    indices = []
    for i in range(len(locMap)):
        if locMap[i] == 0:
            indices.append(i)

    selectVertices(node.name(), indices)

def symSelRealRightClick(*args):
    obj = pc.textField("symMeshLE", query=True, text=True)
    node = pc.PyNode(obj) if pc.objExists(obj) else None

    locMap = tkc.getPerPointData(node, inName=LOCMAP)
    if locMap == None:
        pc.warning("Can't get symMap on mesh '{0}'".format(obj))
        return

    indices = []
    for i in range(len(locMap)):
        if locMap[i] == -1:
            indices.append(i)

    selectVertices(node.name(), indices)

def symResetBaseClick(*args):
    obj = pc.textField("symMeshLE", query=True, text=True)
    node = pc.PyNode(obj) if pc.objExists(obj) else None

    sel = pc.ls(orderedSelection=True)
    indices = None

    if len(sel) > 0 and isinstance(sel[0], pc.general.MeshVertex):
        mesh, indices = getSelectedIndices()

    baseMap = tkc.getPerPointData(node, inName=tkc.BASEMAP)
    if baseMap == None:
        pc.warning("Can't get baseMap on mesh '{0}'".format(obj))
        return

    if indices == None:#Reset whole mesh
        tkc.resetMeshToBase(node)

    else:#Reset selected vertices
        points = node.getPoints()
    
        for i in indices:
            points[i] = baseMap[i]

        node.setPoints(points)
        node.updateSurface()

def connectControls():
    pc.button("symCheckBT", edit=True, c=symCheckClick)
    pc.button("symSelCenterBT", edit=True, c=symSelCenterClick)
    pc.button("symSymSelBT", edit=True, c=symSymSelBTClick)
    pc.button("symSymMeshBT", edit=True, c=symSymMeshBTClick)

    pc.button("symSelRealRightBT", edit=True, c=symSelRealRightClick)
    pc.button("symSelRealCenterBT", edit=True, c=symSelRealCenterClick)
    pc.button("symSelRealLeftBT", edit=True, c=symSelRealLeftClick)
    pc.checkBox("symVerboseCB", edit=True, cc=symVerboseChanged)

    pc.button("symResetBaseBT", edit=True, c=symResetBaseClick)

    pc.textField("symMeshLE", edit=True, cc=initUI)
    pc.checkBox("symUseSelCB", edit=True, cc=initUI)

def selectionChanged():
    if VERBOSE:
        print "selectionChanged !"

    initUI()

def uiDeleted():
    if VERBOSE:
        print "uiDeleted !"

    if OLDPREF != None and OLDPREF != pc.selectPref(query=True, trackSelectionOrder=True):
        pc.selectPref(trackSelectionOrder=OLDPREF)

    killScriptJobs()

    """ It seems that 'uideleted' scriptJobs delete themselves...
    if UIJOBID != None:
        pc.mel.evalDeferred("scriptJob -kill " + str(UIJOBID))
        UIJOBID = None
    """

def killScriptJobs():
    global JOBID

    if JOBID != None:
        pc.mel.evalDeferred("scriptJob -kill " + str(JOBID))
        JOBID = None

def initUI(*args):
    global JOBID
    global TABLE
    global OLDPREF

    if not pc.window('tkSymUI', q=True, exists=True):
        pc.warning("UI cannot be found !")
        uiDeleted()
        return

    useSel = pc.checkBox("symUseSelCB", query=True, value=True)

    pc.control("symMeshLE", edit=True, enable=not useSel)

    aObjs = []
    obj = ""
    objs = ""
    TABLE = None

    if useSel:
        if JOBID == None:
            #register selChanged
            JOBID = pc.scriptJob(event=["SelectionChanged", selectionChanged])
            OLDPREF = pc.selectPref(query=True, trackSelectionOrder=True)

        if not pc.selectPref(query=True, trackSelectionOrder=True):
            pc.selectPref(trackSelectionOrder=True)
        selected = pc.ls(orderedSelection=True)

        for sel in selected:
            if isinstance(sel, pc.general.MeshVertex):
                if not sel.node().getParent().name() in aObjs:
                    aObjs.append(sel.node().getParent().name())
            elif sel.type() == "transform":
                if sel.getShape() != None and sel.getShape().type() == "mesh":
                    aObjs.append(sel.name())
            elif sel.type() == "mesh":
                aObjs.append(sel.getParent().name())

        objs = ",".join(aObjs)

        pc.textField("symMeshLE", edit=True, text=objs)
    else:
        objs = pc.textField("symMeshLE", query=True, text=True)
        #kill selChanged
        killScriptJobs()

    obj = "" if len(aObjs) == 0 else aObjs[0]

    if obj == "" or not pc.objExists(obj) or pc.PyNode(obj).getShape().type() != "mesh":
        pc.textField("symMapStatusLE", edit=True, text="No mesh given !")

        for ctrl in SYMCTRLS:
            pc.control(ctrl, edit=True, enable=False)
        for ctrl in MESHEXISTSCTRLS:
            pc.control(ctrl, edit=True, enable=False)
    else:
        for ctrl in MESHEXISTSCTRLS:
            pc.control(ctrl, edit=True, enable=True)

        #print "obj",obj
        TABLE = tkc.getPerPointData(pc.PyNode(obj), inName=SYMMAP)

        if TABLE != None:
            pc.textField("symMapStatusLE", edit=True, text="Symmetry map found")
            for ctrl in SYMCTRLS:
                pc.control(ctrl, edit=True, enable=True)
        else:
            pc.textField("symMapStatusLE", edit=True, text="No symmetry map, click 'Build' !")
            for ctrl in SYMCTRLS:
                pc.control(ctrl, edit=True, enable=False)

def showUI():
    global UIJOBID

    if (pc.window('tkSymUI', q=True, exists=True)):
        pc.deleteUI('tkSymUI')

    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = pc.loadUI(uiFile=os.path.join(dirname, "UI", "tkSym.ui"))
    pc.showWindow(ui)

    UIJOBID = pc.scriptJob(uid=["tkSymUI", uiDeleted])

    connectControls()

    initUI()

    pc.control("symProgressBar", edit=True, visible=False)