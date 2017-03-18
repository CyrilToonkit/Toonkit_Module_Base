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
    Principal Skinner
    Basic skinning tools

import tkSkinner
reload(tkSkinner)
tkSkinner.showUI()
"""
import os
from functools import partial
import math

import pymel.core as pc 
import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim

import tkMayaCore as tkc
import tkWeightsFilters

__author__ = "Cyril GIBAUD - Toonkit"

MIN_SEL_PROGRESS = 200

SORTRADIOS = ["tkSkinSortDefault", "tkSkinSortByValueRadio", "tkSkinSortByProximityRadio", "tkSkinSortAlphaRadio"]
MODERADIOS = ["tkSkinTypeReplaceRadio", "tkSkinTypeAddRadio", "tkSkinTypeAddpcRadio", "tkSkinTypeScaleRadio"]


SLIDER_DRAGGING = False

SEL = {"comps":[], "infs":[]}

#sortInfs : 0 default, 1 by value, 2 by proximity, 3 Alphabetically
#mode : 0 set, 1 add, 2 addPercent, 3 scale
UI = {"debug":False,"infs":[], "selInfs":[], "showNear":True, "showZero":False, "sortInfs":1, "normalize":True, "useLocks":False, "mode":0}

INFOS = {}
VERTINFOS = {}
OPACITIES = {}

STOREDWEIGHTS = None

def getSoftSelection (opacityMult=1.0):
    if UI["debug"]:
        tkc.startTimer("getSoftSelection", inReset=True)
    allDags, allComps, allOpacities = [], [], []

    # if soft select isn't on, return
    if not mc.softSelect(q=True, sse=True):
        if UI["debug"]:
            tkc.stopTimer("getSoftSelection", inLog=True)
        return allDags, allComps, allOpacities
        
    richSel = OpenMaya.MRichSelection()
    try:
        # get currently active soft selection
        OpenMaya.MGlobal.getRichSelection(richSel)
    except:
        if UI["debug"]:
            tkc.stopTimer("getSoftSelection", inLog=False)
        raise Exception('Error getting soft selection.')

    richSelList = OpenMaya.MSelectionList()
    richSel.getSelection(richSelList)
    selCount = richSelList.length()

    for x in xrange(selCount):
        shapeDag = OpenMaya.MDagPath()
        shapeComp = OpenMaya.MObject()
        try:
            richSelList.getDagPath(x, shapeDag, shapeComp)
        except RuntimeError:
            # nodes like multiplyDivides will error
            continue
        
        compOpacities = {}
        compFn = OpenMaya.MFnSingleIndexedComponent(shapeComp)
        try:
            # get the secret hidden opacity value for each component (vert, cv, etc)
            for i in xrange(compFn.elementCount()):
                weight = compFn.weight(i)
                compOpacities[compFn.element(i)] = weight.influence() * opacityMult
        except Exception, e:
            print e.__str__()
            print 'Soft selection appears invalid, skipping for shape "%s".' % shapeDag.partialPathName()

        allDags.append(shapeDag)
        allComps.append(shapeComp)
        allOpacities.append(compOpacities)
        
    if UI["debug"]:
        tkc.stopTimer("getSoftSelection", inLog=True)

    return allDags, allComps, allOpacities

def getBindPoseTranslation(skin, joint):
    return list(tkc.getRefPose(joint, skin)[3][:3])

def computeDist(posList1, posList2):
    return math.sqrt(pow(posList2[0] - posList1[0], 2) + pow(posList2[1] - posList1[1], 2) + pow(posList2[2] - posList1[2], 2))

def unlockJoints(inJoints):
    locked=False
    unlocked = []
    for jointObj in inJoints:
        if jointObj.lockInfluenceWeights.get() and jointObj.lockInfluenceWeights.get(settable=True):
            jointObj.lockInfluenceWeights.set(False)
            unlocked.append(jointObj.name())
            locked=True
    if locked:
        pc.warning("Joints have been unlocked ({0})".format(unlocked))

def getSkinInfo(inObjects=None):
    global INFOS
    global VERTINFOS
    global SEL
    global OPACITIES    

    timers = {}
    if UI["debug"]:
        print "getSkinInfo called !"
        tkc.startTimer("getSkinInfo", inReset=True)

    if inObjects != None:
        SEL["comps"] = []
        SEL["infs"] = []

        if len(inObjects) > 0:
            allDags, allComps, allOpacities = getSoftSelection()
            if len(allOpacities) > 0:
                for dagIndex in range(len(allOpacities)):
                    node = pc.PyNode(allDags[dagIndex].partialPathName())
                    for index, value in allOpacities[dagIndex].iteritems():
                        rawSelObj = node.vtx[index]
                        SEL["comps"].append(rawSelObj)
                        OPACITIES[rawSelObj] = value
            else:
                components = tkc.expandCompIndices(inObjects)
                for comp in components:
                    SEL["comps"].append(comp)
                    OPACITIES[comp] = 1.0

            #Filter inputs
            for rawSelObj in inObjects:
                if isinstance(rawSelObj, pc.nodetypes.Joint):
                    SEL["infs"].append(rawSelObj)

    if len(SEL["comps"]) == 0:
        if UI["debug"]:
            elapsed = tkc.stopTimer("getSkinInfo")
            print "getSkinInfo took {0:.5f} s (no points selected)".format(elapsed)
            for timer, elapsed in timers.iteritems():
                tkc.stopTimer(timer, inReset=True)

        progressEnd()
        return

    #Build/retrieve dictionaries
    lenComps = len(SEL["comps"])
    if lenComps > MIN_SEL_PROGRESS:
        progressStart(len(SEL["comps"]), "Caching verts infos")
    for selComp in SEL["comps"]:
        if not selComp in VERTINFOS or not "bind" in VERTINFOS[selComp] or not VERTINFOS[selComp]["geo"] in INFOS or "obsolete" in INFOS[VERTINFOS[selComp]["geo"]] or not VERTINFOS[selComp]["geo"].exists() or not VERTINFOS[selComp]["skin"].exists():
            node = selComp.node()
            if not node in INFOS or "obsolete" in INFOS[node] or not INFOS[node]["geo"].exists() or not INFOS[node]["skin"].exists():
                if UI["debug"]:
                    timerName = "getNodeInfo : " + node.name()
                    if not timerName in timers:
                        timers[timerName]=0.0
                    tkc.startTimer(timerName)
                INFOS[node] = {}

                INFOS[node]["geo"] = node
                INFOS[node]["skin"] = tkc.getSkinCluster(node)

                if INFOS[node]["skin"] == None:
                    pc.warning("No skinCluster found on \"{0}\" !".format(node.name()))
                
                INFOS[node]["georig"] = pc.listHistory(INFOS[node]["skin"], type="mesh")[0]

                INFOS[node]["infs"] = INFOS[node]["skin"].influenceObjects()

                if not UI["useLocks"]:
                    unlockJoints(INFOS[node]["infs"])

                #Get bind poses
                INFOS[node]["bind"] = [tkc.getRefPose(inf, INFOS[node]["skin"])[3][:3] for inf in INFOS[node]["infs"]]

                if UI["debug"]:
                    timerName = "getNodeInfo : " + node.name()
                    timers[timerName] = tkc.stopTimer(timerName, False)

            VERTINFOS[selComp] = INFOS[node].copy()
            VERTINFOS[selComp]["infsBind"] = {}

        #Update weights
        if UI["debug"]:
            timerName = "getWeigths"
            if not timerName in timers:
                timers[timerName]=0.0
            tkc.startTimer(timerName)

        VERTINFOS[selComp]["weights"] = pc.skinPercent(VERTINFOS[selComp]["skin"], selComp, query=True, value=True)

        if UI["debug"]:
            timerName = "getWeigths"
            timers[timerName] = tkc.stopTimer(timerName, False)
        
        if lenComps > MIN_SEL_PROGRESS:
            progressInc(1)

    #Get distances
    selComp = SEL["comps"][0]
    if UI["debug"]:
        print "getDistances called !"
        timerName = "getDistances"
        if not timerName in timers:
            timers[timerName]=0.0
        tkc.startTimer(timerName)

    pointPos=VERTINFOS[selComp]["georig"].vtx[selComp.indices()[0]].getPosition(space="world")
    for i in range(len(VERTINFOS[selComp]["infs"])):
        inf = VERTINFOS[selComp]["infs"][i]
        if not inf in VERTINFOS[selComp]["infsBind"]:
            VERTINFOS[selComp]["infsBind"][inf] = computeDist(pointPos, VERTINFOS[selComp]["bind"][i])

    VERTINFOS[selComp]["distances"] = [VERTINFOS[selComp]["infsBind"][inf] for inf in VERTINFOS[selComp]["infs"]]

    if UI["debug"]:
        timerName = "getDistances"
        timers[timerName] = tkc.stopTimer(timerName, False)

    if UI["debug"]:
        elapsed = tkc.stopTimer("getSkinInfo")
        lenComps = len(SEL["comps"])
        print "getSkinInfo took {0:.3f} s for {1} points ({2:.2f} ms / point)".format(elapsed, lenComps, (elapsed * 1000.0)/lenComps)
        
        for timer, elapsed in timers.iteritems():
            print "  - {0} took {1:.3f} s".format(timer, elapsed)
            tkc.stopTimer(timer, inReset=True)

    progressEnd()

def initSkinPaths():
    getSkinInfo()

    if len(SEL["comps"]) == 0:
        pc.warning("No vert selected !")
        return False

    info = VERTINFOS[SEL["comps"][0]]

    if len(info["selWeights"]) == 0:
        return

    if pc.objExists(info["geo"].name() + "_SkinPaths"):
        pc.delete(info["geo"].name() + "_SkinPaths")

    root = pc.group(empty=True, world=True, name=info["geo"].name() + "_SkinPaths")

    index = info["selComponents"][0].indices()[0]

    pointOrigin = pc.group(empty=True, parent=root, name=info["geo"].name() + "_SkinOrigin")

    exprString = "float $arrayOfFloats[]=`pointPosition {0}.vtx[{1}]`;{2}.translateX = $arrayOfFloats[0];{2}.translateY = $arrayOfFloats[1];{2}.translateZ = $arrayOfFloats[2];".format(info["geo"].name(),index, pointOrigin.name())
    pc.expression(string=exprString)

    for i in range(len(info["influences"])):
        if info["selWeights"][0][i] > 0.001:
            inf = info["influences"][i]
            infPeakParent = pc.group(empty=True, parent=root, name=inf.name() + "_SkinPathPeakParent")
            infPeakParent.translate.set(tkc.getBindPoseTranslation())
            infPeak = pc.group(empty=True, world=True, name=inf.name() + "_SkinPathPeak")
            infPeak.translate.set(info["georig"].vtx[index].getPosition())
            infPeakParent.addChild(infPeak)
            tkc.constrain(infPeakParent, inf, "Pose", False)

            distance = pc.createNode("distanceBetween", name=inf.name() + "_DB")
            pointOrigin.worldMatrix[0] >> distance.inMatrix1
            infPeak.worldMatrix[0] >> distance.inMatrix2

            crv = pc.curve( point=[(0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (-0.10000000149011599, 0.80000001192092896, 0.0), (0.10000000149011599, 0.80000001192092896, 0.0), (0.0, 1.0, 0.0), (0.0, 0.80000001192092896, 0.10000000149011599), (0.0, 0.80000001192092896, -0.10000000149011599), (0.0, 1.0, 0.0)], degree=1)
            crv.rename(inf.name() + "_SkinPath")
            pointOrigin.addChild(crv)
            crv.t.set([0,0,0])
            cns = tkc.constrain(crv, infPeak, "Direction", False)
            cns.aimVectorX.set(0.0)
            cns.aimVectorY.set(1.0)
            distance.distance >> crv.sx 
            distance.distance >> crv.sy 
            distance.distance >> crv.sz

def setWeigthsClick(divisions, weight, *args):
    if UI["debug"]:
        print "setWeigthsClick",divisions,weight
        print "mode",UI["mode"]

        tkc.startTimer("setWeigths", inReset=True)

    for vert in SEL["comps"]:
        #weights = STOREDWEIGHTS[vert] if STOREDWEIGHTS != None else VERTINFOS[vert]["weights"]
        weights = VERTINFOS[vert]["weights"]

        if UI["mode"] == 0:
            pc.skinPercent(VERTINFOS[vert]["skin"], vert, transformValue=[(selInf, weight * OPACITIES[vert]) for selInf in UI["selInfs"] if not UI["useLocks"] or not selInf.lockInfluenceWeights.get()], normalize=False)
        elif UI["mode"] == 1:
            pc.skinPercent(VERTINFOS[vert]["skin"], vert, transformValue=[(selInf, weights[VERTINFOS[vert]["infs"].index(selInf)] + weight * OPACITIES[vert]) for selInf in UI["selInfs"]  if not UI["useLocks"] or not selInf.lockInfluenceWeights.get()], normalize=False)
        elif UI["mode"] == 2:
            pc.skinPercent(VERTINFOS[vert]["skin"], vert, transformValue=[(selInf, weights[VERTINFOS[vert]["infs"].index(selInf)] + weight * weights[VERTINFOS[vert]["infs"].index(selInf)] * OPACITIES[vert]) for selInf in UI["selInfs"] if not UI["useLocks"] or not selInf.lockInfluenceWeights.get()], normalize=False)
        else:#UI["mode"] == 3
            pc.skinPercent(VERTINFOS[vert]["skin"], vert, transformValue=[(selInf, weights[VERTINFOS[vert]["infs"].index(selInf)] * weight * OPACITIES[vert]) for selInf in UI["selInfs"]  if not UI["useLocks"] or not selInf.lockInfluenceWeights.get()], normalize=False)

    if UI["normalize"]:
        pc.skinPercent(VERTINFOS[SEL["comps"][0]]["skin"], normalize=True)

    if UI["debug"]:
        tkc.stopTimer("setWeigths", inLog=True)

    if not SLIDER_DRAGGING: 
        getSkinInfo()   
        resfreshUIInfs()

def selectionChanged():
    if UI["debug"]:
        print "selChanged !"

    if not mc.window('tkSkinnerUI', q=True, exists=True):
        cleanUI()
    else:
        refreshUI()

def undoChanged():
    if UI["debug"]:
        print "undoChanged !"

    if not mc.window('tkSkinnerUI', q=True, exists=True):
        cleanUI()
    else:
        refreshUI()

def infDoubleClick(*args):
    if UI["debug"]:
        print "infDoubleClick !",pc.textScrollList("tkSkinInfsLB", query=True, selectIndexedItem=True)

    pc.select(UI["selInfs"], add=pc.getModifiers() == 1)

def smooth(*args):
    paint = tkWeightsFilters.weightsFiltersClass()
    for comp in SEL["comps"]:
        paint.setWeight(comp.indices()[0],OPACITIES[comp]*.25)

def smoothPaint(*args):
    tkWeightsFilters.smooth()

def sharpen(*args):
    paint = tkWeightsFilters.weightsFiltersClass("sharpen")
    for comp in SEL["comps"]:
        paint.setWeight(comp.indices()[0],OPACITIES[comp]*.25)

def sharpenPaint(*args):
    tkWeightsFilters.sharpen()

def harden(*args):
    paint = tkWeightsFilters.weightsFiltersClass("harden")
    for comp in SEL["comps"]:
        paint.setWeight(comp.indices()[0],OPACITIES[comp]*.25)

def hardenPaint(*args):
    tkWeightsFilters.harden()

def selectAllDefs(*args):
    if len(SEL["comps"]) > 0:
        tkc.selectDeformers([SEL["comps"][0].node().getParent()])
    else:
        tkc.selectDeformers()

def selectListDefs(*args):
    pc.select([inf[0] for inf in UI["infs"]])

def infSelChanged(*args):
    global UI

    if UI["debug"]:
        print "infsSelChanged !",pc.textScrollList("tkSkinInfsLB", query=True, selectIndexedItem=True)

    #Check if selection have really changed
    oldSel = [inf.name() for inf in UI["selInfs"]]
    UI["selInfs"] = [UI["infs"][i-1][0] for i in pc.textScrollList("tkSkinInfsLB", query=True, selectIndexedItem=True)]
    newSel = [inf.name() for inf in UI["selInfs"]]

    if oldSel != newSel:
        if len(UI["selInfs"]) > 0 and len(SEL["comps"]) > 0:
            hilited = UI["selInfs"][:]
            geo = VERTINFOS[SEL["comps"][0]]["geo"].getParent()
            hilited.append(geo)
            pc.hilite(hilited, replace=True)

            try:
                pc.mel.eval("doMenuComponentSelection(\""+geo+"\", \"vertex\");")
            except:
                pass
            finally:
                pc.mel.eval("doMenuComponentSelection(\""+geo+"\", \"vertex\");")

            if SEL["infs"] > 0:
                pc.select(SEL["infs"], add=True)

            if UI["mode"] == 0:
                pc.floatSliderGrp("tkSkinSlider", edit=True,v=VERTINFOS[SEL["comps"][0]]["weights"][VERTINFOS[SEL["comps"][0]]["infs"].index(UI["selInfs"][0])])
            elif UI["mode"] == 1:
                pc.floatSliderGrp("tkSkinSlider", edit=True,v=0.0)
            elif UI["mode"] == 2:
                pc.floatSliderGrp("tkSkinSlider", edit=True,v=1.0)
            else:
                pc.floatSliderGrp("tkSkinSlider", edit=True, v=1.0)

def normCBChanged(*args):
    global UI
    UI["normalize"] = pc.checkBox("tkSkinNormCB", query=True, value=True)

def locksCBChanged(*args):
    global UI
    UI["useLocks"] = pc.checkBox("tkSkinLocksCB", query=True, value=True)
    if not UI["useLocks"]:
        if len(SEL["comps"]) > 0:
            unlockJoints(VERTINFOS[SEL["comps"]]["infs"])

def showZeroCBChanged(*args):
    global UI
    UI["showZero"] = pc.checkBox("tkSkinShowZeroCB", query=True, value=True)

    resfreshUIInfs()

def showNearCBChanged(*args):
    global UI
    UI["showNear"] = pc.checkBox("tkSkinShowNearCB", query=True, value=True)

    resfreshUIInfs()

def modeChanged(*args):
    global UI

    UI["mode"] = 0
    if pc.radioButton("tkSkinTypeAddRadio", query=True, select=True):
        UI["mode"] = 1
        pc.floatSliderGrp("tkSkinSlider", edit=True, minValue=-1.0, maxValue=1.0)
    elif pc.radioButton("tkSkinTypeAddpcRadio", query=True, select=True):
        UI["mode"] = 2
        pc.floatSliderGrp("tkSkinSlider", edit=True, minValue=-1.0, maxValue=1.0)
    elif pc.radioButton("tkSkinTypeScaleRadio", query=True, select=True):
        UI["mode"] = 3
        pc.floatSliderGrp("tkSkinSlider", edit=True, minValue=0.0, maxValue=2.0)
    else:
        pc.floatSliderGrp("tkSkinSlider", edit=True, minValue=0.0, maxValue=1.0)

    infSelChanged()

def sortChanged(*args):
    global UI

    UI["sortInfs"] = 0
    if pc.radioButton("tkSkinSortByValueRadio", query=True, select=True):
        UI["sortInfs"] = 1
    elif pc.radioButton("tkSkinSortByProximityRadio", query=True, select=True):
        UI["sortInfs"] = 2
    elif pc.radioButton("tkSkinSortAlphaRadio", query=True, select=True):
        UI["sortInfs"] = 3

    resfreshUIInfs()

def endSliderDrag(*args):
    global SLIDER_DRAGGING
    global STOREDWEIGHTS

    if UI["debug"]:
        print "sliderDrag",pc.floatSliderGrp("tkSkinSlider", q=True, v=True )

    pc.undoInfo(closeChunk=True)

    SLIDER_DRAGGING = False
    STOREDWEIGHTS = None

    getSkinInfo()
    resfreshUIInfs()

def sliderDrag(*args):
    global SLIDER_DRAGGING
    global SLIDER_BASEVALUE
    global STOREDWEIGHTS

    val = pc.floatSliderGrp("tkSkinSlider", q=True, v=True )

    if not SLIDER_DRAGGING:
        pc.undoInfo(openChunk=True)

        #Store weights
        STOREDWEIGHTS = {}
        for vert in SEL["comps"]:
            STOREDWEIGHTS[vert] = VERTINFOS[vert]["weights"][:]

    SLIDER_DRAGGING = True

    if UI["debug"]:
        print "value",val

    setWeigthsClick(0, val)

def connectControls():
    pc.button("tkSkinThird0BT", edit=True, c=partial(setWeigthsClick, 3, 0.0))
    pc.button("tkSkinThird33BT", edit=True, c=partial(setWeigthsClick, 3, 0.33))
    pc.button("tkSkinThird66BT", edit=True, c=partial(setWeigthsClick, 3, 0.66))
    pc.button("tkSkinThird100BT", edit=True, c=partial(setWeigthsClick, 3, 1.0))

    pc.button("tkSkinQuart0BT", edit=True, c=partial(setWeigthsClick, 4, 0.0))
    pc.button("tkSkinQuart25BT", edit=True, c=partial(setWeigthsClick, 4, 0.25))
    pc.button("tkSkinQuart50BT", edit=True, c=partial(setWeigthsClick, 4, 0.50))
    pc.button("tkSkinQuart75BT", edit=True, c=partial(setWeigthsClick, 4, 0.75))
    pc.button("tkSkinQuart100BT", edit=True, c=partial(setWeigthsClick, 4, 1.0))

    pc.button("tkSkinTen0BT", edit=True, c=partial(setWeigthsClick, 10, 0.0))
    pc.button("tkSkinTen10BT", edit=True, c=partial(setWeigthsClick, 10, 0.1))
    pc.button("tkSkinTen20BT", edit=True, c=partial(setWeigthsClick, 10, 0.2))
    pc.button("tkSkinTen30BT", edit=True, c=partial(setWeigthsClick, 10, 0.3))
    pc.button("tkSkinTen40BT", edit=True, c=partial(setWeigthsClick, 10, 0.4))
    pc.button("tkSkinTen50BT", edit=True, c=partial(setWeigthsClick, 10, 0.5))
    pc.button("tkSkinTen60BT", edit=True, c=partial(setWeigthsClick, 10, 0.6))
    pc.button("tkSkinTen70BT", edit=True, c=partial(setWeigthsClick, 10, 0.7))
    pc.button("tkSkinTen80BT", edit=True, c=partial(setWeigthsClick, 10, 0.8))
    pc.button("tkSkinTen90BT", edit=True, c=partial(setWeigthsClick, 10, 0.9))
    pc.button("tkSkinTen100BT", edit=True, c=partial(setWeigthsClick, 10, 1.0))

    pc.button("tkSkinRefreshBT", edit=True, c=refreshSkin)

    pc.textScrollList("tkSkinInfsLB", edit=True, sc=infSelChanged, dcc=infDoubleClick)

    pc.checkBox("tkSkinNormCB", edit=True, cc=normCBChanged)
    pc.checkBox("tkSkinLocksCB", edit=True, cc=locksCBChanged)

    pc.checkBox("tkSkinShowZeroCB", edit=True, cc=showZeroCBChanged)
    pc.checkBox("tkSkinShowNearCB", edit=True, cc=showNearCBChanged)

    pc.radioButton("tkSkinSortDefault", edit=True, onc=sortChanged)
    pc.radioButton("tkSkinSortByValueRadio", edit=True, onc=sortChanged)
    pc.radioButton("tkSkinSortByProximityRadio", edit=True, onc=sortChanged)
    pc.radioButton("tkSkinSortAlphaRadio", edit=True, onc=sortChanged)

    pc.radioButton("tkSkinTypeReplaceRadio", edit=True, onc=modeChanged)
    pc.radioButton("tkSkinTypeAddRadio", edit=True, onc=modeChanged)
    pc.radioButton("tkSkinTypeAddpcRadio", edit=True, onc=modeChanged)
    pc.radioButton("tkSkinTypeScaleRadio", edit=True, onc=modeChanged)

    pc.button("tkSkinSelectAllDefsBT", edit=True, c=selectAllDefs)
    pc.button("tkSkinSelectListerDefsBT", edit=True, c=selectListDefs)

    pc.button("tkSkinSmoothBT", edit=True, c=smooth)
    pc.button("tkSkinSmoothPaintBT", edit=True, c=smoothPaint)

    pc.button("tkSkinSharpenBT", edit=True, c=sharpen)
    pc.button("tkSkinSharpenPaintBT", edit=True, c=sharpenPaint)

    pc.button("tkSkinHardenBT", edit=True, c=harden)
    pc.button("tkSkinHardenPaintBT", edit=True, c=hardenPaint)

def resfreshUIInfs(*args):
    global UI

    oldSel = UI["selInfs"]

    pc.textScrollList("tkSkinInfsLB", edit=True, removeAll=True)
    pc.textScrollList("tkSkinInfsWLB", edit=True, removeAll=True)
    pc.textScrollList("tkSkinInfsDLB", edit=True, removeAll=True)

    if len(SEL["comps"]) == 0:
        return

    info = VERTINFOS[SEL["comps"][0]]

    nInfs = len(info["infs"])
    UI["infs"] = []
    if nInfs > 0:
        infs = []

        for i in range(nInfs):
            weight = info["weights"][i]
            dist = info["distances"][i]
            infs.append((info["infs"][i], weight, dist))

        #filter
        filteredInfs = []
        droppedInfs = []
        for inf in infs:
            if UI["showZero"] or inf[1] > tkc.CONST_EPSILON:
                filteredInfs.append(inf)
            else:
                droppedInfs.append(inf)

        if len(filteredInfs) < 5 and UI["showNear"]:
            droppedInfs.sort(key=lambda inf: inf[2])
            for i in range(5 - len(filteredInfs)):
                if len(droppedInfs) > i:
                    filteredInfs.append(droppedInfs[i])

        if UI["sortInfs"] == 1:#By value
            filteredInfs.sort(key=lambda inf: -inf[1])
        elif UI["sortInfs"] == 2:#By proximity
            filteredInfs.sort(key=lambda inf: inf[2])
        elif UI["sortInfs"] == 3:#Alphabetically
            filteredInfs.sort(key=lambda inf: inf[0].name())

        UI["infs"] = filteredInfs

        infNames = ["{0}".format(inf[0].name()) for inf in filteredInfs]
        infWeights = ["{0:.3f}".format(inf[1]) for inf in filteredInfs]
        infDists = ["{0:.3f}".format(inf[2]) for inf in filteredInfs]

        height = 8 + len(infNames) * 13
        pc.textScrollList("tkSkinInfsLB", edit=True, append=infNames, height=height)
        pc.textScrollList("tkSkinInfsWLB", edit=True, append=infWeights, height=height)
        pc.textScrollList("tkSkinInfsDLB", edit=True, append=infDists, height=height)

        newSel = []
        for oldSelInf in oldSel:
            if oldSelInf.name() in infNames:
                newSel.append(oldSelInf.name())

        if len(newSel) > 0:
            pc.textScrollList("tkSkinInfsLB", edit=True, selectItem=newSel)

def refreshUI(*args):
    getSkinInfo(pc.selected())
    resfreshUIInfs()
    infSelChanged()

def refreshSkin(*args):
    global INFOS
    global VERTINFOS

    """
    if len(SEL["comps"]) > 0:
        node = SEL["comps"][0].node()
        if node in INFOS:
            if UI["debug"]:
                print "Deleting skin cache for node " + node.name()
            INFOS[node]["obsolete"] = True
    """
    INFOS = {}
    VERTINFOS = {}

    refreshUI()

def cleanUI(*args):
    global UI

    if UI["debug"]:
        print "cleaning UI"

    if (mc.window('tkSkinnerUI', q=True, exists=True)):
        mc.deleteUI('tkSkinnerUI')

    jobID = None
    if "selJob" in UI:
        jobID = UI["selJob"]
        pc.mel.evalDeferred("scriptJob -kill " + str(jobID))
        del UI["selJob"]
        if UI["debug"]:
            print "tkSkinner selJob killed (job {0})".format(jobID)

    jobID = None
    if "undoJob" in UI:
        jobID = UI["undoJob"]
        pc.mel.evalDeferred("scriptJob -kill " + str(jobID))
        del UI["undoJob"]
        if UI["debug"]:
            print "tkSkinner undoJob killed (job {0})".format(jobID)

    if "closeJob" in UI:
        #pc.mel.evalDeferred("scriptJob -kill " + str(UI["closeJob"]))
        del UI["closeJob"]

def progressStart(maxValue, status="",isInterruptable=False):
    if pc.control("skinProgressBar_2", exists=True):
        pc.control("skinProgressBar_2", edit=True, visible=True)
        gMainProgressBar = "skinProgressBar_2"
    else:
        gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

    pc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=isInterruptable,
    status=status,
    maxValue=maxValue)

def progressInc(step):
    if pc.control("skinProgressBar_2", exists=True):
        gMainProgressBar = "skinProgressBar_2"
    else:
        gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

    pc.progressBar(gMainProgressBar, edit=True, step=step)

def progressEnd():
    if pc.control("skinProgressBar_2", exists=True):
        pc.control("skinProgressBar_2", edit=True, visible=False)
        gMainProgressBar = "skinProgressBar_2"
    else:
        gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

    pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

def showUI(*args):
    global UI

    if (mc.window('tkSkinnerUI', q=True, exists=True)):
        mc.deleteUI('tkSkinnerUI')

    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = mc.loadUI(uiFile=dirname + "\\UI\\tkSkinner.ui")

    pc.showWindow(ui)

    #pc.window(ui, width=520)

    menuBarLayout = pc.menuBarLayout(parent=ui, width=500)
    slider = pc.floatSliderGrp("tkSkinSlider", pre=3,minValue=0, maxValue=1.0, fieldMinValue=-1.0, fieldMaxValue=2.0, field=True, v=0,dc=sliderDrag,cc=endSliderDrag)

    UI["closeJob"] = pc.scriptJob(uiDeleted=[ui, cleanUI])

    if not "selJob" in UI:
        UI["selJob"] = pc.scriptJob(event=["SelectionChanged", selectionChanged])
        if UI["debug"]:
            print "tkSkinner 'SelectionChanged' initialized (job {0})".format(UI["selJob"])

    if not "undoJob" in UI:
        UI["undoJob"] = pc.scriptJob(event=["Undo", undoChanged])
        if UI["debug"]:
            print "tkSkinner 'Undo' initialized (job {0})".format(UI["undoJob"])

    connectControls()

    #Init UI values
    pc.checkBox("tkSkinShowNearCB", edit=True, value=UI["showNear"])
    pc.checkBox("tkSkinShowZeroCB", edit=True, value=UI["showZero"])
    
    #Crashes maya
    #pc.radioButton(SORTRADIOS[UI["sortInfs"]], edit=True, select=True)
    #pc.radioButton(MODERADIOS[UI["mode"]], edit=True, select=True)

    pc.checkBox("tkSkinLocksCB", edit=True, value=UI["useLocks"])

    mc.control("skinProgressBar_2", edit=True, visible=False)

    refreshUI()