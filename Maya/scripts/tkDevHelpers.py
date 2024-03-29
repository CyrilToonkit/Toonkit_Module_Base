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
DevHelpers
"""
import math
import time
import re
import types
import os
import inspect
from functools import partial

import pymel.core as pc

import tkMayaCore as tkc
import tkSIGroups
import tkSpring
import tkRig

__author__ = "Cyril GIBAUD - Toonkit"

MODULES = [tkc, tkSIGroups, tkSpring, tkRig]

NODESNAMES = "defaultRenderGlobals, miDefaultOptions, mentalrayGlobals, miDefaultFramebuffer"
STOREDATTRIBUTES = {}
UNFOUNDNODES = []

FORBIDDENATTRS = ["publishedNodeInfo", "instObjGroups", "InstObjGroups", "renderLayerInfo"]

def get_default_args(func):
    """
    returns a dictionary of arg_name:default_values for the input function
    """
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if defaults != None and len(defaults) > 0:
        return dict(zip(reversed(args), reversed(defaults)))

    return {}

def getMethods():
    methods = {}

    for module in MODULES:
        objdir = dir(module)
        for key in objdir:
            func = module.__dict__.get(key)
            if isinstance(func, types.FunctionType):
                methods[module.__name__ + "." + func.__name__] = func

    return methods

def filterMethods(inStr="", inDocs=True):
    methods = getMethods()
    filteredMethods = {}

    regexes = []
    splitStr = inStr.split(",")

    for split in splitStr:
        if split != "" and split != "*" and split != ".":
            regexes.append(re.compile("^" + split.replace("*",".*") + "$", re.I))

    if len(regexes) > 0:
        for methodKey in methods.keys():
            methodName = methodKey.split(".")[1]
            for reg in regexes:
                if reg.search(methodName) or (inDocs and methods[methodKey].__doc__ != None and reg.search(str(methods[methodKey].__doc__).replace("\r", "").replace("\n", ""))):
                    filteredMethods[methodKey] = methods[methodKey]
                    break
    
    return filteredMethods

#################################################################################
#   monitorAttrChanges
#################################################################################

def getAttr(inInstance, inMethodName, inDefault="None"):
    if hasattr(inInstance,inMethodName):
        method = getattr(inInstance,inMethodName)
        if callable(method):
            return method()
    return inDefault

def objectInfo(*inArgs):
    sel = pc.ls(sl=True)

    if len(sel) > 0:
        obj = sel[0]
        print ("name : %s, type : %s, nodeType : %s, dagPath %s" % (obj.name(), obj.type(), obj.nodeType(), getAttr(obj, "fullPath")))

def storeAttrs(inAdd=False):
    global STOREDATTRIBUTES
    global UNFOUNDNODES

    UNFOUNDNODES = []
    if not inAdd:
        STOREDATTRIBUTES = {}

    splitNames = NODESNAMES.split(",")

    for splitName in splitNames:
        name = splitName.strip()
        if pc.objExists(name):
            lstAttrs = pc.listAttr(name, scalarAndArray=True)
            for attr in lstAttrs:
                valid=True
                for forbiddenAttr in FORBIDDENATTRS:
                    if forbiddenAttr in attr:
                        valid = False
                        break

                if valid:
                    STOREDATTRIBUTES[name +"."+ attr] = pc.getAttr(name +"."+ attr)
        else:
            UNFOUNDNODES.append(name)

def compareAttrs(inUpdate=True):
    global STOREDATTRIBUTES

    changes = []

    for attr in STOREDATTRIBUTES.keys():
        oldVal = STOREDATTRIBUTES[attr]
        newVal = pc.getAttr(attr)

        if oldVal != newVal:
            changes.append((attr, oldVal, newVal))

        if inUpdate:
            STOREDATTRIBUTES[attr] = newVal

    return changes

def log():
    if len(STOREDATTRIBUTES) > 0:
        print ("Attributes dictionary at %s" % time.strftime('%X %x %Z'))
        print ("-------------------------------------------")
        for key in STOREDATTRIBUTES.keys():
            print (key.ljust(50) + " : %s" % str(STOREDATTRIBUTES[key]))
    else:
        print ("Attributes dictionary is empty at %s" % time.strftime('%X %x %Z'))
    print ("")

def logChanges(inChanges):
    if len(inChanges) > 0:
        print ("Changes at %s" % time.strftime('%X %x %Z'))
        print ("-------------------------------------------")
        for attr_oldVal_newVal in inChanges:
            print ("- " + attr_oldVal_newVal[0].ljust(40) + "%s => %s" % (attr_oldVal_newVal[1], attr_oldVal_newVal[2]))
    else:
        print ("No changes at %s" % time.strftime('%X %x %Z'))
    print ("")

def monitorAttrChangesUI(*inArgs):
    """
    UI for monitorAttrChanges
    """
    # check to see if window exists
    if (pc.window('monitorAttrChangesUI', q=True, exists=True)):
        pc.deleteUI('monitorAttrChangesUI')
    myUI = pc.window('monitorAttrChangesUI', title='Monitor attribute changes', widthHeight=(260, 260))
    colLayout = pc.columnLayout( adjustableColumn=True )

    pc.rowLayout(numberOfColumns=2, adjustableColumn2=2)
    pc.text("Nodes :")
    pc.textField("monitorAttrChangesNodesCB", text=NODESNAMES, cc=textChanged )
    pc.setParent(colLayout)
    
    pc.rowLayout(numberOfColumns=2, adjustableColumn2=1)
    pc.button("Store", command=storeClicked)
    pc.checkBox("monitorAttrChangesAddCB", label="Add", value=False)
    pc.setParent(colLayout)

    pc.rowLayout(numberOfColumns=2, adjustableColumn2=1)
    pc.button("Compare", command=compareClicked)
    pc.checkBox("monitorAttrChangesUpdateCB", label="Update", value=True)
    pc.setParent(colLayout)
    pc.button("Log current values", command=logClicked)

    pc.showWindow(myUI)

#CALLBACKS

def textChanged(*inArgs):
    global NODESNAMES
    NODESNAMES = pc.textField("monitorAttrChangesNodesCB", query=True, text=True)

def storeClicked(*inArgs):
    global STOREDATTRIBUTES
    global UNFOUNDNODES

    storeAttrs(pc.checkBox("monitorAttrChangesAddCB", query=True, value=True))

def compareClicked(*inArgs):
    changes = compareAttrs(pc.checkBox("monitorAttrChangesUpdateCB", query=True, value=True))
    logChanges(changes)

def logClicked(*inArgs):
    log()

#################################################################################
#   devMate
#################################################################################

def UIVisChanged(args):
    #Defer the execution in case hidiung is temporary (docking/undocking)
    pc.evalDeferred("tkDevHelpers.cleanIfHidden()")

def cleanIfHidden():
   if not pc.control("devMateDockControl", query=True, visible=True):
        if pc.window('devMateUI', q=True, exists=True):
            pc.deleteUI('devMateUI')
        pc.deleteUI('devMateDockControl')

def devMateUI(*inArgs):
    if (pc.window('devMateUI', q=True, exists=True)):
        pc.deleteUI('devMateUI')

    mainWindow = pc.mel.eval("$tmp = $gMainPane")
    dockLayout = pc.paneLayout(configuration='single', parent=mainWindow)
    dockName = pc.dockControl("devMateDockControl", allowedArea='all', area='top', floating=False, content=dockLayout, label="Dev' Mate", vcc=UIVisChanged)
 
    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = pc.loadUI(uiFile=os.path.join(dirname, "UI", "tkDevMate.ui"))
    pc.showWindow(ui)

    pc.control(ui, e=True, parent=dockLayout)

    filtersChanged()

def filtersChanged():
    cmds = filterMethods(pc.textField("tkDMFiltersTB", query=True, text=True))
    
    pc.textScrollList("tkDMFunctionsLB", edit=True, removeAll=True)

    cmdskeys = cmds.keys()
    cmdskeys = sorted(cmdskeys)

    for cmd in cmdskeys:
        pc.textScrollList("tkDMFunctionsLB", edit=True, append=cmd)

def printValue(inValue):
    if isinstance(inValue, str):
        return "\"%s\"" % inValue

    return str(inValue)

def functionSelChanged():

    #"%s(%s)" % (methodKey, ",".join(methods[methodKey].func_code.co_varnames))] = 

    sel = pc.textScrollList("tkDMFunctionsLB", query=True, selectItem=True)

    if sel != None and len(sel) > 0:
        methods = filterMethods(pc.textField("tkDMFiltersTB", query=True, text=True), pc.checkBox("tkDMDocCB", query=True, value=True))

        if sel[0] in methods:
            args, varargs, keywords, defaults = inspect.getargspec(methods[sel[0]])
            defaults = get_default_args(methods[sel[0]])

            argsArray =  []
            for argName in args:
                if argName in defaults:
                    argsArray.append("%s=%s" % (argName, printValue(defaults[argName])))
                else:
                    argsArray.append(argName)
            strContent = "#import %s\r\n" % sel[0].split(".")[0]
            strContent += "%s(%s)\r\n\r\n'''\r\n" % (sel[0], ",".join(argsArray))
            strContent += "Documentation : \r\n" + str(methods[sel[0]].__doc__) + "\r\n\r\n"
            strContent += "'''\r\n"
            pc.textField("tkDMFunctionsLE", edit=True, text=strContent)

def docChanged():
    filtersChanged()
    functionSelChanged()

class Tester(object):

    def __init__(self, inName=None, inPath=None, inValues=None):
        self.name = inName
        self.path = inPath
        self.values = inValues or {}

        self.GETTERS = {
            "Objects":partial(pc.ls),
            "Transforms":partial(self.filter, inName="Objects", inType="transform"),
            "Locators":partial(self.filter, inName="Objects", inType="locator"),
            "Joints":partial(self.filter, inName="Objects", inType="joint"),
            "Curves":partial(self.filter, inName="Objects", inType="nurbsCurve"),
            "Meshes":partial(self.filter, inName="Objects", inType="mesh"),
            "Meshes Points":partial(self.meshPoints),
            "Expressions":partial(self.filter, inName="Objects", inType="expression"),
            "Expressions Characters":partial(self.exprCharacters),
            "Constraints":partial(pc.ls, type=["constraint","motionPath"]),
            "parentConstraints":partial(self.filter, inName="Constraints", inType="parentConstraint"),
            "aimConstraints":partial(self.filter, inName="Constraints", inType="aimConstraint"),
            "orientConstraints":partial(self.filter, inName="Constraints", inType="orientConstraint"),
            "scaleConstraints":partial(self.filter, inName="Constraints", inType="scaleConstraint"),
            "pointConstraints":partial(self.filter, inName="Constraints", inType="pointConstraint"),
            "poleVectorConstraints":partial(self.filter, inName="Constraints", inType="poleVectorConstraint"),
            "motionPaths":partial(self.filter, inName="Constraints", inType="motionPath"),
            "follicles":partial(self.filter, inName="Objects", inType="follicle"),
            "Utilities":partial(self.filter, inName="Objects", inType=["addDoubleLinear", "blendColors",
                                                                "condition", "curveInfo", "multDoubleLinear", "multiplyDivide",
                                                                "reverse", "clamp", "plusMinusAverage", "distanceBetween",
                                                                "remapValue", "setRange", "decomposeMatrix", "composeMatrix",
                                                                "multMatrix", "blendTwoAttr", "nearestPointOnCurve", "pairBlend",
                                                                "vectorProduct", "distanceBetween", "wtAddMatrix"]),
            "Deformers":partial(self.filter, inName="Objects", inType=["skinCluster", "blendshape",
                                                                "cluster", "lattice", "wrap", "shrinkWrap"]),
            "skinClusters":partial(self.filter, inName="Deformers", inType="skinCluster"),
            "blendshapes":partial(self.filter, inName="Deformers", inType="blendshape"),
            "clusters":partial(self.filter, inName="Deformers", inType="cluster"),
            "lattices":partial(self.filter, inName="Deformers", inType="lattice"),
            "wraps":partial(self.filter, inName="Deformers", inType="wrap"),
            "shrinkWraps":partial(self.filter, inName="Deformers", inType="shrinkWrap"),
            "Opening":partial(openNode, inPath=self.path),
            "Performance":partial(evaluateNode, inName=self.name, inPath=self.path)
        }

    def _get(self, inProperty):
        getter = self.GETTERS.get(inProperty)
        if not getter is None:
            return getter()

        return None

    def get(self, inProperty):
        prop = self.values.get(inProperty)
        if prop is None:
            self.values[inProperty] = self._get(inProperty)
        else:
            self.values[inProperty]

        return self.values[inProperty]

    def filter(self, inName="Objects", inType=None):
        filtered = {}
        objs = self.get(inName)
        return [obj for obj in objs if obj.type() == inType or obj.type() in inType]

    def getValue(self, inProperty):
        return len(self.get(inProperty)) if isinstance(self.get(inProperty), (list, tuple)) else self.get(inProperty)

    def getValues(self, *args):
        return [str(self.getValue(arg)) for arg in args]

    def exprCharacters(self, inName="Expressions"):
        nChars = 0
        exprs = self.get(inName)
        for expr in exprs:
            nChars += len(expr.getString())

        return nChars

    def meshPoints(self, inName="Meshes"):
        nPoints = 0
        meshes = self.get(inName)
        for mesh in meshes:
            nPoints += pc.polyEvaluate(mesh, vertex=True)

        return nPoints

# *** Objects
def countObjectsOld():
    trans = pc.ls(type="transform")
    groups = []
    for tran in trans:
        if tran.getShape() == None:
            groups.append(tran)
    rslt = {
        "Objects":len(pc.ls()) - 64,
        "Transforms ":len(trans),
        "Goups":len(groups),
        "Locators":len(pc.ls(type="locator")),
        "Joints":len(pc.ls(type="joint")),
        "curves":len(pc.ls(type="nurbsCurve"))
    }

    print ("Objects {0}".format(rslt["Objects"]))
    print (" - transforms {0}".format(rslt["transforms"]))
    print (" - groups {0}".format(rslt["groups"]))
    print (" - locators {0}".format(rslt["locators"]))
    print (" - joints {0}".format(rslt["joints"]))
    print (" - curves {0}".format(rslt["curves"]))

    return rslt

# *** Hierarchy
def traceHierarchy():
    trans = pc.ls(type="transform")
    step = 1
    if len(trans) > 100:
        step = 100.0 / len(trans)
    counter = 0
    count = 0
    depths = 0
    biggestDepth = 0
    for tran in trans:
        counter += step
        if counter >= 1:
            d =  len(tran.getAllParents())
            if d >  biggestDepth:
                biggestDepth = d
            depths += d
            count += 1
            counter = 0
    
    rslt = {
        "Average depth":float(depths) / count,
        "Biggest depth":biggestDepth
    }
    print ("Average depth {0}".format(rslt["Average depth"]))
    print ("Biggest depth {0}".format(rslt["Biggest depth"]))

    return rslt

#Params
def cntparams():
    sel = pc.ls(sl=True)
    nParams = 0
    for selObj in sel:
        nParams += len(tkc.getParameters(selObj, False, "", True))
        
    return nParams
    
#print cntparams()

def cntExprCharacters():
    nChars = 0
    exprs = pc.ls(type="expression")
    for expr in exprs:
        nChars += len(pc.expression(expr, query=True, s=True))

    rslt = {
        "Expressions":len(exprs),
        "Biggest depth":nChars
    }

    return rslt

# *** Constraints (0 base)
def countConstraints():
    cons = pc.ls(type=["constraint","motionPath"])
    #pc.select(pc.ls(type="constraint"))
    
    #pc.select(pc.ls(type="motionPath"))
    specCns = 0
    
    parentConstraints = len(pc.ls(type="parentConstraint"))
    specCns += parentConstraints
    orientConstraints = len(pc.ls(type="orientConstraint"))
    specCns += orientConstraints
    aimConstraints = len(pc.ls(type="aimConstraint"))
    specCns += aimConstraints
    scaleConstraints = len(pc.ls(type="scaleConstraint"))
    specCns += scaleConstraints
    pointConstraints = len(pc.ls(type="pointConstraint"))
    specCns += pointConstraints
    poleVectorConstraints = len(pc.ls(type="poleVectorConstraint"))
    specCns += poleVectorConstraints
    motionPaths = len(pc.ls(type="motionPath"))
    specCns += motionPaths
    
    rslt = {
        "constraints":len(cons),
        "parentConstraints":parentConstraints,
        "aimConstraints":aimConstraints,
        "orientConstraints":orientConstraints,
        "scaleConstraints":scaleConstraints,
        "pointConstraints":pointConstraints,
        "poleVectorConstraints":poleVectorConstraints,
        "motionPaths":motionPaths
    }

    print ("constraints {0}".format(rslt["constraints"]))
    print (" - parentConstraints {0}".format(rslt["parentConstraints"]))
    print (" - orientConstraints {0}".format(rslt["orientConstraints"]))
    print (" - aimConstraints {0}".format(rslt["aimConstraints"]))
    print (" - scaleConstraints {0}".format(rslt["scaleConstraints"]))
    print (" - pointConstraints {0}".format(rslt["pointConstraints"]))
    print (" - poleVectorConstraints {0}".format(rslt["poleVectorConstraints"]))
    print (" - motionPaths {0}".format(rslt["motionPaths"]))

    return rslt

# *** Utilities (0 base)
def countUtilities():
    utilities = ["addDoubleLinear", "blendColors", "condition", "curveInfo", "multDoubleLinear", "multiplyDivide", "reverse", "clamp", "plusMinusAverage", "distanceBetween", "remapValue", "setRange"]
    utils = pc.ls(type=utilities)

    rslt = {"utility nodes":len(utils)}

    print ("utility nodes {0}".format(rslt["utils"]))
    for util in utilities:
        print (" - " + util + " " + str(len(pc.ls(type=util))))

    return rslt

#Deformers (0 base)
def cntdeformers():
    sel = pc.ls(sl=True)
    defs = []
    nDefs = 0
    for selObj in sel:
        skin = tkc.getSkinCluster(selObj)
        if skin != None:
            infs = pc.skinCluster(skin,query=True,inf=True)
            nDefs += len(infs)
            for inf in infs:
                if not inf in defs:
                    defs.append(inf)

    return (nDefs, len(defs))

#Evaluate
def setAnim(inObj, attr="tx", nFrames=100):
    pc.playbackOptions(min=1, max=nFrames)
    cTime = 0
    for f in range(nFrames):
        cTime += 1
        pc.setKeyframe( inObj, attribute=attr, value=math.cos(cTime) * 2, t=cTime)

def evaluate(nFrames=100, refresh=True):
    cTime = 0
    for f in range(nFrames):
        cTime += 1
        pc.currentTime(cTime)
        if refresh:
            pc.refresh()

def importFile(path):
    pc.system.importFile(path)

def openFile(path):
    pc.system.openFile(path, force=True)

def getNodes(nodesPath="Z:\\Toonkit\\RnD\\Src\\GitRepo\\oscar\\build\\OscarEditor\\release\\Data\\Rigs\\"):
    nodes = []
    dirContent = os.listdir(nodesPath)
    for dirItem in dirContent:
        path = os.path.join(nodesPath, dirItem)
        if os.path.isdir(path):
            nodeName = dirItem
            nodePath = os.path.join(path, nodeName + ".ma")
            if os.path.isfile(nodePath):
                nodes.append([nodePath, nodeName])
                
    return nodes

def openNode(inPath):
    return tkc.benchIt(openFile, inPath)[0]

def evaluateNode(inName, inPath):
    if inName == "UnRoll":
        inName = "Unroll"

    roots = None

    modelName = inName + ":" + inName
    rootName = modelName + "_Root"

    if not pc.objExists(rootName):
        roots = [o.name() for o in pc.ls(assemblies=True) if (o.getShape() == None or o.getShape().type() != "camera")]
    else:
        roots = [rootName]

    #Evaluate with all visible
    try:
        pc.setAttr(inName + ":Hidden.visibility", 1)
        tkSIGroups.refreshOverrides()
    except Exception as e:
        print (e)

    for root in roots:
        try:
            setAnim(root, nFrames=100)
        except Exception as e:
            print (e)

    return 100.0 / tkc.benchIt(evaluate, 100)[0]

def testNode(inName, inPath):
    if inName == "UnRoll":
        inName = "Unroll"
    pmsys.newFile(force=True)
    print (" *** " + inName + " ***")
    print ("size " + str(os.path.getsize(inPath) / 1000.0) + " Ko")
    tkc.benchIt(importFile, inPath)
    
    modelName = inName + ":" + inName
    rootName = modelName + "_Root"
    
    countObjects()
    
    exprs = cntExprCharacters()
    print ("expressions " + str(exprs[0]))
    print ("expressions chars " + str(exprs[1]))
    
    countConstraints()
    
    countUtilities()
    
    #Evaluate with all visible
    try:
        pc.setAttr(inName + ":Hidden.visibility", 1)
        tkSIGroups.refreshOverrides()
    except:
        pass
    
    setAnim(rootName, nFrames=1000)
    
    print (100.0 / tkc.benchIt(evaluate, 10)[0])
#testNode(nodes[nodeIndex][1],nodes[nodeIndex][0])