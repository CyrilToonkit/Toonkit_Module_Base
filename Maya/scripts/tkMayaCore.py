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

    You should have received a copy of <the GNU Lesser General Public License
    along with Toonkit Module Lite.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _____   _  __    __  __                              ____                       
 |_   _| | |/ /   |  \/  |   __ _   _   _    __ _     / ___|   ___    _ __    ___ 
   | |   | ' /    | |\/| |  / _` | | | | |  / _` |   | |      / _ \  | '__|  / _ \
   | |   | . \    | |  | | | (_| | | |_| | | (_| |   | |___  | (_) | | |    |  __/
   |_|   |_|\_\   |_|  |_|  \__,_|  \__, |  \__,_|    \____|  \___/  |_|     \___|
                                    |___/                                         
    Toonkit's Maya base library
    ASCII Text font "Ivrit" (http://patorjk.com/software/taag)

VERSIONS :

BETA RC 1.6:-Starting from 1.6, changelog is written in Oscar's Releases directly

BETA RC 1.5:-OSCAR : RigNode explorer added (still BETA !)
            -OSCAR : Generation logic enhancements (Cascading Generation)
            -OSCAR : logging unified (Maya - Softimage)
            -Command 'getanim' fixed (tangents)
            -Maya python toolkit : ReplaceDeformer and SelectDeformers added to menu (Enveloping)
            -Maya python toolkit : BypassNode added to menu (Rigging)

BETA 5.3 :  -Rignode 'poseListener' updated with "PositionRange" parameter to manage position contribution in pose detection
            -Rignode SplineIK can now stretch and Squash
            -OSCAR : Great reunification between DCC codes (Maya-Softimage)
            -Maya toolkit can now return global scaling
            -Maya animation getter/setter fixed (tangents)
            -OSCAR : Preservation of custom sets (must be Toonkit's SIGroups)
            -OSCAR : Generation workflow changed. Now generates "_RAW" versions (without postscripts) for MASTER and AN, and detects inputs obsolescence much better (Comp, Geometries, Postscripts, Poses)
            -CS Code cleaned of warnings and useless code

BETA 5.2 :  -Command 'getanim' updated with start and end arguments (first and last frame of recorded animation)

BETA 5.1 :  -OUAT Specific scripts regarding ALEMBIC caching and playblasting
            -First researches on mayabatch with python, using a trick in userSetup

BETA 5.0 :  -Command 'getplaycontrol' added, returns first, last and current frame
            -userSetup "Specific modules" loading, to load customer-related developments
            -userSetup "safe loading" (loads even if python zmq modules do not exists)
            -TKuserSetup auto-load of needed plug-ins
            -Expressions in always evaluate : False
            -tkMayaCore character API : getAssets, getCharacterName added to be more permessive on rigs names and namespaces
            -tkMayaCore capture completed : now includes 'format' and 'compression' (like maya compmand), 'play' (autoplay) and 'useCamera' (load given camera for capture)
            -tkRig : smooth logic added
            -Enveloping framework : PointData now accepts multiple times the same deformer, and will merge envelope data on the finally
            -OSCAR : Projects paths are now case insensitive
            -OSCAR : RigNode 'Modification date' use to track obsolescence of geometry nodes
            -OSCAR : Publishing is now capaple of publishing parameters to "VisHolders"
            -OSCAR : Publishing now displays merge pop-ups in debug only
            -OSCAR : Node name validity more carefull (no port name in node name)
            -SYNOPTIK : 'Allways on top' (=Form property) and 'Show all' (overrides 'groups' visibilities) options


BETA 4.3 :  -Added rig nodes "Piston" and "Suspension" for mechanical Rigs
            -Maya node "SpreadDeformNode" now exits cleanly when not connected (fixes a crash on "delete")
            -Command 'connectposes' added
            -Command 'cleanproperties' now runs even when no properties were found
            -transferShading definition added to 'tkRig' and exposed in the menu
            -skinCluster are now detected even if not acting on first shape
            -Mimetik : Now plugged to $PROJECTPATH\Actions
            -DCCTranslator : Added "TRUE" and "FALSE" constants for expressions
            -OSCAR : Added the ability to migrate assets (opening from another project, and renaming re-pathing geometries / postscripts)
            -OSCAR : Geometry that have 'OscarAttributes' at import will be ignored
                - Button added in RigCreator to add 'OscarAttributes' on selection
            -OSCAR : SynopticPaths now correctly editable

BETA 4.2 :  -Added operators "WheelNode", "SpreadDeformNode" and relative commands
            -ExtractDeltas python plugin added with its relative command

BETA 4.1 :  -Better implementation of matchAllTransforms concept, using matrices
            -setWeights command adapted to Maya 2015 (pymel 'setWeights' uses a different influences order in 2015, reversed regarding 2013) 

BETA 4.0 :  -Menu cleaned up (no more oscar server management)
            -Debugs on animation (Curve.StaticValue, tangents, extrapolations...)
            -First zmq module for Maya 2015
            -Framework 4.5 => 4.0 (WinXP compatibility)

BETA 3.5 :   Custom Node "tkResPlaneNode" added, as well as creation method "createResPlane" in tkMayaCore, exposed in menu Operators => Resolution Plane Operator
            Core : added a log system that outputs both in Maya script out and SIBar "HelpLine" (see below)
            SIBar : added and "HelpLine" LineEdit linked to core log commands and configured to output Picking information
BETA 3.3 :   Core : storeSelection and loadSelection extended (can now store or retrieve collections, and keep presets if loadSelection("Name", clean=False))
            Core : results of "getConstraintTargets" filtered (no more dupes)
            SIBar "Selection Sets" group added, using Core "storeSelection" and "loadSelection"
BETA 3.2 :   "Path" constraint added and integrated in tkMayaCore library
            SIBar "$CNS" variable added for arbitrary attribute parsing (act on constraints on selected objects)
BETA 3.0 :   SIGroups now works with several shapes per object
            "Rig primitives" (=~ Hprimitives) added in SIBar


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import sys
import re
import shutil
import math
import random
import os
import subprocess
import time
import xml.dom.minidom as minidom
from threading import Timer
from timeit import default_timer
from functools import partial
import ast
import six
basestring = six.string_types
if sys.version_info.major  > 2:
    xrange = range
try:
    from statistics import mean
except:
    def meanFunction(inArray):
        theSum = 0
        for inItem in inArray:
            theSum += inItem
        return theSum / len(inArray)
    mean = meanFunction
import maya.cmds as cmds
import pymel.core as pc
import pymel.core.general as pm
import pymel.core.system as pmsys
import pymel.core.datatypes as dt
from pymel import versions

import maya.api.OpenMaya as om
import maya.OpenMaya as OpenMaya
import TkApi.maya_api as tkApi

import locationModule
from Toonkit_Core.tkToolOptions.tkOptions import Options
import Toonkit_Core.tkProjects.tkContext as ctx
from Toonkit_Core import tkCore as tc
import OscarZmqString as ozs
import OscarZmqMayaString as ozms
import PAlt as palt
import tkMayaTools.ToonkitMayaCore as ToonkitMayaCore
import tkNodeling as tkn

from Toonkit_Core import tkLogger

__author__ = "Cyril GIBAUD - Toonkit"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ____                _              _       
  / ___|___  _ __  ___| |_ __ _ _ __ | |_ ___ 
 | |   / _ \| '_ \/ __| __/ _` | '_ \| __/ __|
 | |__| (_) | | | \__ \ || (_| | | | | |_\__ \
  \____\___/|_| |_|___/\__\__,_|_| |_|\__|___/
                                             
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

LINESEP = "\n"

WORLDSPACE = "world"
OBJECTSPACE = "object"

OPT_PICKED = "tkPickedObjects"

OPT_PICKID = "tkPickId"
OPT_PICKLOGIC = "tkPickLogic"
OPT_PICKCOUNTER = "tkPickCounter"
OPT_PICKMIN = "tkPickMinimum"
OPT_PICKMAX = "tkPickMaximum"
OPT_PICKFIRST = "tkPickFirst"
OPT_PICKLAST = "tkPickLast"
OPT_PICKSELECT = "tkPickSelect"
OPT_PICKARGS = "tkPickArgs"
OPT_PICKCANCEL = "tkPickCancel"

OPT_SEL = "tkSavedSel"
OPT_SELSETS = "tkSavedSets"

CTRL_SIBar = None
CTRL_SIHELPLINE = "tksiHelpLineLE"

G_LOGTIMER = None

CONST_VALUEVARIABLE = "$V"
CONST_ITERVARIABLE = "$N"
CONST_PERCENTVARIABLE = "$P"
CONST_CNSVARIABLE = "$CNS"
CONST_SHAPEVARIABLE = "$SHP"
CONST_OBJWILDCARD = "$OBJNAME"

CONST_ENUMTYPESEP=";"
CONST_ENUMTYPEVALUESSEP=":"#THIS IS A MAYA CONSTRAINT

CONST_NSSEP=":"#THIS IS A MAYA CONSTANT

CONST_TMPNS = "TMPNS"
CONST_LONGTMPNS = "TMPNS:"
CONST_ROOTSUFFIX = "_Root"
CONST_GROUPSUFFIX = "_Grp"
CONST_BUFFERSUFFIX = "_Buffer"
CONST_NEUTRALSUFFIX = "_NeutralPose"
CONST_LAYERSUFFIX = "CtrlLayer"
CONST_EXTRARIGSSUFFIX = "_ExtraRigs"
CONST_KEYSETSPROP = "TK_KeySets"
CONST_KEYSETSTREEPROP = "TK_KeySetsTree"
CONST_CTRLSDICPROP = "TK_CtrlsDic"
CONST_ATTRIBUTES = "OSCAR_Attributes"

CONST_SKINNABLES = ['mesh', 'lattice', 'nurbsSurface', 'nurbsCurve']

BASEMAP = "baseMap"

CONST_MAYACOLORS = [(255,120,120,120)]
CONST_MAYACOLORS.append((255,0,0,0))
CONST_MAYACOLORS.append((255,64,64,64))
CONST_MAYACOLORS.append((255,128,128,128))
CONST_MAYACOLORS.append((255,155,0,40))
CONST_MAYACOLORS.append((255,0,4,96))
CONST_MAYACOLORS.append((255,0,0,255))
CONST_MAYACOLORS.append((255,0,70,25))
CONST_MAYACOLORS.append((255,38,0,67))
CONST_MAYACOLORS.append((255,200,0,200))
CONST_MAYACOLORS.append((255,138,72,51))
CONST_MAYACOLORS.append((255,63,35,31))
CONST_MAYACOLORS.append((255,153,38,0))
CONST_MAYACOLORS.append((255,255,0,0))
CONST_MAYACOLORS.append((255,0,255,0))
CONST_MAYACOLORS.append((255,0,65,153))
CONST_MAYACOLORS.append((255,255,255,255))
CONST_MAYACOLORS.append((255,255,255,0))
CONST_MAYACOLORS.append((255,100,220,250))
CONST_MAYACOLORS.append((255,67,255,163))
CONST_MAYACOLORS.append((255,255,176,176))
CONST_MAYACOLORS.append((255,228,172,121))
CONST_MAYACOLORS.append((255,255,255,99))
CONST_MAYACOLORS.append((255,0,153,84))
CONST_MAYACOLORS.append((255,161,105,48))
CONST_MAYACOLORS.append((255,159,161,48))
CONST_MAYACOLORS.append((255,104,161,48))
CONST_MAYACOLORS.append((255,48,161,93))
CONST_MAYACOLORS.append((255,48,161,161))
CONST_MAYACOLORS.append((255,48,103,161))
CONST_MAYACOLORS.append((255,111,48,161))
CONST_MAYACOLORS.append((255,161,48,105))

CONST_HELPLINESUFFIXES = ["# Log     : "]
CONST_HELPLINESUFFIXES.append("# Warning : ")
CONST_HELPLINESUFFIXES.append("# Error   : ")
CONST_HELPLINESUFFIXES.append("# Picking : ")

CONST_HELPLINECOLORS = [(.16, .16, .16)]
CONST_HELPLINECOLORS.append((1.0, 0.27, 0))
CONST_HELPLINECOLORS.append((0.7, 0.14, 0.14))
CONST_HELPLINECOLORS.append((0.1, 0.1, 0.44))

CONST_CNSINTERPS = ["NoFlip", "Average", "Shortest", "Longest", "Cache"]
TK_INTERP = 2

CONST_NULLINFNAME = "TK_0Deform"

TK_RESPLANE_TYPE = "tkResPlane"

CONST_DELTA = 0.001
CONST_EPSILON = 0.0001

oscarmodulepath = locationModule.OscarModuleLocation()
#we arrived in "Scripts" folder, go up one step
oscarmodulepath = os.path.abspath(os.path.join(oscarmodulepath, os.pardir))

SYNOPTIKPATH = os.path.join(oscarmodulepath, "Standalones", "SynopTiK", "SynopTiK.exe")
MIMETIKPATH = os.path.join(oscarmodulepath, "Standalones", "MimeTiK", "MimeTiK.exe")

UNITS_RATIO = { "mm":0.1,
                "millimeter":0.1,
                "cm":1.0,
                "centimeter":1.0,
                "m":100.0,
                "meter":100.0,
                "km":100000,
                "kilometer":100000,
                "in":2.54,
                "inch":2.54,
                "ft":30.48,
                "foot":30.48,
                "yd":91.44,
                "yard":91.44,
                "mi":160934.4,
                "mile":160934.4}


ANIMTYPES = ["animCurveTA","animCurveTL","animCurveTT","animCurveTU","animCurveUA","animCurveUL","animCurveUT"]

CHANNELS = ["t","tx","ty","tz","r","rx","ry","rz","s","sx","sy","sz"]

RE_ENV = re.compile('%\w+%')

OLD_PARENT_SUFFIX = "_OLDPARENT"

PROJECT_INFO = None

TOOL = None

HELP_LIST = []

# tkDecorators
def noUndos(func):
    def wrapper(*args, **kwargs):
        _exception = None
        oldUndoState = pc.undoInfo(q=True, state=True)
        pc.undoInfo(state=False)
        try:
            rslt = func(*args, **kwargs)
        except Exception as f:
            _exception = f
        pc.undoInfo(state=oldUndoState)
        
        if not _exception is None:
            raise _exception
        return rslt
    return wrapper

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _   _      _                     
 | | | | ___| |_ __   ___ _ __ ___ 
 | |_| |/ _ \ | '_ \ / _ \ '__/ __|
 |  _  |  __/ | |_) |  __/ |  \__ \
 |_| |_|\___|_| .__/ \___|_|  |___/
              |_|                  

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def getTool():
    global TOOL
    if not TOOL:#Try to get core tool instance from interperter level
        try:
            TOOL = eval("tkc.TOOL")
        except:
            pass
    
    if not TOOL:
        TOOL = ToonkitMayaCore.ToonkitMayaCore()
        tc.setProject("maya", TOOL.options["project"])

    return TOOL

def getType(inPyNode):
    if isinstance(inPyNode, pm.Component):
        if isinstance(inPyNode, pm.MeshVertex):
            return "MeshVertex"
        if isinstance(inPyNode, pm.MeshEdge):
            return "MeshEdge"
        if isinstance(inPyNode, pm.MeshFace):
            return "MeshFace"
    
    try:
        return inPyNode.type()
    except Exception as e:
        pass
    
    return None

def getNode(inObj, inRobust=True, inVerbose=True, inConsiderNs=False):

    if isinstance(inObj, basestring):
        if not inRobust or "|" in inObj:
            try:
                return pc.PyNode(inObj)
            except:
                return None

        objs = pc.ls(inObj) if not inConsiderNs else pc.ls([inObj, "*:" + inObj, "*:*:" + inObj])
        if len(objs) == 0:
            return None
        else:
            if inVerbose and len(objs) > 1:
                pc.warning("More than one object matches name '{0}' ({1}), '{2}' was used...".format(
                            inObj, ",".join(["'{}'".format(n.name()) for n in objs]), objs[0]))

            return objs[0]

    return inObj

def getNodes(inStringList, inRobust=True, inVerbose=True):
    nodesList =[]

    for objName in inStringList:
        obj = getNode(objName, inRobust=inRobust, inVerbose=inVerbose)

        if not obj is None:
            nodesList.append(obj)

    return nodesList

def haveVariables(inPath, inCustomVariables=None):
    if inCustomVariables != None:
        for customVar in inCustomVariables:
            if customVar in inPath:
                return True
                
    return RE_ENV.search(inPath) != None

def expandVariables(inPath, inCustomVariables=None):
    expandedPath = inPath
    iterationPath = inPath
    
    while haveVariables(expandedPath, inCustomVariables):
        iterationPath = expandedPath
        
        if inCustomVariables != None:
            for customVar in inCustomVariables:
                expandedPath = expandedPath.replace(customVar, inCustomVariables[customVar])
        matches = RE_ENV.findall(expandedPath)
        
        for match in matches:
            if match[1:-1] in os.environ:
                expandedPath = expandedPath.replace(match, os.environ[match[1:-1]])
            
        if iterationPath == expandedPath:
            break
            
    return expandedPath

def log(inText="", inSeverity=0, inHelpLine=False, inHelpLineOnly=False, inBlockingErrors=False, inUseSuffixes=True, inHelpLineDelay=0):
    global G_LOGTIMER
    fullText = inText
    if inUseSuffixes:
        fullText = CONST_HELPLINESUFFIXES[inSeverity] + inText

    if inSeverity == 1 or  inSeverity == 3:
        tkLogger.warning(inText)
    elif inSeverity == 2:
        if inBlockingErrors:
            pc.error(inText)
        else:
            tkLogger.warning(fullText)
    else:
        tkLogger.info(fullText)

    controlExists = pc.control(CTRL_SIHELPLINE, exists=True)

    if inHelpLine and controlExists:
        if inText != "" and G_LOGTIMER != None:
            G_LOGTIMER.cancel()
            G_LOGTIMER = None

        pc.textField(CTRL_SIHELPLINE, edit=True, text=fullText)
        pc.textField(CTRL_SIHELPLINE, edit=True, bgc=CONST_HELPLINECOLORS[inSeverity])
        if inHelpLineDelay > 0:
            G_LOGTIMER = Timer(inHelpLineDelay, clearHelpLineDeferred)
            G_LOGTIMER.start()

    #Clean the delayed cleaning if still alive
    if not controlExists and G_LOGTIMER != None:
        G_LOGTIMER.cancel()
        G_LOGTIMER = None

def benchIt(infunc, *inArgs):
    start = time.time()
    rslt = infunc(*inArgs)
    end = time.time()
    duration = end - start
    tkLogger.info("> {0} took {1:.4f} s".format(infunc.__name__, duration))
    
    return (duration, rslt)

TIMERS = {}

"""
startTimer("Coco")
for i in range(3):
    print i
print stopTimer("Coco")
"""

def startTimer(inName, inReset=False):
    global TIMERS
    if inReset or not inName in TIMERS:
        TIMERS[inName] = {"elapsed":0.0,"runs":False}

    TIMERS[inName]["runs"]=True
    TIMERS[inName]["date"]=default_timer()
    

def stopTimer(inName, inLog=False, inReset=False):
    elapsed = 0.0

    if inName in TIMERS:
        if TIMERS[inName]["runs"]:
            TIMERS[inName]["runs"]=False
            now = default_timer()
            TIMERS[inName]["elapsed"] += now - TIMERS[inName]["date"]
        elapsed = TIMERS[inName]["elapsed"]

    if inLog:
        tkLogger.info("{0} took {1:.4f} s".format(inName, elapsed))

    if inReset:
        TIMERS[inName] = {"elapsed":0.0,"runs":False}

    return elapsed

def compileLists(l1, l2, l1items, l2items):
    lst =[]
    length = len(l1) / l1items
    id1 = 0
    id2 = 0
    for i in range(length):
        id1 = i * l1items
        id2 = i * l2items
        lst.extend(l1[id1:id1+l1items])
        lst.extend(l2[id2:id2+l2items])
        
    return lst


"""
print "all_body",len(all_body),all_body
dupes = getDuplicates(all_body)
print "all_body dupes",len(dupes),dupes

print "schema_low",len(schema_low),schema_low
dupes = getDuplicates(schema_low)
print "schema_low dupes",len(dupes),dupes

delta = getElementsDelta(schema_low, all_body)
print "delta",len(delta[0]),len(delta[1]),delta

print "-"*75

print "Facial_High",len(Template.Facial_High),Template.Facial_High

print "schema_facial_mid_remove",len(schema_facial_mid_remove),schema_facial_mid_remove

delta = getElementsDelta(schema_facial_mid_remove, Template.Facial_High)
print "delta",len(delta[0]),len(delta[1]),delta

print "-"*75

all_facial = Template.Facial_High + Template.Facial_Mid

print "all_facial",len(all_facial),all_facial

print "schema_facial",len(schema_facial),schema_facial

delta = getElementsDelta(schema_facial, all_facial)
print "delta",len(delta[0]),len(delta[1]),delta

"""

def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def getDuplicates(inList):
    uniqueList = list(set(inList))

    if len(uniqueList) < len(inList):
        dupes = []
        for item in inList:
            if item in dupes:
                continue

            count = inList.count(item)

            if count > 1:
                dupes.extend((count-1) * [item])

        return dupes
    return []

def getElementsDelta(inList1, inList2):
    rslt = [[],[]]
    
    for item in inList1:
        if not item in inList2:
            rslt[0].append(item)

    for item in inList2:
        if not item in inList1:
            rslt[1].append(item)

    return rslt

def pickLog(inText="", inHelpLineDelay=0):
    log(inText, 3, True, inHelpLineDelay=inHelpLineDelay)

def helpLog(inText="", inHelpLineDelay=5):
    log(inText, 0, True, inHelpLineDelay=inHelpLineDelay)

def clearHelpLine():
    global G_LOGTIMER
    log("", 0, True, True, False, False)
    G_LOGTIMER = None

def clearHelpLineDeferred():
    pc.evalDeferred(clearHelpLine)

def getNearestMayaColor(color):
    nearestColor = CONST_MAYACOLORS[0]
    nearestDist = 1000000;
    neareastId = 0;
    counter = 0
    for mayaCol in CONST_MAYACOLORS:
        dist = abs(mayaCol[0] - color[0]) + abs(mayaCol[1] - color[1]) + abs(mayaCol[2] - color[2]) + abs(mayaCol[3] - color[3])
        if(nearestDist > dist):
            nearestDist = dist
            nearestColor = mayaCol
            neareastId = counter
        counter = counter + 1
    return (neareastId, nearestColor)

def getColorFromMayaColor(mayacolor):
    return CONST_MAYACOLORS[mayacolor]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def endsWith(inStr, inEnd):
    return inStr[-len(inEnd):] == inEnd

def startsWith(inStr, inStart):
    return inStr[:len(inStart)] == inStart

def doubleBarelyEquals(val1, val2, delta=CONST_DELTA):
    return abs(val1 - val2) < delta

def listsBarelyEquals(val1, val2, delta=CONST_DELTA):
    val1Length = len(val1) 
    if val1Length != len(val2):
        return False

    for i in range(val1Length):
        if not doubleBarelyEquals(val1[i], val2[i], delta=delta):
            return False

    return True

def vectorBarelyEquals(val1, val2, delta=CONST_DELTA):
    return doubleBarelyEquals(val1.x, val2.x) and doubleBarelyEquals(val1.y, val2.y) and doubleBarelyEquals(val1.z, val2.z) 

def orientationEquals(inObj1, inObj2, inTolerance=0.5):
    mat1 = inObj1.wm.get()
    mat2 = inObj2.wm.get()

    vecX = pc.datatypes.Vector(1,0,0)
    vecY = pc.datatypes.Vector(0,1,0)
    vecZ = pc.datatypes.Vector(0,0,1)

    vec1X = vecX * mat1
    vec1X.normalize()
    vec2X = vecX * mat2
    vec2X.normalize()
    if vec1X.dot(vec2X) <= inTolerance:
        return False

    vec1Y = vecY * mat1
    vec1Y.normalize()
    vec2Y = vecY * mat2
    vec2Y.normalize()
    if vec1Y.dot(vec2Y) <= inTolerance:
        return False

    vec1Z = vecZ * mat1
    vec1Z.normalize()
    vec2Z = vecZ * mat2
    vec2Z.normalize()
    if vec1Z.dot(vec2Z) <= inTolerance:
        return False

    return True

def coordToAngleWeight(inX, inY):
    sign = 1
    if inY < 0:
        sign = -1
    length = math.sqrt(inX*inX+inY*inY)
    normalizedX = inX
    if length > 0:
        normalizedX = inX / length
    angle = sign * math.degrees(math.acos(normalizedX))

    if angle < -90:
        angle += 180
    elif angle > 90:
        angle -= 180

    return (angle, length)
    
def angleWeightTocoords(inAngle, inWeight):
    radAngle = math.radians(inAngle)
    return (math.cos(radAngle) * inWeight, math.sin(radAngle) * inWeight)

def getGlobalScaling(inObj):
    scl = [1,1,1]
    parents = inObj.getAllParents()
    
    for ancestor in parents:
        if ancestor.type() == "transform":
            cscl = ancestor.getScale()
            scl[0] *= cscl[0]
            scl[1] *= cscl[1]
            scl[2] *= cscl[2]
    
    return scl

def hasZeroedScaling(inObj):
    scl = getGlobalScaling(inObj)
    return scl[0] < 0 or scl[1] < 0 or scl[2] < 0

def getUnitScaling():
    unit = pc.currentUnit(linear=True, query=True)
    return UNITS_RATIO[unit]

def hasMethod(inInstance, inMethodName):
    return hasattr(inInstance,inMethodName) and callable(getattr(inInstance,inMethodName))

def getNamespace(inObject):
    if not CONST_NSSEP in str(inObject):
        return ""
    else:
        return  CONST_NSSEP.join(inObject.split(CONST_NSSEP)[:-1]) + CONST_NSSEP

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____                        __  __                                                   _   
 / ___|  ___ ___ _ __   ___  |  \/  | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_ 
 \___ \ / __/ _ \ '_ \ / _ \ | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
  ___) | (_|  __/ | | |  __/ | |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ 
 |____/ \___\___|_| |_|\___| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
                                                       |___/                               

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def addNamespace(inNs):
    """
    Add a namespace if it does not exists

    :param inNs: The namespace to add (without the ":")
    :type inNs: str
    """
    if not pc.namespace(exists=":" + inNs):
        pc.namespace(set=":")
        pc.namespace(add=inNs)

def getUniqueName(inName="Object", inSuffix=""):

    if not pc.objExists(inName+inSuffix):
        return inName+inSuffix

    increment = 1
    if is_number(inName[-1]):
        increment = int(inName[-1])
        inName = inName[0:-1]
    while(pc.objExists(inName+str(increment)+inSuffix)):
        increment = increment + 1

    return inName+str(increment)+inSuffix

def getDuplicates(inPyNodes=None, inLog=False):
    if inPyNodes == None:
        inPyNodes = pc.ls(dag=True)
    #build short name:[PyNodes] dict

    dupes = []

    names = {}
    for dag in inPyNodes:
        name = dag.name()
        if "|" in name:
            shortName = name.split("|")[-1]
            
            if not shortName in names:
                names[shortName] = []
            
            names[shortName].append(dag)
            dupes.append(dag)

    if inLog:
        tkLogger.info("{0} duplicates among {1} objects".format(len(dupes), len(inPyNodes)))
        tkLogger.info("----------------------------------")
        for uniqueName in names:
            tkLogger.info("{0} *{1}({2})".format(uniqueName, len(names[uniqueName]),[n.name() for n in names[uniqueName]]))
            
    return names

def getInstances(inPyNodes=None, inLog=False):
    if inPyNodes == None:
        inPyNodes = pc.ls(shapes=True)

    instanciations = []

    instances = {}

    for shape in inPyNodes:
        parents = pc.listRelatives(shape, ap=True)
        if len(parents) > 1:
            shortName = shape.name().split("|")[-1]
            instanciated = []

            for parent in parents:
                for parentShape in parent.getShapes():
                    if parentShape.name().split("|")[-1] == shortName:
                        instanciated.append(parentShape)
                        break

            instances[shortName] = instanciated
            instanciations.extend(parents)

    if inLog:
        tkLogger.info("{0} instances on {1} transforms".format(len(instances), len(instanciations)))
        tkLogger.info("----------------------------------")
        for shapeName, curInstances in instances.items():
            tkLogger.info("{0} *{1}({2})".format(shapeName, len(curInstances),[n.name() for n in curInstances]))

    return instances

def getRigName(inName):
    return inName if inName[-len(CONST_ROOTSUFFIX):] != CONST_ROOTSUFFIX else inName[:-len(CONST_ROOTSUFFIX)]

def renameFromMapping(inRenamings, inRememberOldName=True):
    for origName, newName in inRenamings.items():
        origObject = getNode(origName)
        if not origObject is None:
            origObject.rename(str(origObject.namespace()) + newName)

def renameRemember(inObj, inName, inRememberOldName=True):
    inObj = getNode(inObj)

    if inRememberOldName:
        if not pc.attributeQuery("nameOrig",node=inObj, exists=True):
            inObj.addAttr("nameOrig", dt="string")
            name = inObj.name()
            if "|" in name:
                name = name.split("|")[-1]

            inObj.nameOrig.set(name)

    inObj.rename(inName)

def restoreNames(inCleanAttrs=True):
    objs = [a.node() for a in pc.ls("*.nameOrig")]

    for obj in objs:
        obj.rename(obj.nameOrig.get())
        if inCleanAttrs:
            obj.nameOrig.delete()

def renameDuplicates(inPyNodes=None, inLog=False, inRememberOldName=True):
    namesDict = getDuplicates(inPyNodes, inLog)
    renamedNodes = []
    MAXITER = 100
    counter = 0
    firstPass = True
    currentRenamedNodes = None

    currentParents = {}

    while len(namesDict) > 0:
        if counter >= MAXITER:
            pc.warning("Exited after {0} iterations, can't rename all objects...".format(counter))
            return renamedNodes
        counter += 1

        if firstPass:
            currentRenamedNodes=[]

        for uniqueName in namesDict:
            for dupNode in namesDict[uniqueName]:
                nodeParent = None
                if dupNode in currentParents:
                    nodeParent = currentParents[dupNode].getParent()
                else:
                    nodeParent = dupNode.getParent()
                    currentParents[dupNode] = nodeParent

                if nodeParent != None:
                    parentName = nodeParent.name().split("|")[-1]
                    currentName = dupNode.stripNamespace().split("|")[-1]
                    
                    newName = "{0}__{1}".format(parentName, currentName)
                    if inLog:
                        tkLogger.info(" -renaming {0} in {1}".format(dupNode.name(), newName))
                    renameRemember(dupNode, newName, inRememberOldName=inRememberOldName)
                    if firstPass:
                        currentRenamedNodes.append(dupNode)
        namesDict = getDuplicates(currentRenamedNodes, inLog)

        if firstPass:
            renamedNodes = currentRenamedNodes
            firstPass = False

    if inLog:
        tkLogger.info("{0} nodes were renamed ({1})".format(len(renamedNodes), [n.name() for n in renamedNodes]), inRaw=True)

    return renamedNodes

def rename(node, newName, respectConventions=True, renameAttrs=False, labelJoints=True):
    oldName = node.name()
    neutral = getNeutralPose(node) if node.type() == "transform" else None
    props = getProperties(node)

    if ":" in oldName:
        ns_name = oldName.split(":")
        ns_newname = newName.split(":")

        for prop in props:
            prop.rename(ns_name[0] + ":" + prop.stripNamespace().replace(ns_name[1], ns_newname[1]))
            if renameAttrs:
                propParams = getParameters(prop)
                oldStrippedName = ns_name[1].replace("_Root", "")
                newStrippedName = ns_newname[1].replace("_Root", "")
                for propParam in propParams:
                    if oldStrippedName in propParam:
                        renamedParamName=propParam.replace(oldStrippedName, newStrippedName)
                        if not cmds.attributeQuery(renamedParamName, node=prop.name(), exists=True):
                            pc.renameAttr("{0}.{1}".format(prop.name(), propParam) , propParam.replace(oldStrippedName, newStrippedName))
        if neutral != None:
            neutral.rename(ns_name[0] + ":" + neutral.stripNamespace().replace(ns_name[1], ns_newname[1]))

        #Detect the special case of a model $NAME:$NAME, if True rename namespace and update newname
        if ns_name[0] == ns_name[1]:
            if respectConventions:
                pc.namespace(rename=[ns_name[0], ns_newname[1]])
                newName = ns_newname[1] + ":" + ns_newname[1]
            elif ns_name[0] != ns_newname[0]:
                pc.namespace(rename=[ns_name[0], ns_newname[0]])
    else:
        for prop in props:
            prop.rename(prop.name().replace(oldName, newName))
            if renameAttrs:
                propParams = getParameters(prop)
                oldStrippedName = oldName.replace("_Root", "")
                newStrippedName = newName.replace("_Root", "")
                for propParam in propParams:
                    if oldStrippedName in propParam:
                        pc.renameAttr("{0}.{1}".format(prop.name(), propParam) , propParam.replace(oldStrippedName, newStrippedName))
        if neutral != None:
            neutral.rename(neutral.name().replace(oldName, newName))

    newName = node.rename(newName).name()

    if labelJoints and node.type() == "joint":
        #side
        if "Left" in node.stripNamespace():
            cmds.setAttr("{0}.side".format(node.name()), 1)
        elif "Right" in node.stripNamespace():
            cmds.setAttr("{0}.side".format(node.name()), 2)
        else:
            cmds.setAttr("{0}.side".format(node.name()), 0)

        #type
        cmds.setAttr("{0}.type".format(node.name()), 18)
        shortName = node.stripNamespace().replace("Left_", "").replace("Right_", "")
        cmds.setAttr("{0}.otherType".format(node.name()), shortName,type="string")
        
    return newName

def importFile(path, newName="", ensureNamespaces=False, convertUnits=True, labelJoints=True):
    oldName = os.path.split(path)[-1].split(".")[0]
    name = newName if newName != "" else oldName
    uniqueName = getUniqueName(name + ":" + name).split(":")[1]

    try:
        pmsys.importFile(path, namespace=CONST_TMPNS)
    except Exception as e:
        pc.warning(e)
    #create sub-namespace if needed
    if not pc.namespace(exists=uniqueName):
        pc.namespace(add=uniqueName)

    #Collect imported objects
    roots = pc.ls(CONST_LONGTMPNS + oldName + ":*", assemblies=True)
    groups = pc.ls(CONST_LONGTMPNS + oldName + ":*", type="objectSet")
    customDisplays = []
    sclUnit = 1.0
    if convertUnits:
        sclUnit = getUnitScaling()
        customDisplays = pc.ls(CONST_LONGTMPNS + oldName + ":*", type=["transform", "joint"])

        for customDisplay in customDisplays:
            shape = customDisplay.getShape()
            dispType = customDisplay.type()

            if(pc.attributeQuery("OLDsize", node=customDisplay, exists=True)):
                #do a display trick if object have displays
                pc.setAttr(customDisplay.name() + ".OLDsize", pc.getAttr(customDisplay.name() + ".OLDsize") / sclUnit)
                updateDisplay(customDisplay)
            elif dispType == "joint":
                pc.setAttr(customDisplay.name() + ".radius", pc.getAttr(customDisplay.name() + ".radius") * sclUnit)
            elif shape != None and shape.type() == "locator":
                pc.setAttr(customDisplay.name() + ".localScaleX", pc.getAttr(customDisplay.name() + ".localScaleX") / sclUnit)
                pc.setAttr(customDisplay.name() + ".localScaleY", pc.getAttr(customDisplay.name() + ".localScaleY") / sclUnit)
                pc.setAttr(customDisplay.name() + ".localScaleZ", pc.getAttr(customDisplay.name() + ".localScaleZ") / sclUnit)

    #Rename objects
    for rigRoot in roots:
        rigName = rigRoot.name().replace(CONST_LONGTMPNS+oldName+ ":"+oldName, uniqueName + ":" + name)
        rigRoot.rename(rigName)
        children = getChildren(rigRoot, True, False, False)
        for obj in children:
            objName = ""
            if CONST_LONGTMPNS+oldName+ ":"+oldName in obj.name():
                objName = obj.name().replace(CONST_LONGTMPNS+oldName+ ":"+oldName, uniqueName + ":" + name)
            else:
                objName = obj.name().replace(CONST_LONGTMPNS+oldName+ ":", uniqueName + ":")
            obj.rename(objName)

            if labelJoints and obj.type() == "joint":
                #side
                if "Left" in obj.stripNamespace():
                    cmds.setAttr("{0}.side".format(obj.name()), 1)
                elif "Right" in obj.stripNamespace():
                    cmds.setAttr("{0}.side".format(obj.name()), 2)
                else:
                    cmds.setAttr("{0}.side".format(obj.name()), 0)

                #type
                cmds.setAttr("{0}.type".format(obj.name()), 18)
                shortName = obj.stripNamespace().replace("Left_", "").replace("Right_", "")
                cmds.setAttr("{0}.otherType".format(obj.name()), shortName,type="string")

    #Rename named non-DAGs still in namespace
    nonDags = pc.ls(CONST_LONGTMPNS + oldName + ":*")
    for nonDag in nonDags:
        nonDagName = ""
        if CONST_LONGTMPNS+oldName+ ":"+oldName in nonDag.name():
            nonDagName = nonDag.name().replace(CONST_LONGTMPNS+oldName+ ":"+oldName, uniqueName + ":" + name)
        else:
            nonDagName = nonDag.name().replace(CONST_LONGTMPNS+oldName+ ":", uniqueName + ":")
        nonDag.rename(nonDagName)

    #Rename groups
    ''' groups renaming performed with non-DAGs, see above
    for group in groups:
        groupName = group.name().replace(CONST_LONGTMPNS+oldName+ ":", uniqueName + ":")
        group.rename(groupName)
    '''
    pc.namespace( removeNamespace = CONST_LONGTMPNS + oldName, mergeNamespaceWithParent = True)
    pc.namespace( removeNamespace = CONST_TMPNS, mergeNamespaceWithParent = True)

    return (roots, groups)

def getOscarType(node):
    mayatype = node.type()
    if mayatype == "transform":
        if (node.__getattribute__('getShape')):
            shape = node.getShape()
            if shape != None:
                node = shape
                mayatype = node.type()

    oscartype = "Unknown (" + mayatype + ")"
    if mayatype == "locator" or mayatype == "transform" :
        ns = node.namespace()
        if ns != "" and (node.stripNamespace() == ns[:-1] or node.stripNamespace() == ns[:-1] + "Shape"):
            oscartype = "Model"
        elif node.name()[-10:] == "_RootShape":
            oscartype = "Root"
        elif mayatype == "transform" and isNeutralPose(node):
            oscartype = "NeutralPose"
        else:
            oscartype = "Null"
    elif mayatype == "joint":
        oscartype = "Deformer"
    elif mayatype == "nurbsCurve":
        oscartype = "Curve"
    elif mayatype == "mesh":
        oscartype = "Mesh"
    elif mayatype == "nurbsSurface":
        oscartype = "Nurbs"
    elif mayatype == "lattice":
        oscartype = "Lattice"
    elif mayatype == "baselattice":
        oscartype = "BaseLattice"

    return oscartype

def storeCollection(inObjects, inName=OPT_SEL, presetHolderName=OPT_SELSETS, add=False):
    selSets = pc.optionVar(query = presetHolderName )
    if pc.optionVar(exists=inName) and not add:
        pc.optionVar(remove=inName)
    for obj in inObjects:
        if hasattr(obj,"longName"):
            pc.optionVar(stringValueAppend=(inName, obj.longName()))
    if selSets == 0 or not inName in selSets:
        pc.optionVar(stringValueAppend=(presetHolderName, inName))

def storeSelection(inName=OPT_SEL):
    sel = pc.ls(sl=True)
    storeCollection(sel, inName)

    return sel

def skipSelected(inNumber=1):
    sel = pc.selected()
    if len(sel) == 0:
        return

    filteredSel = [sel[0]]

    skip = inNumber + 1
    for obj in sel:
        if skip == 0:
            filteredSel.append(obj)
            skip = inNumber + 1

        skip += -1

    pc.select(filteredSel)


def cleanPreset(inName=OPT_SEL, presetHolderName=OPT_SELSETS):
    if pc.optionVar(exists=inName):
        pc.optionVar(remove=inName)
    selSets = pc.optionVar(query = presetHolderName )
    if inName in selSets:
        pc.optionVar(removeFromArray=(presetHolderName, selSets.index(inName)))

def loadCollection(inName=OPT_SEL, clean=True, presetHolderName=OPT_SELSETS, swapNamespace=""):
    actualObjects = []
    objectLongNames = pc.optionVar(query = inName )
    try:
        if not isinstance(objectLongNames, str):
            if not isinstance(objectLongNames, int):
                for longName in objectLongNames:
                    if swapNamespace != "" and ":" in longName:
                        ns = longName.split(":")[0]
                        longName = longName.replace(ns, swapNamespace)
                    obj = getNode(longName)
                    if not obj is None:
                        actualObjects.append(obj)
        else:
            if swapNamespace != "" and ":" in objectLongNames:
                ns = objectLongNames.split(":")[0]
                objectLongNames = objectLongNames.replace(ns, swapNamespace)
            obj = getNode(objectLongNames)
            if not obj is None:
                actualObjects.append(obj)

    except Exception as e:
        pc.error("Cannot get objects." + str(e))

    if clean:
        cleanPreset(inName, presetHolderName)

    return actualObjects

def loadSelection(inName=OPT_SEL, clean=True, presetHolderName=OPT_SELSETS, swapNamespace=""):
    actualObjects = loadCollection(inName, clean, presetHolderName, swapNamespace)

    if len(actualObjects) > 0:
        pc.select(actualObjects, replace=True, noExpand=True)
    else:
        pc.select(clear=True, noExpand=True)

def removeUnknownNodes():
    unknowns = pc.ls(type="unknown")

    if(len(unknowns) > 0):
        tkLogger.debug("Removing 'unknown' nodes : " + ",".join([n.name() for n in unknowns]), inRaw=True)
        for unknown in unknowns:
            if pc.objExists(unknown):
                pc.lockNode(unknown, lock=False)
                pc.delete(unknown)
    else:
        tkLogger.debug("No 'unknown' nodes found")

def deleteUnusedNodes(inSafeAddDoubles=False):
    tkn.deleteUnusedNodes(inSafeAddDoubles=inSafeAddDoubles)

#todo add an option to consider upwards hierarchy (PyNode.getAllParents())
def isVisibleAfterAll(inObj, inDownStream=True, inUpStream=True):
    parent = None
    if inUpStream:
        parent = inObj.getParent()

    visibilites = []

    if not parent is None:
        visibilites = [isVisibleAfterAll(parent, inDownStream=False)]

    visibilites.extend([inObj.visibility.get(), not inObj.overrideEnabled.get() or inObj.overrideVisibility.get()])

    if inObj.type() == "transform" and inDownStream:
        shapes = inObj.getShapes(noIntermediate=True)
        for shape in shapes:
            visibilites.extend([shape.v.get(), not shape.overrideEnabled.get() or shape.overrideVisibility.get()])
    else:
        visibilites.append(not inObj.intermediateObject.get())

    return all(visibilites)

def isSimpleObjectSet(name):
    # We first test for plug-in object sets.
    try:
        apiNodeType = cmds.nodeType(name, api=True)
    except RuntimeError:
        return False

    if apiNodeType == "kPluginObjectSet":
        return True

    # We do not need to test is the object is a set, since that test
    # has already been done by the outliner
    try:
        nodeType = cmds.nodeType(name)
    except RuntimeError:
        return False

    # We do not want any rendering sets
    if nodeType == "shadingEngine":
        return False

    # if the object is not a set, return false
    if not (nodeType == "objectSet" or
        nodeType == "textureBakeSet" or
        nodeType == "vertexBakeSet" or
        nodeType == "character"):
        return False

    # We also do not want any sets with restrictions
    restrictionAttrs = ["verticesOnlySet", "edgesOnlySet", "facetsOnlySet", "editPointsOnlySet", "renderableOnlySet"]
    if any(cmds.getAttr("{0}.{1}".format(name, attr)) for attr in restrictionAttrs):
        return False

    # Do not show layers
    if cmds.getAttr("{0}.isLayer".format(name)):
        return False

    # Do not show bookmarks
    annotation = cmds.getAttr("{0}.annotation".format(name))
    if annotation == "bookmarkAnimCurves":
        return False

    # Whew ... we can finally show it
    return True

def getSoftSelections(opacityMult=1.0, inMergePerDag=True):
    opacities = []
    opacitiesDags = []

    # if soft select isn't on, return
    softSelect = cmds.softSelect(q=True, sse=True)
        
    richSel = OpenMaya.MRichSelection()
    try:
        # get currently active soft selection
        OpenMaya.MGlobal.getRichSelection(richSel)
    except:
        raise Exception('Error getting rich selection.')

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

        if(shapeComp.hasFn(OpenMaya.MFn.kSingleIndexedComponent)):
            compFn = OpenMaya.MFnSingleIndexedComponent(shapeComp)
            try:
                # get the secret hidden opacity value for each component (vert, cv, etc)
                for i in xrange(compFn.elementCount()):
                    value = 1.0
                    if softSelect:
                        value = compFn.weight(i).influence()
                    compOpacities[compFn.element(i)] = value * opacityMult
            except Exception as e:
                pass

        if len(compOpacities) == 0:
            compOpacities = None

        path = shapeDag.partialPathName()

        if inMergePerDag and path in opacitiesDags:
            opacities[opacitiesDags.index(path)][1].update(compOpacities)
        else:
            opacities.append((path, compOpacities))
            opacitiesDags.append(path)

    return opacities

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _____                     _          __                                _           _   _             
 | ____|_  _____  ___ _   _| |_ ___   / _|_ __ ___  _ __ ___    ___  ___| | ___  ___| |_(_) ___  _ __  
 |  _| \ \/ / _ \/ __| | | | __/ _ \ | |_| '__/ _ \| '_ ` _ \  / __|/ _ \ |/ _ \/ __| __| |/ _ \| '_ \ 
 | |___ >  <  __/ (__| |_| | ||  __/ |  _| | | (_) | | | | | | \__ \  __/ |  __/ (__| |_| | (_) | | | |
 |_____/_/\_\___|\___|\__,_|\__\___| |_| |_|  \___/|_| |_| |_| |___/\___|_|\___|\___|\__|_|\___/|_| |_|
                                                                                                       
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def printExecuteError():
    pc.error("No def provided, please give a function callable on one or several objects !")

def executeFromCollection(inFunc=printExecuteError, inColl=[], inObjectsMin=0, inObjectsMax=0, inFirstInArgs=0, inLastInArgs=0, inErrorMessage="Wrong inputs !", inSelectReturn=False, *inArgs):
    listArgs = list(inArgs)
    if isinstance(inFunc, str):
        inFunc = eval(inFunc)
    #print "Execute " + inFunc.__name__ + " on " + str(inColl) + " (args : " + str(listArgs) + ")"

    # Min / Max objects in collection
    if not inObjectsMin == 0 or not inObjectsMax == 0:
        selLength = len(inColl)
        if selLength < inObjectsMin or (not inObjectsMax == 0 and selLength > inObjectsMax):
            pc.error(inErrorMessage)
            return

    # Collection elements in arguments 
    firstInArgs = []
    lastInArgs = []

    if inFirstInArgs > 0:
        firstInArgs = inColl[0:inFirstInArgs]
        inColl = inColl[inFirstInArgs:]

    if inLastInArgs > 0:
        lastInArgs = inColl[-inLastInArgs:]
        inColl = inColl[:-inLastInArgs]

    newArgs = firstInArgs
    newArgs.extend(lastInArgs)
    newArgs.extend(listArgs)

    pc.undoInfo(openChunk=True)

    results = []

    for obj in inColl:
        curinArgs = [obj]
        newSpecArgs = [argCopy for argCopy in newArgs]
        if not len(newSpecArgs) == 0:
            #replace string parameter wildCard $OBJNAME
            counter = 0
            for arg in newSpecArgs:
                if isinstance(arg,str) and CONST_OBJWILDCARD in arg:
                    newSpecArgs[counter] = arg.replace(CONST_OBJWILDCARD, obj.name())
                counter += 1
            curinArgs.extend(newSpecArgs)

        #Log the function call
        rslt = inFunc(*curinArgs)
        formatArgs = []
        for arg in curinArgs:
            strArg = ""
            if isinstance(arg,str):
                strArg = "'{0}'".format(arg)
            else:
                try:
                    strArg = "tkc.getNode('{0}')".format(arg.name())
                except:
                    pass
            if strArg == "":
                strArg = str(arg)
            formatArgs.append(strArg)

        print("tkc.{0}({1})".format(inFunc.__name__, ",".join(formatArgs)))

        if rslt != None:
            results.append(rslt)

    if inSelectReturn:
        pc.select(results, replace=True)

    pc.undoInfo(closeChunk=True)

def executeFromSelection(inFunc=printExecuteError, inObjectsMin=0, inObjectsMax=0, inFirstInArgs=0, inLastInArgs=0, inErrorMessage="Wrong inputs !", inSelectReturn=False, *inArgs):
    '''
    :todo: Selection filters

    '''
    sel = pc.ls(sl=True)
    executeFromCollection(inFunc, sel, inObjectsMin, inObjectsMax, inFirstInArgs, inLastInArgs, inErrorMessage, inSelectReturn, *inArgs)

'''''''''''''''''''''''''''''''''''''''''''''''''''''

Picking objects

testing :

reload(tkc)

tkc.pickSession("resetTRS", 0, 2)

pc.optionVar(remove="tkPickId")

print tkc.getPickedObjects()


'''''''''''''''''''''''''''''''''''''''''''''''''''''

def addSelectionToPicked(transforms=True,shapes=False, verify=True, deselect=True):
    if pc.optionVar(query=OPT_PICKCOUNTER) <= 0:
        return

    sel = pc.ls(sl=True, transforms=transforms,shapes=shapes)
    if len(sel) > 0:
        executed = addObjectsToPicked(sel, verify)
        if deselect and not executed:
            pc.select(clear=True)
    
def addObjectsToPicked(inObjects, verify=True):
    actualObjects = []
    objectLongNames = []
    if verify:
        objectLongNames = pc.optionVar(query = OPT_PICKED )
    
    counter = pc.optionVar(query=OPT_PICKCOUNTER)
    pickLogic = pc.optionVar(query = OPT_PICKLOGIC)
    strArgs = pc.optionVar(query = OPT_PICKARGS )
    args = "("
    if strArgs != 0 and len(strArgs) > 0:
        for arg in strArgs:
            args += ("," if len(args) == 1 else "") + str(ozs.stringtoobject(arg))
    args += ") - "

    pickLog(pickLogic + args + str(counter-1) + " objs left")

    for inObject in inObjects:
        if not verify or isinstance(objectLongNames, int) or not inObject.longName() in objectLongNames:
            pc.optionVar(stringValueAppend=(OPT_PICKED, inObject.longName()))
            counter = counter - 1
            pc.optionVar(intValue=[OPT_PICKCOUNTER, counter])
            if counter == 0:
                break

    if counter == 0:
        picked = getPickedObjects()
        if picked[0] != "":
            executeFromCollection(eval(picked[0]), picked[1], picked[2], picked[3], picked[4], picked[5], "", picked[6], *picked[7])
            return True

    return False

def cleanPickSession():
    pc.optionVar( remove=OPT_PICKED )
    pc.optionVar(remove=OPT_PICKLOGIC)
    pc.optionVar(remove=OPT_PICKMIN)
    pc.optionVar(remove=OPT_PICKMAX)
    pc.optionVar(remove=OPT_PICKCOUNTER)
    pc.optionVar(remove=OPT_PICKFIRST)
    pc.optionVar(remove=OPT_PICKLAST)
    pc.optionVar(remove=OPT_PICKSELECT)
    if pc.optionVar(exists=OPT_PICKARGS):
        pc.optionVar(remove=OPT_PICKARGS)
    pc.optionVar(remove=OPT_PICKCANCEL)

    jobId = pc.optionVar(query=OPT_PICKID)
    pc.optionVar(remove=OPT_PICKID)
    helpLog("Pick session ended (id: " +str(jobId) + ")")

    pc.mel.evalDeferred("scriptJob -kill " + str(jobId))

    if pc.popupMenu("tempMM", query=True, exists=True):
        pc.deleteUI("tempMM")
    
    loadSelection()

def getPickedObjects(clean=True):
    actualObjects = []

    if not pc.optionVar(exists=OPT_PICKID) or pc.optionVar(query=OPT_PICKCANCEL):
        if clean:
            cleanPickSession()
        return ["", actualObjects, 0, 0]

    objectLongNames = pc.optionVar(query = OPT_PICKED )
    pickLogic = pc.optionVar(query = OPT_PICKLOGIC)
    pickMin = pc.optionVar(query = OPT_PICKMIN )
    pickMax = pc.optionVar(query = OPT_PICKMAX )
    pickFirst = pc.optionVar(query = OPT_PICKFIRST )
    pickLast = pc.optionVar(query = OPT_PICKLAST )
    pickSelect = pc.optionVar(query = OPT_PICKSELECT ) == 1
    strArgs = pc.optionVar(query = OPT_PICKARGS )

    args = []

    if strArgs != 0 and len(strArgs) > 0:
        for strArg in strArgs:
            args.append(ozs.stringtoobject(strArg))

    try:
        if not isinstance(objectLongNames, str):
            if not isinstance(objectLongNames, int):
                for longName in objectLongNames:
                    obj = getNode(longName)
                    if not obj is None:
                        actualObjects.append(obj)
                    else:
                        pc.warning(longName + " cannot be found?")
        else:
            obj = getNode(objectLongNames)
            if not obj is None:
                actualObjects.append(obj)
            else:
                pc.warning(objectLongNames + " cannot be found?")
    except Exception as e:
        pickLogic = ""
        pc.error("Cannot get picked objects." + str(e))

    finally:
        if clean:
            cleanPickSession()
            
        return [pickLogic, actualObjects, pickMin, pickMax, pickFirst, pickLast, pickSelect, args ]

def killJob(jobId):
    pc.scriptJob(kill=jobId)

def endPickSession():
    pc.optionVar(intValue=[OPT_PICKCOUNTER,0])
    addObjectsToPicked([], False)

def cancelPickSession():
    pc.optionVar(intValue=[OPT_PICKCANCEL, 1])
    pc.optionVar(intValue=[OPT_PICKCOUNTER,0])
    addObjectsToPicked([], False)

def pickSession(inFuncName="printExecuteError", inObjectsMin=0, inObjectsMax=0, inFirstInArgs=0, inLastInArgs=0, inMessage="Pick session started",startWithSelection=True, selectReturns=False, *inArgs):
    sel = [] 

    realSel = storeSelection()

    if startWithSelection:
        sel = realSel

    pc.select(clear=True)

    jobId = pc.scriptJob(event=["SelectionChanged", addSelectionToPicked])

    pc.optionVar( remove=OPT_PICKED )
    pc.optionVar(intValue=(OPT_PICKID, jobId))
    pc.optionVar(stringValue=(OPT_PICKLOGIC, inFuncName))
    pc.optionVar(intValue=(OPT_PICKMIN, inObjectsMin))
    pc.optionVar(intValue=(OPT_PICKMAX, inObjectsMax))
    pc.optionVar(intValue=(OPT_PICKCOUNTER, (1000000 if inObjectsMax <= 0 else inObjectsMax)))
    pc.optionVar(intValue=(OPT_PICKFIRST, inFirstInArgs))
    pc.optionVar(intValue=(OPT_PICKLAST, inLastInArgs))
    pc.optionVar(intValue=(OPT_PICKSELECT, 1 if selectReturns else 0))
    pc.optionVar(intValue=[OPT_PICKCANCEL, 0])

    for arg in inArgs:
        pc.optionVar(stringValueAppend=(OPT_PICKARGS, ozs.objecttostring(arg)))

    if pc.popupMenu("tempMM", query=True, exists=True):
        pc.deleteUI("tempMM")

    pc.popupMenu("tempMM", button=2 ,parent="viewPanes",mm=True)
    pc.menuItem("End picking", command="tkc.endPickSession()")
    pc.menuItem("Cancel picking", command="tkc.cancelPickSession()")

    pickLog(inMessage + " (id: " + str(jobId) + ")")

    selLen = len(sel)
    if selLen > 0:
        if selLen > inObjectsMin:
            pc.optionVar(intValue=(OPT_PICKMAX, selLen))
            pc.optionVar(intValue=(OPT_PICKCOUNTER, selLen))
        addObjectsToPicked(sel, False)

 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _____                     __                          
 |_   _| __ __ _ _ __  ___ / _| ___  _ __ _ __ ___  ___ 
   | || '__/ _` | '_ \/ __| |_ / _ \| '__| '_ ` _ \/ __|
   | || | | (_| | | | \__ \  _| (_) | |  | | | | | \__ \
   |_||_|  \__,_|_| |_|___/_|  \___/|_|  |_| |_| |_|___/
                                                        
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setTRS(inTarget, inTValues = [0.0,0.0,0.0], inRValues = [0.0,0.0,0.0], inSValues = [1.0,1.0,1.0], inTrans=True, inRot=True, inScl=True, inWorldSpace=False, inPreserve=False):
    """
        Simple pymel setTransform wrapping, exposed SI style
        
        :param inTarget: target object transform (the one that'll move)
        :param inTValues: Translation values
        :param inRValues: Rotation values
        :param inSValues: Scale values
        :param inTrans: set translation if True
        :param inRot: set rotation if True
        :param inScl: set scale if True
        :param inWorldSpace: set transforms in world space if True

        :type inTarget: nt.Transform
        :type inTValues: list
        :type inRValues: list
        :type inSValues: list
        :type inTrans: bool
        :type inRot: bool
        :type inScl: bool
        :type inWorldSpace: bool
    
    transSpace = (WORLDSPACE if inWorldSpace else OBJECTSPACE)

    if inTrans and inTValues != None:
        inTarget.setTranslation(inTValues, space=transSpace)
    if inRot and inRValues != None:
        inTarget.setRotation(inRValues, space=transSpace)
    if inScl and inSValues != None:
        inTarget.setScale(inSValues)
    """
    kwargs = {("worldSpace" if inWorldSpace else "objectSpace"):True, "preserve":inPreserve}

    if inWorldSpace and inTrans and inTValues != None:
        kwargs["translation"]=inTValues
    if inRot and inRValues != None:
        kwargs["rotation"]=inRValues
    if inScl and inSValues != None:
        kwargs["scale"]=inSValues

    pc.undoInfo(openChunk=True)
    pc.xform(inTarget, **kwargs)

    if not inWorldSpace and inTrans and inTValues != None:
        if pc.getAttr(inTarget.tx, settable=True):
            pc.setAttr(inTarget.tx, inTValues[0])
        if pc.getAttr(inTarget.ty, settable=True):
            pc.setAttr(inTarget.ty, inTValues[1])
        if pc.getAttr(inTarget.tz, settable=True):
            pc.setAttr(inTarget.tz, inTValues[2])

    pc.undoInfo(closeChunk=True)

def matchTRS(inTarget, inRef, inTrans=True, inRot=True, inScl=True, inWorldSpace=True, inLocalApproach=False):
    """
        Match all Transforms of an object on another
        
        :param inTarget: target object (the one that'll move)
        :param inRef: reference object
        :param inTrans: match translation
        :param inRot: match rotation
        :param inScl: match scaling
        :param inWorldSpace: match the object in world space if True

        :type inTarget: nt.Transform
        :type inRef: nt.Transform
        :type inTrans: bool
        :type inRot: bool
        :type inScl: bool
        :type inWorldSpace: bool
    """
    
    transSpace = (WORLDSPACE if inWorldSpace else OBJECTSPACE)
    
    #Store previous values in case of a partial match
    trans = None
    if not inTrans:
        trans = inTarget.getTranslation(space=transSpace)
    rot = None
    if not inRot:
        rot = ozms.getPymelRotation(inTarget, space=transSpace)
    scl = None
    if not inScl:
        scl = inTarget.getScale()

    #Match matrices because it's the only approach that always works (negative scaling...)
    if not inLocalApproach or not inWorldSpace:

        if not inWorldSpace:
            refMatrix = pc.xform(inRef, query=True, worldSpace=inWorldSpace, matrix=True )
            pc.xform( inTarget, worldSpace=inWorldSpace, matrix=refMatrix )
        else:
            #Get "ref" world matrix as a starter for computation
            worldRefMat = inRef.worldMatrix.get()

            #Put the "ref" rotate pivot offset in world space
            refRp = inRef.rp.get()
            worldRefRpVec = refRp * worldRefMat

            #Put the "target" rotate pivot offset in world space
            worldTargetMat = inTarget.worldMatrix.get()

            targetRp = inTarget.rp.get()
            worldTargetRp = targetRp * worldTargetMat

            targetSp = inTarget.sp.get()

            #Add the "ref" rotate pivot and remove "target" rotate pivot to matrix
            worldRefMat.a30 += worldRefRpVec[0] - worldTargetRp[0]
            worldRefMat.a31 += worldRefRpVec[1] - worldTargetRp[1]
            worldRefMat.a32 += worldRefRpVec[2] - worldTargetRp[2]

            #Push matrix result in "target"
            pc.xform(inTarget, worldSpace=True, matrix=worldRefMat)
            #Reapply rotate pivot and scale pivot
            pc.xform(inTarget, rp=targetRp, sp=targetSp, rt=[0,0,0], p=True)

    else:#After years of fighting, use parent + scale constraint
        #print "New global Match"

        refParent = getDirectParent(inRef)
        targetParent = getDirectParent(inTarget)
        refMatcher = inRef

        #print "refParent", refParent, "targetParent", targetParent
        if refParent != targetParent:
            if refParent != None:
                refMatcher = pc.group(name=inRef.name() + "_matcher", empty=True, parent=refParent)
            else:
                refMatcher = pc.group(name=inRef.name() + "_matcher", empty=True, world=True)

            pc.setAttr(refMatcher.name() + ".t", pc.getAttr(inRef.name() + ".t"))
            pc.setAttr(refMatcher.name() + ".r", pc.getAttr(inRef.name() + ".r"))
            pc.setAttr(refMatcher.name() + ".s", pc.getAttr(inRef.name() + ".s"))
            if targetParent != None:
                pc.parent(refMatcher, targetParent)
            else:
                pc.parent(refMatcher, world=True)

        pc.setAttr(inTarget.name() + ".t", pc.getAttr(refMatcher.name() + ".t"))
        pc.setAttr(inTarget.name() + ".r", pc.getAttr(refMatcher.name() + ".r"))
        pc.setAttr(inTarget.name() + ".s", pc.getAttr(refMatcher.name() + ".s"))

        if refParent != targetParent:
            pc.delete(refMatcher)

        #refMatrix = pc.xform(inRef, query=True, worldSpace=inWorldSpace, matrix=True )
        #pc.xform( inTarget, worldSpace=inWorldSpace, matrix=refMatrix )

    #Restore previous values in case of a partial match
    if trans != None:
        setTRS(inTarget, trans, None, None, inWorldSpace=inWorldSpace)
    if rot != None:
        setTRS(inTarget, None, rot, None, inWorldSpace=inWorldSpace)
    if scl != None:
        setTRS(inTarget, None, None, scl)

    compensateCns(inTarget)

def matchT(inTarget, inRef, inWorldSpace=True):
    matchTRS(inTarget=inTarget, inRef=inRef, inTrans=True, inRot=False, inScl=False, inWorldSpace=inWorldSpace)

def matchR(inTarget, inRef, inWorldSpace=True):
    matchTRS(inTarget=inTarget, inRef=inRef, inTrans=False, inRot=True, inScl=False, inWorldSpace=inWorldSpace)

def matchS(inTarget, inRef, inWorldSpace=True):
    matchTRS(inTarget=inTarget, inRef=inRef, inTrans=False, inRot=False, inScl=True, inWorldSpace=inWorldSpace)

def resetTRS(inTarget, inTrans=True, inRot=True, inScl=True, inWorldSpace=False):
    """
        Reset all Transforms of an object (set them to 0)
        
        :param inTarget: target object (the one that'll move)
        :param inTrans: reset translation
        :param inRot: reset rotation
        :param inScl: reset scaling
        :param inWorldSpace: reset the object in world space if True

        :type inTarget: nt.Transform
        :type inRef: nt.Transform
        :type inTrans: bool
        :type inRot: bool
        :type inScl: bool
        :type inWorldSpace: bool
    """
    setTRS(inTarget,inTrans=inTrans, inRot=inRot, inScl=inScl, inWorldSpace=inWorldSpace)

def resetT(inTarget, inWorldSpace=False):
    """
        Reset Translation of an object (set them to 0)
        
    """
    setTRS(inTarget,inRot=False,inScl=False, inWorldSpace=inWorldSpace)

def resetR(inTarget, inWorldSpace=False):
    """
        Reset Rotation of an object (set them to 0)
        
    """
    setTRS(inTarget,inTrans=False,inScl=False, inWorldSpace=inWorldSpace)

def resetS(inTarget, inWorldSpace=False):
    """
        Reset Scale of an object (set them to 1)
        
    """
    setTRS(inTarget,inRot=False,inTrans=False, inWorldSpace=inWorldSpace)

def getGlobalScale(inObj, inheritedOnly):
    scl = [1.0,1.0,1.0] if inheritedOnly else inObj.getScale()
    parents = inObj.getAllParents()
    
    for par in parents:
        parScl = par.getScale()
        scl[0] *= parScl[0]
        scl[1] *= parScl[1]
        scl[2] *= parScl[2]
    
    return scl

def getLocalScale(inObj, inGlobalScale):
    scl = inObj.getScale()
    parents = inObj.getAllParents()
    
    for par in parents:
        parScl = par.getScale()
        scl[0] /= parScl[0]
        scl[1] /= parScl[1]
        scl[2] /= parScl[2]
    
    return scl

def getDistance(inObj1, inObj2):
    glob1 = inObj1.getTranslation(space="world")
    glob2 = inObj2.getTranslation(space="world")
    
    return math.sqrt(math.pow(glob1[0] - glob2[0], 2) + math.pow(glob1[1] - glob2[1], 2) + math.pow(glob1[2] - glob2[2], 2))

def addBuffer(inTarget, inSuffix=CONST_BUFFERSUFFIX):
    parents = pc.listRelatives(inTarget, parent=True)
    myBuffer = None

    uniqueName = getUniqueName(inTarget.name() + inSuffix)

    if len(parents) != 0:
        myBuffer = pc.group(name=uniqueName, empty=True, parent=parents[0])
    else:
        myBuffer = pc.group(name=uniqueName, empty=True, world=True)#Parent to world

    name = myBuffer.name()
    pc.setAttr(name + ".rotateX", keyable=False)
    pc.setAttr(name + ".rotateY", keyable=False)
    pc.setAttr(name + ".rotateZ", keyable=False)

    pc.setAttr(name + ".translateX", keyable=False)
    pc.setAttr(name + ".translateY", keyable=False)
    pc.setAttr(name + ".translateZ", keyable=False)

    pc.setAttr(name + ".scaleX", keyable=False)
    pc.setAttr(name + ".scaleY", keyable=False)
    pc.setAttr(name + ".scaleZ", keyable=False)

    pc.setAttr(name + ".visibility", keyable=False)

    matchTRS(myBuffer, inTarget)#, inLocalApproach=True)

    #Unlock / relock
    attrs = {}
    for channel in CHANNELS:
        attr = inTarget.attr(channel)
        attrs[channel] = (attr.isLocked(), attr.isKeyable(), attr.isInChannelBox())
        attr.setLocked(False)

    pc.parent(inTarget, myBuffer)

    for channel, info in attrs.items():
        attr = inTarget.attr(channel)
        attr.setLocked(info[0])

    return myBuffer

def getNeutralPose(inTarget, inSuffix=None):
    parents = inTarget.getAllParents()

    neutralName = inTarget.name() + (inSuffix or CONST_NEUTRALSUFFIX)
    for parent in parents:
        if parent.name() == neutralName:
            return parent

    return None

def setNeutralPose(inTarget, globalScalingFix=True, inSuffix=None):
    oldNeutral = getNeutralPose(inTarget, inSuffix)

    if oldNeutral != None:
        if len(pc.listConnections(oldNeutral, destination=False)) != 0:
            return setNeutralPose(inTarget, globalScalingFix=True, inSuffix="_Buffer")
            #resetTRS(inTarget)
            #print oldNeutral.name() + " is a connected NeutralPose, skipping setNeutralPose"

        oldNeutral.rename(oldNeutral.name() + "_OBSOLETE")
        #removeNeutralPose(inTarget, globalScalingFix)

    cnsTargets = []
    matchers = []
    if globalScalingFix :
        scl = inTarget.getScale()
        negScale = scl[0] < 0 or scl[1] < 0 or scl[2] < 0 
        if negScale:
            cnsUsing = getConstraintsUsing(inTarget)
            if len(cnsUsing) > 0:
                for cns in cnsUsing:
                    targets = getConstraintOwner(cns)
                    for target in targets:
                        if not target in cnsTargets:
                            cnsTargets.append(target)
                #print "Global scaling fix applied on %s constrained objects (%s)" % (inTarget.name(), str(cnsTargets))
                for target in cnsTargets:
                    '''
                    matchers.append(createRigObject(target, target.name() + "_TKMatcher", "Transform", mode="sibling", match=True ))
                    '''
                    matchers.append([target.getTranslation(space=WORLDSPACE), ozms.getPymelRotation(target, space=WORLDSPACE), target.getScale()])

    neutral = addBuffer(inTarget, inSuffix or CONST_NEUTRALSUFFIX)

    for i in range(len(cnsTargets)):
        '''
        matchTRS(cnsTargets[i], matchers[i])
        '''
        cnsTargets[i].setTranslation(matchers[i][0], space=WORLDSPACE)
        cnsTargets[i].setRotation(matchers[i][1], space=WORLDSPACE)
        cnsTargets[i].setScale(matchers[i][2])
        compensateCns(cnsTargets[i], True)
        '''
        pc.delete(matchers[i])
        '''

    if oldNeutral != None:
        parent = oldNeutral.getParent()
        pc.parent(neutral, parent)

        attrs = {}
        for channel in CHANNELS:
            attr = oldNeutral.attr(channel)
            attrs[channel] = (attr.isLocked(), attr.isKeyable(), attr.isInChannelBox())
            attr.setLocked(False)

        matchTRS(oldNeutral, inTarget)

        for channel, info in attrs.items():
            attr = oldNeutral.attr(channel)
            attr.setLocked(info[0])

        #matchTRS(oldNeutral, inTarget, inLocalApproach=True)
        pc.parent(inTarget, oldNeutral)
        neutralName=neutral.name()
        pc.delete(neutral)
        oldNeutral.rename(neutralName)
        neutral = oldNeutral

    return neutral

def getNeutralPoses(inTarget, inSuffix=None):
    neutralPoses = []

    neutral = getNeutralPose(inTarget, inSuffix=inSuffix)

    while not neutral is None:
        neutralPoses.append(neutral)
        neutral = getNeutralPose(neutral, inSuffix=inSuffix)

    return neutralPoses

def removeNeutralPose(inTarget, globalScalingFix=True, inSuffix=None):
    neutral = getNeutralPose(inTarget, inSuffix)

    if neutral != None:
        cnsTargets = []
        matchers = []
        if globalScalingFix :
            scl = neutral.getScale()
            negScale = scl[0] < 0 or scl[1] < 0 or scl[2] < 0 
            if negScale:
                cnsUsing = getConstraintsUsing(inTarget)
                if len(cnsUsing) > 0:
                    for cns in cnsUsing:
                        targets = getConstraintOwner(cns)
                        for target in targets:
                            if not target in cnsTargets:
                                cnsTargets.append(target)
                    #print "Global scaling fix applied on %s constrained objects (%s)" % (inTarget.name(), str(cnsTargets))
                    for target in cnsTargets:
                        '''
                        matchers.append(createRigObject(target, target.name() + "_TKMatcher", "Transform", mode="sibling", match=True ))
                        '''
                        matchers.append([target.getTranslation(space=WORLDSPACE), ozms.getPymelRotation(target, space=WORLDSPACE), target.getScale()])

        neutralParents = pc.listRelatives(neutral, parent=True)
        if len(neutralParents) != 0:
            pc.parent(inTarget,neutralParents[0])
        else:
            pc.parent(inTarget, world=True)
        pc.delete(neutral)

        for i in range(len(cnsTargets)):
            '''
            matchTRS(cnsTargets[i], matchers[i])
            '''
            cnsTargets[i].setTranslation(matchers[i][0], space=WORLDSPACE)
            cnsTargets[i].setRotation(matchers[i][1], space=WORLDSPACE)
            cnsTargets[i].setScale(matchers[i][2])      
            compensateCns(cnsTargets[i], True)
            '''
            pc.delete(matchers[i])
            '''

def getTopNeutralPose(inTarget, inSuffix=None):
    return getNeutralPoses(inTarget, inSuffix=inSuffix)[-1]

def getAllAutomatedCtrls(ctrls, inSuffix=None):
    return [x for x in ctrls if len(getNeutralPoses(x, inSuffix=inSuffix)) > 1]

def freezeTransform(inObj):
    objParent = inObj.getParent()
    if objParent != None:
        pc.parent(inObj, world=True)

    pc.makeIdentity(inObj, apply=True)
    pc.makeIdentity(inObj, apply=False)

    if objParent != None:
        pc.parent(inObj, objParent)

def setLimits(inNode,   inMinTx=1, inMaxTx=-1, inMinTy=1, inMaxTy=-1, inMinTz=1, inMaxTz=-1,
                        inMinRx=1, inMaxRx=-1, inMinRy=1, inMaxRy=-1, inMinRz=1, inMaxRz=-1,
                        inMinSx=1, inMaxSx=-1, inMinSy=1, inMaxSy=-1, inMinSz=1, inMaxSz=-1):

    args = {}
    
    if inMinTx >= inMaxTx:
        args["etx"] = [False, False]
    else:
        args["etx"] = [True, True]
        args["tx"] = [inMinTx, inMaxTx]
    
    if inMinTy >= inMaxTy:
        args["ety"] = [False, False]
    else:
        args["ety"] = [True, True]
        args["ty"] = [inMinTy, inMaxTy]

    if inMinTz >= inMaxTz:
        args["etz"] = [False, False]
    else:
        args["etz"] = [True, True]
        args["tz"] = [inMinTz, inMaxTz]


    if inMinRx >= inMaxRx:
        args["erx"] = [False, False]
    else:
        args["erx"] = [True, True]
        args["rx"] = [inMinRx, inMaxRx]
    
    if inMinRy >= inMaxRy:
        args["ery"] = [False, False]
    else:
        args["ery"] = [True, True]
        args["ry"] = [inMinRy, inMaxRy]

    if inMinRz >= inMaxRz:
        args["erz"] = [False, False]
    else:
        args["erz"] = [True, True]
        args["rz"] = [inMinRz, inMaxRz]


    if inMinSx >= inMaxSx:
        args["esx"] = [False, False]
    else:
        args["esx"] = [True, True]
        args["sx"] = [inMinSx, inMaxSx]
    
    if inMinSy >= inMaxSy:
        args["esy"] = [False, False]
    else:
        args["esy"] = [True, True]
        args["sy"] = [inMinSy, inMaxSy]

    if inMinSz >= inMaxSz:
        args["esz"] = [False, False]
    else:
        args["esz"] = [True, True]
        args["sz"] = [inMinSz, inMaxSz]

    pc.transformLimits(inNode, **args)

def getConnected(inNode, inCustomChannels=None, inUseTransforms=True):
    connectedChannels = []

    channels = CHANNELS if inUseTransforms else []

    if not inCustomChannels is None:
        channels.extend(inCustomChannels)

    if len(channels) == 0:
        raise ValueError("No channels given for getConnected on {0}".format(inNode))

    for channel in channels:
        if len(inNode.attr(channel).inputs()) > 0:
            connectedChannels.append(channel)

    return connectedChannels

def isConnected(inNode, inCustomChannels=None, inUseTransforms=True):
    return len(getConnected(inNode, inCustomChannels=inCustomChannels, inUseTransforms=inUseTransforms)) > 0


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _   _ _                         _           
 | | | (_) ___ _ __ __ _ _ __ ___| |__  _   _ 
 | |_| | |/ _ \ '__/ _` | '__/ __| '_ \| | | |
 |  _  | |  __/ | | (_| | | | (__| | | | |_| |
 |_| |_|_|\___|_|  \__,_|_|  \___|_| |_|\__, |
                                        |___/ 

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def getChildrenRecursively(node, filterNeutrals=True, filterProps=True, useIgnoreTags=False):
    childrenNodes = pc.listRelatives(node,children=True)
    childrenFilteredNodes = []

    for child in childrenNodes:
        if (child.type() == "transform" or child.type() == "joint") and (not filterProps or not isProperty(child)):
            curChild = child

            if useIgnoreTags and len(getParameters(curChild, containerName="OscarAttributes")) > 0:
                continue

            if not isNeutralPose(curChild):
                childrenFilteredNodes.append(curChild)

            childrenFilteredNodes.extend(getChildrenRecursively(curChild, filterNeutrals=filterNeutrals, filterProps=filterProps, useIgnoreTags=useIgnoreTags))

    return childrenFilteredNodes

def getChildren(node, recursive, filterNeutrals=True, filterProps=True, useIgnoreTags=False):
    if recursive and useIgnoreTags:
        return getChildrenRecursively(node, filterNeutrals, filterProps, useIgnoreTags)

    childrenNodes = pc.listRelatives(node,children= not recursive, allDescendents=recursive)
    childrenFilteredNodes = []

    for child in childrenNodes:
        if (child.type() == "transform" or child.type() == "joint") and (not filterProps or not isProperty(child)):
            curChild = child

            if useIgnoreTags and len(getParameters(curChild, containerName="OscarAttributes")) > 0:
                continue

            if not recursive:
                while(isNeutralPose(curChild)):
                    neutralChildren = pc.listRelatives(curChild,children=True)
                    if len(neutralChildren) > 0:
                        curChild = neutralChildren[0]
                childrenFilteredNodes.append(curChild)
            else:
                if not filterNeutrals or not isNeutralPose(curChild):
                    childrenFilteredNodes.append(curChild)

    return childrenFilteredNodes

def isChildOf(inObject, inParent, inUseNamespace=True):
    if inUseNamespace:
        return inObject.namespace() == inParent.namespace()

    return inParent in inObject.getAllParents()

def getAllParents(inObject, inConsiderConstraints=True):
    if not inConsiderConstraints:
        return inObject.getAllParents()

    curObj = inObject
    curParent = curObj.getParent()
    curCons = [c for c in getConstraints(curObj) if c.type() == "parentConstraint"]

    realParent = getConstraintTargets(curCons[0])[0] if len(curCons) > 0 else curParent

    allParents = []

    while not realParent is None:
        allParents.append(realParent)

        curObj = realParent
        curParent = curObj.getParent()
        curCons = [c for c in getConstraints(curObj) if c.type() == "parentConstraint"]
        
        realParent = getConstraintTargets(curCons[0])[0] if len(curCons) > 0 else curParent

    return allParents

def sortHierarchically(inObjects, inConsiderConstraints=True):
    levelDict = {}

    for obj in inObjects:
        if obj in levelDict:
            pass
        parents = getAllParents(obj, inConsiderConstraints=inConsiderConstraints)
        lenParents = len(parents)
        solved=False
        for i in range(lenParents):
            if parents[i] in levelDict:
                levelDict[obj] = levelDict[parents[i]]+1+i
                solved = True
                break
            else:
                levelDict[parents[i]] = lenParents - i - 1
        if not solved:
            levelDict[obj] = lenParents

    return sorted(inObjects, key=lambda o: levelDict[o])

def parent(child,parent=None, inRememberParent=False):
    firstparent = getDirectParent(child)

    #ignore NeutralPoses
    while isNeutralPose(firstparent):
        child = firstparent
        firstparent = getDirectParent(child)

    coll = child.getChildren(ad=True)
    coll.append(child)

    ns = ""

    if parent == None and not inRememberParent:
        pc.parent(child, world=True)
    else:
        if inRememberParent:
            if firstparent != None:
                parentName = firstparent.name() + OLD_PARENT_SUFFIX
                parent = getNode(parentName)
                if parent is None:
                    parent = pc.group(empty=True, name=parentName)

        if parent is None:
            pc.parent(child, world=True)
        else:
            parent.addChild(child)
            ns = parent.namespace()

    for obj in coll:
        oldNs = obj.namespace()
        if oldNs != ns:
            obj.rename(obj.swapNamespace(ns))

def reParent(inObjects):
    if len(inObjects) == 0:
        parents = pc.ls(["*:*" + OLD_PARENT_SUFFIX, "*" + OLD_PARENT_SUFFIX])
        for curParent in parents:
            children = curParent.getChildren()
            for child in children:
                if not child in inObjects:
                    inObjects.append(child) 

    for obj in inObjects:
        oldParents = pc.listRelatives(obj, parent=True)
        if oldParents != None and len(oldParents) > 0:
            oldParent = oldParents[0]
            if oldParent.endswith(OLD_PARENT_SUFFIX):
                oldParentName = oldParent[:-len(OLD_PARENT_SUFFIX)]
                obj = getNode(oldParentName)
                if not obj is None:
                    parent(obj, obj)
                    if cmds.listRelatives(oldParent.name(), children=True) == None:
                        cmds.delete(oldParent.name())
                else:
                    cmds.warning(oldParentName + " cannot be found !")

def getDirectParent(node):
    return palt.getparent(node)

def getParent(node, root=False, model=False, ignoreNeutral=True, ignoreLayers=False, ignoreBuffers=False, inRootSuffix="_Root"):
    if root and model:
        root = False

    lenRootSuffix = len(inRootSuffix)

    if root and node.name()[-lenRootSuffix:] == inRootSuffix:
        return node

    if model and node.getParent() == None:
        return node

    parentNode = getDirectParent(node)
    parentNodeParent = getDirectParent(parentNode)
    
    #ignore NeutralPoses
    if ignoreNeutral:
        while isNeutralPose(parentNode):
            parentNode = getDirectParent(parentNode)

    if ignoreLayers:
        while isLayer(parentNode):
            parentNode = getDirectParent(parentNode)

    if ignoreBuffers:
        while isBuffer(parentNode):
            parentNode = getDirectParent(parentNode)
            if ignoreNeutral:
                while isNeutralPose(parentNode):
                    parentNode = getDirectParent(parentNode)

    while (model and parentNodeParent != None) or (root and parentNode != None and parentNode.name()[-lenRootSuffix:] != inRootSuffix):
        parentNode = parentNodeParent
        if parentNode == None:
            break
        parentNodeParent = getDirectParent(parentNode)
        
    return parentNode

def getShapes(transform):
    try:
        return transform.getShapes()
    except:
        pass

    return [transform]

def getShape(inTransform):
    shapes = inTransform.getShapes()

    for shape in shapes:
        if not shape.intermediateObject.get() and shape.name().endswith("Deformed"):
            return shape

    for shape in shapes:
        if not shape.intermediateObject.get():
            return shape

    return inTransform.getShape()

def getTransform(shape ):
    if shape.type() != "transform" :
        return getDirectParent(shape)

def getDuplicatedShapes(noIntermediate=True):
    transform_shapes = {}

    for s in pc.ls(type="mesh", noIntermediate=noIntermediate):
        transformName = s.getParent().name()

        if not transformName in transform_shapes:
            transform_shapes[transformName] = []

        transform_shapes[transformName].append(s)

    duplicatedShapes = {key:value for (key,value) in transform_shapes.items() if len(value) > 1}

    return duplicatedShapes

def getProperties(node):
    children = pc.listRelatives(node, children=True)
    filteredChildren =  []
    for child in children:
        if len(child.name()) > len(node.name()):
            if child.name()[:len(node.name())] == node.name() and isProperty(child):
                filteredChildren.append(child)
    return filteredChildren

def getProperty(node, strName):
    return getNode(node + "_" + strName)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____  _               _     _           _                             _   _             
 |  _ \(_) __ _    ___ | |__ (_) ___  ___| |_ ___    ___ _ __ ___  __ _| |_(_) ___  _ __  
 | |_) | |/ _` |  / _ \| '_ \| |/ _ \/ __| __/ __|  / __| '__/ _ \/ _` | __| |/ _ \| '_ \ 
 |  _ <| | (_| | | (_) | |_) | |  __/ (__| |_\__ \ | (__| | |  __/ (_| | |_| | (_) | | | |
 |_| \_\_|\__, |  \___/|_.__// |\___|\___|\__|___/  \___|_|  \___|\__,_|\__|_|\___/|_| |_|
          |___/            |__/                                                           

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def isProperty(obj):
    if obj != None and obj.type() == "transform" and obj.getShape()==None and not CONST_NEUTRALSUFFIX in obj.name():
        parent = obj.getParent()
        if parent != None:
            parentName = obj.getParent().name()
            if len(parentName) < len(obj.name()) and obj.name()[:len(parentName)] == parentName and not obj.tx.isKeyable() and not obj.ry.isKeyable():
                return True
    return False

def isElement(obj):
    return pc.objExists("{0}_{1}".format(obj.name(), CONST_ATTRIBUTES))

def isNeutralPose(obj, inSuffix=None):
    suffix = inSuffix or CONST_NEUTRALSUFFIX
    if obj != None and obj.type() == "transform" and obj.getShape() == None:
        if obj.name().endswith(suffix):
            return True
    return False

def isLayer(obj):
    if obj != None and obj.type() == "transform" and obj.getShape() == None:
        if obj.name().endswith(CONST_LAYERSUFFIX):
            return True
    return False

def isBuffer(obj):
    if obj != None and obj.type() == "transform":
        if obj.name().endswith(CONST_BUFFERSUFFIX):
            return True
    return False

def isRoot(obj):
    if obj != None and obj.type() == "transform":
        splitNs = obj.name().split(":")
        return len(splitNs) == 2 and splitNs[0] == splitNs[1]
    return False

def find(inPatterns):
    """
    Look for an object with name matching one of the given patterns

    :param inPatterns: The possible patterns to find the object 
    :type inPatterns: list(str)
    :return: The found object or None
    :rtype: pyNode
    """
    for pattern in inPatterns:
        foundObjs = pc.ls(pattern)

        if len(foundObjs) > 0:
            return foundObjs[0]

    return None


fuckedUpLetters = ("A", "P", "Q", "e", "q")
def createText(inText, inMesh=False, inFont="Times New Roman", normalized=False):
    txtRoot = pc.textCurves(ch=0, f=inFont+"|h-20|w400|c0", t=inText)
    children = getChildren(txtRoot, False)
    space = 0.5
    if len(children) > 1:
        space = children[1].tx.get()

    width = len(inText) * space
    center = width / 2.0

    rootName = txtRoot[0]

    if not inMesh:
        pc.rename(rootName, rootName + "_Old")

        newRoot = pc.group(name=rootName, empty=True, world=True)
        newRoot.tx.set(center)
        for child in children:
            childrenCurves = getChildren(child, False)
            for childrenCurve in childrenCurves:
                pc.parent(childrenCurve, newRoot)
                pc.makeIdentity(childrenCurve, apply=True, t=1, r=1, s=0, n=0)
                pc.makeIdentity(childrenCurve, apply=False, t=1, r=1, s=1)
                pc.parent(childrenCurve.getShape(), newRoot, shape=True, add=True)
                pc.delete(childrenCurve)
            
        pc.delete(rootName + "_Old")

        if normalized:
            newRoot.sx.set(1/width)
            newRoot.sy.set(1/width)
            newRoot.t.set([0,0,0])

        return newRoot

    meshLetters = []
    counter = 0
    for child in children:
        meshLetter = pc.planarSrf(child, name="#", ch=0, tol=0.01, o=1, po=1)
        
        if inText[counter] in fuckedUpLetters:
            pc.polyNormal(meshLetter, normalMode=0, userNormalMode=0, ch=0)
        
        meshLetters.append(meshLetter)
        counter += 1
        
    mesh = pc.polyUnite(meshLetters,ch=0, mergeUVSets=0, name=inText + "_MeshText")[0]
    pc.delete(txtRoot)
    
    return mesh

def createRigObject(refObject=None, name="rigObject", type="Null", mode="child", match=False):
    if type == "Model":
        #pc.warning("No models in Maya ! Rigs will directly start with the root.")
        #pc.select(clear=True)
        if not pc.namespace(exists=name):
            pc.namespace( add=name)
        obj = pc.spaceLocator(name=name + ":" + name)
        return obj

    if "$refObject" in name:
        refObjectName = ""
        if refObject != None:
            refObjectName = refObject.name()
        name = name.replace("$refObject", refObjectName)

    name = getUniqueName(name)

    parent = refObject

    mode = mode.lower()

    if mode != "child":
        if parent == None:
            pc.Error("Cannot parent an object up the world !")
            return None

        parent = getDirectParent(parent)

    obj = None
    rootName = ""
    if parent != None:
        if isRoot(parent):
            rootName = getRigName(parent.name())
        else:
            root = getParent(parent, True)
            if root != None:
                rootName = getRigName(root.name())

    if rootName != "" and ":" in rootName:
        ns = rootName.split(":")[0] + ":"
        if not ns in name:
            name = ns + name

    #Create types
    if type == "Null" or type == "Locator" or type == "Root":
        obj = pc.spaceLocator(name=name)
        if parent != None:
            pc.parent(obj, parent)
    elif type == "Transform" or type == "Group":
        if parent == None:
            obj = pc.group(name=name, empty=True, world=True)
        else:
            obj = pc.group(name=name, empty=True, parent=parent)
    elif type == "Deformer":
        palt.clearselection()
        obj = pc.joint(name=name)
        if parent != None:
            palt.parent(obj, parent)
            #pc.parent(obj, parent)
        #Create/Add to set
        envelopeGrpName = rootName + "_Envelope" + CONST_GROUPSUFFIX
        #print "5"
        if(rootName != ""):
            #if not pc.objExists(envelopeGrpName):
            #print "6"
            if not palt.exists(envelopeGrpName):
                #print "7"
                pc.sets(name=envelopeGrpName, empty=True)
                #print "8"
            #print "9"
            pc.sets(envelopeGrpName, include=obj)
            #print "10"

    elif type == "Controller":
        #Simple "cube" from Curve
        obj = createCubeIcon(name)
        if parent != None:
            pc.parent(obj, parent)

        #Create/Add to set
        controlsGrpName = rootName + "_Controls" + CONST_GROUPSUFFIX
        if(rootName != ""):
            if not pc.objExists(controlsGrpName):
                pc.sets(name=controlsGrpName, empty=True)
            pc.sets(controlsGrpName, include=obj)
    else:
        pc.error("Unknown type " + type)
        return None

    if refObject != None:
        if match:
            matchTRS(obj, refObject)
    
        if mode == "child":
            pass
        elif mode == "parent":
            palt.parent(refObject, obj)
        elif mode == "constraining":
            pc.parentConstraint(obj, refObject, name= obj.name() + "_to_" + refObject.name() + "_prCns")
        elif mode == "constrained":
            pc.parentConstraint(refObject, obj, name= refObject.name() + "_to_" + obj.name() + "_prCns")
        else:
            pass
            #pc.error(mode + " mode doesn't exists !")
    return obj

def setObjectColor(node, color, onTransform=False):
    shapes = []

    if node.type() == "transform":
        shapes = node.getShapes()
    else:
        shapes = [node]

    if pc.versions.current() > 201600:
        for node in shapes:
            pc.setAttr(node.name() + ".overrideEnabled", 1)
            pc.setAttr(node.name() + ".overrideRGBColors", True)
            pc.setAttr(node.name() + ".overrideColorR", color[1]/255.0)
            pc.setAttr(node.name() + ".overrideColorG", color[2]/255.0)
            pc.setAttr(node.name() + ".overrideColorB", color[3]/255.0)
    else:
        mayaColorId = getNearestMayaColor(color)[0]
        for node in shapes:
            pc.setAttr(node.name() + ".overrideEnabled", 1)
            pc.setAttr(node.name() + ".overrideColor", mayaColorId)

def clearObjectColor(node):
    if node.type() == "transform":
        shape = node.getShape()
        if shape == None:
            if not onTransform:
                return
        else:
            node = shape

    pc.setAttr(node.name() + ".overrideEnabled", 0)
    pc.setAttr(node.name() + ".overrideColor", 0)

def createDisplayParams(icon, offset=(0,0,0), scale=(1,1,1), size=1.0, name="Box"):
    addParameter(icon, name="displayName", inType="string", default=name, expose=False)
    addParameter(icon, name="size", inType="double", default=size, expose=False)
    
    addParameter(icon, name="offsetDisplayX", inType="double", default=offset[0], expose=False)
    addParameter(icon, name="offsetDisplayY", inType="double", default=offset[1], expose=False)
    addParameter(icon, name="offsetDisplayZ", inType="double", default=offset[2], expose=False)

    addParameter(icon, name="scaleDisplayX", inType="double", default=scale[0], expose=False)
    addParameter(icon, name="scaleDisplayY", inType="double", default=scale[1], expose=False)
    addParameter(icon, name="scaleDisplayZ", inType="double", default=scale[2], expose=False)

    #Old parameters for updates
    addParameter(icon, name="OLDsize", inType="double", default=size, expose=False)
    
    addParameter(icon, name="OLDoffsetDisplayX", inType="double", default=offset[0], expose=False)
    addParameter(icon, name="OLDoffsetDisplayY", inType="double", default=offset[1], expose=False)
    addParameter(icon, name="OLDoffsetDisplayZ", inType="double", default=offset[2], expose=False)

    addParameter(icon, name="OLDscaleDisplayX", inType="double", default=scale[0], expose=False)
    addParameter(icon, name="OLDscaleDisplayY", inType="double", default=scale[1], expose=False)
    addParameter(icon, name="OLDscaleDisplayZ", inType="double", default=scale[2], expose=False)

def createCubeIcon(name="cvCube", offset=(0,0,0), scale=(1,1,1), size=1.0, displayName="Box"):
    points=[(-0.5, -0.5, -0.5)]
    points.append((0.5, -0.5, -0.5))
    points.append((0.5, -0.5, 0.5))
    points.append((-0.5, -0.5, 0.5))
    points.append((-0.5, -0.5, -0.5))

    points.append((-0.5, 0.5, -0.5))

    points.append((-0.5, 0.5, 0.5))
    points.append((0.5, 0.5, 0.5))
    points.append((0.5, 0.5, -0.5))
    points.append((-0.5, 0.5, -0.5))

    points.append((-0.5, 0.5, 0.5))
    points.append((-0.5, -0.5, 0.5))
    points.append((0.5, -0.5, 0.5))
    points.append((0.5, 0.5, 0.5))
    points.append((0.5, 0.5, -0.5))
    points.append((0.5, -0.5, -0.5))

    for i in range(len(points)):
        point = list(points[i])
        point[0] = point[0] * scale[0] * size + offset[0]
        point[1] = point[1] * scale[1] * size + offset[1]
        point[2] = point[2] * scale[2] * size + offset[2]
        points[i] = tuple(point)

    icon = pc.curve(d=1,p=points, name=name);

    createDisplayParams(icon, name=displayName)

    return icon

def createRingsIcon(name="cvRings", offset=(0,0,0), scale=(1,1,1), size=1.0, displayName="Rings"):
    pts = [ [0.0,0.0,-1.108],
            [0.7836, 0, -0.7836],
            [1.10819418755, 0, 0],
            [0.7836, 0, 0.7836],
            [0.0,0.0,1.108],
            [-0.7836, 0, 0.7836],
            [-1.10819418755, 0, 0],
            [-0.7836, 0, -0.7836] ]

    for i in range(len(pts)):
        point = pts[i]
        point[0] = point[0] * scale[0] * size + offset[0]
        point[1] = point[1] * scale[1] * size + offset[1]
        point[2] = point[2] * scale[2] * size + offset[2]
        pts[i] = point

    crv1 = curve(list(pts), name=name, closed=True)
    
    crv2 = curve(list(pts), name=name + "_2", closed=True)
    pc.setAttr(crv2.name() + ".rotateX", 90)
    pc.makeIdentity(crv2,apply=True, t=1, r=1, s=1, n=0)
    crvShape = crv2.getShape()
    pc.parent(crvShape, crv1, shape=True, relative=True)
    pc.delete(crv2)
   
    crv3 = curve(list(pts), name=name + "_3", closed=True)
    pc.setAttr(crv3.name() + ".rotateZ", 90)
    pc.makeIdentity(crv3,apply=True, t=1, r=1, s=1, n=0)
    crvShape = crv3.getShape()
    pc.parent(crvShape, crv1, shape=True, relative=True)
    pc.delete(crv3)

    createDisplayParams(crv1, name=displayName)

    return crv1

POINT_POSITIONS = None

def updateDisplay(node):
    global POINT_POSITIONS
    if(pc.attributeQuery( "size", node=node, exists=True )):
        unitScl = getUnitScaling()

        OLDsize = pc.getAttr(node.name() + ".OLDsize")
        OLDt = dt.Vector(pc.getAttr(node.name() + ".OLDoffsetDisplayX"),pc.getAttr(node.name() + ".OLDoffsetDisplayY"),pc.getAttr(node.name() + ".OLDoffsetDisplayZ"))
        OLDs = (pc.getAttr(node.name() + ".OLDscaleDisplayX"),pc.getAttr(node.name() + ".OLDscaleDisplayY"),pc.getAttr(node.name() + ".OLDscaleDisplayZ"))

        size = pc.getAttr(node.name() + ".size")
        t = dt.Vector(pc.getAttr(node.name() + ".offsetDisplayX"),pc.getAttr(node.name() + ".offsetDisplayY"),pc.getAttr(node.name() + ".offsetDisplayZ"))
        s = (pc.getAttr(node.name() + ".scaleDisplayX"),pc.getAttr(node.name() + ".scaleDisplayY"),pc.getAttr(node.name() + ".scaleDisplayZ"))

        if doubleBarelyEquals(size, OLDsize) and vectorBarelyEquals(t, OLDt) and listsBarelyEquals(s, OLDs):
            return

        shapes = getShapes(node)
        shape = node if len(shapes) == 0 else shapes[0]
        nodeType = pc.nodeType(shape)

        if len(shapes) > 0 or nodeType == "joint":   
            if nodeType == "locator":
                shape = shapes[0]
                pc.setAttr(shape.name() + ".localPositionX", t.x * size)
                pc.setAttr(shape.name() + ".localPositionY", t.y * size)
                pc.setAttr(shape.name() + ".localPositionZ", t.z * size)

                pc.setAttr(shape.name() + ".localScaleX", s[0] * size * (1/unitScl))
                pc.setAttr(shape.name() + ".localScaleY", s[1] * size * (1/unitScl))
                pc.setAttr(shape.name() + ".localScaleZ", s[2] * size * (1/unitScl))
            elif nodeType == "nurbsCurve":
                for shape in shapes:
                    #getPoints transformed by "old" values

                    # sl = om.MGlobal.getSelectionListByName(shape.name())
                    # omNode = sl.getDependNode(0)
                    # mFnSet = om.MFnNurbsCurve(omNode)
                    # cvs = mFnSet.cvPositions()
                    cvs = tkApi.getPointPositions(shape.name())
                    newCvs = []

                    #setPoints transformed by "new" values
                    for cv in cvs:
                        newCvs.append((
                            size * (s[0] * ((cv[0] / OLDsize - OLDt.x * unitScl) / OLDs[0]) + t.x * unitScl),
                            size * (s[1] * ((cv[1] / OLDsize - OLDt.y * unitScl) / OLDs[1]) + t.y * unitScl),
                            size * (s[2] * ((cv[2] / OLDsize - OLDt.z * unitScl) / OLDs[2]) + t.z * unitScl)
                            ))
                    POINT_POSITIONS = newCvs
                    pc.setPointPositions(shape.name())
                    POINT_POSITIONS = None
                    # mFnSet.setCVPositions(newCvs)
                    # mFnSet.updateCurve()

            elif nodeType == "joint":
                pc.setAttr(node.name() + ".radius", size * unitScl)
            else:
                pc.warning("Displays can't affect objects of type : " + nodeType)

            #Update parameters
            pc.setAttr(node.name() + ".OLDsize", size)
            pc.setAttr(node.name() + ".OLDoffsetDisplayX", t.x)
            pc.setAttr(node.name() + ".OLDoffsetDisplayY", t.y)
            pc.setAttr(node.name() + ".OLDoffsetDisplayZ", t.z)

            pc.setAttr(node.name() + ".OLDscaleDisplayX", s[0])
            pc.setAttr(node.name() + ".OLDscaleDisplayY", s[1])
            pc.setAttr(node.name() + ".OLDscaleDisplayZ", s[2])

def getDisplay(node):
    unitScl = getUnitScaling()

    decorated = False
    t = dt.Vector(0.0,0.0,0.0)
    r = dt.EulerRotation(0.0,0.0,0.0)
    s = (1.0,1.0,1.0)
    size = 1.0
    name = "Box"
    shape = None

    if(pc.attributeQuery( "size", node=node, exists=True )):
        decorated = True
        size = node.radius.get() if node.type() == "joint" else node.OLDsize.get()
        t = dt.Vector(pc.getAttr(node.name() + ".OLDoffsetDisplayX"),pc.getAttr(node.name() + ".OLDoffsetDisplayY"),pc.getAttr(node.name() + ".OLDoffsetDisplayZ"))
        s = (pc.getAttr(node.name() + ".OLDscaleDisplayX"),pc.getAttr(node.name() + ".OLDscaleDisplayY"),pc.getAttr(node.name() + ".OLDscaleDisplayZ"))
        if pc.attributeQuery( "displayName", node=node, exists=True ):
            name = pc.getAttr(node.name() + ".displayName")
        else:
            addParameter(node, name="displayName", inType="string", default=name, expose=False)

    shapes = getShapes(node)
    if len(shapes) > 0:
        shape = shapes[0]
        nodeType = pc.nodeType(shape)

        if nodeType == "locator":
            if not decorated:
                t.x = pc.getAttr(shape.name() + ".localPositionX")
                t.y = pc.getAttr(shape.name() + ".localPositionY")
                t.z = pc.getAttr(shape.name() + ".localPositionZ")

                s0 = pc.getAttr(shape.name() + ".localScaleX") * unitScl
                s1 = pc.getAttr(shape.name() + ".localScaleY") * unitScl
                s2 = pc.getAttr(shape.name() + ".localScaleZ") * unitScl

                s = (s0, s1, s2)

        if nodeType == "joint":
            if not decorated:
                size = pc.getAttr(shape.name() + ".radius") / unitScl

    if not decorated:
        createDisplayParams(node, (t.x,t.y,t.z), (s[0],s[1],s[2]), size, name)

    return ([t,r,s], size, name)

def setDisplay(node, trs=(dt.Vector(0.0,0.0,0.0), dt.EulerRotation(0.0,0.0,0.0), (1.0,1.0,1.0)), size=1.0, select=False, displayName="Box"):
    if(not pc.attributeQuery( "size", node=node, exists=True )):
        getDisplay(node)

    if size == 0:
        size = 0.001

    if 0 in trs[2]:
        sclList = list(trs[2])
        if sclList[0] == 0:
            sclList[0] = 0.001
        if sclList[1] == 0:
            sclList[1] = 0.001
        if sclList[2] == 0:
            sclList[2] = 0.001
        trs = (trs[0], trs[1], tuple(sclList))

    if displayName != "":
        if pc.attributeQuery( "displayName", node=node, exists=True ):
            pc.setAttr(node.name() + ".displayName", displayName)
        else:
            addParameter(node, name="displayName", inType="string", default=displayName, expose=False)

    pc.setAttr(node.name() + ".size", size)

    pc.setAttr(node.name() + ".offsetDisplayX", trs[0].x)
    pc.setAttr(node.name() + ".offsetDisplayY", trs[0].y)
    pc.setAttr(node.name() + ".offsetDisplayZ", trs[0].z)

    pc.setAttr(node.name() + ".scaleDisplayX", trs[2][0])
    pc.setAttr(node.name() + ".scaleDisplayY", trs[2][1])
    pc.setAttr(node.name() + ".scaleDisplayZ", trs[2][2])
    updateDisplay(node)

    if select :
        pc.select(node, replace=True)
        

def closestPoint(inMesh, inPositions=[0.0, 0.0, 0.0], inKeepNode=False):
    #print "closestPoint(", inMesh, inPositions, inKeepNode
    inTransform = inMesh
    
    if inMesh.type() == "transform":
        inMesh = inMesh.getShape()
    else:
        inTransform = inMesh.getParent()

    isMesh = inMesh.type() == "mesh"

    closestNode = pc.createNode("closestPointOnMesh" if isMesh else "closestPointOnSurface", name=inMesh.name() + "_closestPoint")
    pc.connectAttr(inMesh.name() + (".outMesh" if isMesh else ".worldSpace[0]"), closestNode.name() + (".inMesh" if isMesh else ".inputSurface"))
    
    #print "closestNode",closestNode

    #Very stupid trick to get "object space" tranformations
    loc = pc.group(name="ObjectSpaceGetter",empty=True)
    pc.setAttr(loc.name() + ".tx", inPositions[0])
    pc.setAttr(loc.name() + ".ty", inPositions[1])
    pc.setAttr(loc.name() + ".tz", inPositions[2])
    
    pc.parent(loc, inTransform)
    
    pc.setAttr(closestNode.name() + ".inPositionX", pc.getAttr(loc.name() + ".tx"))
    pc.setAttr(closestNode.name() + ".inPositionY", pc.getAttr(loc.name() + ".ty"))
    pc.setAttr(closestNode.name() + ".inPositionZ", pc.getAttr(loc.name() + ".tz"))

    pc.delete(loc)

    closestValues = {}
    
    closestValues["position"] = (closestNode.positionX.get(), closestNode.positionY.get(), closestNode.positionZ.get())
    closestValues["u"] = closestNode.parameterU.get()
    closestValues["v"] = closestNode.parameterV.get()

    if isMesh:
        closestValues["normal"] = (closestNode.normalX.get(), closestNode.normalY.get(), closestNode.normalZ.get())
        closestValues["face"] = closestNode.closestFaceIndex.get()
        closestValues["vertex"] = closestNode.closestVertexIndex.get()
    """
    else:
        #spans = inMesh.spansUV.get()

        rangeU = inMesh.mmu.get()
        rangeU = rangeU[1] - rangeU[0]

        rangeV = inMesh.mmv.get()
        rangeV = rangeV[1] - rangeV[0]

        if rangeU != 1.0:
            closestValues["u"] /= rangeU

        if rangeV != 1.0:
            closestValues["v"] /= rangeV
    """
    if not inKeepNode:
        pc.delete(closestNode)

    return closestValues

def constrainToPoint(inObj, inRef, inOffset=True, inU=None, inV=None, useFollicule=True, inEnsureAttachment=True, inDetectionOffset=[0.0, 0.0, 0.0]):

    createdObjects = []

    if inU == None or inV == None:
        wt = inObj.getTranslation(space="world")
        closestInfo = closestPoint(inRef, [wt[0] + inDetectionOffset[0], wt[1] + inDetectionOffset[1], wt[2] + inDetectionOffset[2]])
        if inU == None:
            inU = closestInfo['u']
        if inV == None:
            inV = closestInfo['v']

    cnsObj = inObj
    if inOffset and not useFollicule:
        parentObj = inObj.getParent()
        if parentObj != None:
            cnsObj = pc.group(empty=True, parent=parentObj, name=inObj.name() +"_polyCnsOffset")
        else:
            cnsObj = pc.group(empty=True, world=True, name=inObj.name() +"_polyCnsOffset")
        
        createdObjects.append(cnsObj.name())
    
    if useFollicule:
        geoMesh = inRef.getShape()
        isMesh = geoMesh.type() == "mesh"
        if isMesh:
            
             # creat follicle
            fol = pc.createNode( 'follicle', name=inObj +'_to_'+inRef.stripNamespace()+'_fol' )

            # let's do a dirty special case for forollicles applied in the case of a geoContrainer
            #Spere_GeoCons:GeoConstrainer_Constrained_Output
            #Spere_GeoCons:GeoConstrainer_Root_RigParameters

            if inObj.name().endswith("_Constrained_Output") and pc.objExists(inObj.name().replace("_Constrained_Output", "_Root_RigParameters")):
                rigName = inObj.stripNamespace()[:-19]
                rigParamsName = inObj.name().replace("_Constrained_Output", "_Root_RigParameters")

                offsetUNode = pc.createNode( 'addDoubleLinear', name='fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_addU")
                offsetUNode.input1.set(inU)
                pc.connectAttr(rigParamsName + "." + rigName + "_OffsetU", offsetUNode.input2)
                offsetUNode.output >> fol.parameterU

                offsetVNode = pc.createNode( 'addDoubleLinear', name='fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_addV")
                offsetVNode.input1.set(inV)
                pc.connectAttr(rigParamsName + "." + rigName + "_OffsetV", offsetVNode.input2)
                offsetVNode.output >> fol.parameterV
            else:
                fol.parameterU.set( inU )
                fol.parameterV.set( inV )

            geoMesh = inRef.getShape()

            folP = fol.getParent()

            folName = inObj.namespace() + 'fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_polyCnsOffset"

            parentObj = None

            update=False
            output_trans = None
            if pc.objExists(folName):
                update = True
                output_trans = pc.xform(inObj, query=True, worldSpace=True, matrix=True )

                oldFolP = folP

                folP = getNode(folName)

                folP.addChild(fol, shape=True, add=True)
                cmds.parent(oldFolP.getShape().name(), shape=True, removeObject=True)
                fol = folP.getShape()
                pc.delete(oldFolP)

                parentObj = folP.getParent()
            else:
                folP.rename(folName)

                parentObj = inObj.getParent()

            geoMesh.outMesh >> fol.inputMesh
            multMatrix = pc.createNode( 'multMatrix', name='fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_multMatrix")
            geoMesh.worldMatrix[0] >> multMatrix.matrixIn[0]
            parentObj.worldInverseMatrix[0] >> multMatrix.matrixIn[1]
            multMatrix.matrixSum >> fol.inputWorldMatrix
            fol.outTranslate >> folP.translate
            fol.outRotate >> folP.rotate

            createdObjects.append(fol)

            if not update:
                pc.parent(folP, inObj.getParent())
                pc.parent(inObj, folP)
        else:
            # creat non follicle system
            folP = pc.createNode("transform")
            fol = pc.createNode("pointOnSurfaceInfo", name=inObj +'_to_'+inRef.stripNamespace()+'_fol')
            folP.addAttr("useVDirection", at="bool", k=True)
            folP.addAttr("parameterU", at="float", k=True)
            folP.addAttr("parameterV", at="float", k=True)

            if inObj.name().endswith("_Constrained_Output") and pc.objExists(inObj.name().replace("_Constrained_Output", "_Root_RigParameters")):
                rigName = inObj.stripNamespace()[:-19]
                rigParamsName = inObj.name().replace("_Constrained_Output", "_Root_RigParameters")

                offsetUNode = pc.createNode( 'addDoubleLinear', name='fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_addU")
                offsetUNode.input1.set(inU)
                pc.connectAttr(rigParamsName + "." + rigName + "_OffsetU", offsetUNode.input2)
                offsetUNode.output >> folP.parameterU

                offsetVNode = pc.createNode( 'addDoubleLinear', name='fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_addV")
                offsetVNode.input1.set(inV)
                pc.connectAttr(rigParamsName + "." + rigName + "_OffsetV", offsetVNode.input2)
                offsetVNode.output >> folP.parameterV
            else:
                folP.parameterU.set(inU)
                folP.parameterV.set(inV)
            
            geoMesh = inRef.getShape()
            parentObj = None            

            # Node Created :
            geoMesh.worldSpace[0] >> fol.inputSurface
            fourByFourMatrix = pc.createNode("fourByFourMatrix", name = 'fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_fourByFourMatrix")
            multMatrix = pc.createNode('multMatrix', name='fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_multMatrix")
            decomposeMatrix = pc.createNode("decomposeMatrix",name='fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_decompMatrix" )

            conditionU = pc.createNode("condition", name = 'fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_condtionU")
            conditionV = pc.createNode("condition", name = 'fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_condtionV")
            folP.useVDirection >> conditionU.firstTerm
            folP.useVDirection >> conditionV.firstTerm

            fol.positionX >> fourByFourMatrix.in30
            fol.positionY >> fourByFourMatrix.in31
            fol.positionZ >> fourByFourMatrix.in32
            fol.normalizedNormalX >> fourByFourMatrix.in10
            fol.normalizedNormalY >> fourByFourMatrix.in11
            fol.normalizedNormalZ >> fourByFourMatrix.in12

            fol.normalizedTangentU >> conditionU.colorIfFalse
            fol.normalizedTangentV >> conditionU.colorIfTrue
            fol.normalizedTangentU >> conditionV.colorIfTrue
            fol.normalizedTangentV >> conditionV.colorIfFalse

            conditionV.outColorR >> fourByFourMatrix.in00
            conditionV.outColorG >> fourByFourMatrix.in01
            conditionV.outColorB >> fourByFourMatrix.in02
            conditionU.outColorR >> fourByFourMatrix.in20
            conditionU.outColorG >> fourByFourMatrix.in21
            conditionU.outColorB >> fourByFourMatrix.in22

            fourByFourMatrix.output >> multMatrix.matrixIn[0]
            folP.parentInverseMatrix >> multMatrix.matrixIn[1]
            multMatrix.matrixSum >> decomposeMatrix.inputMatrix
            decomposeMatrix.outputRotate >> folP.rotate
            decomposeMatrix.outputTranslate >> folP.translate

            update = False
            output_trans = None
            folName = inObj.namespace() + 'fol_'+inObj.stripNamespace() +'_to_'+inRef.stripNamespace() + "_polyCnsOffset"
            folP.parameterU >> fol.parameterU
            folP.parameterV >> fol.parameterV

            if pc.objExists(folName):
                oldFolP = getNode(folName)
                output_trans = pc.xform(inObj, query=True, worldSpace=True, matrix=True )
                pc.parent(folP, oldFolP.getParent())
                pc.parent(inObj, folP)
                pc.delete(oldFolP)
                folP.rename(folName)
                parentObj = folP.getParent()
                update = True
            else:
                folP.rename(folName)
                parentObj = folP.getParent()

            if not update:
                pc.parent(folP, inObj.getParent())
                pc.parent(inObj, folP)
            if not inOffset:
                resetTRS(inObj)
            else:
                if not output_trans is None:
                    pc.xform(inObj, ws=True, matrix= output_trans)

                    constraints = getConstraints(inObj)

                    for constraint in constraints:
                        if constraint.type() == "orientConstraint":
                            constraint.restRotate.set(ozms.getPymelRotation(inObj))
            createdObjects.append(folP)

        if not inOffset:
            resetTRS(inObj)
        else:
            if not output_trans is None:
                pc.xform( inObj, worldSpace=True, matrix=output_trans )

            constraints = getConstraints(inObj)

            for constraint in constraints:
                if constraint.type() == "orientConstraint":
                    constraint.restRotate.set(ozms.getPymelRotation(inObj))

        cnsObj = folP
    else:
        cns = pc.pointOnPolyConstraint(inRef, cnsObj)
        createdObjects.append(cns)
        
        pc.setAttr(cns + ".%sU0" % inRef.stripNamespace().split("|")[-1], inU)
        pc.setAttr(cns + ".%sV0" % inRef.stripNamespace().split("|")[-1], inV)
    
    if inOffset and not useFollicule:
        pc.parent(inObj, cnsObj)

    if inEnsureAttachment and listsBarelyEquals(cnsObj.getTranslation(space="world"), [0.0, 0.0, 0.0]):
        removeAllCns(inObj, inTypes=["follicle"] if useFollicule else ["pointOnPolyConstraint"])

        tkLogger.debug(tc.smartJoin("Does not attach with values",inDetectionOffset))

        if inDetectionOffset == [0.0, 0.0, 0.0]:
            inDetectionOffset = [0.0001, 0.0001, 0.0001]
        else:
            inDetectionOffset = [2*v for v in inDetectionOffset]

        if inDetectionOffset[0] > 0.01:
            tkLogger.warning("Follicle attachement failed, check your UVs and UVsets, or export/reimport as obj...")
            return createdObjects
        
        createdObjects = constrainToPoint(inObj, inRef, inOffset=inOffset, useFollicule=useFollicule, inDetectionOffset=inDetectionOffset)

    return createdObjects

def getExternalConstraints(inRoot, inSource=True, inDestination=False, returnObjects=False, inReturnAll=False, inProgress=False):
    cnsAll = []
    externalTargets = []

    if not isinstance(inRoot,(list,tuple)):
        inRoot = [inRoot]

    allChildren = []
    for root in inRoot:
        allChildren.extend(root.getChildren(allDescendents=True, type="transform"))
    allChildren.extend(inRoot)

    if len(allChildren) > 0:
        gMainProgressBar = None

        if inProgress:
            gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

            pc.progressBar( gMainProgressBar,
            edit=True,
            beginProgress=True,
            isInterruptable=True,
            status="Walking contraints",
            maxValue=len(allChildren))

        allChildrenStr = [n.name() for n in allChildren]

        for child in allChildren:
            targets = []

            if inSource:
                constraints = getConstraintsUsing(child)
                for constraint in constraints:
                    for target in getConstraintOwner(constraint):
                        targets.append((target, constraint))
            if inDestination:
                constraints = getConstraints(child)
                for constraint in constraints:
                    for target in getConstraintTargets(constraint):
                        targets.append((target, constraint))

            targets = list(set(targets))
            cnsAll.extend(targets)

            filteredTargets = []
            for target in targets:
                if not target[0].name() in allChildrenStr:
                    filteredTargets.append(target)

            externalTargets.extend(filteredTargets)

            if inProgress:
                pc.progressBar(gMainProgressBar, edit=True, step=1)

        if inProgress:
            pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    returnList = []

    if returnObjects:
        returnList.append(list(set([t[0] for t in externalTargets])))

    if inReturnAll:
         returnList.append(list(set([t[1] for t in cnsAll])))

    if len(returnList) == 0:
         return list(set([t[1] for t in externalTargets]))

    returnList.insert(0, list(set([t[1] for t in externalTargets])))

    return returnList

def getExternalLinks(inRoot, inChildren=True, inSource=True, inDestination=True, inManaged=None, inAllChildren=None):
    CONSTRAINT_TYPES = ["parentConstraint", "pointConstraint", "scaleConstraint", "orientConstraint", "aimConstraint"]

    if not inManaged:
        inManaged = []

    extInputs = []
    extOutputs = []

    if not isinstance(inRoot,(list,tuple)):
        inRoot = [inRoot]

    allChildren = []
    if inChildren:
        for root in inRoot:
            allChildren.extend(root.getChildren(allDescendents=True, type="transform"))
    allChildren.extend(inRoot)

    inManagedBefore = inManaged[:]

    for child in allChildren:
        if child.type() in CONSTRAINT_TYPES:
            continue

        if inSource:
            cons = child.listConnections(source=True, destination=False, plugs=True, connections=True)
            for con in cons:
                if con[1].node().type() in CONSTRAINT_TYPES:
                    continue

                if con[1].node().type() == "transform" and con[1].node() in (inAllChildren or allChildren):
                    continue

                if con[1].node() in inManaged:
                    continue

                inManaged.append(con[1].node())

                if con[1].node().type() == "transform":
                    extInputs.append(con)
                else:
                    ins, outs = getExternalLinks(con[1].node(), inChildren=False, inSource=True, inDestination=False, inManaged=inManaged, inAllChildren=(inAllChildren or allChildren))
                    for curin in ins:
                        extInputs.append(curin)
                    for out in outs:
                        extOutputs.append(out)

        if inDestination:
            cons = child.listConnections(source=False, destination=True, plugs=True, connections=True)
            for con in cons:
                if con[1].node().type() in CONSTRAINT_TYPES:
                    continue

                if con[1].node().type() == "transform" and con[1].node() in  (inAllChildren or allChildren):
                    continue

                if con[1].node() in inManagedBefore:
                    continue

                inManagedBefore.append(con[1].node())
                if not con[1].node() in inManaged:
                    inManaged.append(con[1].node())

                if con[1].node().type() == "transform":
                    extOutputs.append(con)
                else:
                    ins, outs = getExternalLinks(con[1].node(), inChildren=False, inSource=False, inDestination=True, inManaged=inManaged, inAllChildren=(inAllChildren or allChildren))

    return (extInputs, extOutputs)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ____                _             _       _       
  / ___|___  _ __  ___| |_ _ __ __ _(_)_ __ | |_ ___ 
 | |   / _ \| '_ \/ __| __| '__/ _` | | '_ \| __/ __|
 | |__| (_) | | | \__ \ |_| | | (_| | | | | | |_\__ \
  \____\___/|_| |_|___/\__|_|  \__,_|_|_| |_|\__|___/
                                                     
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def getConstraintTargets(inCons):
    targets = []
    if inCons.type() == "motionPath":
        cons = pc.listConnections(inCons.name() + ".geometryPath")
        if len(cons) > 0:
            targets.append(cons[0])
    elif inCons.type() == "follicle":
        cons = pc.listConnections(inCons.name() + ".inputMesh")
        if len(cons) > 0:
            targets.append(cons[0])
    elif inCons.type() == "decomposeMatrix":
        cons = pc.listHistory(inCons, type="nurbsSurface")
        if len(cons) > 0:
            targets.append(cons[0])
    else:
        targets = [c.node() for c in pc.listConnections(inCons.name() + ".target", destination=False, type=["transform","joint","mesh","ikEffector"], exactType=True, plugs=True) if "matrix" in c.name().lower()]

    cleanedTargets = []
    for source in targets:
        if not source in cleanedTargets:
            if source.type() == "mesh" or source.type() == "nurbsSurface":
                source = source.getParent()
            cleanedTargets.append(source)

    return cleanedTargets

def getConstraintOwner(inCons):
    targets=[]
    consType = inCons.type()

    if consType == "motionPath":
        targets = inCons.allCoordinates.listConnections()

    elif consType == "follicle":
        targets = inCons.outTranslate.listConnections()
        targets = [t.getChildren(type="transform")[0] if t.name().endswith("_polyCnsOffset") else t for t in targets]

    elif pc.objExists(inCons + ".constraintTranslateX"):
        targets = pc.listConnections(inCons + ".constraintTranslateX")
        if len(targets) == 0:
            targets = pc.listConnections(inCons + ".constraintTranslate")
            if len(targets) == 0 and pc.objExists(inCons + ".constraintRotateX"):
                targets = pc.listConnections(inCons + ".constraintRotateX")
                if len(targets) == 0:
                    targets = pc.listConnections(inCons + ".constraintRotate")
    elif pc.objExists(inCons + ".constraintRotateX"):
        targets = pc.listConnections(inCons + ".constraintRotateX")
        if len(targets) == 0:
            targets = pc.listConnections(inCons + ".constraintRotate")
    elif pc.objExists(inCons + ".constraintScaleX"):
        targets = pc.listConnections(inCons + ".constraintScaleX")
    else:
        pc.warning("Can't find " + inCons.name() + " connection !" )

    return targets

def getConstraintsUsing(inObject):
    filteredConstraints = []
    filteredNames = []

    constraints = pc.listConnections(inObject.attr("parentMatrix"), source=False, type=["constraint", "motionPath"])

    #In case of motionTrail the "cns" is on the shape
    shapes = getShapes(inObject)
    if len(shapes) > 0:
        if shapes[0].type() == "nurbsCurve":
            motionPathCons = pc.listConnections(shapes[0], source=False, type=["motionPath"])
            if len(motionPathCons) > 0:
                constraints.extend(motionPathCons)
        if shapes[0].type() == "mesh":
            folliclesPlugs = pc.listConnections(shapes[0], source=False, type=["follicle"], plugs=True)
            if len(folliclesPlugs) > 0:
                constraints.extend([f.node() for f in folliclesPlugs])

    for cons in constraints:
        if not cons.name() in filteredNames:
            filteredNames.append(cons.name())
            filteredConstraints.append(cons)

    return filteredConstraints

def getConstraints(inObject):
    filteredConstraints = []
    filteredNames = []

    constraints = pc.listConnections(inObject, destination=False, type=["constraint", "motionPath"])
    objParent = inObject.getParent()
    if objParent != None and objParent.name().endswith("_polyCnsOffset"):
        shape = objParent.getShape()
        if shape != None and shape.type() == "follicle":
            constraints.append(shape)
        elif objParent.hasAttr("useVDirection"):
            constraints.append(pc.listConnections(objParent, destination=False)[0])
        else:
            constraints.extend(pc.listConnections(objParent, destination=False, type=["constraint", "motionPath"]))

    # CBB :filteredConstraints = list(set(constraints))
    for cons in constraints:
        if not cons.name() in filteredNames:
            filteredNames.append(cons.name())
            filteredConstraints.append(cons)
    '''
    constraints = pc.ls(type="constraint")
    for cons in constraints:
        targets=[]
        if pc.objExists(cons + ".constraintTranslateX"):
            targets = pc.listConnections(cons + ".constraintTranslateX")
        elif pc.objExists(cons + ".constraintRotateX"):
            targets = pc.listConnections(cons + ".constraintRotateX")
        elif pc.objExists(cons + ".constraintScaleX"):
            targets = pc.listConnections(cons + ".constraintScaleX")
        else:
            pc.warning("Can't find " + cons.name() + " connection !" )

        for target in targets:
            if inObject.name() == target.name():
                filteredConstraints.append(cons)
                break

    motionPaths = pc.ls(type="motionPath")
    '''

    return filteredConstraints

#DEPRECATE
def getExternalConstraintsOnHierarchy(inRoot):
    externalCns = []
    children = getChildren(inRoot, True)
    for child in children:
        cns = getConstraintsUsing(child)
        for cn in cns:
            targets = getConstraintOwner(cn)
            for target in targets:
                if not isChildOf(target, inRoot, inUseNamespace=False):
                    externalCns.append(cn)
                    break
    return externalCns

def selectConstraining(inObj):
    constraining = []
    cns = getConstraints(inObj)
    for c in cns:
        targets = getConstraintTargets(c)
        for target in targets:
            if not target.longName() in constraining:
                constraining.append(target.longName())
    if len(constraining) > 0 :
        pc.select(constraining, replace=True)
    else:
        pc.select(clear=True)

def removeAllCns(inObj, inTypes=None):
    cns = getConstraints(inObj)
    for c in cns:
        typ = c.type()

        if not inTypes is None and not typ in inTypes:
            continue

        try:
            pc.delete(c)
        except:
            pass

        if typ == "follicle":
            par = inObj.getParent()

            #Try this as we may be in reference...
            try:
                par.getParent().addChild(inObj)
                pc.delete(par)
            except:
                pass

def selectConstrained(inObj):
    constrained = []
    cns = getConstraintsUsing(inObj)
    for c in cns:
        targets = getConstraintOwner(c)
        for target in targets:
            if not target.longName() in constrained:
                constrained.append(target.longName())
    if len(constrained) > 0 :
        pc.select(constrained, replace=True)
    else:
        pc.select(clear=True)

def compensateCns(inObj, doubleIt=False):
    constraints = getConstraints(inObj)
    for cons in constraints:
        constraintTargets = getConstraintTargets(cons)
        if len(constraintTargets) == 0:
            pc.error("Constraint " + cons + " on " + inObj.name() + " returned no targets !!")
        
        constraintTargets.append(cons)
        
        if cons.type() == "parentConstraint":
            pc.parentConstraint(*constraintTargets, edit=True, maintainOffset=True)
            if doubleIt:
                pc.parentConstraint(*constraintTargets, edit=True, maintainOffset=True)
        if cons.type() == "pointConstraint":
            pc.pointConstraint(*constraintTargets, edit=True, maintainOffset=True)
            if doubleIt:
                pc.pointConstraint(*constraintTargets, edit=True, maintainOffset=True)
        if cons.type() == "orientConstraint":
            pc.orientConstraint(*constraintTargets, edit=True, maintainOffset=True)
            if doubleIt:
                pc.orientConstraint(*constraintTargets, edit=True, maintainOffset=True)
        if cons.type() == "aimConstraint":
            pc.aimConstraint(*constraintTargets, edit=True, maintainOffset=True)
            if doubleIt:
                pc.aimConstraint(*constraintTargets, edit=True, maintainOffset=True)
        if cons.type() == "scaleConstraint":
            pc.scaleConstraint(*constraintTargets, edit=True, maintainOffset=True)
            if doubleIt:
                pc.scaleConstraint(*constraintTargets, edit=True, maintainOffset=True)

def pathConstrain(inObject, inSource, tangent=True, parametric=False, addPercent=True):
    name = inObject.name() + "_to_" + inSource.name() + "_pathCns"
    curveShapes = getShapes(inSource)
    if len(curveShapes) == 0 or curveShapes[0].type() != "nurbsCurve":
        pc.warning("Given source (%s) don't have a nurbsCurve shape !" % inSource.name())
        return None

    curveShape = curveShapes[0]

    #Create motion path node
    #We have to create with pathAnimation command to be able to change "parametric" attribute...
    motionPathNode = pc.pathAnimation(inObject, c=curveShape, name=name, follow=tangent, fractionMode=not parametric)
    motionPathNode = getNode(motionPathNode)

    #Disconnect all
    cons = set(pc.listConnections(motionPathNode))
    for con in cons:
        if con.exists() and con.name() != inObject.name() and con.name() != inSource.name():
            pc.delete(con)

    if addPercent:
        pcAttrName = addParameter(motionPathNode, name="percent", inType="double", default=0.0, min=0.0, max = 100.0)
        md1 = pc.createNode("multiplyDivide", name=name + "_Mult1")
        pc.setAttr(md1.name() + ".input2X", 0.01)
        pc.connectAttr(pcAttrName, md1.name() + ".input1X", force=True)
        if parametric:
            md2 = pc.createNode("multiplyDivide", name=name + "_Mult2")
            pc.connectAttr( md1.name() + ".outputX", md2.name() + ".input1X", force=True)
            pc.connectAttr( curveShape.name() + ".spans", md2.name() + ".input2X", force=True)
            pc.connectAttr( md2.name() + ".outputX", motionPathNode.name() + ".uValue", force=True)
        else:
            pc.connectAttr( md1.name() + ".outputX", motionPathNode.name() + ".uValue", force=True)

    #Connect inObject to motion path
    pc.connectAttr(motionPathNode.name() + ".allCoordinates", inObject.name() + ".translate", force=True)

    return motionPathNode

def unpinAll(*args):
    pins = pc.ls(["*:*_PinIntoPosition","*_PinIntoPosition"], transforms=True)

    for pin in pins:
        cns = getConstraintsUsing(pin)
        for c in cns:
            targets = getConstraintOwner(c)
            for target in targets:
                compensateCns(target)
            pc.delete(c)
        pc.delete(pin)

def constrain(inObject, inSource, inType="Pose", inOffset=True, inAdditionnalArg=True, globalScalingFix=True):
    contraint = None

    matcher = None
    if globalScalingFix and (inType=="Pose" or inType=="parentConstraint"or inType=="parent") and (hasZeroedScaling(inSource) != hasZeroedScaling(inObject)):
        refObj = None
        if inOffset:
            refObj = inObject
        else:
            refObj = inSource
        matcher = [refObj.getTranslation(space=WORLDSPACE), ozms.getPymelRotation(refObj, space=WORLDSPACE), refObj.getScale()]

    if inType == "Pin":
        pinName = inObject.name() + "_PinIntoPosition"
        pinObj = getNode(pinName)
        if not pinObj is None:
            cns = getConstraintsUsing(pinObj)
            compensateCns(inObject)
            pc.delete(cns)
            pc.delete(pinObj)
        else:
            storeSelection()
            rigObj = createRigObject(None, pinName, "Transform", mode="child" )

            pos = inObject.getTranslation(space="world")
            annotation = pc.annotate(inObject, point=[pos[0], pos[1]+5, pos[2]], text="Pined !") 

            pc.parent(annotation.getParent(), rigObj)

            loadSelection()
            try:
                contraint = pc.parentConstraint(rigObj,inObject, name=getUniqueName(inObject.name() + "_pinCns"), maintainOffset=True)
                pc.setAttr(contraint.name() + ".interpType", TK_INTERP)
            except:
                pass

            try:
                pc.scaleConstraint(rigObj,inObject, name=getUniqueName(inObject.name() + "_pinsCns"), maintainOffset=True)
            except:
                pass
    else:
        name = inObject.name() + "_to_" + inSource.stripNamespace()

        if inType == "Pose" or inType == "parentConstraint"  or inType == "parent":
            contraint = pc.parentConstraint(inSource,inObject, name=getUniqueName(name + "_prCns"), maintainOffset=inOffset)
            pc.setAttr(contraint.name() + ".interpType", TK_INTERP)
        elif inType == "Position" or inType == "pointConstraint"  or inType == "point":
            contraint = pc.pointConstraint(inSource,inObject, name=getUniqueName(name + "_pCns"), maintainOffset=inOffset)
        elif inType == "Orientation" or inType == "orientConstraint"  or inType == "orient":
            contraint = pc.orientConstraint(inSource,inObject, name=getUniqueName(name + "_oCns"), maintainOffset=inOffset)
            pc.setAttr(contraint.name() + ".interpType", TK_INTERP)
        elif inType == "Direction" or inType == "aimConstraint"  or inType == "aim":
            contraint = pc.aimConstraint(inSource,inObject, name=getUniqueName(name + "_aCns"), maintainOffset=inOffset)
            if inAdditionnalArg != False and inAdditionnalArg != True:
                pc.setAttr(contraint.name() + ".worldUpType", 1)
                pc.connectAttr(inAdditionnalArg + ".worldMatrix[0]", contraint.name() + ".worldUpMatrix")
        elif inType == "Scaling" or inType == "Scale" or inType == "scaleConstraint"  or inType == "scale":
            contraint = pc.scaleConstraint(inSource,inObject, name=getUniqueName(name + "_sCns"), maintainOffset=inOffset)
        elif inType == "Path" or inType == "pathConstraint"  or inType == "path":
            contraint = pathConstrain(inObject, inSource, inOffset, inAdditionnalArg)
        elif inType.lower() == "surface" or inType.lower() == "mesh" or inType.lower() == "pointonpoly" or inType.lower() == "follicle":
            u = None
            v = None
            if inAdditionnalArg != False and inAdditionnalArg != True and isinstance(inAdditionnalArg, tuple) or isinstance(inAdditionnalArg, list):
                u = inAdditionnalArg[0]
                v = inAdditionnalArg[1]
                if len(inAdditionnalArg) > 2:
                    inAdditionnalArg = inAdditionnalArg[2]
                else:
                    inAdditionnalArg = True

            contraint = constrainToPoint(inObject, inSource, inOffset, u, v, inAdditionnalArg)[-1]

    if matcher != None:
        #print "Global scaling fix applied on %s" % inObject.name()
        inObject.setTranslation(matcher[0], space=WORLDSPACE)
        inObject.setRotation(matcher[1], space=WORLDSPACE)
        inObject.setScale(matcher[2])
        compensateCns(inObject, True)

    return contraint

def getCnsOffset(inCns, inIndex=0):
    t = dt.Vector(0.0,0.0,0.0)
    r = dt.EulerRotation(0.0,0.0,0.0)
    s = (1.0,1.0,1.0)
    cnsName = inCns.name()
    
    if inCns.type() == "parentConstraint":
        baseString = ".target["+str(inIndex)+"].targetOffset"

        t.x = pc.getAttr(cnsName + baseString + "TranslateX")
        t.y = pc.getAttr(cnsName + baseString + "TranslateY")
        t.z = pc.getAttr(cnsName + baseString + "TranslateZ")
        r.x = pc.getAttr(cnsName + baseString + "RotateX")
        r.y = pc.getAttr(cnsName + baseString + "RotateY")
        r.z = pc.getAttr(cnsName + baseString + "RotateZ")
        
        sclCns = cnsName.replace("_prCns", "_sCns")
        if "_prCns" in cnsName and pc.objExists(sclCns):
            s = getCnsOffset(getNode(sclCns))[2]
    elif inCns.type() == "pointConstraint":
        t.x = pc.getAttr(cnsName + ".offsetX")
        t.y = pc.getAttr(cnsName + ".offsetY")
        t.z = pc.getAttr(cnsName + ".offsetZ")
    elif inCns.type() == "orientConstraint":
        r.x = pc.getAttr(cnsName + ".offsetX")
        r.y = pc.getAttr(cnsName + ".offsetY")
        r.z = pc.getAttr(cnsName + ".offsetZ")
    elif inCns.type() == "aimConstraint":
        r.x = pc.getAttr(cnsName + ".offsetX")
        r.y = pc.getAttr(cnsName + ".offsetY")
        r.z = pc.getAttr(cnsName + ".offsetZ")         
    elif inCns.type() == "scaleConstraint":
        s0 = pc.getAttr(cnsName + ".offsetX")
        s1 = pc.getAttr(cnsName + ".offsetY")
        s2 = pc.getAttr(cnsName + ".offsetZ")
        s = (s0, s1, s2)
    
    return [t, r, s]

def setCnsOffset(inCns, t = dt.Vector(0.0,0.0,0.0), r = dt.EulerRotation(0.0,0.0,0.0), s = (1.0,1.0,1.0), inIndex=0):
    cnsName = inCns.name()

    if inCns.type() == "parentConstraint":
        baseString = ".target["+str(inIndex)+"].targetOffset"

        pc.setAttr(cnsName + baseString + "TranslateX", t[0])
        pc.setAttr(cnsName + baseString + "TranslateY", t[1])
        pc.setAttr(cnsName + baseString + "TranslateZ", t[2])
        pc.setAttr(cnsName + baseString + "RotateX", r[0])
        pc.setAttr(cnsName + baseString + "RotateY", r[1])
        pc.setAttr(cnsName + baseString + "RotateZ", r[2])
        
        sclCns = cnsName.replace("_prCns", "_sCns")
        if "_prCns" in cnsName and pc.objExists(sclCns):
            setCnsOffset(getNode(sclCns), s = s)
    elif inCns.type() == "pointConstraint":
        pc.setAttr(cnsName + ".offsetX", t[0])
        pc.setAttr(cnsName + ".offsetY", t[1])
        pc.setAttr(cnsName + ".offsetZ", t[2])
    elif inCns.type() == "orientConstraint":
        pc.setAttr(cnsName + ".offsetX", r[0])
        pc.setAttr(cnsName + ".offsetY", r[1])
        pc.setAttr(cnsName + ".offsetZ", r[2])
    elif inCns.type() == "aimConstraint":
        pc.setAttr(cnsName + ".offsetX", r[0])
        pc.setAttr(cnsName + ".offsetY", r[1])
        pc.setAttr(cnsName + ".offsetZ", r[2])         
    elif inCns.type() == "scaleConstraint":
        pc.setAttr(cnsName + ".offsetX", s[0])
        pc.setAttr(cnsName + ".offsetY", s[1])
        pc.setAttr(cnsName + ".offsetZ", s[2])

def saveString(inString, inPath):
    error = None

    f = None
    try:
        f = open(inPath, 'w')
        f.write(inString)
    except Exception as e:
        error = e
    finally:
        if f != None:
            f.close()

    if not error is None:
        raise error

def loadString(inPath):
    error = None
    content = ""

    f = None
    try:
        f = open(inPath, 'r')
        content = f.read()

    except Exception as e:
        error = e
    finally:
        if f != None:
            f.close()

    if not error is None:
        raise error

    return content

def storeConstraints(inObjects, inRemove=False, inPath=None):
    constraints = []

    for obj in inObjects:
        cons = getConstraints(obj)
        for con in cons:
            targets = getConstraintTargets(con)
            index = 0
            for target in targets:

                offset = getCnsOffset(con, index)
                offset = [[offset[0][0], offset[0][1], offset[0][2]],[offset[1][0], offset[1][1], offset[1][2]],[offset[2][0], offset[2][1], offset[2][2]]]

                constraints.append({"source":str(obj.stripNamespace()),
                                    "target":str(target.stripNamespace()),
                                    "type":con.type(),
                                    "offset":offset})
                index += 1

            if inRemove:
                pc.delete(con)

    if len(constraints) > 0 and inPath != None:
        f = None
        try:
            f = open(inPath, 'w')
            f.write(str(constraints))
        except Exception as e:
            pc.warning("Cannot save constraints file to " + inPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    return constraints

def storeConstraintsList(inConstraints, inRemove=False, inPath=None):
    constraints = []

    for con in inConstraints:
        offset = getCnsOffset(con)
        offset = [[offset[0][0], offset[0][1], offset[0][2]],[offset[1][0], offset[1][1], offset[1][2]],[offset[2][0], offset[2][1], offset[2][2]]]
        constraints.append({"source":str(getConstraintOwner(con)[0].stripNamespace()),
                            "target":str(getConstraintTargets(con)[0].stripNamespace()),
                            "type":con.type(),
                            "offset":offset})
        if inRemove:
            pc.delete(con)

    if len(constraints) > 0 and inPath != None:
        f = None
        try:
            f = open(inPath, 'w')
            f.write(str(constraints))
        except Exception as e:
            pc.warning("Cannot save constraints file to " + inPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    return constraints

def loadConstraints(inConstraints, inObjects=None, inRemoveOld=False, inMaintainOffset=False):
    if isinstance(inConstraints, basestring):
        cnsPath = inConstraints
        inConstraints = None

        f = None
        try:
            f = open(cnsPath, 'r')
            inConstraints = eval(f.read())

        except Exception as e:
            pc.warning("Cannot load constraints file from " + cnsPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    if inConstraints is None:
        pc.warning("No constraints given !")
        return

    sources = {}
    nodes = []

    for con in inConstraints:
        sourceName = con["source"]

        #TODO : Manage every objects in inObjects (right now only the first one is taken into account) 
        if not inObjects is None and len(inObjects) > 0:
            sourceName = str(inObjects[0].stripNamespace())

        node = sources.get(sourceName)

        if node is None:
            node = getNode(sourceName, inConsiderNs=True)

            if node is None:
                pc.warning("Can't find source object {0}".format(sourceName))
                continue

            if inObjects is None or node in inObjects:
                sources[sourceName] = node

                if not node in nodes:
                    nodes.append(node)

    if inRemoveOld:
        for node in nodes:
            removeAllCns(node)

    oldNode = None
    oldType = None
    offsetIndex = 0

    for con in inConstraints:

        sourceName = con["source"]

        #TODO : Manage every objects in inObjects (right now only the first one is taken into account) 
        if not inObjects is None and len(inObjects) > 0:
            sourceName = str(inObjects[0].stripNamespace())
        
        node = sources.get(sourceName)
        
        if node is None:
            continue

        targetName = con["target"]
        target = getNode(targetName, inConsiderNs=True)

        if target is None:
            pc.warning("Can't find target object {0}".format(targetName))
            continue

        #print "constrain({0}, {1}, '{2}')".format(node, target, con["type"])
        
        attrs = {}
        for channel in CHANNELS:
            attr = node.attr(channel)
            attrs[channel] = (attr.isLocked(), attr.isKeyable(), attr.isInChannelBox())
            attr.setLocked(False)

        newCns = constrain(node, target, con["type"])
        if node == oldNode and con["type"] == oldType:
            offsetIndex += 1
        else:
            oldNode = node
            oldType = con["type"]
            offsetIndex = 0

        if not inMaintainOffset and con["type"] != "follicle":
            setCnsOffset(newCns,    t = dt.Vector(con["offset"][0][0],con["offset"][0][1],con["offset"][0][2]),
                                    r = dt.EulerRotation(con["offset"][1][0],con["offset"][1][1],con["offset"][1][2]),
                                    s = (con["offset"][2][0],con["offset"][2][1],con["offset"][2][2]), inIndex=offsetIndex)

        for channel, info in attrs.items():
            attr = node.attr(channel)
            attr.setLocked(info[0])

def storePoses(inObjects, customOnly=False, containerName="", keyableOnly=True, inPath=None):
    poses = []

    for obj in inObjects:
        attrs = getParameters(obj, customOnly=customOnly, containerName=containerName, keyableOnly=keyableOnly)
        for attr in attrs:
            poses.append({"source":str(obj.stripNamespace()),
                                "attr":attr,
                                "value":obj.attr(attr).get()})

    if len(poses) > 0 and inPath != None:
        f = None
        try:
            f = open(inPath, 'w')
            f.write(str(poses))
        except Exception as e:
            pc.warning("Cannot save poses file to " + inPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    return poses

def loadPoses(inPoses, inObjects=None, inApply=True, inActivationAttr=None):
    if isinstance(inPoses, basestring):
        posesPath = inPoses
        inPoses = None

        f = None
        try:
            f = open(posesPath, 'r')
            inPoses = eval(f.read())

        except Exception as e:
            pc.warning("Cannot load poses file from " + posesPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    if inPoses is None:
        pc.warning("No poses given !")
        return

    if not inApply:
        return inPoses

    sources = {}

    for pose in inPoses:
        sourceName = pose["source"]
        node = sources.get(sourceName)

        if node is None:
            node = getNode(sourceName, inConsiderNs=True)
            
            if node is None:
                pc.warning("Can't find source object {0}".format(sourceName))
                continue

            if inObjects is None or node in inObjects:
                sources[sourceName] = node

    for pose in inPoses:
        node = sources.get(pose["source"])
        
        if node is None:
            continue

        if node.attr(pose["attr"]).get() == pose["value"]:
            continue

        if not inActivationAttr is None:
            layerName = node.name() + "_poseLayer"
            layerNode = node.getParent()
            if not layerNode.name() == layerName:
                layerObj = pc.group(empty=True, name=layerName)
                layerNode.addChild(layerObj)
                layerObj.t.set([0,0,0])
                layerObj.r.set([0,0,0])
                layerObj.s.set([1,1,1])
                layerNode = layerObj
                layerNode.addChild(node)

            activeMul = pc.createNode("multDoubleLinear", name="{0}_poseLayer_{1}_active".format(node.name(), pose["attr"]))
            activeMul.input1.set(pose["value"])
            inActivationAttr >> activeMul.input2

            output = activeMul.output

            if pose["attr"].startswith("s"):#scaling
                activeMul.input1.set(pose["value"] - 1)
                plusOne = pc.createNode("addDoubleLinear", name="{0}_poseLayer_{1}_scaleAdd_active".format(node.name(), pose["attr"]))
                activeMul.output >> plusOne.input1
                plusOne.input2.set(1)
                output = plusOne.output

            output >> layerNode.attr(pose["attr"])
        else:
            node.attr(pose["attr"]).set(pose["value"])

    return inPoses

def freeze(inObject):
    storeSelection()
    pc.select(inObject)
    pc.mel.eval("DeleteHistory")
    loadSelection()

def freezeModeling(inObject):
    storeSelection()
    pc.select(inObject)
    pc.mel.eval("BakeNonDefHistory")
    loadSelection()

def substShapes(inObject, inRef):
    refShapes = getShapes(inRef)
    objectShapes = getShapes(inObject)

    overrideEnabled = 0
    overrideColor = 0
    rgbColors = False
    rgb = (0.0,0.0,0.0)

    defaultName = "NewShape"

    if(len(objectShapes) > 0):
        defaultName = objectShapes[0].name()
        overrideEnabled = objectShapes[0].overrideEnabled.get()
        overrideColor = objectShapes[0].overrideColor.get()
        
        if pc.versions.current() > 201600:
            rgbColors = objectShapes[0].overrideRGBColors.get()
            if rgbColors:
                rgb = (objectShapes[0].overrideColorR.get(), objectShapes[0].overrideColorG.get(), objectShapes[0].overrideColorB.get())

        overrideVisibilityLinks = pc.listConnections(objectShapes[0].name() + ".overrideVisibility", source=False, plugs=True)
        
        for overrideVisibilityLink in overrideVisibilityLinks:
            #print "link destination " + overrideVisibilityLink
            if overrideVisibilityLink.node().type() == "expression":
                overrideVisibilityLink.node().setExpression(overrideVisibilityLink.node().getExpression().replace(objectShapes[0].name(), refShapes[0].name()))
            else:
                pc.disconnectAttr(objectShapes[0].name() + ".overrideVisibility", overrideVisibilityLink)
                pc.connectAttr(refShapes[0].name() + ".overrideVisibility", overrideVisibilityLink)
                
        overrideVisibilityLinks = pc.listConnections(objectShapes[0].name() + ".overrideVisibility", destination=False, plugs=True)
        
        for overrideVisibilityLink in overrideVisibilityLinks:
            #print "link source " + overrideVisibilityLink
            if overrideVisibilityLink.node().type() == "expression":
                overrideVisibilityLink.node().setExpression(overrideVisibilityLink.node().getExpression().replace(objectShapes[0].name(), refShapes[0].name()))
            else:
                pc.disconnectAttr(overrideVisibilityLink, objectShapes[0].name() + ".overrideVisibility")
                pc.connectAttr(overrideVisibilityLink, refShapes[0].name() + ".overrideVisibility")

        overrideVisibilityLinks = pc.listConnections(objectShapes[0].name() + ".visibility", source=False, plugs=True)
        
        for overrideVisibilityLink in overrideVisibilityLinks:
            #print "link destination " + overrideVisibilityLink
            if overrideVisibilityLink.node().type() == "expression":
                overrideVisibilityLink.node().setExpression(overrideVisibilityLink.node().getExpression().replace(objectShapes[0].name(), refShapes[0].name()))
            else:
                pc.disconnectAttr(objectShapes[0].name() + ".visibility", overrideVisibilityLink)
                pc.connectAttr(refShapes[0].name() + ".visibility", overrideVisibilityLink)
                
        overrideVisibilityLinks = pc.listConnections(objectShapes[0].name() + ".visibility", destination=False, plugs=True)
        
        for overrideVisibilityLink in overrideVisibilityLinks:
            #print "link source " + overrideVisibilityLink
            if overrideVisibilityLink.node().type() == "expression":
                overrideVisibilityLink.node().setExpression(overrideVisibilityLink.node().getExpression().replace(objectShapes[0].name(), refShapes[0].name()))
            else:
                pc.disconnectAttr(overrideVisibilityLink, objectShapes[0].name() + ".visibility")
                pc.connectAttr(overrideVisibilityLink, refShapes[0].name() + ".visibility")

        """
        overrideVisibilityLinks = pc.listConnections(objectShapes[0].name() + ".overrideVisibility", destination=False)

        for link in overrideVisibilityLinks:
            if link.type() == "expression":
                link.setExpression(link.getExpression().replace(objectShapes[0].name(), refShapes[0].name()))
        """

    newNames = []
    for i in range(len(refShapes)):
        if i < len(objectShapes):
            newNames.append(objectShapes[i].name())
        else:
            newNames.append(defaultName)

    pc.delete(objectShapes)

    counter = 0
    for shape in refShapes:
        pc.parent(shape, inObject, add=True, shape=True)
        shape.overrideEnabled.set(overrideEnabled)
        shape.overrideColor.set(overrideColor)
        if rgbColors:
            shape.overrideRGBColors.set(True)
            shape.overrideColorR.set(rgb[0])
            shape.overrideColorG.set(rgb[1])
            shape.overrideColorB.set(rgb[2])
        shape.rename(newNames[counter])
        counter += 1
    
    pc.delete(inRef)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ____                           _              
  / ___| ___  ___  _ __ ___   ___| |_ _ __ _   _ 
 | |  _ / _ \/ _ \| '_ ` _ \ / _ \ __| '__| | | |
 | |_| |  __/ (_) | | | | | |  __/ |_| |  | |_| |
  \____|\___|\___/|_| |_| |_|\___|\__|_|   \__, |
                                           |___/ 

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def getPointsCount(inObject):
    oscarType = getOscarType(inObject)
    #print oscarType
    if oscarType == "Curve":
        shapes = getShapes(inObject)
        if len(shapes) > 0:
            return shapes[0].numCVs()
    elif oscarType == "Lattice":
        shapes = getShapes(inObject)
        if len(shapes) > 0:
            return pc.getAttr(shapes[0] + ".sDivisions") * pc.getAttr(shapes[0] + ".tDivisions") * pc.getAttr(shapes[0] + ".uDivisions")
    if oscarType == "Nurbs":
        shapes = getShapes(inObject)
        if len(shapes) > 0:
            return shapes[0].numCVsInU() * shapes[0].numCVsInV()
    else:
        return pc.polyEvaluate(inObject, vertex=True)

    return -1

def getPoints(inObject, normalized=True):
    crvShapes = getShapes(inObject)
    pos = []

    offset=[0,0,0]
    scale=[1,1,1]

    if normalized and pc.attributeQuery( "offsetDisplayX", node=inObject, exists=True ):
        offset[0] = pc.getAttr(inObject.name()+ ".offsetDisplayX")
        offset[1] = pc.getAttr(inObject.name()+ ".offsetDisplayY")
        offset[2] = pc.getAttr(inObject.name()+ ".offsetDisplayZ")

        scale[0] = pc.getAttr(inObject.name()+ ".scaleDisplayX")
        scale[1] = pc.getAttr(inObject.name()+ ".scaleDisplayY")
        scale[2] = pc.getAttr(inObject.name()+ ".scaleDisplayZ")

    if len(crvShapes) > 0:
        if crvShapes[0].type() == "nurbsCurve":

            sl = om.MGlobal.getSelectionListByName(crvShapes[0].name())
            node = sl.getDependNode(0)
            mFnSet = om.MFnNurbsCurve(node)
            cvs = mFnSet.cvPositions()

            for point in cvs:
                pos.append(((point.x - offset[0])/scale[0], (point.y - offset[1])/scale[1], (point.z - offset[2])/scale[2]))

        elif crvShapes[0].type() == "mesh":

            sl = om.MGlobal.getSelectionListByName(crvShapes[0].name())
            node = sl.getDependNode(0)
            mFnSet = om.MFnMesh(node)

            points = mFnSet.getPoints()

            for point in points:
                pos.append(((point.x - offset[0])/scale[0], (point.y - offset[1])/scale[1], (point.z - offset[2])/scale[2]))

        elif crvShapes[0].type() == "lattice":
            ns = pc.getAttr(crvShapes[0].name() + ".sDivisions")
            nt = pc.getAttr(crvShapes[0].name() + ".tDivisions")
            nu = pc.getAttr(crvShapes[0].name() + ".uDivisions")

            for s in range(ns):
                    for t in range(nt):
                        for u in range(nu):
                            point = crvShapes[0].point(s, t, u)
                            pos.append(((point.x - offset[0])/scale[0], (point.y - offset[1])/scale[1], (point.z - offset[2])/scale[2]))

        elif crvShapes[0].type() == "nurbsSurface":

            sl = om.MGlobal.getSelectionListByName(crvShapes[0].name())
            node = sl.getDependNode(0)
            mFnSet = om.MFnNurbsSurface(node)
            points = mFnSet.cvPositions()

            for point in points:
                pos.append(((point.x - offset[0])/scale[0], (point.y - offset[1])/scale[1], (point.z - offset[2])/scale[2]))

        else:
            pc.warning("Unknown Geometry type : " + crvShapes[0].type())

    return pos
    
def curve(points, name="", parent=None, degree=3, closed=False, verbose=False):
    curve = None 
    if closed:
        for i in range(degree):
            points.append(points[i])

        knots = range(len(points) + degree - 1)
        curve = pc.curve( point=points, degree=degree, knot=knots, periodic= True)
        if verbose:
            tkLogger.info("pc.curve( point={0}, degree={1}, knot={2}, periodic= True)".format(points, degree, knots))
    else:
        curve = pc.curve( point=points, degree=degree)
        if verbose:
            tkLogger.info("pc.curve( point={0}, degree={1})".format(points, degree))

    pc.rename(curve, name)

    if parent != None:
            pc.parent(curve, parent)

    return curve


def complexity (inObj):
    """Compute the "complexity" of a mesh

        Input arguments:
        inObj -- a meshes

        Return values:
        complexity_mesh

    """
 
    nVerts = pc.polyEvaluate(inObj, vertex=True)
    bb = inObj.getBoundingBox()
    volume = bb.width()*bb.depth()*bb.height()
    
    if volume == 0:
        complexity_mesh = 0
    else:
        complexity_mesh = nVerts / volume ** .33#pseudo cubic root 

    return complexity_mesh

def polyReduceComplexity (inObj, inMinComplx, inMaxComplx, inMinPercent = 0, inMaxPercent = 80, **inPolyReduceArguments):
    """Use polyReduce from Maya or not depending on a threshold

        Input arguments:
        inObj -- a mesh
        inMinComplx -- Threshold min for complexity
        inMaxComplx -- Threshold max for complexity
        inMinPercent -- (default 0)
        inMaxPercent -- (default 100)
        **inPolyReduceArguments -- argument for polyReduce (default default value for polyReduce)

        Return values:


    """
    
    defaultArguments={"percentage":10,"ver":1,"trm":0,"shp":0,"keepBorder":1,"keepMapBorder":1, "keepColorBorder":1, "keepFaceGroupBorder": 1, "keepHardEdge":1, "keepCreaseEdge":1,"keepBorderWeight":0.5,"keepMapBorderWeight":0.5,"keepColorBorderWeight":0.5,"keepFaceGroupBorderWeight":0.5,"keepHardEdgeWeight":0.5,"keepCreaseEdgeWeight":0.5,"useVirtualSymmetry":0,"symmetryTolerance":0.01, "sx":0, "sy":1, "sz":0, "sw":0, "preserveTopology":1, "keepQuadsWeight":1, "vertexMapName":"", "cachingReduce":1,"ch":0,"p":50,"vct":0,"tct":0,"replaceOriginal":1}
    if len(inPolyReduceArguments) > 0: #if polyreduceagument has values
        for key in inPolyReduceArguments.keys():
            if key in defaultArguments.keys():
                cp=inPolyReduceArguments[key]
                defaultArguments[key]=cp
                
            else:
                pc.warning("Wrong argument", key, "please try the short argument")
            inPolyReduceArguments=defaultArguments.copy()
    else: #if dictionary is empty
        #Values by default
        inPolyReduceArguments=defaultArguments.copy()

    if "p" in inPolyReduceArguments:
        del inPolyReduceArguments["p"]
    if "percentage" in inPolyReduceArguments:
        del inPolyReduceArguments["percentage"]

  
    density = complexity (inObj)
    if inMinComplx >= inMaxComplx:
        pc.warning("Minimum value must be inferior strict to maximum value !")
    else:
        if inMinPercent >= inMaxPercent:
            pc.warning("Minimum percent must be inferior strict to maximum percent !")
        else:
            if density <= inMinComplx:
                pc.warning("Not enought density !")
               
            if density > inMinComplx and density < inMaxComplx:
                if inMaxComplx == 0:
                    raise ValueError("Wrong value for inMaxComplx")
                else:
                    per = (density*inMaxPercent)/(inMaxComplx)
                    try:
                        pc.polyReduce(inObj,p=per, **inPolyReduceArguments)
                    except:
                        pc.warning("Can't reduce " + inObj)
               
            if density >= inMaxComplx:
                if inMaxComplx != 0:
                    try:
                        pc.polyReduce(inObj,p=inMaxPercent, **inPolyReduceArguments)
                    except:
                        pc.warning("Can't reduce " + inObj)
    return

POLYTOPOLY = "PolyToPoly"
POINTTOPOINT = "PointToPoint"

def sampleGeometry(inObj, inRef, inType=POLYTOPOLY, inProgress=True):
    if inObj.type() == "transform":
        inObj = inObj.getShape()

    if inRef.type() == "transform":
        inRef = inRef.getShape()

    sampling = []

    if inType == POLYTOPOLY:
        points = inObj.getPoints(space="world")

        numFaces = inObj.numFaces()

        if inProgress:
            gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

            pc.progressBar( gMainProgressBar,
            edit=True,
            beginProgress=True,
            isInterruptable=True,
            status="Gatoring...",
            maxValue=numFaces)

        for i in range(numFaces):
            #get polygon center
            ids = inObj.getPolygonVertices(i)
            centerPoint = points[ids[0]]
            for j in range(1,len(ids)):
                centerPoint += points[ids[j]]
            centerPoint /= len(ids)

            closestPoint, closestFaceId = inRef.getClosestPoint(centerPoint, space="world")
            sampling.append(closestFaceId)

            if inProgress:
                pc.progressBar(gMainProgressBar, edit=True, step=1)

        if inProgress:
            pc.progressBar(gMainProgressBar, edit=True, endProgress=True)
    else:
        pc.warning("Sampling type " + inType + " is not implemented !")

    return sampling

def deserializeComponents(inFacesStrs):
    if not isinstance(inFacesStrs, (list, tuple)):
        inFacesStrs = (inFacesStrs,)

    facesIndices = []

    reg = re.compile(r".*\[([0-9:]+)\]")

    for faceStr in inFacesStrs:
        match = reg.match(faceStr)

        if not match is None:
            strDigits = match.groups()[0]

            if ":" in strDigits:
                start, end = strDigits.split(":")
                facesIndices.extend(range(int(start), int(end) + 1))
            else:
                facesIndices.append(int(strDigits))

    return facesIndices

def serializeComponents(inIndices, inComponentTag="f"):
    inFacesStrs = []

    inIndices.sort()

    start = inIndices[0]
    last = start - 1

    for i in range(len(inIndices)):
        currentIndex = inIndices[i]
        if currentIndex - last == 1:#continue range
            last = currentIndex
        else:#push range
            if last != start:
                inFacesStrs.append("{0}[{1}:{2}]".format(inComponentTag, start, last))
            else:
                inFacesStrs.append("{0}[{1}]".format(inComponentTag, start))

            start = currentIndex
            last = currentIndex

    if last != start:
        inFacesStrs.append("{0}[{1}:{2}]".format(inComponentTag, start, last))
    else:
        inFacesStrs.append("{0}[{1}]".format(inComponentTag, start))

    start = currentIndex
    last = currentIndex

    return inFacesStrs

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____        __                            _   _             
 |  _ \  ___ / _| ___  _ __ _ __ ___   __ _| |_(_) ___  _ __  
 | | | |/ _ \ |_ / _ \| '__| '_ ` _ \ / _` | __| |/ _ \| '_ \ 
 | |_| |  __/  _| (_) | |  | | | | | | (_| | |_| | (_) | | | |
 |____/ \___|_|  \___/|_|  |_| |_| |_|\__,_|\__|_|\___/|_| |_|
                                                              
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def muteDeformers(inMesh):
    envelopes = {}
    defs = pc.listHistory(inMesh, gl=True, pdo=True, lf=True, f=False, il=2)
    if defs != None:
        for deformer in defs:
            if pc.attributeQuery("envelope" , node=deformer, exists=True):
                envelopes[deformer] = deformer.envelope.get()
                deformer.envelope.set(0.0)

    return envelopes

def restoreDeformers(inMesh, inDeformers):
    for envelope in inDeformers.keys():
        if envelope != "":
            pc.setAttr("{0}.envelope".format(envelope), inDeformers[envelope])

def getSets(inObj):
    allSets = [s for s in pc.ls(type="objectSet") if pc.mel.eval("setFilterScript " + s.name())]
    objSets = inObj.listConnections(type="objectSet")
    
    return [s for s in objSets if s in allSets]

def removeFromSets(inObjects):
    if not isinstance(inObjects, (list, tuple)):
        inObjects = [inObjects]

    allSets = [s for s in pc.ls(type="objectSet") if pc.mel.eval("setFilterScript " + s.name())]
    for thisSet in allSets:
        for obj in inObjects:
            if pc.sets(thisSet, im=obj):
                pc.sets(thisSet, rm=obj)

def matchSets(inObj, inRef):
    removeFromSets(inObj)
    
    allSets = getSets(inRef)
    for thisSet in allSets:
        pc.sets(thisSet, forceElement=inObj)


def duplicateAndClean(inSourceMesh, inTargetName="$REF_dupe", inMuteDeformers=True, inResetDisplayType=True, inRemoveFromSets=True):
    inSourceMesh = getNode(inSourceMesh)

    #Make sure every deformer is at 0 before duplication
    envelopes = {}
    if inMuteDeformers:
        envelopes = muteDeformers(inSourceMesh)
    
    dupe = pc.duplicate(inSourceMesh, rr=True)[0]

    if inRemoveFromSets:
        removeFromSets(dupe)

    if '$REF' in inTargetName:
        inTargetName = inTargetName.replace('$REF', inSourceMesh.name())

    dupe = dupe.rename(inTargetName)
    
    shapes = dupe.getShapes()
    if shapes != None:
        for shape in shapes:
            if shape.intermediateObject.get():
                pc.delete(shape)
            elif inResetDisplayType:
                shape.overrideDisplayType.set(0)

    if inMuteDeformers:
        restoreDeformers(inSourceMesh, envelopes)

    return dupe

def getSkinCluster(inObject):
    skins = pc.listHistory(inObject, type="skinCluster", levels=3)

    for skin in skins:
        geo = skin.getGeometry()[0]
        if geo == inObject or geo.getParent() == inObject:
            return skin

    skins = pc.listHistory(inObject, type="skinCluster")

    for skin in skins:
        geo = skin.getGeometry()[0]
        if geo == inObject or skin.getGeometry()[0].getParent() == inObject:
            return skin

    return None

def getFFDs(inObject):
    shapes = getShapes(inObject)
    if len(shapes) == 0:
        pc.warning("Can't get any shapes on given object ("+inObject.name()+") !")
        return None

    lattices = []

    for shape in shapes:
        sets = pc.listConnections(shape, type="objectSet", destination=False)
        for set in sets:
            latt = pc.listConnections(set, type="ffd", destination=False)
            if len(latt) > 0:
                lattices.extend(latt)

    return lattices

SKIN_DATA = None

def setWeights(inObject, inInfluences=[], inValues=[], inMode=0, inOpacity=1.0, inNormalize=True):
    """
    inInfluences is an influence short names list (no namespaces) : ["Influence1", "Influence2",...]
    inValues are given "per influence" :
        [Inf_1_Vert_1, Inf_1_Vert_2,...Inf_1_Vert_[n],  Inf_2_Vert_1, Inf_2_Vert_2,...Inf_2_Vert_[n]] 

    Modes :
        0 : Replace
        1 : Overwrite
        2 : Add
        3 : Blend
    """
    global SKIN_DATA
    skin = getSkinCluster(inObject)

    valLength = len(inValues)
    infLength = len(inInfluences)

    if infLength == 0:
        pc.warning(inObject.name() + " : Invalid parameters, influences can't be empty !")
        return

    #print "setWeights : %s, %s, %s" % (inObject.name(), str(inInfluences), str(inValues))

    oldInfs = None
    oldWeights = None

    if skin != None:
        if infLength == 0 and inValues == 0:
            #detach
            pc.skinCluster(skin, edit=True, unbind=True)
            return 

        if inMode > 0:
            oldInfs = skin.influenceObjects()
            oldWeights = getWeights(inObject)

        #detach
        pc.skinCluster(skin, edit=True, unbind=True)

    ns = inObject.namespace()

    #verify values before setting weights
    nVerts = getPointsCount(inObject)

    if valLength != 0:
        expectedValLength = infLength * nVerts
        if valLength != expectedValLength:
            pc.warning(inObject.name() + " : Invalid parameters, values length doesn't match influences and verts length  ("+ str(valLength) +" given, "+ str(expectedValLength) +" expected, "+ str(infLength) +" influences * "+str(nVerts)+" verts)")
            return

    #Re-package influences and values in case influences are showing more than once
    infSet = set(inInfluences)
    if len(inInfluences) != len(infSet):
        for inf in infSet:
            count = inInfluences.count(inf)
            if count > 1:
                firstOcc = inInfluences.index(inf)
                occ = firstOcc + 1
                for i in xrange(count-1):
                    occ = inInfluences.index(inf, occ)

                    del inInfluences[occ]

                    newValues = inValues[firstOcc*nVerts:nVerts]
                    dupValues = inValues[occ*nVerts:nVerts]
                    for i in xrange(nVerts):
                        inValues[firstOcc*nVerts + i] += inValues[occ*nVerts + i]

                    del inValues[occ*nVerts:occ*nVerts + nVerts]

        valLength = len(inValues)
        infLength = len(inInfluences)

    #verify if every influence exists
    nullInfs = []
    for i in xrange(infLength):
        inf = inInfluences[i]
        if not palt.exists(inf):
            nullInfs.append(i)

    if len(nullInfs) > 0:
        pc.warning(inObject.name() + " : Some deformers were not found, '"+ CONST_NULLINFNAME +"' joint will be created if it does not exists already")
        
        nullInf = ns + CONST_NULLINFNAME
        nullInfValues = None

        nullInfObj = getNode(nullInf)

        if nullInfObj is None:
            parent = getParent(inObject, False, True)

            if not parent == None and not parent.namespace() == "":
                nullInf = CONST_NULLINFNAME

            nullInfObj = createRigObject(parent, name=nullInf, type="Deformer")

        nullInfs.sort()
        nullInfs.reverse()

        for i in nullInfs:
            pc.warning(inObject.name() + " : Deformer " + inInfluences[i] + " not found and ignored")
            del inInfluences[i]
            if nullInfValues == None:
                nullInfValues = inValues[i*nVerts:(i+1)*nVerts]
            else:
                for j in xrange(len(nullInfValues)):
                    nullInfValues[j] += inValues[i*nVerts + j]
            del inValues[i*nVerts:(i+1)*nVerts]

        inInfluences.append(nullInfObj.name())
        inValues.extend(nullInfValues)

        #print "NullDef values : (" + str(len(nullInfValues)) + ") " + str(nullInfValues)

        valLength -= -1 + len(nullInfs) * nVerts
        infLength -= -1 + len(nullInfs)

    # print "inInfluences",inInfluences
    # print "oldInfs",oldInfs
    #If we have old weights info
    if not oldInfs is None:

        oldInfsStr = [n.name() for n in oldInfs]

        mergedInfs = list(dict.fromkeys(inInfluences + oldInfsStr))
        nNewInfs = len(mergedInfs) - len(inInfluences)

        oldInfsIndices = [oldInfsStr.index(inf) if inf in oldInfsStr else -1 for inf in mergedInfs]

        #Update full grid
        if nNewInfs > 0:
            infLength += nNewInfs
            inValues.extend([0.0] * (nVerts * nNewInfs))
            valLength += nVerts * nNewInfs

            inInfluences = mergedInfs

        #Manage fusion
        for i in xrange(nVerts):
            weights = []
            totalWeights = 0.0

            oldPointWeights = []
            totalOldWeights = 0.0

            #Get info
            for j, inf in enumerate(inInfluences):
                val = inValues[j*nVerts + i] * inOpacity
                totalWeights += val
                weights.append(val)
                oldVal = 0.0
                oldIndex = oldInfsIndices[j]
                if oldIndex != -1:
                    oldVal = oldWeights[oldIndex*nVerts + i]
                    totalOldWeights += oldVal
                oldPointWeights.append(oldVal)

            ratio = (100.0 - totalWeights) / 100.0

            #Set values
            for j, (weight, oldWeight) in enumerate(zip(weights, oldPointWeights)):
                if inMode == 1:#Overwrite
                    inValues[j*nVerts + i] = weight + ratio * oldWeight

                elif inMode == 2:#Add
                    inValues[j*nVerts + i] = weight + oldWeight

                elif inMode == 3:#Blend
                    inValues[j*nVerts + i] = weight + (1.0 - inOpacity) * oldWeight


    #If the object shape is hidden, maya will crash at binding, make everything visible
    #and store shape connections if necessary

    hiddenShapes = []
    lockedShapes = []
    connections = {}

    shapes = inObject.getShapes()
    for shape in shapes:
        attr = shape.visibility
        if not attr.get():
            hiddenShapes.append(attr)

            if attr.isLocked():
                lockedShapes.append(attr)
                attr.setLocked(False)

            connections[shape] = getNodeConnections(shape, "v", inSource=True, inDestination=False, inDisconnect=True)

            attr.set(1)
        
    skin = pc.animation.skinCluster(inObject, inInfluences, name=inObject.name() + "_skinCluster", toSelectedBones=True)
    realInfs = pc.skinCluster(skin,query=True,inf=True)

    #Restore shapes visibilities and connections
    for hiddenShape in hiddenShapes:
        hiddenShape.set(0)

    for obj, cons in connections.items():
        setNodeConnections(cons, obj)

    for lockedShape in lockedShapes:
        lockedShape.setLocked(True)

    if valLength != 0:
        defaultNorm = pc.skinCluster(skin,query=True, normalizeWeights=True)
        pc.skinCluster(skin,edit=True,normalizeWeights=0)

        #remap inValues from [Def1pt1, Def1pt2, Def2pt1, Def2pt2] to [Def1pt1, Def2pt1, Def1pt2, Def2pt2]
        pmValues = []
        infIndices = range(infLength)
        if versions.current() < 201400:
            infIndices.reverse()
        for dim1i in range(nVerts):
            for dim2i in range(infLength):
                pmValues.append(inValues[dim1i + dim2i * nVerts] / 100.0)

        if pc.objectType(inObject.getShape()) == "lattice" or pc.objectType(inObject.getShape()) == "nurbsSurface":
            skin.setWeights(skin.getGeometry()[-1], infIndices, pmValues)
        else:
            SKIN_DATA = pmValues
            pc.setSkinWeight(skin.name(), cl=True)
            SKIN_DATA = None

        pc.skinCluster(skin,edit=True,normalizeWeights=defaultNorm)
        if inNormalize:
            #CBB : Can't believe we have to select the mesh...
            # pc.select(inObject, replace=True)
            pc.skinPercent( skin, inObject, normalize=True)

    if len(nullInfs) == 0:#Maybe we can clean 0Deform
        nullInf = ns + CONST_NULLINFNAME
        if palt.exists(nullInf) and len(pc.listConnections(nullInf, type="skinCluster")) == 0:
            pc.delete(nullInf)

    return skin

def getWeights(inObject, inInfluence=None):
    skin = getSkinCluster(inObject)
    if skin == None:
        pc.warning("Can't get any skinCluster on given object ("+inObject.name()+") !")
        return []
    infWeights = []

    infObjs = pc.skinCluster(skin,query=True,inf=True)

    #Verify if we didn't retrieve a 0Deform
    nullInf = None
    nullInfIndex = -1
    for i in range(len(infObjs)):
        inf = infObjs[i]
        if CONST_NULLINFNAME in inf.name():
            nullInf = inf
            nullInfIndex = i
            break

    if not inInfluence is None:
        influenceWeight = tkApi.get_weights_data(inObject.name(), inInfluence = inInfluence)["classic_linear"]

        return [w * 100.0 for w in influenceWeight]
    else:
        skinData = tkApi.get_weights_data(inObject.name())
        rawWeights = []
        for x in range(0, len(skinData["classic_linear"]), len(skinData["influences"])):
            rawWeights.append(tuple(skinData["classic_linear"][x:x+len(skinData["influences"])]))
        dim1 = len(rawWeights)
        if dim1 > 0:
            dim2 = len(rawWeights[0])
            for dim2i in range(dim2):
                for dim1i in range(dim1):
                    infWeights.append(rawWeights[dim1i][dim2i] * 100.0)

        if nullInf != None:
            pc.warning("Some deformers were missing, '"+ CONST_NULLINFNAME +"' joint is ignored")

    return infWeights

def addWeights(inObj, inInfluences, inWeights):
    if not isinstance(inInfluences, (list, tuple)):
        inInfluences = [inInfluences]
        
    if not isinstance(inWeights[0], (list, tuple)):
        inWeights = [inWeights]

    skin = getSkinCluster(inObj)
    
    if skin is None:
        pc.warning("No skinning found on " + inObj.name())
        return

    infs = skin.influenceObjects()
    nVerts = pc.polyEvaluate(inObj, vertex=True)
    
    weights = getWeights(inObj)
    
    newInfs = infs[:]
    newWeights = weights[:]
    
    #Add weight to weightArray
    i = 0
    kepsIndices = []
    for newInf in inInfluences:
        if not newInf in infs:
            newInfs.append(newInf)
            kepsIndices.append(len(newInfs) - 1)
            #New influence, extend weights
            newWeights.extend(inWeights[i])
        else:
            index = infs.index(newInf)
            kepsIndices.append(index)
            #Existing influence, add weights
            j = 0
            for w in inWeights[i]:
                newWeights[nVerts*index + j] += w
                j += 1
        i += 1

    #print "newInfs",len(newInfs),newInfs
    #print "verts",nVerts
    #print "newWeights",len(newWeights)
    #print "nVerts * nInfs",nVerts * len(newInfs)

    #Normalize keeping added influences
    for i in range(nVerts):
        totalWeight = 0.0
        totalWeight2 = 0.0
        for j in range(len(newInfs)):
            w = newWeights[nVerts*j + i]
            if not j in kepsIndices:
                totalWeight2 += w
            totalWeight += w

        if totalWeight == 100.0:
            continue

        lockedWeights = 0.0
        for keptIndex in kepsIndices:
            lockedWeights += newWeights[nVerts*keptIndex + i]

        #pre-normalize locked
        if lockedWeights > 100.0:
            #print "pre-normalize",lockedWeights
            factor = 100.0 / lockedWeights
            lockedWeights = 100.0

            for keptIndex in kepsIndices:
                newWeights[nVerts*keptIndex + i] *= factor

        #actually normalize        
        remainingWeight = 100.0 - lockedWeights
        factor = remainingWeight / totalWeight2

        for j in range(len(newInfs)):
            if j in kepsIndices:
                continue
            newWeights[nVerts*j + i] *= factor
    
    #Finally set weights
    setWeights(inObj, [n.name() for n in newInfs], newWeights)

def smartMirrorSkin(inTarget, inSource=None, inSides=["Left_", "Right_"]):
    """Maya mirror skin but add usefull deformers by label side, usable on unique object or side object to oposit side (left/right) if inSource used"""
    if not inSource == None:
        sourceDeformers = getDeformers([inSource])
    else:
        sourceDeformers = getDeformers([inTarget])

    mirrorDeformers = []
    notFoundDfm = []
    continueWithLostDfm = "Yes"
    for sourceDfm in sourceDeformers:
        sideDfm = sourceDfm.side.get()
        if sideDfm == 1:
            mirrorDfm = getNode("::{}{}".format(inSides[sideDfm], sourceDfm.otherType.get()))
            if mirrorDfm is None:
                notFoundDfm.append("{}{}".format(inSides[sideDfm], sourceDfm.otherType.get()))
                continue
            mirrorDeformers.append(mirrorDfm)
        elif sideDfm == 2:
            mirrorDfm = getNode("::{}{}".format(inSides[sideDfm-2], sourceDfm.otherType.get()))
            if mirrorDfm is None:
                notFoundDfm.append("{}{}".format(inSides[sideDfm-2], sourceDfm.otherType.get()))
                continue
            mirrorDeformers.append(mirrorDfm)
        else:
            mirrorDeformers.append(sourceDfm)
    targetSkinNode = getSkinCluster(inTarget)

    if len(notFoundDfm) != 0:
        lostDfmStr = '\n - ' + '\n - '.join(notFoundDfm)
        continueWithLostDfm = cmds.confirmDialog( title='Mirror Dfm Not Found !', message='Somme deformers not found : ' + lostDfmStr + "\n Do you realy want to mirror skin ?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    
    if continueWithLostDfm == "Yes":
        if not inSource is None:
            if targetSkinNode != None:
                pc.skinCluster(targetSkinNode, edit=True, unbind=True)
            skinCluster = pc.skinCluster(inTarget, mirrorDeformers, name=inTarget.name() + "_skinCluster", toSelectedBones=True)
            pc.copySkinWeights(ss=getSkinCluster(inSource), ds=skinCluster, mirrorMode='YZ', ia="label", sa="closestPoint")
        else:
            mirrorDeformers = [x for x in mirrorDeformers if x not in sourceDeformers]
            pc.skinCluster(targetSkinNode, e=True, lw=True, wt=0, ai=mirrorDeformers)
            for dfm in mirrorDeformers:
                dfm.liw.set(0)
            pc.copySkinWeights(ss=getSkinCluster(inTarget), ds=targetSkinNode, mirrorMode='YZ', ia="label", sa="closestPoint")

def getPointInfluences(inSkin, inInfluences, inPointIndex):
    NInfs = inInfluences if not isinstance(inInfluences, (list, tuple)) else len(inInfluences)

    NSkin = len(inSkin)
    NVerts = int(NSkin / NInfs)
    
    return [inSkin[i] for i in range(inPointIndex, NSkin, NVerts)]

def setPointInfluences(inSkin, inInfluences, inPointIndex, inValues):
    inValues = inValues[:]

    NInfs = inInfluences if not isinstance(inInfluences, (list, tuple)) else len(inInfluences)

    NSkin = len(inSkin)
    NVerts = int(NSkin / NInfs)
    
    for i in range(inPointIndex, NSkin, NVerts):
        inSkin[i] = inValues.pop(0)
        
    return inSkin

def _limitDeformers(inSkin, inInfluences, inMax=4, inSharpen=.5, inVerbose=True, inProgress=True):
    NInfs = inInfluences if not isinstance(inInfluences, (list, tuple)) else len(inInfluences)

    NSkin = len(inSkin)
    pointsN = NSkin / NInfs
    
    gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')
    if inProgress:
        pc.progressBar( gMainProgressBar,
                edit=True,
                beginProgress=True,
                isInterruptable=False,
                status="Limit deformers...",
                maxValue=pointsN)

    for i in range(int(pointsN)):
        values = getPointInfluences(inSkin, inInfluences, i)
        
        inf_vals = []
        for j in range(len(values)):
            inf_vals.append([inInfluences[j], values[j]])

        #sort by value
        inf_vals.sort(key=lambda v: -v[1])
        
        counter = 0
        remainingWeight = 0
        
        for inf_val in inf_vals:
            if inf_val[1] <= 0.0:
                break
            
            counter += 1

            if counter > inMax:
                remainingWeight += inf_val[1]
                inf_val[1] = 0

        if remainingWeight >= 0.0001:
            if inVerbose:
                tkLogger.info("{0} deformers on vertex {1} ({2} to remove)".format(counter, i, counter - inMax))

            currentTotal = 100.0 - remainingWeight
            mul = 100.0 / currentTotal
            
            for inf_val in inf_vals:
                if inf_val[1] <= 0.0:
                    break
    
                inf_val[1] = inf_val[1] * mul

                if inSharpen > 0.0:
                    inf_val[1] = (1-inSharpen) * inf_val[1] + inSharpen * (inf_val[1] * inf_val[1])
            
            #resort
            inf_vals.sort(key=lambda v: inInfluences.index(v[0]))
            
            setPointInfluences(inSkin, inInfluences, i, [l[1] for l in inf_vals])
            
        if inProgress:
            pc.progressBar(gMainProgressBar, edit=True, step=1)

    if inProgress:
        pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    return inSkin

def limitDeformers(inObj, inMax=4, inSharpen=.5, inVerbose=False, inProgress=True):
    inObj = getNode(inObj)
    skinCls = getSkinCluster(inObj)

    skin = getWeights(inObj)
    influences = [inf.name() for inf in pc.skinCluster(skinCls, query=True, inf=True)]
    
    skin = _limitDeformers(skin, influences, inMax=inMax, inSharpen=inSharpen, inVerbose=inVerbose, inProgress=inProgress)
    
    setWeights(inObj, inInfluences=influences, inValues=skin, inMode=0, inOpacity=1.0, inNormalize=True)

def _averagePoints(inSkin, inInfluences, inPointsIndices=None, inStrength=1.0, inVerbose=True, inProgress=True):
    NInfs = inInfluences if not isinstance(inInfluences, (list, tuple)) else len(inInfluences)

    NSkin = len(inSkin)
    pointsN = NSkin / NInfs

    if inPointsIndices is None:
        inPointsIndices = range(pointsN)

    #Get points weights
    valuesList = []
    for pointIndex in inPointsIndices:
        valuesList.append(getPointInfluences(inSkin, inInfluences, pointIndex))

    #Average
    totals = [0] * NInfs
    for i, pointIndex in enumerate(inPointsIndices):
        for j, value in enumerate(valuesList[i]):
            totals[j] += value

    average = [n / NSkin for n in totals]

    for pointIndex in inPointsIndices:
        if inStrength >= 1.0:
            setPointInfluences(inSkin, inInfluences, pointIndex, average)
        else:
            values = []
            for i, value in enumerate(valuesList[pointIndex]):
                values.append(value * (1 - inStrength) + average[i] * inStrength)

            setPointInfluences(inSkin, inInfluences, pointIndex, values)

    return inSkin

def averagePoints(inObj, inPointsIndices=None, inStrength=1.0, inVerbose=True, inProgress=True):
    skin = getWeights(inObj)
    skinCls = getSkinCluster(inObj)
    influences = [inf.name() for inf in pc.skinCluster(skinCls, query=True, inf=True)]
    
    skin = _averagePoints(skin, influences, inPointsIndices)
    
    setWeights(inObj, inInfluences=influences, inValues=skin, inMode=0, inOpacity=1.0, inNormalize=True)

def getInfluencedPoints(inObj, inInfluences):
    points = []

    skin = getSkinCluster(inObj)
    infs = skin.getInfluence()
    
    infNodes = []
    
    for inf in inInfluences:
        if pc.objExists(inf):
            infNode = getNode(inf)
            if infNode in infs:
                infNodes.append(infNode)

    for infNode in infNodes:
        weights = getWeights(inObj, infNode)
        
        points.extend([i for i in range(len(weights)) if weights[i] > 0.01])

    return ["{0}.vtx[{1}]".format(inObj, i) for i in list(set(points))]

def getSkinPointCount(inSkin):
    inObject, infs, weights, ns = inSkin

    return int(len(weights) / len(infs))

def storeSkin(inObject):
    skin = getSkinCluster(inObject)
    
    if skin == None:
        return None

    infObjs = pc.skinCluster(skin,query=True,inf=True)

    ns = infObjs[0].namespace()

    infs = [str(inf.stripNamespace()) for inf in infObjs]
    weights = getWeights(inObject)
    
    return [inObject, infs, weights, ns]

def serializeSkin(skin):
    return "{0};{1};{2};{3}".format(str(skin[0].stripNamespace()), str(skin[1]), str(skin[2]), skin[3])

def deserializeSkin(serializedSkin):
    skin = None
    try:
        objName, jointNames, weightsString, ns = serializedSkin.split(";")
        obj = getNode(objName)
        if obj is None:
            objs = pc.ls("*:" + objName)
            if len(objs) > 0:
                for subObj in objs:
                    shape = subObj.getShape()
                    if shape != None and shape.type() in CONST_SKINNABLES:
                        obj = subObj
                        break

        weightsString = weightsString.strip("[]")
        weights = [float(f) for f in weightsString.split(",")]

        joints = eval(jointNames)
        if pc.objExists(joints[0]):
            ns = ""
        else:
            objs = pc.ls("*:" + joints[0], type="joint")
            if len(objs) > 0:
                ns = objs[0].namespace()

        skin = [obj, joints, weights, ns]
    except Exception as e:
        pc.warning("Deserialize skin error : " + str(e))
        return None

    return skin

def storeSkins(inObjects, inPath=None):
    skins = []
    
    for inObject in inObjects:
        skin = storeSkin(inObject)
        if skin != None:
            #skin[0] = skin[0].name()
            skins.append(skin)
        else:
            pc.warning("Can't get skin on " + inObject.name())
    
    if len(skins) > 0 and inPath != None:
        f = None
        try:
            f = open(inPath, 'w')
            
            for skin in skins:
                f.write(serializeSkin(skin)+LINESEP)
        except Exception as e:
            pc.warning("Cannot save skin file to " + inPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    return skins

def zeroOutDeformers(inSkin, inInfluences=[]):
    infs = inSkin[1]
    weights = inSkin[2]
    nVerts = int(len(weights) / len(infs))

    i = 0
    for inf in inInfluences:
        if inf in infs:
            index = infs.index(inf)
            weights[index * nVerts : (index + 1) * nVerts ] = [0.0] * nVerts
        i += 1

    inSkin[2] = weights

    return inSkin

def applyWeightMap(inSkin, inWeightMap):
    infs = inSkin[1]
    nInfs = len(infs)
    weights = inSkin[2]
    nVerts = int(len(weights) / nInfs)

    for i in xrange(nInfs):
        for j in xrange(nVerts):
            weights[i * nVerts + j] *= inWeightMap.get(j, 0.0)

    inSkin[2] = weights

    return inSkin

def loadSkin(inSkin, inObject=None, inZeroInfs=None, inMode=0, inOpacity=1.0, inNormalize=True, inRemapDict=None, inWeightMap=None):
    """
        Modes :
            0 : Replace
            1 : Overwrite
            2 : Add
            3 : Blend
    """
    if not inZeroInfs is None:
        if isinstance(inZeroInfs, basestring):
            inZeroInfs = ",".split(inZeroInfs)
        zeroOutDeformers(inSkin, inZeroInfs)

    if not inWeightMap is None and len(inWeightMap) > 0:
        if inMode == 0:
            inMode = 1
        applyWeightMap(inSkin, inWeightMap)

    if not inRemapDict is None:
        infs = inSkin[1]
        for i in xrange(len(infs)):
            infs[i] = inRemapDict.get(infs[i], infs[i])

    obj = inSkin[0] if inObject == None else inObject

    if obj is None:
        pc.warning("No object given !")
        return None

    ns = obj.namespace()
    infs = []

    if cmds.objExists(ns + inSkin[1][0]):
        infs = [ns + inf for inf in inSkin[1]]
    elif cmds.objExists(inSkin[3] + inSkin[1][0]):
        infs = [inSkin[3] + inf for inf in inSkin[1]]

    if len(infs) > 0:
        weights = inSkin[2]
        
        skin = getSkinCluster(obj)
        
        cons = []

        if skin != None:
            cons = getNodeConnections(skin, "nodeState")

        newSkin = setWeights(obj, infs, weights, inMode=inMode, inOpacity=inOpacity, inNormalize=inNormalize)

        if len(cons) > 0:
            #print "cons", str(cons)
            setNodeConnections(newSkin, cons)

        return newSkin
    else:
        pc.warning("No influences given !")
        return None

def loadSkins(inSkins, inObjects=None, inZeroInfs=None, inMode=0, inOpacity=1.0, inNormalize=True, inRemapDict=None, inWeightMaps=None):
    """
        Modes :
            0 : Replace
            1 : Overwrite
            2 : Add
            3 : Blend
    """

    inWeightMaps = inWeightMaps or []

    if isinstance(inSkins, basestring):
        skinsPath = inSkins

        inSkins = []
        f = None
        try:
            f = open(skinsPath, 'r')
            lines =  f.readlines()

            for line in lines:
                inSkins.append(deserializeSkin(line))

        except Exception as e:
            pc.warning("Cannot load skinnings file from " + skinsPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

        if len(inSkins) == 0:
            pc.warning("Cannot deserialize skin infos from " + skinsPath)
            return

    if inObjects == None or len(inObjects) == 0:
        for idx, inSkin in enumerate(inSkins):
            wm = inWeightMaps[idx] if len(inWeightMaps) > idx else None
            loadSkin(inSkin, inZeroInfs=inZeroInfs, inMode=inMode, inOpacity=inOpacity, inNormalize=inNormalize, inRemapDict=inRemapDict, inWeightMap=wm)
    else:
        for inObject in inObjects:
            pointCount = pc.polyEvaluate(inObject, vertex=True)
            found = None

            for idx, inSkin in enumerate(inSkins):
                wm = inWeightMaps[idx] if len(inWeightMaps) > idx else None
                if not inSkin[0] is None and inObject.stripNamespace() == inSkin[0].split(":")[-1]:
                    loadSkin(inSkin, inObject, inZeroInfs=inZeroInfs, inMode=inMode, inOpacity=inOpacity, inNormalize=inNormalize, inRemapDict=inRemapDict, inWeightMap=wm)
                    found = inSkin
                    break

            if found is None:
                #Second pass, apply to an object with matching pointCount
                for idx, inSkin in enumerate(inSkins):
                    wm = inWeightMaps[idx] if len(inWeightMaps) > idx else None
                    if pointCount == getSkinPointCount(inSkin):
                        loadSkin(inSkin, inObject, inZeroInfs=inZeroInfs, inMode=inMode, inOpacity=inOpacity, inNormalize=inNormalize, inRemapDict=inRemapDict, inWeightMap=wm)
                        found = inSkin
                        break

            if not found:
                pc.warning("Can't find skin for object "+ inObject.name())

def reSkin(inObjects):
    for inObject in inObjects:
        skin = storeSkin(inObject)
        if skin != None:
            pc.skinCluster(inObject,edit=True, unbind=True)
            loadSkin(skin)
        else:
            pc.warning("Can't get skin on " + inObject.name())

def getDeformers(inMeshes):
    defs = []
    for obj in inMeshes:
        skin = getSkinCluster(obj)
        if skin != None:
            defs.extend(skin.getInfluence())

    return list(set(defs))

def selectDeformers(inObjs=None):
    if inObjs == None:
        inObjs = pc.selected()

    defs = getDeformers(inObjs)
    
    if len(defs) > 0:
        pc.select(defs, replace=True)
    else:
        pc.select(clear=True)

def combine(inObjects, inMergeUVSets=1, inConstructionHistory=False,  inName="COMBINED", inKeepSkinning=True, inReduce=1.0):
    dupinObjects = pc.duplicate(inObjects, rr=True)

    if inReduce < 1.0:
        for obj in dupinObjects:
            pc.polyReduce(obj, percentage=inReduce*100.0, uvWeights=0, colorWeights=0, keepQuadsWeight=1, keepBorder=1, keepMapBorder=1, keepOriginalVertices=0, keepHardEdge=1, compactness=0.5, triangulate=0, replaceOriginal=1, cachingReduce=0, ch=0)

    mesh = pc.polyUnite(dupinObjects,ch=0, mergeUVSets=inMergeUVSets, name=inName)[0]

    if inKeepSkinning:
        pc.skinCluster(mesh, getDeformers(inObjects))

        argSel = inObjects[:]
        argSel.append(mesh)

        pc.select(argSel)

        pc.copySkinWeights(surfaceAssociation="closestPoint", influenceAssociation="closestJoint", noMirror=True)

    pc.select(mesh)

    return mesh

def gator(inSources, inRef, inCopyMatrices=False, inDirectCopy=False, inReversed=False, inWeightMaps=None):
    startTimer("Gator", inReset=True)
    inWeightMaps = inWeightMaps or []

    if inReversed:
        sourcesSkins = []
        skinnedSources = []

        for source in inSources:
            sourceSkin = getSkinCluster(source)
            if sourceSkin == None:
                pc.warning("No skinCluster found on ref object " + source.name())
            else:
                sourcesSkins.append(sourceSkin)
                skinnedSources.append(source)

        infs = getDeformers(skinnedSources)

        if getSkinCluster(inRef) != None:
            pc.skinCluster(inRef,edit=True, unbind=True)

        skin = pc.skinCluster(inRef,infs, toSelectedBones=True, name=inRef.name() + "_skinCluster")

        pc.select(skinnedSources)
        pc.select(inRef, add=True)

        pc.copySkinWeights(surfaceAssociation="closestPoint", influenceAssociation="closestJoint", noMirror=True)
    else:
        refSkin = getSkinCluster(inRef)
        if refSkin == None:
            pc.error("No skinCluster found on ref object " + inRef.name())
        
        refSkinName = refSkin.name()

        storedSkin = None
        if inDirectCopy:
            storedSkin = storeSkin(inRef)

        infs = getDeformers([inRef])
        for idx, source in enumerate(inSources):
            oldWeights = None
            wm = inWeightMaps[idx] if len(inWeightMaps) > idx else None

            if getSkinCluster(source) != None:
                if not wm is None:
                    oldWeights = storeSkin(source)
                if not (inDirectCopy and not wm is None):
                    pc.skinCluster(source,edit=True, unbind=True)

            if not (inDirectCopy and not wm is None):
                skin = pc.skinCluster(source,infs, toSelectedBones=True, name=source.name() + "_skinCluster")

            if inDirectCopy:
                skin = loadSkin(storedSkin, inObject=source, inWeightMap=wm)
            else:
                pc.copySkinWeights(ss=refSkin, ds=skin, surfaceAssociation="closestPoint", influenceAssociation=["label", "oneToOne"], noMirror=True)

                if not oldWeights is None:
                    #reverse the wm
                    pCount = getSkinPointCount(oldWeights)
                    reversedWm = {}
                    for i in xrange(pCount):
                        value = wm.get(i, 0.0)
                        if value < 1.0:
                            reversedWm[i] = 1.0 - value

                    skin = loadSkin(oldWeights, inObject=source, inWeightMap=reversedWm)

            skinName = skin.name()
            if inCopyMatrices:
                haveChanged = False
                for inf in infs:
                    refIndex = -1
                    targetIndex = -1

                    cons = cmds.listConnections(inf.name(), type="skinCluster", plugs=True)
                    for con in cons:
                        if refSkinName+".matrix[" in con:
                            refIndex = con[len(refSkinName+".matrix["):-1]
                        elif skinName+".matrix[" in con:
                            targetIndex = con[len(skinName+".matrix["):-1]

                    if refIndex != -1 and targetIndex != -1:
                        pc.setAttr(skinName+".bindPreMatrix["+targetIndex+"]",pc.getAttr(refSkinName+".bindPreMatrix["+refIndex+"]"), type="matrix")
                        haveChanged = True
                    else:
                        pc.warning("Cannot resolve indices for " + inf + ", " + skinName)

                if pc.versions.current() > 201600:
                    #With maya 2016, binding pre-matrices are cached into skinCluster node so we have to consider the node dirty...
                    pc.dgdirty(skin)

    stopTimer("Gator", inLog=True)

def setRefPose(inDef, inSkins=None, inMatrix=None):
    attrs = pc.listConnections(inDef, type="skinCluster", plugs=True)
    if inSkins == None:
        inSkins = pc.listConnections(inDef, type="skinCluster")
    
    for skin in inSkins:
        haveChanged = False
        for attr in attrs:
            if attr.type() == "matrix" and attr.node() == skin:
                m = inDef.worldInverseMatrix.get() if inMatrix == None else inMatrix
                skin.bindPreMatrix[attr.index()].set(m)
                haveChanged = True
                break
        
        if haveChanged and pc.versions.current() > 201600:
            #With maya 2016, binding pre-matrices are cached into skinCluster node so we have to consider the node dirty...
            pc.dgdirty(skin)

def getRefPose(inDef, inSkin):
    attrs = pc.listConnections(inDef, type="skinCluster", plugs=True)
    for attr in attrs:
        if attr.node() == inSkin and attr.type() == "matrix":
            return inSkin.bindPreMatrix[attr.index()].get()
    
    return None

def setRefPoses(inDefs=None, inSkins=None):
    if inDefs == None and inSkins == None:
        raise Exception("Deformers and skinClusters cannot both be 'None' !")
        
    if inDefs == None:
        inDefs = []
        for skin in inSkins:
            inDefs.extend(skin.getInfluence())
    
    for inf in inDefs:
        setRefPose(inf, inSkins)

def replaceDeformers(oldDefs, newDef=None, doDelete=False, inSkins=None, inRefsSkins=None):
    skins_defs = {}

    skins_refs = {}
    if inRefsSkins != None:
        for i in range(len(inSkins)):
            skins_refs[inSkins[i]] = inRefsSkins[i]

    for oldDef in oldDefs:
        skins = oldDef.listConnections(type="skinCluster", source=False)
        for skin in skins:
            if inSkins != None and not skin in inSkins:
                continue
            if skin in skins_defs:
                if not oldDef in skins_defs[skin]:
                    skins_defs[skin].append(oldDef)
            else:
                 skins_defs[skin] = [oldDef]

    for skin in iter(skins_defs):
        #Deactivate normalization
        normalization = pc.getAttr(skin.name() + ".normalizeWeights")
        pc.setAttr(skin.name() + ".normalizeWeights", 0)
        
        geo = skin.getGeometry()[-1]
        influences = skin.getInfluence()
        mergedValues = None
        
        if newDef == None:
            refSkin = skins_refs[skin]
            refGeo = refSkin.getGeometry()[-1]
            refInfluences = refSkin.getInfluence()
            
            for inf in skins_defs[skin]:
                index = influences.index(inf.name())
                vertsValues = list(skin.getWeights(geo, index))
                if mergedValues == None:
                    mergedValues = vertsValues
                else:
                    for i in range(len(vertsValues)):
                        mergedValues[i] += vertsValues[i]
            
            #print "mergedValues",len(mergedValues),mergedValues
            newDefsValues = {}
            for inf in refInfluences:
                index = refInfluences.index(inf.name())
                vertsValues = list(refSkin.getWeights(refGeo, index))
                #print "vertsValues",len(vertsValues),vertsValues
                nonZero=False
                newWeights=[]
                for i in range(len(mergedValues)):
                    newWeights.append(mergedValues[i] * vertsValues[i])
                    if newWeights[-1] > 0.0:
                        nonZero=True
                if nonZero:
                    newDefsValues[inf] = newWeights
                
            #set new deformerS weights
            for newDef, newWeights in newDefsValues.items():
                if not newDef.name() in influences:
                    skin.addInfluence(newDef, weight=0.0)
                    influences = skin.getInfluence()
                index = influences.index(newDef.name())
                skin.setWeights(geo, [index], newWeights, normalize=False)
        else:
            if not newDef.name() in influences:
                skin.addInfluence(newDef, weight=0.0)
                influences = skin.getInfluence()
            else:
                index = influences.index(newDef.name())
                mergedValues = list(skin.getWeights(geo, index))
            
            newDefIndex = influences.index(newDef.name())
    
            for inf in skins_defs[skin]:
                index = influences.index(inf.name())
                vertsValues = list(skin.getWeights(geo, index))
                if mergedValues == None:
                    mergedValues = vertsValues
                else:
                    for i in range(len(vertsValues)):
                        mergedValues[i] += vertsValues[i]

            #set new deformer weights
            skin.setWeights(geo, [newDefIndex], mergedValues, normalize=False)

        #set old deformer weights to 0.0 and remove them from influence list
        zeroWeights = [0.0 for i in range(len(mergedValues))]
        for inf in skins_defs[skin]:
            skin.setWeights(geo, [influences.index(inf.name())], zeroWeights, normalize=False)
        for inf in skins_defs[skin]:
             skin.removeInfluence(inf)
        
        #Reset normalization     
        pc.setAttr(skin.name() + ".normalizeWeights", normalization)

    if doDelete:
        pc.delete(oldDefs)

def safeReplaceDeformers(ns, oldDefsStr, newDefStr, doDelete=False):
    oldDefs = []
    oldDefsSplit = [ns + ":" + defName for defName in oldDefsStr.split(",")] 
    for oldDef in oldDefsSplit:
        obj = getNode(oldDef)
        if not obj is None:
            oldDefs.append(obj)
        else:
            pc.warning(oldDef + " does not exists !")

    newDefName = ns + ":" + newDefStr
    newDef = getNode(newDefName)

    if len(oldDefs) > 0 and newDef != None:
        replaceDeformers(oldDefs, newDef, doDelete=doDelete)
    else:
        pc.warning("Can't execute safeReplaceDeformers, not enough objects found (%s, %s, %s)" % (ns, oldDefsStr, newDefStr))

def removeUnusedInfs(inSkin, inInfs=None):
    removedInfluences = []

    #Convert PyNodes to string as we'll use quicker maya cmds implementation for this purpose
    if not isinstance(inSkin, basestring):
        inSkin = inSkin.name()

    if inInfs == None:
        inInfs = cmds.skinCluster(inSkin,query=True,inf=True)
    elif not isinstance(inInfs[0], basestring):
        inInfs = [n.name() for n in inInfs]

    weightedInfluences = cmds.skinCluster(inSkin, query=True, wi=True)
        
    #Set skinCluster to HasNoEffect so it won't process after each removal (if we can !)
    oldState = None
    stateAttrname = "{0}.nodeState".format(inSkin)

    if len(pc.listConnections(stateAttrname)) == 0:
        oldState = cmds.getAttr(stateAttrname)
        cmds.setAttr(stateAttrname, 1)

    for inf in inInfs:
        if not inf in weightedInfluences:
            #remove the influence since it has no effect
            cmds.skinCluster(inSkin, edit=True, ri=inf)
            removedInfluences.append(inf)

    #restore the old node state
    if not oldState is None:
        cmds.setAttr(stateAttrname, oldState)

    return removedInfluences

type_priority = {
        "blendShape":10,
        "cluster":15,
        "skinCluster":20,
        "shrinkWrap":25,
        "nonLinear":27,
        "ffd":30
        }

def getSelectedIndices(node=None):
    vertSel = pc.ls(orderedSelection=True)
    
    if len(vertSel) == 0:
        return (None, None)
    
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

def expandCompIndices(inComps):
    comps = []

    nodeComps = {}
    
    for comp in inComps:
        node = comp.node()
        if not node in nodeComps:
            if isinstance(comp, pc.general.MeshVertex):
                nodeComps[node] = [c for c in node.vtx]
            elif isinstance(comp, pc.general.MeshFace):
                nodeComps[node] = [c for c in node.f]
            else:
                break

        for curIdx in comp.indices():
            comps.append(nodeComps[node][curIdx])

    return comps

COMPS_SHORTCUTS = {
    "MeshVertex":"vtx",
    "MeshFace":"f",
    "MeshEdge":"e"
}

def selectComponents(node, indices, inType):
    compShortcut = COMPS_SHORTCUTS[inType]
    
    strSel = ["{0}.{1}[{2}]".format(node.name(), COMPS_SHORTCUTS[inType], index) for index in indices]
    pc.select(strSel)

def selectLoops(skip=1, showWaves=False):
    node, indices = getSelectedIndices()
    
    if node is None:
        pc.warning("Nothing selected !")
        return
    
    compType = getType(pc.selected()[0])
    
    if compType is None:
        pc.warning("Unknown component type selected !")
        return
    
    managed = indices
    
    finallySelected = managed[:]
    
    counter = 0
    skipper = skip
    while True and counter < 1000:
        pc.mel.eval("GrowPolygonSelectionRegion")
        node, selected = getSelectedIndices()
        filtered=[]
        
        for comp in selected:
            if comp in managed:
                continue
            
            managed.append(comp)
            filtered.append(comp)
        
        if len(filtered) > 0:
            selectComponents(node, filtered, compType)
            if skipper == 0:
                skipper = skip
                
                finallySelected.extend(filtered)
            else:
                skipper -= 1
        else:
            break
                
        counter += 1
        
        if showWaves:
            pc.refresh()
            time.sleep(0.1)

    if counter >= 1000:
        pc.warning("BROKEN LOOP !")
        
    selectComponents(node, finallySelected, compType)

def equilibratePointWeight(inPoint, inRightToLeft = False, inPrefixes = None, inSkin = None, inInfs = None):
    if inPrefixes == None:
        inPrefixes = ["Left", "Right"]
    if inRightToLeft:
        inPrefixes[0], inPrefixes[1] = inPrefixes[1], inPrefixes[0]

    node = inPoint.node()
    if inSkin == None:
        inSkin = getSkinCluster(node)

    if inSkin == None:
        pc.warning("No skinCluster found on {0}".format(node.name()))
        return

    if inInfs == None:
        inInfs = [inf.name() for inf in inSkin.getInfluence()]

    weights = pc.skinPercent(inSkin, inPoint, query=True, value=True )
    
    sidedWeights = 1.0
    leftWeights = 0.0

    numInfs = len(inInfs)
    rangeInfs = range(numInfs)

    for i in rangeInfs:
        if inInfs[i].split(":")[-1].startswith(inPrefixes[0]) and inInfs[i].replace(inPrefixes[0], inPrefixes[1]) in inInfs:
            leftWeights += weights[i]
        elif not inInfs[i].split(":")[-1].startswith(inPrefixes[1]):
            sidedWeights -= weights[i]
    
    if leftWeights > 0:
        norm = (sidedWeights / 2.0) / leftWeights
        
        newWeights = weights[:] 
        
        for i in rangeInfs:
            if inInfs[i].split(":")[-1].startswith(inPrefixes[0]):
                rightName = inInfs[i].replace(inPrefixes[0], inPrefixes[1])
                if rightName in inInfs:
                    newWeights[i] *= norm
                    rightI  = inInfs.index(rightName)
                    newWeights[rightI] = newWeights[i]
        
        pc.skinPercent(inSkin, inPoint, transformValue=[(inInfs[i],newWeights[i]) for i in rangeInfs] )

def equilibrateSelPointsWeights(inRightToLeft = False, inPrefixes = None):
    node, indices = getSelectedIndices()
    
    selPoints = [node.vtx[i] for i in indices]
    
    if len(selPoints) == 0:
        pc.warning("Please select some points to equilibrate")
        return

    inSkin = getSkinCluster(node)
    inInfs = [inf.name() for inf in inSkin.getInfluence()]
    
    for selPoint in selPoints:
        equilibratePointWeight(selPoint, inRightToLeft, inPrefixes, inSkin, inInfs)

def reorderDeformers(inObj, inTypesPriorities=None):

    objName = inObj
    if not isinstance(objName, basestring):
        objName = objName.name()

    if inTypesPriorities == None:
        inTypesPriorities = type_priority

    managedHistory = cmds.ls(cmds.listHistory(objName, gl=True, pdo=True, lf=True, f=False, il=2), type=list(inTypesPriorities.keys()))
    if len(managedHistory) < 2:
        return

    sortedHistory = sorted(managedHistory, key=lambda x: inTypesPriorities[cmds.nodeType(x)], reverse=True)

    maxIterations = len(managedHistory)
    iterations = 0

    if managedHistory != sortedHistory:
        tkLogger.debug("Need to reorder {0} deformers".format(objName))
        while managedHistory != sortedHistory:
            iterations += 1
            if maxIterations <= iterations:
                cmds.warning("Max iterations reached ({0}), cannot reorder deformers correctly !!".format(maxIterations))
                break

            for i in range(len(managedHistory)):
                if managedHistory[i] != sortedHistory[i]:
                    newIndex = sortedHistory.index(managedHistory[i])
                    if newIndex > 0:
                        #Embed reorderDeformers in try/except because it can fail if deformers are not correctly disconnected
                        try:
                            cmds.reorderDeformers(sortedHistory[newIndex-1], managedHistory[i], objName)
                        except:
                            pass

                        managedHistory = cmds.ls(cmds.listHistory(objName, gl=True, pdo=True, lf=True, f=False, il=2), type=list(inTypesPriorities.keys()))
                        break
    else:
        tkLogger.debug("No need to reorder {0} deformers".format(objName))

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____                                _                   __     _   _        _ _           _          __  
 |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___   / /__ _| |_| |_ _ __(_) |__  _   _| |_ ___  __\ \ 
 | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __| | |/ _` | __| __| '__| | '_ \| | | | __/ _ \/ __| |
 |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \ | | (_| | |_| |_| |  | | |_) | |_| | ||  __/\__ \ |
 |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/ | |\__,_|\__|\__|_|  |_|_.__/ \__,_|\__\___||___/ |
                                                         \_\                                           /_/ 

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def getSelectedAttrs():
    """
    Get selected attributes in channel box
    """
    selAttrs = []
    
    sel = pc.selected()
    
    if len(sel) > 0:
        attrs = pc.channelBox("mainChannelBox", query=True, sma=True)
    
        if not attrs is None and len(attrs) > 0:
            for selObj in sel:
                for selAttr in attrs:
                    if pc.attributeQuery(selAttr, node=selObj, exists=True):
                        selAttrs.append("{0}.{1}".format(selObj.name(), selAttr))

    return selAttrs

def getConnectionsRecur(inNode, inSource=False, inDestination=True, inAlreadyCollected=None):
    if inAlreadyCollected is None:
        inAlreadyCollected = []

    cons = [con for con in pc.listConnections(inNode, source=inSource, destination=inDestination) if(inAlreadyCollected is None or not con in inAlreadyCollected)]
    
    inAlreadyCollected.extend(cons)
    
    thisCons = cons[:]
    for con in thisCons:
        cons.extend(getConnectionsRecur(con, inSource=inSource, inDestination=inDestination, inAlreadyCollected=inAlreadyCollected))

    return cons

def graphAttrs(inAttrs=None, inSource=False, inDestination=True, inMaxDepth=100, inShowNodal=True):
    if inAttrs is None:
        inAttrs = getSelectedAttrs()

    if len(inAttrs) == 0:
        pc.warning("No attributes given !")
        return []

    collectedNodes = []

    attrNodes = getNodes(inAttrs)

    for attrNode in attrNodes:
        collectedNodes.extend(getConnectionsRecur(attrNode, inSource=inSource, inDestination=inDestination))
    
    if inShowNodal:
        allNodes = collectedNodes[:]
        allNodes.extend(attrNodes)
        
        pc.select(clear=True)
        
        nodeEd = pc.mel.eval("nodeEditorWindow")
        pc.select(allNodes)
        pc.nodeEditor(nodeEd, edit=True, createTab=[-1], traversalDepthLimit=0)
        pc.evalDeferred("pc.nodeEditor(\""+nodeEd+"\", edit=True, addNode=\"\")")
        
    return collectedNodes



ATTRWALK = {
    "unitConversion":"input",
    "multDoubleLinear":"input1",
    "addDoubleLinear":"input1"
}

def getRealAttr(inAttr, inSkipCurves=True):
    ns = ""
    if ":" in inAttr:
        ns = inAttr.split(":")[0] + ":"

    conAttr = ""
    conAttrs = pc.listConnections(inAttr, destination=False, plugs=True)

    if len(conAttrs) > 0:
        for conAttrCandidate in conAttrs:
            candidate = conAttrCandidate
            if candidate.nodeType() in ATTRWALK:
                candidate = candidate.node().attr(ATTRWALK[candidate.nodeType()])

            if not inSkipCurves or not candidate.nodeType() in ANIMTYPES:
                conAttr = candidate
                if not inSkipCurves and candidate.nodeType() in ANIMTYPES:
                    return candidate
                break

    while conAttr != "":
        inAttr = conAttr.name()
        conAttr = ""
        conAttrs = pc.listConnections(inAttr, destination=False, plugs=True)
        if len(conAttrs) > 0:
            for conAttrCandidate in conAttrs:
                candidate = conAttrCandidate
                if candidate.nodeType() in ATTRWALK:
                    candidate = candidate.node().attr(ATTRWALK[candidate.nodeType()])

                if not inSkipCurves or not candidate.nodeType() in ANIMTYPES:
                    conAttr = candidate
                    if not inSkipCurves and candidate.nodeType() in ANIMTYPES:
                        return candidate
                    break

    return inAttr

def setRealAttr(inAttr, inValue):
    ns = ""
    if ":" in inAttr:
        ns = inAttr.split(":")[0] + ":"

    conAttr = ""
    conAttrs = pc.listConnections(inAttr, destination=False, plugs=True)
    for conAttrCandidate in conAttrs:
        if not conAttrCandidate.nodeType() in ANIMTYPES:
            conAttr = conAttrCandidate
            break
    while conAttr != "":
        inAttr = conAttr
        conAttr = ""
        conAttrs = pc.listConnections(inAttr, destination=False, plugs=True)
        for conAttrCandidate in conAttrs:
            if not conAttrCandidate.nodeType()in ANIMTYPES:
                conAttr = conAttrCandidate
                break

    splitAttr = inAttr.split(".")
    objName = splitAttr[0]
    attrName = splitAttr[1]

    pc.cutKey(objName, attribute=attrName)
    pc.setAttr(inAttr, inValue)

def get_next_free_multi_index( attr_name, start_index=0 ):
    '''Find the next unconnected multi index starting at the passed in index.'''
    # assume a max of 10 million connections
    while start_index < 10000000:
        if len( pc.connectionInfo('{0}[{1}]'.format(attr_name, start_index), sfd=True ) or [] ) == 0:
            return start_index
        start_index += 1

    return start_index

def disconnect(inParam):
    cons = pc.listConnections(inParam, destination=False, plugs=True)
    try:
        for con in cons:
            pc.disconnectAttr(con, inParam)
            if con.node().type() == "expression" and len(pc.listConnections(con, source=False, destination=True)) == 0:
                pc.delete(con.node())
    except:
        return False

    return True

def getAllConnections(inAttr, inSource=True, inDestination=True, inExcludeTypes=None, inVerbose=False, inSkipConversions=True):
    inExcludeTypes = inExcludeTypes or []

    cons = []
    if inSource:
        #print "inSource",inAttr.listConnections(source=True, destination=False, plugs=True, connections=True)
        #for connnn in inAttr.listConnections(source=True, destination=False, plugs=True, connections=True):
        #    print (connnn[1].node().type())
        
        tempCons = [ c for c in inAttr.listConnections(source=True, destination=False, plugs=True, connections=True, skipConversionNodes=inSkipConversions) if not c[1].node().type() in inExcludeTypes]
        for i in range(len(tempCons)):
            tempCons[i] = (tempCons[i][1], tempCons[i][0])
        cons.extend(tempCons)

    if inDestination:
        #print "inDestination",inAttr.listConnections(source=False, destination=True, plugs=True, connections=True)
        cons.extend([ c for c in inAttr.listConnections(source=False, destination=True, plugs=True, connections=True, skipConversionNodes=inSkipConversions) if not c[1].node().type() in inExcludeTypes])

    if len(cons) == 0 and inAttr.isCompound():
        childAttrs = inAttr.children()
        for childAttr in childAttrs:

            if inSource:
                #print "inSource",childAttr.listConnections(source=True, destination=False, plugs=True, connections=True)
                tempCons = [ c for c in childAttr.listConnections(source=True, destination=False, plugs=True, connections=True, skipConversionNodes=inSkipConversions) if not c[1].node().type() in inExcludeTypes]
                for i in range(len(tempCons)):
                    tempCons[i] = (tempCons[i][1], tempCons[i][0])
                cons.extend(tempCons)

            if inDestination:
                #print "childAttr",inAttr.listConnections(source=False, destination=True, plugs=True, connections=True)
                cons.extend([ c for c in childAttr.listConnections(source=False, destination=True, plugs=True, connections=True, skipConversionNodes=inSkipConversions) if not c[1].node().type() in inExcludeTypes])

    if inVerbose:
        for con in cons:
            tkLogger.debug(str(con) + " " + con[1].node().type())

    return cons

def getNodeConnections(inNode, *args, **kwargs):
    """
    kwargs includes :
        inSource (default True)
        inDestination (default True)
        inDisconnect (default False)
        inExcludeTypes (default None)
        inCustomOnly (default False)
        inVerbose (default False)
    """
    
    inSource = kwargs.get("inSource", True)
    inDestination = kwargs.get("inDestination", True)
    inDisconnect = kwargs.get("inDisconnect", False)
    inExcludeTypes = kwargs.get("inExcludeTypes")
    inCustomOnly = kwargs.get("inCustomOnly", False)
    inVerbose = kwargs.get("inVerbose", False)

    if len(args) == 0:#Auto-detect attrs
        connections = inNode.listConnections(source=inSource, destination=inDestination, plugs=True, connections=True, skipConversionNodes=False)
        args = []
        for connection in connections:
            #print connection[0], type(connection[0])
            #print connection[0].getAlias(), type(connection[0].getAlias())
            args.append(connection[0].getAlias() or connection[0].shortName())

    cons = []
    for arg in args:
        cons.extend(getAllConnections(inNode.attr(arg), inSource, inDestination, inExcludeTypes, inVerbose))

    if kwargs.get("inDisconnect", False):
        for con in cons:
            con[0].disconnect(con[1])

    baked = str(cons)
    return cons

def setNodeConnections(inCons, inNode=None, inDestination=False, inSetBefore=False):
    for linkOutput, linkInput in inCons:
        outputAttr = linkOutput
        inputAttr = linkInput

        if not inNode is None:
            if inDestination:
                #print ("linkOutput",linkOutput, type(linkOutput))
                outputName = linkOutput.split(".")[-1]
                
                """
                if not pc.attributeQuery(outputName, node=inNode, exists=True):
                    pc.warning("Can't 'setNodeConnections', '{0}' don't have attribute '{1}' !".format(inNode.name(), outputName))
                    continue
                """
                try:
                    outputAttr = inNode.attr(outputName)
                except:
                    continue
            else:
                #print ("linkInput",linkInput, type(linkInput))
                inputName = linkInput.split(".")[-1]
                """
                if not pc.attributeQuery(inputName, node=inNode, exists=True):
                    pc.warning("Can't 'setNodeConnections', '{0}' don't have attribute '{1}' !".format(inNode.name(), inputName))
                    continue
                """
                try:
                    inputAttr = inNode.attr(inputName)
                except:
                    continue
        try:
            if len(inputAttr.listConnections(source=True, destination=False)) > 0:
                pc.warning("Can't 'setNodeConnections', '{0}' already connected !".format(inputAttr))
                continue
        except:
            continue

        if inSetBefore:
            outputAttr.set(inputAttr.get())
        
        try:
            outputAttr >> inputAttr
        except:
            pass

def matchConnections(inNode, inRefNode, *args, **kwargs):
    """
    kwargs includes :
        inSource (default True)
        inDestination (default True)
        inDisconnect (default False)
        inShape (default False)
        inCustomOnly (default False)
    """
    inCustomOnly = kwargs.get("inCustomOnly", False)
    
    setNodeConnections(getNodeConnections(inRefNode, *args, **kwargs), inNode)

    if kwargs.get("inShape", False) and inNode.type() == "transform" and inRefNode.type() == "transform":
        shape = inNode.getShape()
        refShape = inRefNode.getShape()

        if not shape is None and not refShape is None:
            setNodeConnections(getNodeConnections(refShape, *args, **kwargs), shape)

def serializeConnections(inCons):
    return "|".join([a.stripNamespace() + ";" + b.stripNamespace() for a,b in inCons])

def deserializeConnections(serializedCons):
    newCons = []

    serCons = serializedCons.split("|")

    for serCon in serCons:
        a,b = serCon.split(";")


        nodeName, attrName = a.split(".", 1)
        node = getNode(nodeName, inConsiderNs=True)
        aAttr = "." + attrName

        if not node is None and node.hasAttr(attrName):
            aAttr = node.attr(attrName)

        nodeName, attrName = b.split(".", 1)
        node = getNode(nodeName, inConsiderNs=True)
        bAttr = "." + attrName

        if not node is None and node.hasAttr(attrName):
            bAttr = node.attr(attrName)

        newCons.append((aAttr, bAttr))

    return newCons

def storeConnections(inNode, *args, **kwargs):
    """
    kwargs includes :
        inSource (default True)
        inDestination (default True)
        inDisconnect (default False)
        inExcludeTypes (default None)
        inCustomOnly (default False)
        inVerbose (default False)

        inPath (default None)
    """
    
    inPath = kwargs.get("inPath")

    cons = getNodeConnections(inNode, *args, **kwargs)

    if len(cons) > 0 and inPath != None:
        f = None
        try:
            f = open(inPath, 'w')
            f.write(serializeConnections(cons))
        except Exception as e:
            pc.warning("Cannot save connections file to " + inPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    return cons

def loadConnections(inCons, inObject):
    if isinstance(inCons, basestring):
        consPath = inCons

        inCons = []
        f = None
        try:
            f = open(consPath, 'r')
            lines =  f.read()
            inCons = deserializeConnections(lines)
        except Exception as e:
            pc.warning("Cannot load connections file from " + consPath + " : " + str(e))
        finally:
            if f != None:
                f.close()

    #Resolve destinations
    cleanCons = []

    for a,b in inCons:
        if isinstance(a, basestring):
            pc.warning("Can't find source '{0}'".format(a))
            continue

        attrName = b
        if isinstance(b, basestring):
            attrName = b[1:]
        else:
            attrName = b.longName()

        if inObject.hasAttr(attrName):
            cleanCons.append((a, inObject.attr(attrName)))
        else:
            pc.warning("Can't find attribute '{0}' on '{1}'".format(attrName, inObject))

    setNodeConnections(cleanCons, inObject)

#connectDisconnectedChildren(pc.PyNode("rl4Embedded_Alix.bsOutputs"), inNode=None)
def connectEmptyChildren(inAttr, inNode=None):
    inNode = inNode or inAttr.node()
    
    arrayIndices = inAttr.getArrayIndices()
    
    lastIndex = arrayIndices[-1]
    
    for i in range(lastIndex+1):
        if not i in arrayIndices or len(inAttr[i].listConnections(source=False, destination=True)) == 0:
            inNode.addAttr("mock" + str(i))
            inAttr[i] >> inNode.attr("mock" + str(i))

#Valid for metahuman topology
MH_MEASURES = [
    (1537, 4608),
    (16972, 16851),
    (6004, 2925),
    ]

def getDistances(inMesh, inPoints):
    dist = []
    
    for startPoint, endPoint in inPoints:
        dist.append((pc.pointPosition("{0}.vtx[{1}]".format(inMesh, endPoint)) - pc.pointPosition("{0}.vtx[{1}]".format(inMesh, startPoint))).length())
    
    return dist
    
def getOffsets(inMesh1, inMesh2, inMesh1Points, inMesh2Points=None):
    inMesh2Points = inMesh2Points or inMesh1Points[:]

    dists1 = getDistances(inMesh1, inMesh1Points)
    dists2 = getDistances(inMesh2, inMesh2Points)
    
    offsets = []
    
    for i, d in enumerate(dists1):
        offsets.append(dists2[i]/d)

    return offsets

def matchMeshes(inMesh1, inMesh2, inMesh1Points, inMesh2Points=None, inReturnOnly=False):
    inMesh2Points = inMesh2Points or inMesh1Points[:]

    offsets = getOffsets(inMesh1, inMesh2, inMesh1Points, inMesh2Points)
    offset = mean(offsets)

    origScale = inMesh1.scale.get()

    newScale = [
        (origScale[0] * offset) / inMesh2.scaleX.get(),
        (origScale[1] * offset) / inMesh2.scaleY.get(),
        (origScale[2] * offset) / inMesh2.scaleZ.get(),
    ]

    lockedChannels = []
    channels = ["tx","ty","tz","rx","ry","rz","sx","sy","sz"]
    for channel in channels:
        if inMesh1.attr(channel).isLocked():
            inMesh1.attr(channel).unlock()
            lockedChannels.append(channel)

    inMesh1.scale.set(newScale)

    tOffset = pc.pointPosition("{0}.vtx[{1}]".format(inMesh2, inMesh2Points[1][1]), world=True) - pc.pointPosition("{0}.vtx[{1}]".format(inMesh1, inMesh1Points[1][1]), world=True)

    newTranslation = [
        inMesh1.translateX.get() + tOffset[0],
        inMesh1.translateY.get() + tOffset[1],
        inMesh1.translateZ.get() + tOffset[2],
    ]

    if inReturnOnly:
        inMesh1.scale.set(origScale)
    else:
        inMesh1.translate.set(newTranslation)

    for channel in lockedChannels:
        inMesh1.attr(channel).lock()

    return (newTranslation, [0.0, 0.0, 0.0], newScale)

def getParameters(inobject=None, customOnly=True, containerName="", keyableOnly=False):
    if containerName != "":
        inobject = getNode(inobject.name() + "_" + containerName)

    parameters = []

    if inobject != None:
        parameters = pc.listAttr(inobject, ud=customOnly, keyable=keyableOnly, shortNames=True)

    return parameters

def addProperty(inobject=None, name="NewProperty"):
    objectName = ""
    if isinstance(inobject, basestring):
        objectName = inobject
    else:
        objectName = inobject.name()

    prop = pc.group(name=objectName + "_" + name, empty=True, parent=inobject)
    pc.setAttr(prop.name() + ".tx", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".ty", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".tz", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".rx", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".ry", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".rz", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".sx", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".sy", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".sz", keyable=False, channelBox=False)
    pc.setAttr(prop.name() + ".v", keyable=False, channelBox=False)

    pc.setAttr(prop.name() + ".inheritsTransform", 0)
    pc.setAttr(prop.name() + ".visibility", 0)
    pc.setAttr(prop.name() + ".lodVisibility", 0)

    if "TK_OSCAR" in name:
        pc.setAttr(prop.name() + ".nodeState", 2)

    return prop

"""
booleanType : 0 = Enum, 1 = Int, 2= Bool
"""
def addParameter(inobject=None, name="NewParam", inType="double", default=None, min=None, max = None, softmin=None, softmax=None, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True):
    objectName = ""
    if isinstance(inobject, basestring):
        objectName = inobject
    else:
        objectName = inobject.name()

    if pc.objectType(getNode(objectName)) == "character" and "." in name:
        pc.character(name, addElement = getNode(objectName))
        return objectName + "." + name
    if containerName != "":
        realContainerName = objectName + "_" + containerName

        containerNode = getNode(realContainerName)
        if containerNode is None:
            inobject = addProperty(inobject, containerName)
        else:
            inobject = containerNode

        if isinstance(inobject, basestring):
            objectName = inobject
        else:
            objectName = inobject.name()

    increment = 0
    uniqueName = name
    if skipIfExists and pc.attributeQuery( uniqueName,node=objectName ,exists=True ):
        return "{0}.{1}".format(objectName, uniqueName)
    else:
        while(pc.attributeQuery( uniqueName,node=objectName ,exists=True )):
            increment += 1
            uniqueName = name + str(increment)

    name = uniqueName

    #base values
    if inType == "double" or inType == "doubleLinear" or inType == "float" or inType == "int":
        default = 0 if default == None else default
        min = -1000000 if min == None else min
        max = 1000000 if max == None else max
        softmin = -6000 if softmin == None else softmin
        softmax = 6000 if softmax == None else softmax
        if inType == "int":
            inType = "long"
    elif inType == "bool":
        inType = "enum;False:True" if booleanType == 0 else ("byte" if booleanType == 1 else "bool")
        default = 0 if (default == None or not default) else 1
        min = 0
        max = 1
        softmin = 0
        softmax = 1
    elif "enum" in inType:
        default = 0 if default == None else default
        if isinstance(default, basestring):
            enumValues = inType.split(";")[1].split(":")
            index = enumValues.index(default)
            if index == -1:
                index = 0
            default = index
    else:#shoud be string...
        default = "" if default == None else default

    if "enum" in inType:
        values = inType.split(";")[1]
        pc.addAttr(inobject, longName=name, attributeType="enum", keyable=expose and keyable, en=values, defaultValue=default, niceName=nicename)
    elif inType == "string":
        pc.addAttr(inobject, longName=name, dataType=inType, keyable=expose and keyable, niceName=nicename)
        if default != "":
            pc.setAttr(objectName + "." + name, default, type="string")
    else:
        pc.addAttr(inobject, longName=name, attributeType=inType, keyable=expose and keyable, defaultValue=default, minValue=min, maxValue=max,softMinValue=softmin,softMaxValue=softmax, niceName=nicename)

    if expose and not keyable:
        pc.setAttr(objectName + "." + name, channelBox=True)
    elif readOnly:
        pc.setAttr(objectName + "." + name, keyable=False, channelBox=True, lock=True )

    return objectName + "." + name

DECORATE_PREFIX = "TkDecorate_"
def decorate(inObj, inAttrs, inPrefix=DECORATE_PREFIX):
    """Add attributes on an dagobject (with an added prefix), based on a dictionary key/values"""

    for attrName, attrValue in inAttrs.items():
        attrName = inPrefix + attrName

        if not pc.hasAttr(inObj, attrName):
            inObj.addAttr(attrName, dataType='string')

        inObj.attr(attrName).set(str(attrValue), type="string")

def readDecoration(inObj, inPrefix=DECORATE_PREFIX):
    """Read a dagobject custom attributes (starting with a prefix) and return them in a dictionary"""
    attrs = getParameters(inObj)

    decoration = {}

    for attr in attrs:
        if attr.startswith(inPrefix):
            value = inObj.attr(attr).get()
            #Brute-force deserialize the value
            try:
                value = ast.literal_eval(value)
            except:
                pass

            decoration[attr[len(inPrefix):]] = value

    return decoration

PPDTYPES= { "int":"Int32Array",
            "vector":"vectorArray",
            "double":"doubleArray"}

def addPerPointData(inMeshT, inName="PerPointData", value=None, inType="int"):
    prop = getProperty(inMeshT, inName)
    if prop != None:
        pc.delete(prop)

    numVertices = inMeshT.numVertices()

    prop = addProperty(inMeshT, inName)
    pc.select(prop)
    pc.addAttr(longName="data", dt=PPDTYPES[inType])
    pc.setAttr(prop.name() + ".data", value if value != None else [0 for i in range(numVertices)])

def setPerPointData(inMeshT, inIndex, inValue, inName="PerPointData"):
    prop = getProperty(inMeshT, inName)
    if prop == None:
        pc.warning("Can't find perpoint data '{0}'".format(inName))
        return 

    val = pc.getAttr(prop.name() + ".data")
    val[inIndex] = inValue
    pc.setAttr(prop.name() + ".data", val)

def getPerPointData(inMeshT, inIndex=None, inName="PerPointData"):
    prop = getProperty(inMeshT, inName)
    if prop != None:
        data = pc.getAttr(prop.name() + ".data")
        return data if inIndex == None else data[index]
    
    return None

def createBaseMap(inMeshT):
    prop = getProperty(inMeshT, BASEMAP)
    if prop != None:
        pc.delete(prop)

    points = inMeshT.getPoints()
    
    return addPerPointData(inMeshT, BASEMAP, points, "vector")

def resetMeshToBase(inMeshT):
    baseData = getPerPointData(inMeshT, None, BASEMAP)
    if baseData == None:
        pc.warning("{0} don't have a '{1}'' !", inMeshT.name(), BASEMAP)
        return

    inMeshT.setPoints(baseData)
    inMeshT.updateSurface()

def resetAll(inTarget, inParams=True):
    resetTRS(inTarget)

    if inParams:
        params = getParameters(inTarget, keyableOnly=True)
        for param in params:
            attrName = inTarget.name() + "." + param
            default = pc.addAttr(attrName, query=True, defaultValue=True)
            if default != None and pc.getAttr(attrName, settable=True):
                pc.setAttr(attrName, default)

def extractConditions(inCode, inFuncName):
    contents = []
    if inFuncName in inCode:
        startIdx = inCode.index(inFuncName)
        idx = startIdx + len(inFuncName)
        searchIdx = idx
        endIdx = inCode.index(")", searchIdx)
        condCommaIdx = inCode.index(",", searchIdx)
        firstTermCommaIdx = inCode.index(",", condCommaIdx + 1)
        
        openingIdx = inCode.find("(", searchIdx, endIdx)
        count = 100
        while openingIdx > -1:
            if openingIdx < firstTermCommaIdx and endIdx > firstTermCommaIdx:
                #print "  * firstTermCommaIdx " + str(firstTermCommaIdx) + " pushed to " + str(endIdx + 1)
                firstTermCommaIdx = inCode.index(",", endIdx + 1)
                #print " * firstTermCommaIdx = " + str(firstTermCommaIdx)
            searchIdx = endIdx + 1
            endIdx = inCode.index(")", searchIdx)
            openingIdx = inCode.find("(", openingIdx + 1, endIdx)
            count -= 1
            if count < 0:
                break
        contents = [inCode[idx:condCommaIdx],inCode[condCommaIdx+1:firstTermCommaIdx],inCode[firstTermCommaIdx+1:endIdx]]
        contents.append(inCode[startIdx:endIdx+1])

        if len(inCode) > len(contents[3]):
            leading = ""
            trailing = ""
            if startIdx > 0:
                leading = inCode[:startIdx]
            if endIdx + 1 < len(inCode):
                trailing = inCode[endIdx + 1:]
            #print "leading '" + leading + "'"
            #print "trailing '" + trailing + "'"
            contents[1] = leading + contents[1] + trailing
            contents[2] = leading + contents[2] + trailing
            contents[3] = inCode

    return contents

def translateConds(inCode, inParam):
    inNewCode = inCode
    if "cond(" in inNewCode:
        contents = extractConditions(inNewCode, "cond(")
        ifTrue = contents[1]
        ifFalse = contents[2]
        #print " ifTrue " + ifTrue
        #print " ifFalse " + ifFalse
        if "cond(" in ifTrue:
            ifTrue = translateConds(ifTrue, inParam)
        if "cond(" in ifFalse:
            ifFalse = translateConds(ifFalse, inParam)
        
        ifTrue = ifTrue if("if(" in ifTrue) else inParam + " = " + ifTrue + ";"
        ifFalse = ifFalse if("if(" in ifFalse) else (inParam + " = " + ifFalse) + ";"
        
        newSyntax = "if(" + contents[0] + ")\n{\n" + ifTrue + "\n}\nelse\n{\n" + ifFalse + "\n}\n"
        
        inNewCode = inNewCode.replace(contents[3], newSyntax)
    return inNewCode

def setExpression(inParam, inCode, inContainer="$SOURCE_Expr"):
    #XSI translation
    if "cond(" in inCode:
        code = translateConds(inCode, inParam)
    else:
        code = inParam + " = " + inCode
    node = None
    cons = pc.listConnections(inParam, destination=False)
    for con in cons:
        pc.delete(con)

    if inContainer != "":
        inContainer = inContainer.replace("$SOURCE", inParam.replace(".", "_"))
        node = pc.expression(s=code, name=inContainer)
        pc.expression(node, edit=True, alwaysEvaluate=False)
    else:
        node = pc.expression(s=code)
        pc.expression(node, edit=True, alwaysEvaluate=False)

    return node

def linkVisibility(node, strSourceParam, direct=False, glob=False, specValue=None):
    #print "linkVisibility", node,strSourceParam,direct,glob,specValue
    paramName = ".visibility"

    if not glob:
        #As we have inconsistencies with the behaviour of "overrideVisibility" connections, let's try to use "visibility" everywhere
        #paramName = ".overrideVisibility"

        if node.type() == "transform": 
            shape = node.getShape()
            if shape != None:
                node = shape
            """
            else:
                node = node.name()
            """
    else:
        if not pc.getAttr(node + ".visibility", settable=True):
            pc.warning(node + ".visibility already connected !")
            return

    finalExpr = strSourceParam
    if specValue != None:
        finalExpr = "(" + finalExpr + " >= " + str(specValue) + ")"

    cons = pc.listConnections(node + paramName, destination=False)
    if len(cons) > 0:
        if(cons[0].type() == "expression"):
            exprName = cons[0].name()
            oldCode = pc.expression(cons[0], query=True, s=True)
            if not strSourceParam in oldCode:
                oldCodeSplit = oldCode.split("=")
                if(len(oldCodeSplit) == 2):
                    newCode = oldCodeSplit[0] + "=" + oldCodeSplit[1].rstrip("; ") + " * " + finalExpr
                    pc.delete(cons[0])
                    pc.expression(s=newCode, name=exprName)
        #else:
            #print "Unknown connection Type " + cons[0].type()
    else:
        if direct:
            #Skip joints (hidden joints)
            if "Deformers" in strSourceParam or node.type() != "joint":
                if specValue == None:
                    pc.connectAttr(strSourceParam, node + paramName)
                else:
                    condition = pc.createNode("condition", name=node.name() + "_vis_cond")
                    pc.connectAttr(strSourceParam, condition.firstTerm)
                    pc.setAttr(condition.secondTerm, specValue)
                    pc.setAttr(condition.colorIfFalse.colorIfFalseR, 0)
                    pc.setAttr(condition.colorIfTrue.colorIfTrueR, 1)
                    pc.connectAttr(condition.outColor.outColorR, node.name() + paramName)
        else:
            setExpression(node + paramName, finalExpr)

def unLinkVisibility(node):
    shape = node.getShape()
    if shape != None:
        node = shape.name()
    else:
        node = node.name()

    #As we have inconsistencies with the behaviour of "overrideVisibility" connections, let's try to use "visibility" everywhere
    cons = pc.listConnections(node + ".visibility", destination=False)

    if len(cons) > 0:
        pc.delete(cons)

def getDefinition(inParam):
    inParamSplit = inParam.split(".")
    sNode = inParamSplit[0]
    sParam = ".".join(inParamSplit[1:])

    if not pc.attributeQuery(sParam, node=sNode, exists=True):
        return (None, None, None, None, None, None)

    pcParam = pc.Attribute(inParam)

    stype = pcParam.get(type=True);
    default = None if stype== "string" else pc.addAttr(inParam, query=True, defaultValue=True)
    hardmin = None if stype== "string" else pcParam.getMin();
    hardmax = None if stype== "string" else pcParam.getMax();
    softmin = None if stype== "string" else pcParam.getSoftMin();
    softmax = None if stype== "string" else pcParam.getSoftMax();
    niceName = pc.attributeName(pcParam, nice=True)

    if stype == "enum" and hardmin == 0 and hardmax == 1:
        stype = "bool"
        hardmin = hardmax = softmin = softmax = None
    elif stype == "doubleAngle":
        stype = "double"

    if stype == "enum":
        enumDict = pcParam.getEnums()
        enumValues = enumDict.keys()
        enumValues.sort(key=lambda v: enumDict[v])
        stype = stype + ";" + ":".join(enumValues)

    return (stype, default, hardmin, hardmax, softmin, softmax, niceName)

def getParamsDictionary(inNode, strName, bidirectionnal=False):
    dic = {}

    if pc.objExists(inNode):
        params = getParameters(inNode, customOnly=True, containerName=strName, keyableOnly=False)

        fullname = inNode.name() + "_" + strName
        for param in params:
            val = pc.getAttr(fullname + "." + param)
            dic[param] = val
            if bidirectionnal:
                dic[val] = param

    return dic

#Does not work in parallel ? Try something else than nodeState=2 ?
def createLazySwitch(inConstrained, inConstrainers, inAttr=None, inAttrName="switch",inTranslation=True, inRotation=True, inDebug=False):
    if inDebug:
        tkLogger.info(tc.smartJoin("createLazySwitch(",inConstrained, inConstrainers,inAttr,inAttrName,inTranslation,inRotation,")"))

    inConstrained.t.disconnect()
    inConstrained.r.disconnect()

    parent = inConstrained.getParent()

    if parent is None:
        pc.warning("Can't create a lazy switch from scene root !")
        return

    if inAttr is None and pc.attributeQuery(inAttrName , node=parent, exists=True):
        pc.deleteAttr(parent.attr(inAttrName))

    switchAttr = inAttr or getNode(addParameter(parent, inAttrName, "enum;"+":".join([n.name() for n in inConstrainers])))
    
    for inConstrainer in inConstrainers:
        name = "{0}_LazyTo_{1}".format(inConstrainer,inConstrained)
        if pc.objExists(name):
            pc.delete(name)

    tkn.deleteUnusedNodes()

    i = 0
    oldTransform = None
    for inConstrainer in inConstrainers:
        name = "{0}_LazyTo_{1}".format(inConstrainer,inConstrained)

        constrainedNode = pc.group(name=name, empty=True)
        parent.addChild(constrainedNode)    
        matchTRS(constrainedNode, inConstrained)
        
        cns = constrain(constrainedNode, inConstrainer, "parent")

        if not inTranslation:
            pc.disconnectAttr(cns.name() + ".constraintTranslateX", constrainedNode.name() + ".translateX")
            pc.disconnectAttr(cns.name() + ".constraintTranslateY", constrainedNode.name() + ".translateY")
            pc.disconnectAttr(cns.name() + ".constraintTranslateZ", constrainedNode.name() + ".translateZ")


        if not oldTransform is None:
            t, r, s = oldTransform
            
            #Translation
            if inTranslation:
                oldCond = None
                oldConds = inConstrained.t.listConnections(type=["condition", "unitConversion"], source=True, destination=False)

                if inDebug:
                    tkLogger.info(tc.smartJoin("oldConds",inConstrained.t,oldConds))

                for possibleOldCond in oldConds:
                    if possibleOldCond.type() == "condition":
                        oldCond = possibleOldCond
                        break
                    else:
                        possibleOldConds = possibleOldCond.input.listConnections(type=["condition"], source=True, destination=False)
                        if inDebug:
                            tkLogger.info(tc.smartJoin("possibleOldConds",possibleOldCond.input,possibleOldConds))
                        if len(possibleOldConds) > 0:
                            oldCond = possibleOldConds[0]
                            break

                if oldCond is None:
                    tkn.condition(switchAttr, i, "==", constrainedNode.t, t) >> inConstrained.t
                else:
                    if inDebug:
                        tkLogger.info(tc.smartJoin("Old cond for",inConstrained.t,oldCond ))
                    tkn.condition(switchAttr, i, "==", constrainedNode.t, oldCond.outColor) >> inConstrained.t

            #Rotation
            if inRotation:
                oldCond = None
                oldConds = inConstrained.r.listConnections(type=["condition", "unitConversion"], source=True, destination=False)
                if inDebug:
                    tkLogger.info(tc.smartJoin("oldConds",inConstrained.r,oldConds))
                for possibleOldCond in oldConds:
                    if possibleOldCond.type() == "condition":
                        oldCond = possibleOldCond
                        break
                    else:
                        possibleOldConds = possibleOldCond.input.listConnections(type=["condition"], source=True, destination=False)
                        if inDebug:
                            tkLogger.info(tc.smartJoin("possibleOldConds",possibleOldCond.input,possibleOldConds))
                        if len(possibleOldConds) > 0:
                            oldCond = possibleOldConds[0]
                            break

                if oldCond is None:
                    tkn.condition(switchAttr, i, "==", constrainedNode.r, r) >> inConstrained.r
                else:
                    if inDebug:
                        tkLogger.info(tc.smartJoin("Old cond for",inConstrained.r,oldCond))
                    tkn.condition(switchAttr, i, "==", constrainedNode.r, oldCond.outColor) >> inConstrained.r

        tkn.conditionAnd(cns.nodeState, tkn.condition(switchAttr, i, "!=", 2, 0))

        oldTransform = (constrainedNode.t, constrainedNode.r, constrainedNode.s)
        i += 1

    return switchAttr

"""
type = "Parent" or "Orient"
"""
def applySwitchSpace(strType, strChild, strIndexAttr, listConstrainers, inLazy=False):
    # take care of switching contraints on "child"
    childNode = getNode(strChild)

    parent = getParent(childNode)
    if parent == None:
        return

    #Clean
    if parent.name() == strChild + "_switchSpacer":
        #We already have a switchSpacer
        removeAllCns(parent)

        if strType != "Parent":
            matchTRS(parent, childNode)

        resetTRS(childNode)
    else:
        parent = addBuffer(childNode, inSuffix="_switchSpacer")

    constrainerNodes = []
    #Ge real constrainers
    for contrainer in listConstrainers:
        if pc.objExists(contrainer):
            constrainerNodes.append(getNode(contrainer))

    objectNames = [n.stripNamespace() for n in constrainerNodes]

    #Recreate index attr
    inputCons = cmds.listConnections(strIndexAttr, source=True, destination=False, plugs=True)
    outputCons = cmds.listConnections(strIndexAttr, source=False, destination=True, plugs=True)

    oldValue = cmds.getAttr(strIndexAttr)

    pc.deleteAttr(strIndexAttr)
    splitAttr = strIndexAttr.split(".")
    attrHolderNode = getNode(splitAttr[0])
    param = addParameter(attrHolderNode, splitAttr[1], "enum;"+":".join(objectNames))

    if inputCons != None and len(inputCons) > 0:
        for inputC in inputCons:
            pc.connectAttr(inputC, strIndexAttr, force=True)
    else:
        val = min(oldValue, len(objectNames) - 1)
        if val > 0:
            cmds.setAttr(param, val)

    if outputCons != None and len(outputCons) > 0:
        for outputC in outputCons:
            pc.connectAttr(strIndexAttr, outputC, force=True)

    if inLazy:
        #print "tkc.createLazySwitch(tkc.getNode('" + parent.name() + "'), ["+",".join([("tkc.getNode('" + n.name() + "')") for n in constrainerNodes])+"], inAttr=tkc.getNode('" + param + "'), inTranslation="+str(strType == "Parent") + ")"
        createLazySwitch(parent, constrainerNodes, inAttr=getNode(param), inTranslation=strType == "Parent")
    else:
        constraints = []
        for contrainerNode in constrainerNodes:
            cn = constrain(parent, contrainerNode, "parent")
            constraints.append(cn)

        if strType != "Parent":
            pc.disconnectAttr(constraints[0].name() + ".constraintTranslateX", parent.name() + ".translateX")
            pc.disconnectAttr(constraints[0].name() + ".constraintTranslateY", parent.name() + ".translateY")
            pc.disconnectAttr(constraints[0].name() + ".constraintTranslateZ", parent.name() + ".translateZ")

        counter = 0
        for constraint in constraints:
            condition = pc.createNode("condition", name=constraint.name() + "_cond")
            pc.connectAttr(param, condition.firstTerm, force=True)
            pc.setAttr(condition.secondTerm, counter)
            pc.setAttr(condition.colorIfFalse.colorIfFalseR, 0)
            pc.setAttr(condition.colorIfTrue.colorIfTrueR, 1)
            pc.connectAttr(condition.outColor.outColorR, constraint.name() + "." + objectNames[counter] + "W" + str(counter), force=True)
            counter += 1



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ___       _                      _   _             
 |_ _|_ __ | |_ ___ _ __ __ _  ___| |_(_) ___  _ __  
  | || '_ \| __/ _ \ '__/ _` |/ __| __| |/ _ \| '_ \ 
  | || | | | ||  __/ | | (_| | (__| |_| | (_) | | | |
 |___|_| |_|\__\___|_|  \__,_|\___|\__|_|\___/|_| |_|
                                                     
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def detectFormatting(inVariable, inStrValue, inCurrentValue):
    formattedValue = str(inCurrentValue)
    varIndex = inStrValue.find(inVariable)
    formatter = "NOFORMAT"
    formatString = "NOFORMAT"
    if len(inStrValue) > varIndex + 2 and inStrValue[varIndex + 2] == "(":
        try:
            endFormatIndex = inStrValue.find(")", varIndex + 2)
            if endFormatIndex == -1:
                raise Exception('Cannot get format closing bracket !')
            formatter = inStrValue[varIndex + 3:endFormatIndex]
            inVariable = inVariable + "(" + formatter + ")"
            formatString = "'%"+formatter+"'%(float("+ formattedValue +"))"
            formattedValue = eval(formatString)
        except Exception as e:
            formattedValue = str(inCurrentValue)
            pc.warning("Cannot evaluate formatting : " + formatString + "(" + str(e) +")")
    return (inVariable, str(formattedValue))

def parseValue(strValue, strType="string", strCurrentValue="", inCounter=0, inMaximum=1, inAllowComments=False, inExcludeNS=True):
    rslt = None

    if inAllowComments:
        strValue = strValue.split("#")[0]

    currentValue = strCurrentValue

    operator = ""
    operators = ["+","-","*","/"]
    
    strValue = strValue.lstrip(" ").rstrip(" ")

    if strValue[0] in operators:
        if strValue[0] != "-":
            operator = strValue[0]
            strValue = strValue[1:]
    if strValue[-1] in operators:
        operator = strValue[-1]
        strValue = strValue[0:-1]

    maxRef = inMaximum
    if inMaximum > 1:
        maxRef = inMaximum - 1

    #Variables 

    #string formatting
    wasFormatted = False

    if CONST_VALUEVARIABLE in strValue:
        var_value = detectFormatting(CONST_VALUEVARIABLE, strValue, currentValue)
        if var_value[0] != CONST_VALUEVARIABLE:
            wasFormatted = True
        strValue = strValue.replace(var_value[0], var_value[1])

    if CONST_ITERVARIABLE in strValue:
        var_value = detectFormatting(CONST_ITERVARIABLE, strValue, inCounter)
        if var_value[0] != CONST_ITERVARIABLE:
            wasFormatted = True
        strValue = strValue.replace(var_value[0], var_value[1])

    if CONST_PERCENTVARIABLE in strValue:
        var_value = detectFormatting(CONST_PERCENTVARIABLE, strValue, (inCounter * 100.0)/maxRef)
        if var_value[0] != CONST_PERCENTVARIABLE:
            wasFormatted = True
        strValue = strValue.replace(var_value[0], var_value[1])

    if strType != "string" or not wasFormatted:
        try:
            rslt = eval(strValue)
            rslt = str(rslt)
        except:
            rslt = strValue
    else:
        rslt = strValue

    if strType != "string" and strType != "bool":
        if currentValue != "":
            
            if operator != "":
                try:
                    rslt = eval(currentValue + " " + operator + " " + rslt)
                except:
                    tkLogger.error("Cannot evaluate    |" + currentValue + " " + operator + " " + str(rslt) + "|")
                    return None
            else:
                try:
                    rslt = eval(rslt)
                except:
                    tkLogger.error("Cannot evaluate    |" + str(rslt) + "|")
                    return None
    else:
        strippedPart = ""
        if inExcludeNS:
            newCurrentValue = currentValue.split(":")[-1]
            strippedPart = currentValue[:-len(newCurrentValue)]
            currentValue = newCurrentValue

        if operator == "+":
            rslt = currentValue + rslt
        elif operator == "-":
            rslt = rslt + currentValue
        elif operator == "*":
            search_replace = rslt.split("|")
            rslt = currentValue.replace(search_replace[0], search_replace[1])
        elif operator == "/":
            cutNumber = int(rslt)
            if cutNumber > 0:
                rslt = currentValue[cutNumber:]
            elif  cutNumber < 0:
                rslt = currentValue[0:cutNumber]

        if inExcludeNS and not strippedPart in rslt:
            rslt = strippedPart + rslt

    #Convert result
    try:
        if strType == "int":
            rslt = int(float(rslt))
        elif strType == "float" or type == "double" :
            rslt = float(rslt)
        elif strType == "bool":
            rslt = True if eval(rslt) else False
    except:
        tkLogger.error("Cannot convert  " + str(rslt) + " to " + strType)
        return None
        
    return rslt

def setAttrParse(strAttr, strValue, strType="string", strCurrentValue="", inCounter=1, inMaximum=1):
    pc.setAttr(strAttr, parseValue(strValue, strType, strCurrentValue, inCounter, inMaximum))

def setAttrParseOnSel(strAttr, strValue, strType="double"):
    sel = pc.ls(sl=True)
    selLen = len(sel)
    for i in range(0, selLen):
        attrName = sel[i].name() + "." + strAttr
        objName = sel[i].name()
        shortAttrName = strAttr
        if "." in shortAttrName:
            index = shortAttrName.rfind('.')
            objName += "." + shortAttrName[:index]
            shortAttrName = shortAttrName[index+1:]
        if pc.attributeQuery(shortAttrName , node=objName, exists=True ):
            value = pc.getAttr(attrName)
            setAttrParse(attrName, strValue, strType, str(value), i, selLen)
        else:
            pc.warning(sel[0].name() + "." + strAttr + " don't exists")

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____  _                 _                                   _                 
 / ___|(_)_ __ ___  _ __ | | ___    ___  _ __   ___ _ __ __ _| |_ ___  _ __ ___ 
 \___ \| | '_ ` _ \| '_ \| |/ _ \  / _ \| '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
  ___) | | | | | | | |_) | |  __/ | (_) | |_) |  __/ | | (_| | || (_) | |  \__ \
 |____/|_|_| |_| |_| .__/|_|\___|  \___/| .__/ \___|_|  \__,_|\__\___/|_|  |___/
                   |_|                  |_|                                     

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def createResPlane(target=None, topRef=None, middleRef=None, endRef=None, name="tkResPlaneNode"):
    if(topRef is None or middleRef is None or endRef is None):
        pc.error("You must provide three reference objects, top, middle and end transforms !")

    if(target is None):
        target = pc.spaceLocator(name="ResPlaneTarget")

    resPlaneNode = pc.createNode(TK_RESPLANE_TYPE, name=name)

    pc.connectAttr(topRef.name() + ".worldMatrix[0]", resPlaneNode + ".topMat")
    pc.connectAttr(middleRef.name() + ".worldMatrix[0]", resPlaneNode + ".middleMat")
    pc.connectAttr(endRef.name() + ".worldMatrix[0]", resPlaneNode + ".endMat")

    pc.connectAttr(target.name() + ".parentMatrix[0]", resPlaneNode + ".parentMat")
    pc.connectAttr(resPlaneNode + ".outputTrans", target.name() + ".translate")

    return resPlaneNode

def resPlaneTestScene():
    sourcePath = "Z:\\ToonKit\\RnD\\Src\\TK_ResPlaneNode\\x64\\Release\\tkResPlaneNode.mll"
    destPath = "Z:\\ToonKit\\RnD\\MAYA\\WORKGROUP_2013x64\\plug-ins\\tkResPlaneNode.mll"

    pmsys.newFile(force=True)
    pc.unloadPlugin( 'tkResPlaneNode.mll' )
    shutil.copy(sourcePath, destPath);
    pc.loadPlugin( 'tkResPlaneNode.mll' )

    #Create objects
    topRef = pc.spaceLocator(name="TopRef")
    pc.setAttr(topRef.name() + ".ty", 5.0)
    middleRef = pc.spaceLocator(name="MiddleRef")
    pc.setAttr(middleRef.name() + ".ty", 3.0)
    pc.setAttr(middleRef.name() + ".tz", 1.0)
    endRef = pc.spaceLocator(name="EndRef")

    targetLoc = pc.spaceLocator(name="ResPlaneTarget")

    resPlaneNode = pc.createNode(TK_RESPLANE_TYPE, name="tkResPlaneNode")

    pc.connectAttr(topRef.name() + ".worldMatrix[0]", resPlaneNode + ".topMat")
    pc.connectAttr(middleRef.name() + ".worldMatrix[0]", resPlaneNode + ".middleMat")
    pc.connectAttr(endRef.name() + ".worldMatrix[0]", resPlaneNode + ".endMat")

    pc.connectAttr(targetLoc.name() + ".parentMatrix[0]", resPlaneNode + ".parentMat")
    pc.connectAttr(resPlaneNode + ".outputTrans", targetLoc.name() + ".translate")

def reParentHair():
    sel = pc.ls(sl=True)
    for selObj in sel:
        cns = getConstraints(selObj)
        if len(cns) == 1:
            targets = getConstraintTargets(cns[0])
            if len(targets) == 1:
                pc.delete(cns)
                pc.parent(selObj, targets[0])
            else:
                pc.error("Wrong number of targets on " + cns[0].name())
        else:
            pc.error("Wrong number of constraints on " + selObj.name())
        

def getSpreadDeform(inCurve, inRefCurve=None):
    spreadDeform = None
    shapes =  pc.listRelatives(curv, shapes=True)

    spreadDeform = None

    for shape in shapes:
        spreadDeformers = pc.listConnections(shape, type="tkSpreadDeform", destination=False)
        if len(spreadDeformers) > 0:
            for curSpreadDeform in spreadDeformers:
                if inRefCurve == None or inRefCurve in pc.listConnections(curSpreadDeform, destination=False):
                    spreadDeform = curSpreadDeform
                    break

    return spreadDeform

def applySpreadDeform(inCurve, inRefCurve, inRefParent, inEnv=1.0):
    '''
    Call on selection
    sel = pc.ls(sl=True)
    applySpreadDeform(sel[0], sel[1], sel[2])
    '''
    
    #Get refCurve skinCluster and original shape, check for errors
    oParent = inCurve.getParent()
    
    refCrvShapes = pc.listRelatives(inRefCurve, shapes=True)
    if len(refCrvShapes) == 0:
        pc.error("Cannot get shapes on 'RefCurve' (%s), aborting" % inRefCurve.name())
        return None
    
    refCrvShape = None
    skins = []

    for shape in refCrvShapes:
        refCrvShape = shape
        skins = pc.listConnections(refCrvShape, type="skinCluster")
        if len(skins) > 0:
            break

    if len(skins) == 0:
        pc.error("Cannot get skinCluster on 'RefCurve' shapes (%s), aborting" % str(refCrvShapes))
        return None

    #Get Orig shape before skinCluster
    skin = skins[0]

    # Python37 compatibility:
    orig = pc.listConnections(skin, type="nurbsCurve", plugs=True, destination=False)
    if orig == []:
        grp = pc.listConnections(skin, type="groupParts", destination=False)
        tweak = pc.listConnections(grp[0], type="tweak", destination=False)
        grp2 = pc.listConnections(tweak[0], type="groupParts", destination=False)
        orig = pc.listConnections(grp2[0], type="nurbsCurve", plugs=True, destination=False)
    refCurveOrigShape = orig[0].node()
        
    #Do apply
    deform = pc.deformer(inCurve, type="tkSpreadDeform")[0]
    
    if oParent != None:
        pc.connectAttr(oParent.name() + ".matrix", deform.name() + ".localMatrix", force=True)

    refMat = pc.getAttr(inRefParent.name() + ".matrix")
    pc.setAttr(deform.name() + ".staticPoseMatrix", refMat)
    pc.connectAttr(inRefParent.name() + ".matrix", deform.name() + ".refMatrix", force=True)
    pc.connectAttr(refCurveOrigShape.name() + ".worldSpace[0]", deform.name() + ".refCurve", force=True)
    pc.connectAttr(inRefCurve.name() + ".worldSpace[0]", deform.name() + ".deformedCurve", force=True)
    
    pc.setAttr(deform.name() + ".envelope", inEnv)

    return deform

def normalizeDeformers(inDefs, inReduceOnly=False, inAttributeName = "envelope", inNormalValue=1.0):
    total=0
    for deform in inDefs:
        total += pc.getAttr(deform.name() + "." + inAttributeName)
        
    if total > inNormalValue or not inReduceOnly:
        ratio = inNormalValue / total
        for deform in inDefs:
            pc.setAttr(deform.name() + "." + inAttributeName, pc.getAttr(deform.name() + "." + inAttributeName) * ratio)

def applySpreadDeforms(inCurves, inRefCurve, inRefParent, inRadius=0.0):
    '''
    Apply on test scene
    curves = [pc.PyNode("curve2"), pc.PyNode("curve3"), pc.PyNode("curve4"), pc.PyNode("curve5"), pc.PyNode("curve6"), pc.PyNode("curve7"), pc.PyNode("curve8"), pc.PyNode("curve9"), pc.PyNode("curve10")]
    refCurve = pc.PyNode("curve1")
    refParent = pc.PyNode("locator1")

    applySpreadDeforms(curves, refCurve, refParent, inRadius=0.0)
    '''

    #get positions by first cv global translation
    refPosition =  inRefCurve.cv[0].getPosition("world")
    
    dist = 1.0

    if inRadius == 0.0:#We have to calculate radius so that the farest item gets a minimal influence (0.1)
        if len(inCurves) == 1:
            inRadius = 1
        else: 
            farestDist = 0.0
            for curv in inCurves:
                position = curv.cv[0].getPosition("world")
                dist = (position - refPosition).length()
                if farestDist < dist:
                    farestDist = dist
            inRadius = farestDist * 1.1
        
    for curv in inCurves:
        position = curv.cv[0].getPosition("world")
        if len(inCurves) == 1:
            factor = 1
        else:
            dist = (position - refPosition).length()
            factor = 1 - (dist / inRadius)
        
        #Verify if SpreadDeformer is not already applied
        spreadDeformer = None
        otherSpreadDeformers = []

        spreadDeformers = []

        shapes =  pc.listRelatives(curv, shapes=True)
        for shape in shapes:
            curSpreadDeformers = pc.listConnections(shapes[0], type="tkSpreadDeform", destination=False)
            if len(curSpreadDeformers) > 0:
                spreadDeformers.extend(curSpreadDeformers)

        for candidate in spreadDeformers:
            #get the deformation reference
            defCurves = pc.listConnections(candidate.name() + ".deformedCurve")

            if len(defCurves) > 0 and defCurves[0].name() == inRefCurve.name():
                spreadDeformer = candidate
            else:
                otherSpreadDeformers.append(candidate)
        
        if factor > 0:
            if spreadDeformer == None:
                tkLogger.debug(curv.name() + " will be deformed (dist: " + str(dist) + " => factor: " + str(factor) + ")")
                spreadDeformer = applySpreadDeform(curv, inRefCurve, inRefParent, inEnv=factor)
            else:
                tkLogger.debug(curv.name() + " aleady deformed, update factor (dist: " + str(dist) + " => factor: " + str(factor) + ")")
                pc.setAttr(spreadDeformer.name() + ".envelope", factor)

            if len(otherSpreadDeformers) > 0:
                otherSpreadDeformers.append(spreadDeformer)
                #normalize envelopes
                normalizeDeformers(otherSpreadDeformers, True)

        else:
            pc.warning(curv.name() + " is too far regarding radius and will NOT be deformed (dist: " + str(dist) + " / " + str(inRadius) + ")")
            if spreadDeformer != None:
                #todo remove deformer 'cleanly'
                pc.delete(spreadDeformer)

'''
strlng = Language
    0 : AutoDetect (code starts with : #python,//js, //mel...)
    1 : Python
    2 : Javascript (not available here)
    3 : mel
'''
def executeCode(strcode, strlng=1, functionName="", args=[]):
    return executeCode2(strcode, strlng, functionName, args)
    """
    rslt = []
    if strlng == 0:#Auto-detect
        strcodeStart = strcode[:20]
        if strcodeStart.startswith("#python"):
            strlng = 1
        elif strcodeStart.startswith("//js"):
            strlng = 2
        elif strcodeStart.startswith("//mel"):
            strlng = 3

    if strlng == 1:#Python
        globs = None
        if functionName != "":
            strcode += "\nreturn " + functionName + "(" + ",".join(args) + ")"
            globs = {"defRslt":None}
        rslt = evalAsFunction(strcode, None, globs)
    else:
        print "Cannot evaluate language ! Only python is available in this version !" 

    return rslt
    """

def executeFile(path, strlng=1, functionName="", args=[]):
    code = None
    try:
        #print "executeFile(path={0}, strlng={1}, functionName={2}, args={3})".format(path, strlng, functionName, args)
        with open(path, 'r') as content_file:
            code = content_file.read()
            #print "executeFile code :\n{0}".format(code)
    except:
        return None

    if len(functionName) > 0 and not "def do(" in code:
        functionName = ""

    return executeCode(code, strlng, functionName, args)

def executeCode2(strcode, strlng=1, functionName="", args=[]):
    rslt = []
    if strlng == 0:#Auto-detect
        strcodeStart = strcode[:20]
        if strcodeStart.startswith("#python"):
            strlng = 1
        elif strcodeStart.startswith("//js"):
            strlng = 2
        elif strcodeStart.startswith("//mel"):
            strlng = 3

    if strlng == 1:#Python
        globs = None
        if functionName != "":
            globs = {"defRslt":None}
            strcode += "\nreturn " + functionName
            func = evalAsFunction(strcode, None, globs)
            rslt = func(*args)
            return rslt
        return evalAsFunction(strcode, None, globs)
    else:
        tkLogger.error("Cannot evaluate language ! Only python is available in this version !")

    return None

def evalAsFunction(code, local_vars = None, global_vars = None):
    if local_vars is None:
        local_vars = {}
    if global_vars is None:
        global_vars = globals()
    retval = None
    context = {}
    code = re.sub(r"(?m)^", "    ", code)
    code = code.replace("\r\n", "\n")
    code = "def anon(" + ','.join(local_vars.keys()) + "):\n" + code
    exec (code, global_vars, context)
    retval = context['anon'](*(local_vars.values()))
    return retval

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _____                    _       _            
 |_   _|__ _ __ ___  _ __ | | __ _| |_ ___  ___ 
   | |/ _ \ '_ ` _ \| '_ \| |/ _` | __/ _ \/ __|
   | |  __/ | | | | | |_) | | (_| | ||  __/\__ \
   |_|\___|_| |_| |_| .__/|_|\__,_|\__\___||___/
                    |_|                         

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#Displays
DISPLAY_IS_CHANGING = False
def AEupdateDisplaysDC(plug, slider):
    global DISPLAY_IS_CHANGING
    val = pc.floatSliderGrp( slider, q=1, v=1 )
    if val == 0 and ("size" in plug or "scale" in plug):
        val = 0.001

    obj_Attr = plug.split(".")
    #pc.setAttr( plug, val )
    #try to act on other selected Objects
    sel = pc.selected()
    if not DISPLAY_IS_CHANGING :
        pc.undoInfo(openChunk=True)
        tkLogger.debug("Undo Chunk Opened")
        DISPLAY_IS_CHANGING = True
    for selObj in sel:
        if pc.attributeQuery(obj_Attr[1], node=selObj, exists=True):
            pc.setAttr( selObj.name() + "." + obj_Attr[1], val )
            updateDisplay(selObj)

def AEupdateDisplaysCC(plug, slider):
    global DISPLAY_IS_CHANGING
    try:
        val = pc.floatSliderGrp( slider, q=1, v=1 )
        if val == 0 and ("size" in plug or "scale" in plug):
            val = 0.001

        obj_Attr = plug.split(".")
        #pc.setAttr( plug, val )
        #try to act on other selected Objects
        sel = pc.selected()
        for selObj in sel:
            if pc.attributeQuery(obj_Attr[1], node=selObj, exists=True):
                pc.setAttr( selObj.name() + "." + obj_Attr[1], val )
                updateDisplay(selObj)
    except:
        pass
    if DISPLAY_IS_CHANGING:
        pc.undoInfo(closeChunk=True)
        tkLogger.debug("Undo Chunk Closed")
    DISPLAY_IS_CHANGING = False

def AEupdateInitValues(plug, scrollField):
    val = pc.scrollField( scrollField, q=1, text=1 )
    pc.setAttr( plug, val )

def AEupdateTextField(plug, textField):
    val = pc.textFieldGrp( textField, q=1, text=True )
    pc.setAttr( plug, val )

def AEupdateCBField(plug, CBField):
    val = pc.checkBoxGrp( CBField, q=1, value1=True )
    pc.setAttr( plug, val )

def AEaddDisplaysDoubleMenu(plug, sliderLabel, annot ):
    obj_Attr = plug.split(".")
    node = getNode(obj_Attr[0])
    props = []
        
    pc.columnLayout()

    if isProperty(node):
        props.append(node)
    else:
        props = getProperties(node)

        if pc.attributeQuery( obj_Attr[1], node=obj_Attr[0] ,exists=True ):
            val = pc.getAttr( plug )
            slider = pc.floatSliderGrp( annotation=annot, label=sliderLabel, minValue=-10, maxValue=10, fieldMinValue=-100, fieldMaxValue=100, v=val )
            pc.floatSliderGrp( slider, e=1, dc="tkc.AEupdateDisplaysDC('" + plug + "', '" + slider + "')" )
            pc.floatSliderGrp( slider, e=1, cc="tkc.AEupdateDisplaysCC('" + plug + "', '" + slider + "')" )
            pc.setParent( u=1 )
            if obj_Attr[1] == "size":
                pc.button(label="Reset Displays", c="tkc.setDisplay(pc.PyNode('"+ obj_Attr[0] +"'), select=True)")
        elif obj_Attr[1] == "size":
            pc.text( label="Selected object don't have displays !")
            pc.button(label="Add displays", c="tkc.getDisplay(pc.PyNode('"+ obj_Attr[0] +"'))")

    for prop in props:
        if pc.attributeQuery( obj_Attr[1], node=prop ,exists=True ):
            otherPlug = prop.name() + "." + obj_Attr[1]
            val = pc.getAttr(otherPlug)
            if "TK_OSCAR_ElementInfo" in prop.name():
                if obj_Attr[1] == "tk_type":
                    enumField = pc.attrEnumOptionMenuGrp(at=otherPlug, l=sliderLabel, en=False)
                elif obj_Attr[1] == "tk_guideRule":
                    enumField = pc.attrEnumOptionMenuGrp(at=otherPlug, l=sliderLabel)
                elif obj_Attr[1] == "tk_placeHolder" or obj_Attr[1] == "tk_upVReference" or obj_Attr[1] == "tk_target" or obj_Attr[1] == "tk_guideParent":
                    if val == None:
                        val = ""
                    textField = pc.textFieldGrp(annotation=annot, label=sliderLabel, text=val)
                    pc.textFieldGrp(textField, e=1, cc="tkc.AEupdateTextField('" + otherPlug + "', '" + textField + "')")
                elif obj_Attr[1] == "tk_invert" or obj_Attr[1] == "tk_invertUp":
                    cbField = pc.checkBoxGrp(annotation=annot, label=sliderLabel, value1=val)
                    pc.checkBoxGrp(cbField, e=1, cc="tkc.AEupdateCBField('" + otherPlug + "', '" + cbField + "')")
                #pc.attrEnumOptionMenuGrp( enumField, e=1, cc="tkc.AEupdateInitValues('" + otherPlug + "', '" + scrollField + "')" )
            elif "TK_OSCAR_InitValues" in prop.name():
                if obj_Attr[1] == "initValues":
                    pc.text( label="Use element name, without the prefix, example :")
                    pc.text( label="0_Ctrl.offsetDisplayX = ctr_dist(0_Ctrl, 1_Ctrl)")
                    scrollField = pc.scrollField( editable=True, wordWrap=False, text=val )
                    pc.scrollField( scrollField, e=1, cc="tkc.AEupdateInitValues('" + otherPlug + "', '" + scrollField + "')" )
                elif obj_Attr[1] == "guideHelpers":
                    pc.text( label="Give a type (Curve or PoleVector), then an equal sign and a list of Element names, example :")
                    pc.text( label="Curve=Point0_Ctrl,Point1_Ctrl,Point2_Ctrl")
                    scrollField = pc.scrollField( editable=True, wordWrap=False, text=val )
                    pc.scrollField( scrollField, e=1, cc="tkc.AEupdateInitValues('" + otherPlug + "', '" + scrollField + "')" )

def stripMockNamespace(inName):
    return inName.replace("None:", "")

def showSynopTiK():
    cmdLine = []

    char = getFirstSelectedCharacter()
    synPaths = ""
    root = None

    if char != None:
        prop = getProperty(char, CONST_ATTRIBUTES)
        if prop != None:
            synPaths = pc.getAttr(prop.name() + ".SynopticPath")
    else:
        pc.error("Select a controller or a Character root to open SynopTiK !")

    if synPaths != "":
        ns = char.namespace()
        if ns == "":
            ns = "None:"
        cmdLine.append(ns[:-1])

        projectDirectory = cmds.workspace(q=True, rd=True)
        if projectDirectory[-1] == "\\" or projectDirectory[-1] == "/":
            projectDirectory = projectDirectory[:-1]

        xmlPath = SYNOPTIKPATH.replace(".exe", ".exe.config")
        if os.path.isfile(xmlPath):
            doc = minidom.parse(xmlPath)

            search, replace = [None, None]

            for settingHolder in doc.getElementsByTagName("SynopTiK.Properties.Settings"):
                for setting in settingHolder.childNodes:
                    if setting.nodeType == setting.ELEMENT_NODE:
                        if setting.attributes["name"].value == "VariableOverride":
                            search, replace = setting.getElementsByTagName("value")[0].firstChild.nodeValue.split(":")

            if search != None and replace != None:
                tkLogger.debug(tc.smartJoin("search", search, "replace", replace))
                synPaths = synPaths.replace(search, replace)

        customVars = {'$PROJECTPATH':projectDirectory}
        synPaths = expandVariables(synPaths, customVars)

        if haveVariables(synPaths, customVars):
            tkLogger.warning("Synoptic pages path contains unknown environment variables or have incorrect formatting ({0}) !!".format(synPaths))

        cmdLine.append(synPaths)
        #print str(cmdLine)
        subprocess.Popen(SYNOPTIKPATH + " " + " ".join(cmdLine))

DEFORMERS_CRITERIA = [
    {
        "name":"unused",
        "pattern":"{Prefix}_HandRig_Hand_Deform",
    },
    {
        "name":"unused",
        "type":"joint",
        "typeNegate":True,
    },
    {
        "name":"twists",
        "pattern":"{Prefix}_Twist{Location:(_Up|_Dwn)*}_{Number:[0-9]*}_Deform",
    },
    {
        "name":"volumes",
        "pattern":"{Prefix}{VolumeDeformer:(AngleDeformer[0-9]*_Main|Stretch[0-9]*|StretchUp|Mastoid_[0-9]_*)}_Deform",
    },
    {
        "name":"semi",
        "pattern":"{Prefix}_Semi_Deform",
    },
    {
        "name":"eyes",
        "pattern":"{Prefix}_Eye_{Suffix}",
    },
    {
        "name":"tongue",
        "pattern":"{Prefix}Tongue_{Suffix}",
    },
    {
        "name":"breath",
        "pattern":"{Prefix}_Breath_{Suffix}",
    },
    {
        "name":"teeth",
        "pattern":"{Prefix}_Teeth_{Suffix}",
    },
    {
        "name":"fingers",
        "pattern":"{Prefix}_HandRig_{Suffix}",
        "parent":"body",
    },
    {
        "name":"squash",
        "pattern":"{Prefix}Head_Squash_{Suffix}",
    },
    {
        "name":"worldDef",
        "pattern":"{Prefix}World_Main_Deform",
    },
]

def objectMatches(inObject, inCriterion):
    pattern = inCriterion.get("pattern")
    if not pattern is None and not "{" in pattern:
        pattern = "{{value:{0}}}".format(pattern)
    patternDiffer = inCriterion.get("patternNegate", False)
    
    type = inCriterion.get("type")
    if not type is None and not "{" in type:
        type = "{{value:{0}}}".format(type)
    typeDiffer = inCriterion.get("typeNegate", False)

    if not pattern is None and ctx.match(pattern, inObject.name()) == patternDiffer:
        return False

    if not type is None and ctx.match(type, inObject.type()) == typeDiffer:
        return False

    return True

def filterObjects(inObjects, inCriteria, inDefaultName="unfiltered", inCreateSets=True, inRootSetName="filtered"):
    default=inObjects[:]
    
    collections = {}
    
    for obj in inObjects:
        matchingCriterion=None
        
        for criterion in inCriteria:
            if objectMatches(obj, criterion):
                matchingCriterion = criterion
                break
                
        if not matchingCriterion is None:
            default.remove(obj)
            
            if not matchingCriterion["name"] in collections:
                collections[matchingCriterion["name"]] = [obj]
            else:
                collections[matchingCriterion["name"]].append(obj)

    if len(default) > 0:
        if inDefaultName in collections:
            collections[inDefaultName].extend(default)
        else:
            collections[inDefaultName] = default
    
    if inCreateSets:
        mayaSets = []
        for name, content in collections.items():
            pc.select(content)
            mayaSets.append(pc.sets(name=name))
        
        if len(mayaSets) > 0:
            pc.select(mayaSets, noExpand=True)
            pc.sets(name=inRootSetName)
            
            criteriaDict={i["name"]:i for i in inCriteria}
            
            for mayaSet in mayaSets:
                if mayaSet.name() in criteriaDict:
                    parent = criteriaDict[mayaSet.name()].get("parent")
                    if not parent is None and pc.objExists(parent):
                        pc.sets(parent, forceElement=mayaSet)

    return collections


def getAssets(inCategory=""):
    assets=[]
    assetsProps = pc.ls("*:*" + CONST_KEYSETSPROP)

    for assetProp in assetsProps:
        parent = assetProp.getParent()
        if parent != None:
            assets.append(parent)

    return assets

def getFirstSelectedCharacter():
    charRoot = None
    sel = pc.ls(sl=True)
    for selObj in sel:
        curObj = selObj
        while curObj != None:
            prop = getProperty(curObj, CONST_ATTRIBUTES)
            if prop != None and pc.attributeQuery( "SynopticPath", node=prop, exists=True ):
                return curObj
            curObj = curObj.getParent()
    return None

def getCharacterName(inNameSpace=""):
    pattern = stripMockNamespace(inNameSpace + ":*" + CONST_KEYSETSPROP)
    assetProp = pc.ls(pattern)
    if len(assetProp) > 0:
        return assetProp[0].stripNamespace()[:-(len(CONST_KEYSETSPROP) + 1)]
    return ""

def getCharacters(inCharacters=[]):
    if len(inCharacters) == 0:
        char = getFirstSelectedCharacter()
        if char != None:
            inCharacters.append(char)
    else:
        newChars = []
        for char in inCharacters:
            if isinstance(char, basestring):
                charNode = getNode(char)
                if not charNode is None:
                    newChars.append(charNode)
                else:
                    charName = getCharacterName(char)
                    charRootName = stripMockNamespace(char + ":" + charName)
                    if charName != "" :
                        charRootNode = getNode(charRootName)
                        if not charRootNode is None:
                            newChars.append(charRootNode)

            else:
                newChars.append(char)
        inCharacters = newChars

    return inCharacters

def getKeyables(inCategory="All", inCharacters=[], ordered=False):
    keyables=[]
    inCharacters = getCharacters(inCharacters)

    for char in inCharacters:
        prop = getProperty(char, CONST_KEYSETSPROP)
        if prop != None:
            if cmds.objExists(prop.name() + "." + inCategory):
                stringValue = pc.getAttr(prop.name() + "." + inCategory)
                objNames = stringValue.replace("$", char.namespace()).split(",")
                for objName in objNames:
                    if cmds.objExists(objName):
                        keyables.append(objName)

    if ordered:
        keyables = orderControls(keyables)

    return keyables

def getKeySets(inCharacter=None):
    chars = [] if inCharacter is None else [inCharacter]
    chars = getCharacters(chars)

    if len(chars) > 0:
        prop = getProperty(chars[0], CONST_KEYSETSPROP)
        return getParameters(prop)

def getKeySetParent(inNamespace, inKeySet, inProp=None):
    if inProp is None:
        chars = getCharacters([inNamespace])
        assert len(chars)>0, "Can't find any character named {}".format(inNamespace)
        prop = getProperty(chars[0], CONST_KEYSETSTREEPROP)
    else:
        prop = inProp

    if not prop is None:
        if cmds.objExists(prop.name() + "." + inKeySet):
            return pc.getAttr(prop.name() + "." + inKeySet)

    return None

def getKeySetParents(inNamespace, inKeySet, inProp=None):
    if inProp is None:
        chars = getCharacters([inNamespace])
        assert len(chars)>0, "Can't find any character named {}".format(inNamespace)
        prop = getProperty(chars[0], CONST_KEYSETSTREEPROP)
    else:
        prop = inProp

    parents = []

    parent = getKeySetParent(inNamespace, inKeySet, prop)
    while not parent is None:
        parents.insert(0, parent)

        parent = getKeySetParent(inNamespace, parent, prop)

    return parents

def getKeySetsHierarchy(inCharacters=[]):
    inCharacters = getCharacters(inCharacters)

    createdSets = []

    for char in inCharacters:
        ns = char.split(":")[0]

        if len(ns) > 0:
            ns += ":"

        prop = getProperty(char, CONST_KEYSETSTREEPROP)
        assert prop != None, "Property {0} can't be found on char {1}, you must have at least two categories in your asset.".format(CONST_KEYSETSTREEPROP, char)
        keySets = getKeySets(char)

        keySetsHierachy = []

        for keySet in keySets:
            keySetsHierachy.append((keySet,getKeySetParents(char, keySet, prop)))
            
    return sorted(keySetsHierachy, key=lambda x: len(x[1]))

def getControlsHierarchy(char, inSet, inHierarchy=None, inOrder=True):
    inHierarchy = inHierarchy or getKeySetsHierarchy(inCharacters=[char])
    
    #print "inHierarchy ?",inHierarchy

    ctrls = getKeyables(inSet, [char])
    
    if len(ctrls) == 0:
        return [[],[],[]]
    
    childSets = []
    
    toRemove = []
    
    for keySet in inHierarchy:
        if len(keySet[1]) > 0 and (keySet[1][0] == inSet or keySet[1][0] == "$"+inSet):
            childSets.append(keySet[0])
            #print "ctrls",len(ctrls),ctrls
            subControls = getKeyables(keySet[0], [char])
            toRemove.extend(subControls)
            #print "subControls",len(subControls),subControls

    toRemove = list(set(toRemove))

    return [item for item in ctrls if not item in toRemove], sorted(childSets), ctrls

def orderControls(inControls):
    orderedControls = []
    controlsDic = {}

    for control in inControls:
        controlNode = getNode(control)

        prop = getProperty(controlNode, CONST_ATTRIBUTES)
        if prop != None:
            orderedControls.append(controlNode)
            controlsDic[controlNode.name()] = pc.getAttr(prop + ".HierarchyLevel")

    orderedControls = sorted(orderedControls, key=lambda hierarControl: controlsDic[hierarControl.name()])

    return orderedControls

def getFps():
    fps = None
    fpsInfo = {'film': 24, 'game': 15, 'pal': 25, 'ntsc':30, 'show':48, 'palf':50, 'ntscf':60}

    fpsValue = pc.currentUnit(query=True, time=True)
    if fpsValue in fpsInfo:
        fps = fpsInfo[fpsValue]
    elif "fps" in fpsValue:
        fps = int(fpsValue[:-3])
    
    return fps

def capture(filepath, start=None, end=None, width=100, height=100, displaymode="smoothShaded", showFrameNumbers=True, format="iff", compression="jpg", ornaments=False, play=False, useCamera=None, i_inFilmFit=0, i_inDisplayResolution=0, i_inDisplayFilmGate=0, i_inOverscan=1.0, i_inSafeAction=0, i_inSafeTitle=0, i_inGateMask=0, f_inMaskOpacity=0.8, quality=90):
    storeSelection()
    pc.select(cl=True)
    names = []
    name = ""

    if start == None:
        start = pc.currentTime(query=True)
    if end == None:
        end = start

    pan = pc.playblast(activeEditor=True)
    app = pc.modelEditor(pan, query=True, displayAppearance=True)
    tex = pc.modelEditor(pan, query=True, displayTextures=True)
    wireOnShaded = pc.modelEditor(pan, query=True, wireframeOnShaded=True)
    xray = pc.modelEditor(pan, query=True, xray=True)
    jointXray = pc.modelEditor(pan, query=True, jointXray=True)
    hud = pc.modelEditor(pan, query=True, hud=True)
    
    #Camera settings
    oldCamera = None
    if useCamera != None:
        curCam = pc.modelEditor(pan, query=True, camera=True)
        if curCam != useCamera:
            oldCamera = curCam
            pc.modelEditor(pan, edit=True, camera=useCamera)

    camera = pc.modelEditor(pan, query=True, camera=True)
    if camera.type() == "transform":
        camera = camera.getShape()

    filmFit = pc.getAttr(camera + ".filmFit")
    displayResolution = pc.getAttr(camera + ".displayResolution")
    displayFilmGate = pc.getAttr(camera + ".displayFilmGate")
    overscan = pc.getAttr(camera + ".overscan")
    safeAction = pc.getAttr(camera + ".displaySafeAction")
    safeTitle = pc.getAttr(camera + ".displaySafeTitle")
    displayGateMask = pc.getAttr(camera + ".displayGateMask")
    displayGateMaskOpacity = pc.getAttr(camera + ".displayGateMaskOpacity")

    pc.setAttr(camera + ".filmFit", i_inFilmFit)
    pc.setAttr(camera + ".displayResolution", i_inDisplayResolution)
    pc.setAttr(camera + ".displayFilmGate", i_inDisplayFilmGate)
    pc.setAttr(camera + ".overscan", i_inOverscan)
    pc.setAttr(camera + ".displaySafeAction", i_inSafeAction)
    pc.setAttr(camera + ".displaySafeTitle", i_inSafeTitle)
    pc.setAttr(camera + ".displayGateMask", i_inGateMask)
    pc.setAttr(camera + ".displayGateMaskOpacity", f_inMaskOpacity)

    #visible types
    nurbsCurvesShowing = pc.modelEditor(pan, query=True, nurbsCurves=True)

    if displaymode == "wireframe":
        pc.modelEditor(pan, edit=True, displayAppearance="wireframe", wireframeOnShaded=False, hud=ornaments)
    else:
        pc.modelEditor(pan, edit=True, displayAppearance="smoothShaded", wireframeOnShaded=False, hud=ornaments)

    pc.modelEditor(pan, edit=True, nurbsCurves=False, displayTextures= "textured" in displaymode or displaymode == "OpenGL")

    if format == "iff" and showFrameNumbers:
        name = pc.playblast(format=format, compression=compression, quality=quality, sequenceTime=False, clearCache=True, viewer=play, showOrnaments=ornaments, framePadding=4, forceOverwrite=True, percent=100, filename=filepath, startTime=start, endTime=end, width=width, height=height)
        for i in range(start, end + 1):
            oldFileName = name.replace("####", str(i).zfill(4))
            newFileName = oldFileName.replace(".", "_", 1)
            if os.path.isfile(newFileName):
                os.remove(newFileName)
            os.rename(oldFileName, newFileName)
            names.append(newFileName)
    else:
        if format == "iff":
            name = pc.playblast(format=format, compression=compression, quality=quality, sequenceTime=False, clearCache=True, viewer=play, showOrnaments=ornaments, framePadding=4, forceOverwrite=True, percent=100, completeFilename=filepath, startTime=start, endTime=end, width=width, height=height)
        else:
            name = pc.playblast(format=format, compression=compression, quality=quality, sequenceTime=False, clearCache=True, viewer=play, showOrnaments=ornaments, framePadding=4, forceOverwrite=True, percent=100, filename=filepath, startTime=start, endTime=end, width=width, height=height)

        names.append(name)

    #Reset values
    pc.modelEditor(pan, edit=True, displayAppearance=app, displayTextures=tex, wireframeOnShaded=wireOnShaded, xray=xray, jointXray=jointXray, nurbsCurves=nurbsCurvesShowing, hud=hud)

    #Camera
    pc.setAttr(camera + ".filmFit", filmFit)
    pc.setAttr(camera + ".displayResolution", displayResolution)
    pc.setAttr(camera + ".displayFilmGate", displayFilmGate)
    pc.setAttr(camera + ".overscan", overscan)
    pc.setAttr(camera + ".displaySafeAction", safeAction)
    pc.setAttr(camera + ".displaySafeTitle", safeTitle)
    pc.setAttr(camera + ".displayGateMask", displayGateMask)
    pc.setAttr(camera + ".displayGateMaskOpacity", displayGateMaskOpacity)

    if oldCamera != None:
        pc.modelEditor(pan, edit=True, camera=oldCamera)
    
    loadSelection()

    return names

def checkGeometry(obj):
    problems = []
    
    crvShapes = obj.getShapes()
    
    vertices = crvShapes[0].getVertices()[1]
    numVerts = crvShapes[0].numVertices()
    
    verticesIndices = range(numVerts)
    
    for vert in vertices:
        if vert in verticesIndices:
            verticesIndices.remove(vert)
    
    if len(verticesIndices) > 0:
        strIndices = [str(number) for number in verticesIndices]
        problems.append("Mesh "+ obj.name() +" have " + str(len(verticesIndices)) + " orphan vertices " + str(verticesIndices))
        
    if len(problems) > 0:
        for problem in problems:
            tkLogger.warning(problem)
    else:
        tkLogger.info("No problems found on " + obj.name())
        
    return problems == 0

ALLOWEDNODES = ["transform", "joint", "skinCluster", "ffd", "baseLattice", "wrap", "blendShape", "groupParts", "groupId", "shadingEngine"]
TYPES = ["mesh", "lattice", "nurbsCurve", "nurbsSurface"]

def checkHistory(inObjects=None, inAllowedNodes=None, inCheckTypes=None):
    inAllowedNodes = inAllowedNodes or ALLOWEDNODES
    inCheckTypes = inCheckTypes or TYPES
    
    objs = None

    if not inObjects is None:
        if not isinstance(inObjects, (list, tuple)):
            inObjects = [inObjects]

        objs = [obj for obj in getNodes(inObjects) if obj.type() in inAllowedNodes]
    else:
        objs = pc.ls(type=inCheckTypes)

    allAllowed = inAllowedNodes + inCheckTypes

    defectObjects = []

    for obj in objs:
        forbidden = [defo for defo in pc.listHistory(obj) if not defo.type() in allAllowed]
        
        if len(forbidden) > 0:
            defectObjects.append(obj)
            pc.warning("{0} have forbidden history ({1})".format(obj, ",".join(["{0}[{1}]".format(n.name(), n.type()) for n in objs])))

    if len(defectObjects) > 0:
        pc.select(defectObjects)
    else:
        tkLogger.info("No problematic history found on given objects ({0})".format(",".join([n.name() for n in objs])))

    return defectObjects

MANAGED_DEFORMERS = {
    "ffd":True,
    "skinCluster":True,
    "blendShape":True,
    "tweak":False,
}

def getCleanHistory(inTransform):
    histo = inTransform.listHistory()
    
    cleanHisto = []
    
    for deform in histo:
        if not isinstance(deform, pc.nodetypes.GeometryFilter):
            continue
        
        deformType = deform.type()
        
        if not deformType in MANAGED_DEFORMERS:
            pc.warning("Unmanaged deformer '{0}' ({1}) on '{2}'".format(deform, deform.type(), inTransform))
            continue
            
        if MANAGED_DEFORMERS[deformType]:
            affected = False
            for geo in deform.getOutputGeometry():
                if geo.getParent() == inTransform:
                    cleanHisto.append(deform)
        
    return cleanHisto

def killTurtle(*args):
    pc.mel.eval("ilrClearScene")

NS_TOKEN = "$NS"
def createView(inNs, inHookObj, inName=NS_TOKEN+"_face_cam", inKeySets=None, inExclude=None, inInclude=None,
    inIncludeTypes=None, inOffset=None, inFrameOn=None, inWindowSize=(800, 600)):

    inKeySets = inKeySets or []
    if not isinstance(inKeySets, (list, tuple)):
        inKeySets = (inKeySets,)

    inExclude = inExclude or []
    if not isinstance(inExclude, (list, tuple)):
        inExclude = (inExclude,)

    inInclude = inInclude or []
    if not isinstance(inInclude, (list, tuple)):
        inInclude = (inInclude,)

    inIncludeTypes = inIncludeTypes or []
    if not isinstance(inIncludeTypes, (list, tuple)):
        inIncludeTypes = (inIncludeTypes,)

    inOffset = inOffset or ([0.0] * 6)
    while len(inOffset) < 6:
        inOffset.append(0.0)

    inFrameOn = inFrameOn or []
    if not isinstance(inFrameOn, (list, tuple)):
        inFrameOn = (inFrameOn,)

    modelName = inNs.rstrip(":")

    cam = inName.replace(NS_TOKEN, modelName)
    windowName = cam + "UI"
    camNode = None

    storeSelection()

    if pc.window(windowName, exists=True):
        pc.deleteUI(windowName)

    if not pc.objExists(cam):
        faceCtrl = getNode(inNs + inHookObj)
        camRootName = cam + "_Root"
        camNode = pc.camera()[0]
        camNode.rename(cam)
        
        camNode.focalLength.set(100)

        camGroupNode = pc.group(name=camRootName)
        constraintNode = constrain(camGroupNode ,faceCtrl, "Pose", False)

        constraintNode.target[0].targetOffsetTranslate.targetOffsetTranslateX.set(inOffset[0])
        constraintNode.target[0].targetOffsetTranslate.targetOffsetTranslateY.set(inOffset[1])
        constraintNode.target[0].targetOffsetTranslate.targetOffsetTranslateZ.set(inOffset[2])
        constraintNode.target[0].targetOffsetRotate.targetOffsetRotateX.set(inOffset[3])
        constraintNode.target[0].targetOffsetRotate.targetOffsetRotateY.set(inOffset[4])
        constraintNode.target[0].targetOffsetRotate.targetOffsetRotateZ.set(inOffset[5])

        pc.viewPlace(camNode, lookAt=faceCtrl.getTranslation(space="world"))
        camNode.rotate.set([0.0,0.0,0.0])
        
        framedObjects = []
        for obj in inFrameOn:
            if pc.objExists(inNs + inHookObj):
                framedObjects.append(inNs + inHookObj)
        
        if len(framedObjects) > 0:
            pc.select(framedObjects)
            pc.viewFit(camNode)
    else:
        camNode = pc.PyNode(cam)

    win = pc.window(windowName, wh=inWindowSize, t=windowName)
    pc.paneLayout()
    mp = pc.modelPanel(cam=camNode.name())
    pc.modelEditor(mp, edit=True, displayAppearance="smoothShaded", wireframeOnShaded=True, headsUpDisplay=False)

    def cleanModelPanel(inModelPanelName):
        pc.isolateSelect(inModelPanelName, state=False)
        pc.deleteUI(inModelPanelName, panel=True)

    pc.window(win, edit=True, closeCommand=partial(cleanModelPanel, mp))

    isolate = []

    if len(inIncludeTypes) > 0: 
       isolate.extend([n.name() for n in pc.ls(inNs+"*", type="mesh")])

    ctrls = []

    for keySet in inKeySets:
        ctrls.extend(getKeyables(keySet, [modelName]))

    isolate.append([n for n in ctrls if not n.split(":")[-1] in inExclude])

    for inc in inInclude:
        isolate.extend(pc.ls(inNs + inc))

    if len(isolate) > 0:
        pc.select(isolate)
        pc.isolateSelect(mp, state=True)
    else:
        pc.warning("No objects found to isolate ! (KeySet(s) : {0}, including : {1},excluding : {2})".format(inKeySets, inExclude, inInclude))

    pc.showWindow(win)

    loadSelection()

"""
#Facial cam
excluded = ["Left_Eye_Target","Left_Spec_Target","LookAt","Spec_LookAt", "Spec_Aim", "Right_Eye_Target","Right_Spec_Target"]
offsets = [3.0, -70.0, 0.0, 90.0, 90.0, 0.0]
createView("sun_fds_rig_v004:", "TK_Neck_Head_Output", inName=NS_TOKEN+"_face_cam", inKeySets="Facial_Main", inExclude=excluded, inIncludeTypes=["mesh"], inOffset=offsets)

#UI cam
included = ["Facial_GUI", "*_Frame", "*_TextHolder"]
offsets = [0.0, 1.25, 194.0, 0.0, 0.0, 0.0]
createView("sun_fds_rig_v004:", "Facial_GUI", inName=NS_TOKEN+"_ui_cam", inKeySets="Facial_GUI", inInclude=included, inOffset=offsets, inFrameOn="Facial_GUI")
"""

def closeAllWindows(*args):
    mainWindow = pc.mel.eval("$melVariable=$gMainWindow")
    uis = pc.lsUI(wnd=True)
    for ui in uis:
        if pc.window(ui, query=True, exists=True) and ui.name() != mainWindow:
            tkLogger.debug("closing", ui.name())
            pc.deleteUI(ui)

def emptyDirectory(inPath):
    for the_file in os.listdir(inPath):
        file_path = os.path.join(inPath, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            tkLogger.error(str(e))
"""
def checkTextValidity(inText):

    


    return textValidity
"""

def search_changed(*args):
    """Search in the Toolkit Menu

    Input arguments:
    *args -- keyword enter by user he wants to find in the Toolkit Menu

    Return values:


    """
    
    #Keyword enter by the user
    text = args[0]
    text=text.lower()

    checkBoxR=pc.checkBox("tkSearchToolUnion",query=True, value=True)


    #Remove the words
    wordToRemove = ["in", "of", "and", "to","if", "or", "a", "an", "the", "neither"]
    textSplit=text.split()

    textCopy = textSplit[:] 
    for item in wordToRemove:
        for k in textCopy:
            if item == k:
                textSplit.remove(item)
    
    
    pc.setParent("tkSearchTool")
    try:
        pc.deleteUI("tkSearchToolButtons")
    except:
        pass
    pc.columnLayout("tkSearchToolButtons")


    #It contains all the data from the Toonkit menu
    resultSearch=False
    for k in range(len(HELP_LIST)):

        isin=False
        if HELP_LIST[k] is not None:

            #Search in name, description, menuPath
            if len(HELP_LIST[k]["menuPath"]) > 1:
                menuPath=" ".join(HELP_LIST[k]["menuPath"]).lower()

            else:
                menuPath=HELP_LIST[k]["menuPath"][0].lower()

            researchText = [HELP_LIST[k]["name"].lower(), menuPath, HELP_LIST[k]["desc"].lower()]
            researchText=" ".join(researchText)

            #Consider keywords union
            if checkBoxR == True:
                for item in textSplit:

                    if item in researchText:
                        isin=True
                    else:
                        isin=False
                        break;

            #Consider keywords independently 
            else:
                for item in textSplit:
                    isin = item in researchText

                    if isin:
                        break

        if isin:
            resultSearch=True
            inter=HELP_LIST[k]["menuPath"][:]
            inter.append(HELP_LIST[k]["name"])
            menuPath2=" => ".join(inter)
            if HELP_LIST[k]["optionBox"]:
                pc.rowColumnLayout(numberOfColumns=3, cs=[(2,5),(3,20)])
                pc.button(label=HELP_LIST[k]["name"], c=HELP_LIST[k]["code"], annotation=HELP_LIST[k]["desc"])
                pc.button(label="options", c=HELP_LIST[k]["optionBox"], annotation=HELP_LIST[k]["desc"])
                pc.text(label="(Menu Path: "+ menuPath2+" )")
                pc.setParent(u=1)
            else:
                pc.rowColumnLayout(numberOfColumns=2, cs=[(2,20)])
                pc.button(label=HELP_LIST[k]["name"], c=HELP_LIST[k]["code"], annotation=HELP_LIST[k]["desc"])
                pc.text(label="(Menu Path: "+ menuPath2+" )")
                pc.setParent(u=1)

    if resultSearch is False:
        pc.text("No results")

def search_changedCallback(*args):
    value=pc.textFieldGrp("blabla",query=True, text=True)
    search_changed(value)

def showSearch(*args):
    
    #Display the Search menu window
    if (pc.window("tkSearchTool", q=True, exists=True)):
        pc.deleteUI("tkSearchTool")
    pc.window("tkSearchTool", title = "Search")
    pc.columnLayout(adjustableColumn=True)
    pc.rowLayout(numberOfColumns=2, adjustableColumn2=1, columnWidth2=(230, 120), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    pc.textFieldGrp("blabla",label='Search in Toonkit Menu', text='', changeCommand=search_changed)
    pc.checkBox("tkSearchToolUnion", label="Match all words", value=False, changeCommand=search_changedCallback)
    pc.setParent(u=1)
    pc.rowLayout("tkSearchHelpRowLayout", numberOfColumns=2, adjustableColumn2=2, columnWidth2=(50, 300), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    pc.text("Help :")
    pc.helpLine()
    pc.setParent(u=1)
    pc.columnLayout("tkSearchToolButtons",adjustableColumn=True)

    pc.showWindow()