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

Implements tkExpressions to create nodes from arbitrary expression string and convert Maya Expressions

Todo :
Reuse if possible for multi-attribute used as single (multiplyDivide, Reverse...)
Attributes types variations (typically scalars/vectors)

Example usages (MACROS section is full of examples of the library part):

#Proximities system
import pymel.core as pc
import tkNodeling as tkn
reload(tkn)

locs = ["mod:motionPathRig_Loc_00","mod:motionPathRig_Loc_01","mod:motionPathRig_Loc_02","mod:motionPathRig_Loc_03","mod:motionPathRig_Loc_04","mod:motionPathRig_Loc_05","mod:motionPathRig_Loc_06","mod:motionPathRig_Loc_07","mod:motionPathRig_Loc_08","mod:motionPathRig_Loc_09","mod:motionPathRig_Loc_10","mod:motionPathRig_Loc_11","mod:motionPathRig_Loc_12","mod:motionPathRig_Loc_13","mod:motionPathRig_Loc_14","mod:motionPathRig_Loc_15","mod:motionPathRig_Loc_16","mod:motionPathRig_Loc_17","mod:motionPathRig_Loc_18","mod:motionPathRig_Loc_19","mod:motionPathRig_Loc_20","mod:motionPathRig_Loc_21","mod:motionPathRig_Loc_22","mod:motionPathRig_Loc_23","mod:motionPathRig_Loc_24","mod:motionPathRig_Loc_25","mod:motionPathRig_Loc_26","mod:motionPathRig_Loc_27","mod:motionPathRig_Loc_28","mod:motionPathRig_Loc_29","mod:motionPathRig_Loc_30","mod:motionPathRig_Loc_31","mod:motionPathRig_Loc_32","mod:motionPathRig_Loc_33","mod:motionPathRig_Loc_34","mod:motionPathRig_Loc_35","mod:motionPathRig_Loc_36","mod:motionPathRig_Loc_37","mod:motionPathRig_Loc_38","mod:motionPathRig_Loc_39","mod:motionPathRig_Loc_40","mod:motionPathRig_Loc_41","mod:motionPathRig_Loc_42","mod:motionPathRig_Loc_43","mod:motionPathRig_Loc_44","mod:motionPathRig_Loc_45","mod:motionPathRig_Loc_46","mod:motionPathRig_Loc_47"]
ctrls = ["mod:Path_Curve_Ctrl1","mod:Path_Curve_Ctrl2","mod:Path_Curve_Ctrl3","mod:Path_Curve_Ctrl4","mod:Path_Curve_Ctrl5","mod:Path_Curve_Ctrl6","mod:Path_Curve_Ctrl7","mod:Path_Curve_Ctrl8","mod:Path_Curve_Ctrl9","mod:Path_Curve_Ctrl10","mod:Path_Curve_Ctrl11","mod:Path_Curve_Ctrl12","mod:Path_Curve_Ctrl13","mod:Path_Curve_Ctrl14","mod:Path_Curve_Ctrl15","mod:Path_Curve_Ctrl16","mod:Path_Curve_Ctrl17","mod:Path_Curve_Ctrl18","mod:Path_Curve_Ctrl19","mod:Path_Curve_Ctrl20","mod:Path_Curve_Ctrl21","mod:Path_Curve_Ctrl22","mod:Path_Curve_Ctrl23","mod:Path_Curve_Ctrl24","mod:Path_Curve_Ctrl25","mod:Path_Curve_Ctrl26","mod:Path_Curve_Ctrl27","mod:Path_Curve_Ctrl28","mod:Path_Curve_Ctrl29","mod:Path_Curve_Ctrl30","mod:Path_Curve_Ctrl31","mod:Path_Curve_Ctrl32","mod:Path_Curve_Ctrl33","mod:Path_Curve_Ctrl34","mod:Path_Curve_Ctrl35","mod:Path_Curve_Ctrl36","mod:Path_Curve_Ctrl37","mod:Path_Curve_Ctrl38","mod:Path_Curve_Ctrl39","mod:Path_Curve_Ctrl40","mod:Path_Curve_Ctrl41","mod:Path_Curve_Ctrl42","mod:Path_Curve_Ctrl43","mod:Path_Curve_Ctrl44","mod:Path_Curve_Ctrl45","mod:Path_Curve_Ctrl46","mod:Path_Curve_Ctrl47","mod:Path_Curve_Ctrl48","mod:Path_Curve_Ctrl49","mod:Path_Curve_Ctrl50","mod:Path_Curve_Ctrl51","mod:Path_Curve_Ctrl52","mod:Path_Curve_Ctrl53","mod:Path_Curve_Ctrl54","mod:Path_Curve_Ctrl55","mod:Path_Curve_Ctrl56","mod:Path_Curve_Ctrl57","mod:Path_Curve_Ctrl58","mod:Path_Curve_Ctrl59","mod:Path_Curve_Ctrl60","mod:Path_Curve_Ctrl61","mod:Path_Curve_Ctrl62","mod:Path_Curve_Ctrl63","mod:Path_Curve_Ctrl64","mod:Path_Curve_Ctrl65","mod:Path_Curve_Ctrl66","mod:Path_Curve_Ctrl67","mod:Path_Curve_Ctrl68","mod:Path_Curve_Ctrl69","mod:Path_Curve_Ctrl70","mod:Path_Curve_Ctrl71","mod:Path_Curve_Ctrl72","mod:Path_Curve_Ctrl73","mod:Path_Curve_Ctrl74","mod:Path_Curve_Ctrl75","mod:Path_Curve_Ctrl76"]
ctrlsNodes = [pc.PyNode(n) for n in ctrls]
for loc in locs:
    locNode = pc.PyNode(loc)
    tkn.createProximitiesSystem(locNode, *ctrlsNodes, inResultObjName=loc)


#Expressions
import tkNodeling as tkn
reload(tkn)

#Condition
#expr = "locator3.tx = cond(locator1.tx > 0, 1, -1)"

#Basic arithmetic
expr = "locator3.tx = (-locator1.tx + abs(locator2.tx)) * 2.0"

print tkn.compileNodes(expr)

#Expression conversion
print tkn.convertExpression(pc.selected()[0])

#TODO

multMatrix
composeMatrix

"""

import os
import sys
import re
import logging
import base64
import hashlib
from string import ascii_lowercase

import tkExpressions as tke
import pymel.core as pc
import pymel.core.datatypes as dt

__author__ = "Cyril GIBAUD - Toonkit"


#################################################################################
#                           CONSTANTS                                           #
#################################################################################

# Values
#################################################################################

EPSILON = sys.float_info.epsilon * 10
OMEGA = 1.0/EPSILON

MAX_NAME_LEN = 150
SAFE_FACTORISATION = True

# Words
#################################################################################

WORLD = "World"
LOCAL = "Local"

EPSILON_NAME = "eps"
OMEGA_NAME = "omg"

ATTR_SEPARATOR = "_"
NS_SEPARATOR = ":"

# Nodes formattings
#################################################################################

DECMAT_FORMAT = "{0}_Dec"
COMPMAT_FORMAT = "{0}_Comp"

NEG_FORMAT = "{0}_Neg"
ADD_FORMAT = "{0}_{1}_Add"
SUBSTRACT_FORMAT = "{0}_{1}_Sub"
MUL_FORMAT = "{0}_{1}_Mul"
PM_MUL_FORMAT = "{0}_{1}_PMMul"
ABS_FORMAT = "{0}_Abs"
WORLD_MATRIX_FORMAT = "{0}_World"
VECTOR_FORMAT = "{0}_TO_{1}_{2}_Vec"
DISTANCE_FORMAT = "{0}_TO_{1}_{2}_Dist"
MAGNITUDE_FORMAT = "{0}_Mag"
POW_FORMAT = "{0}_{1}_Pow"
DOT_FORMAT = "{0}_ON_{1}_Dot"
CROSS_FORMAT = "{0}_ON_{1}_Cross"
DIVIDE_FORMAT = "{0}_OVER_{1}_Div"

BLEND_FORMAT = "{0}_{1}_{2}_Blend"
CLAMP_FORMAT = "{0}_{1}_{2}_Clamp"
REVERSE_FORMAT = "{0}_Rev"
SIN_FORMAT = "{0}_Sin"
COS_FORMAT = "{0}_Cos"
MOD_FORMAT = "{0}_{1}_Mod"
KEEP_FORMAT = "{0}_Keep"
ACCU_FORMAT = "{0}_Accu"

CURVEINFO_FORMAT = "{0}_Info"
CLOSESTPOINT_FORMAT = "{0}_{1}_Close"
POINTONCURVE_FORMAT = "{0}_{1}_{2}_POC"
CONDITION_FORMAT = "{0}_{1}_{2}_IFT_{3}_IFF_{4}_Cond"

VELOCITY_FORMAT = "{0}_Vel"
ANGVELOCITY_FORMAT = "{0}_Angvel"

UTILITY_TYPES = ["addDoubleLinear", "blendColors",
                "condition", "curveInfo", "multDoubleLinear", "multiplyDivide",
                "reverse", "clamp", "plusMinusAverage", "distanceBetween",
                "remapValue", "setRange", "decomposeMatrix", "composeMatrix",
                "multMatrix", "blendTwoAttr", "nearestPointOnCurve", "pairBlend",
                "vectorProduct", "distanceBetween", "wtAddMatrix"]

# Output names
#################################################################################

OUT3DS = {
    "plusMinusAverage":         "output3D",
    "vectorProduct":            "output",
    "nearestPointOnCurve":      "position",
    "decomposeMatrix":          "outputTranslate"
}

# Profiling
#################################################################################

PROFILE = False
VERBOSE = False
CREATED_NODES = {}
CALLS = {}

def profiled(func):
    """
    Profiling decorator
    """
    def wrapper(*args, **kwargs):

        if PROFILE:
            global CALLS
            kwargs["func"] = func.__name__
            if not kwargs["func"] in CALLS:
                CALLS[kwargs["func"]] = 1
            else:
                CALLS[kwargs["func"]] += 1

        if VERBOSE:
            print "VERBOSE :: calling ",func.__name__,args,kwargs

        rslt = func(*args, **kwargs)

        if VERBOSE:
            print "VERBOSE :: returns ",rslt
            print ""

        return rslt

    return wrapper

#Profiling functions
def startProfiling(inVerbose=False):
    global PROFILE
    PROFILE = True

    global VERBOSE
    VERBOSE = inVerbose

    global CREATED_NODES
    CREATED_NODES = {}

    global CALLS
    CALLS = {}

def stopProfiling(inLog=False, inClearNodes=True):
    global PROFILE
    PROFILE = False

    if inClearNodes:
        global CREATED_NODES

    nodes = []
    for function, createdNodes in CREATED_NODES.iteritems():
        nodes.extend(createdNodes)

    if inLog:
        print "-"*20

        print "{0} nodes created total".format(len(nodes))
        print ""
        for function, number in CALLS.iteritems():
            print "{0:03d} calls to '{1}' ({2} nodes)".format(number, function, len(CREATED_NODES.get(function, [])))
        print ""
        for function, createdNodes in CREATED_NODES.iteritems():
            print "{0} ({1} nodes) :".format(function, len(createdNodes))
            for createdNode in createdNodes:
                print " -{0}".format(createdNode)

        print "-"*20

    if inClearNodes:
        CREATED_NODES = {}

    return nodes

#################################################################################
#                           HELPERS                                             #
#################################################################################

def getNode(inObj):
    if isinstance(inObj, basestring):
        return pc.PyNode(inObj)
    
    return inObj

def deleteUnusedNodes():
    numDeleted = pc.mel.eval("MLdeleteUnused()")
    print numDeleted

def reduceName(inName):
    if inName[0] in tke.Expr.WORDS:
        inName = tke.Expr.WORDS[inName[0]] + inName[1:]

    if not len(inName) > MAX_NAME_LEN:
        return inName

    chunks = inName.split(NS_SEPARATOR)
    name = chunks.pop()

    ns = "" if len(chunks) == 0 else NS_SEPARATOR.join(chunks) + NS_SEPARATOR

    if not len(name) > MAX_NAME_LEN:
        return inName

    name = "{0}___{1}".format(name[:MAX_NAME_LEN/2], name[-MAX_NAME_LEN/2:])

    return "{0}{1}".format(ns, name)

#Supposed to reduce .ma size, but does not help so much in most cases.
#May be be usefull if we have to increase the value of MAX_NAME_LEN in case of very deep utility tree
def hashNodes(inHolder="Global_SRT", inTypes=UTILITY_TYPES):
    if not pc.objExists(inHolder):
        return

    holder = pc.PyNode(inHolder)
    pc.addAttr(holder, longName="nodesHash", dt="stringArray")

    nodes = pc.ls(type=inTypes)

    nodesDic = []
    nodesKeys = []
    for node in nodes:
        name = node.name()
        hashedName = base64.urlsafe_b64encode(hashlib.md5(name).digest()).rstrip("=").replace("-", "_")
        if hashedName[0].isdigit():
            hashedName = ascii_lowercase[int(hashedName[0])] + hashedName[1:]

        if hashedName in nodesKeys:
            print pc.warning("Duplicate hash " + hashedName) 

        node = node.rename(hashedName)
        nodesDic.append(node.name() + " " + name)

    holder.nodesHash.set(nodesDic)

#TODO implement
def unhashNodes(inHolder="Global_SRT", inTypes=UTILITY_TYPES):
    if not pc.objExists(inHolder):
        return

    holder = pc.PyNode(inHolder)
    if not pc.attributeQuery("nodesHash", node=holder, exists=True):
        return

    print holder.nodesHash.get()

def create(inType, inName, inHI=False, **kwargs):
    node = pc.createNode(inType, name=inName)

    if not inHI:
        node.isHistoricallyInteresting.set(0)

    funcName = kwargs.get("func", None)

    if funcName:
        global CREATED_NODES
        funcName = kwargs.get("func", "unknown")
        if not funcName in CREATED_NODES:
            CREATED_NODES[funcName] = [node]
        else:
            CREATED_NODES[funcName].append(node)

    return node

# Formatting
#################################################################################

def formatScalar(inScalar):
    if isinstance(inScalar, (list,tuple, dt.Vector)):
        return "_".join([formatScalar(scl) for scl in inScalar])

    if abs(inScalar) <= EPSILON:
        return "eps"
    elif abs(inScalar) >= OMEGA:
        return "omg" if inScalar > 0 else "minusOmg"

    return str(inScalar).replace(".", "dot").replace("-", "minus")

def formatAttr(inAttr, stripNamespace=False, inSeparator=ATTR_SEPARATOR):
    inAttr = getNode(inAttr)

    if not isinstance(inAttr, pc.general.Attribute):
        return inAttr.stripNamespace() if stripNamespace else inAttr.name() 

    nodeName = str(inAttr.node().stripNamespace() if stripNamespace else inAttr.node().name())

    short = inAttr.shortName().replace("[", "_").replace("]", "_")

    return "{0}{1}{2}".format(nodeName, inSeparator, short)

def get3DOut(inObj):
    inObj = getNode(inObj)

    if isinstance(inObj, pc.general.Attribute):
        return inObj

    return inObj.attr(OUT3DS.get(inObj.type(), "t"))

#################################################################################
#                           NODES CREATION                                      #
#################################################################################

# Comparison
#################################################################################

@profiled
def condition(inAttr1, inAttr2, inCriterion=0, inAttrTrue=None, inAttrFalse=None, inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)
    inAttr2 = getNode(inAttr2)

    attr2Scalar = isinstance(inAttr2, (int,float))
    
    if isinstance(inCriterion, basestring):
        try:
            inCriterion = tke.CONDITION_NICECRITERIA.index(inCriterion)
        except:
            raise ValueError("Criterion string '{0}' is not valid (available values : {1}) !".format(inCriterion, tke.CONDITION_NICECRITERIA))

    attr2Name = formatScalar(inAttr2) if attr2Scalar else formatAttr(inAttr2, True)
    attrTrueName = "None" if inAttrTrue is None else (formatScalar(inAttrTrue) if isinstance(inAttrTrue, (int,float)) else formatAttr(inAttrTrue, True))
    attrFalseName = "None" if inAttrFalse is None else (formatScalar(inAttrFalse) if isinstance(inAttrFalse, (int,float)) else formatAttr(inAttrFalse, True))
    nodeName = inName or reduceName(CONDITION_FORMAT.format(formatAttr(inAttr1), tke.CONDITION_CRITERIA[inCriterion], attr2Name,attrTrueName,attrFalseName))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outColorR

    node = create("condition", nodeName, **kwargs)
    node.operation.set(inCriterion)
    inAttr1 >> node.firstTerm

    if attr2Scalar:
        node.secondTerm.set(inAttr2)
    else:
        inAttr2 >> node.secondTerm

    outVectors = False

    if not inAttrTrue is None:
        attrTrueScalar = isinstance(inAttrTrue, (int,float))
        if attrTrueScalar:
            node.colorIfTrueR.set(inAttrTrue)
        else:
            if inAttrTrue.type() in ["double3", "float3"]:
                outVectors = True
                inAttrTrue >> node.colorIfTrue
            else:
                inAttrTrue >> node.colorIfTrueR
    
    if not inAttrFalse is None:
        attrFalseScalar = isinstance(inAttrFalse, (int,float))
        if attrFalseScalar:
            node.colorIfFalseR.set(inAttrFalse)
        else:
            if inAttrFalse.type() in ["double3", "float3"]:
                outVectors = True
                inAttrFalse >> node.colorIfFalse
            else:
                inAttrFalse >> node.colorIfFalseR

    return node.outColorR if not outVectors else node.outColor

@profiled
def conditionOr(inAttr, inCond, **kwargs):
    oldCond = None
    oldConds = inAttr.listConnections(source=True, destination=False, type="condition")
    if len(oldConds) > 0:
        oldCond = oldConds[0]

    locked = inAttr.isLocked()
    if locked:
        inAttr.setLocked(False)

    if not oldCond is None:
        if oldCond.name() != inCond.node().name():
            oldCond.outColorR.disconnect(inAttr)

            inCond = condition(inCond.node().firstTerm.listConnections(plugs=True)[0], inCond.node().secondTerm.get(), "!=", inCond.node().colorIfTrueR.get(), oldCond.outColorR)
            inCond >> inAttr
    else:
        inCond >> inAttr

    if locked:
        inAttr.setLocked(True)

    return inCond

@profiled
def conditionAnd(inAttr, inCond, **kwargs):
    oldCond = None
    oldConds = inAttr.listConnections(source=True, destination=False, type="condition")
    if len(oldConds) > 0:
        oldCond = oldConds[0]

    locked = inAttr.isLocked()
    if locked:
        inAttr.setLocked(False)

    if not oldCond is None:
        if oldCond.name() != inCond.node().name():
            oldCond.outColorR.disconnect(inAttr)

            inCond = condition(inCond.node().firstTerm.listConnections(plugs=True)[0], inCond.node().secondTerm.get(), "!=", oldCond.outColorR, inCond.node().colorIfFalseR.get())
            inCond >> inAttr
    else:
        inCond >> inAttr

    if locked:
        inAttr.setLocked(True)

    return inCond

# Algebra
#################################################################################

#Unary

@profiled
def neg(inAttr1,inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)

    nodeName = inName or reduceName(NEG_FORMAT.format(formatAttr(inAttr1)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output

    return mul(inAttr1, -1)

@profiled
def nabs(inAttr, inName=None, **kwargs):
    inAttr = getNode(inAttr)

    nodeName = inName or reduceName(ABS_FORMAT.format(formatAttr(inAttr.name())))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outColorR

    mulName = (inName + "_absMul") if inName else None
    mulInvert = mul(inAttr, -1.0, inName=mulName)

    cond = condition(inAttr, 0, ">", inAttr, mulInvert, inName=nodeName)

    return cond

#Binary

#Todo take different input types
@profiled
def add(inAttr1, inAttr2, inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)
    inAttr2 = getNode(inAttr2)

    attr1Vector = isinstance(inAttr1, list)
    attr2Vector = isinstance(inAttr2, list)

    attr1Scalar = attr1Vector or isinstance(inAttr1, (int,float))
    attr2Scalar = attr2Vector or isinstance(inAttr2, (int,float))

    attr1Matrix = False

    ns = ""
    if not attr1Scalar:
        ns = str(inAttr1.node().namespace())
        attr1Vector = inAttr1.type() in ["double3", "float3"]
        if not attr1Vector:
            if inAttr1.type() is None or inAttr1.type() == "matrix":
                attr1Matrix = True
    elif not attr2Scalar:
        ns = str(inAttr2.node().namespace())
        attr2Vector = inAttr2.type() in ["double3", "float3"]

    attr1Name = formatScalar(inAttr1) if attr1Scalar else formatAttr(inAttr1, True)
    attr2Name = formatScalar(inAttr2) if attr2Scalar else formatAttr(inAttr2, True)

    nodeName = inName or ns + reduceName(ADD_FORMAT.format(attr1Name, attr2Name))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        if attr1Matrix:
            return pc.PyNode(nodeName).matrixSum
        elif attr1Vector or attr2Vector:
            return pc.PyNode(nodeName).output3D

        return pc.PyNode(nodeName).output

    node = None
    out = None

    if attr1Vector or attr2Vector:
        node = create("plusMinusAverage", nodeName, **kwargs)
        node.operation.set(1)#Add
        out = node.output3D
    else:
        if attr1Matrix:
            node = create("wtAddMatrix", nodeName, **kwargs)
            out = node.matrixSum
        else:
            node = create("addDoubleLinear", nodeName, **kwargs)
            out = node.output

    if attr1Matrix:
        inAttr1 >> node.wtMatrix[0].matrixIn
        inAttr2 >> node.wtMatrix[1].matrixIn

        return out

    if attr1Scalar:
        if attr2Vector:
            node.input3D[0].set(inAttr1)
        else:
            node.input1.set(inAttr1)
    else:
        if attr2Vector:
            inAttr1 >> node.input3D[0]
        else:
            inAttr1 >> node.input1

    if attr2Scalar:
        if attr1Vector:
            node.input3D[1].set(inAttr2)
        else:
            node.input2.set(inAttr2)
    else:
        if attr1Vector:
            inAttr2 >> node.input3D[1]
        else:
            inAttr2 >> node.input2

    return out

def pointMatrixMul(inPoint, inMat, inName=None, vectorMultiply=False, **kwargs):
    inPoint = getNode(inPoint)
    attr1Scalar = isinstance(inPoint, (list,tuple))

    ns = ""
    if not attr1Scalar:
        ns = str(inPoint.node().namespace())

    attr1Name = formatScalar(inPoint) if attr1Scalar else formatAttr(inPoint, True)
    attr2Name = formatAttr(inMat, True)

    nodeName = inName or ns + reduceName(PM_MUL_FORMAT.format(attr1Name, attr2Name))

    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output

    node = create("pointMatrixMult", nodeName, **kwargs)
    node.vectorMultiply.set(vectorMultiply)

    inMat >> node.inMatrix

    if attr1Scalar:
        node.inPoint.set(inPoint)
    else:
        inPoint >> node.inPoint

    return node.output

#Todo take different input types
@profiled
def mul(inAttr1, inAttr2, inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)
    inAttr2 = getNode(inAttr2)

    attr1Scalar = isinstance(inAttr1, (int,float))
    attr2Scalar = isinstance(inAttr2, (int,float))

    attr1Vector = False
    attr2Vector = False

    attr1Matrix = False
    attr2Matrix = False

    ns = ""
    if not attr1Scalar:
        ns = str(inAttr1.node().namespace())
        attr1Vector = inAttr1.type() in ["double3", "float3"]
        if not attr1Vector:
            if inAttr1.type() is None or inAttr1.type() == "matrix":
                attr1Matrix = True
    elif not attr2Scalar:
        ns = str(inAttr2.node().namespace())
        attr2Vector = inAttr2.type() in ["double3", "float3"]

    attr1Name = formatScalar(inAttr1) if attr1Scalar else formatAttr(inAttr1, True)
    attr2Name = formatScalar(inAttr2) if attr2Scalar else formatAttr(inAttr2, True)

    nodeName = inName or ns + reduceName(MUL_FORMAT.format(attr1Name, attr2Name))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        if attr1Matrix:
            return pc.PyNode(nodeName).matrixSum
        return pc.PyNode(nodeName).output

    node = None
    if attr1Vector or attr2Vector:
        node = create("multiplyDivide", nodeName, **kwargs)
        node.operation.set(1)#Multiply
    else:
        if attr1Matrix:
            node = create("multMatrix", nodeName, **kwargs)
        else:
            node = create("multDoubleLinear", nodeName, **kwargs)

    if attr1Matrix:
        inAttr1 >> node.matrixIn[0]
        inAttr2 >> node.matrixIn[1]

        return node.matrixSum
    else:
        if attr1Scalar:
            if attr2Vector:
                node.input1.set([inAttr1, inAttr1, inAttr1])
            else:
                node.input1.set(inAttr1)
        else:
            if not attr1Vector and attr2Vector:
                inAttr1 >> node.input1X
                inAttr1 >> node.input1Y
                inAttr1 >> node.input1Z
            else:
                inAttr1 >> node.input1

        if attr2Scalar:
            if attr1Vector:
                node.input2.set([inAttr2, inAttr2, inAttr2])
            else:
                node.input2.set(inAttr2)
        else:
            if not attr2Vector and attr1Vector:
                inAttr2 >> node.input2X
                inAttr2 >> node.input2Y
                inAttr2 >> node.input2Z
            else:
                inAttr2 >> node.input2

    return node.output

#Todo take different input types, scalar inputs, naming...
@profiled
def sub(inAttr1, inAttr2, inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)
    inAttr2 = getNode(inAttr2)

    attr1Vector = isinstance(inAttr1, list)
    attr2Vector = isinstance(inAttr2, list)

    attr1Scalar = attr1Vector or isinstance(inAttr1, (int,float))
    attr2Scalar = attr2Vector or isinstance(inAttr2, (int,float))

    ns = ""
    if not attr1Scalar:
        ns = str(inAttr1.node().namespace())
        attr1Vector = inAttr1.type() in ["double3", "float3"]

    if not attr2Scalar:
        ns = str(inAttr2.node().namespace())
        attr2Vector = inAttr2.type() in ["double3", "float3"]

    attr1Name = formatScalar(inAttr1) if attr1Scalar else formatAttr(inAttr1, True)
    attr2Name = formatScalar(inAttr2) if attr2Scalar else formatAttr(inAttr2, True)

    nodeName = inName or ns + reduceName(SUBSTRACT_FORMAT.format(attr1Name, attr2Name))
    if pc.objExists(nodeName)  and (not SAFE_FACTORISATION or not "___" in nodeName):
        node = pc.PyNode(nodeName)
        
        if attr1Vector or attr2Vector:
            return pc.PyNode(nodeName).output3D

        return node.output

    node = None
    out = None

    #print "attr1Vector",attr1Vector,"attr1Scalar",attr1Scalar
    #print "attr2Vector",attr2Vector,"attr2Scalar",attr2Scalar

    if attr1Vector or attr2Vector:
        node = create("plusMinusAverage", nodeName, **kwargs)
        node.operation.set(2)#Substract
        out = node.output3D

        if attr1Vector:
            if attr1Scalar:
                node.input3D[0].input3D.set(inAttr1)
            else:
                inAttr1 >> node.input3D[0]
        else:
            if attr1Scalar:
                node.input3D[0].input3Dx.set(inAttr1)
                node.input3D[0].input3Dy.set(inAttr1)
                node.input3D[0].input3Dz.set(inAttr1)
            else:
                inAttr1 >> node.input3D[0].input3Dx
                inAttr1 >> node.input3D[0].input3Dy
                inAttr1 >> node.input3D[0].input3Dz

        if attr2Vector:
            if attr2Scalar:
                node.input3D[1].input3D.set(inAttr2)
            else:
                inAttr2 >> node.input3D[1]
        else:
            if attr2Scalar:
                node.input3D[1].input3Dx.set(inAttr2)
                node.input3D[1].input3Dy.set(inAttr2)
                node.input3D[1].input3Dz.set(inAttr2)
            else:
                inAttr2 >> node.input3D[1].input3Dx
                inAttr2 >> node.input3D[1].input3Dy
                inAttr2 >> node.input3D[1].input3Dz

        return out
    else:
        mulName = (inName + "_subsMul") if inName else None
        invert2 = mul(inAttr2, -1.0, inName=mulName)

        return add(inAttr1, invert2, inName=nodeName)

@profiled
def npow(inAttr1, inAttr2=2.0, inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)
    inAttr2 = getNode(inAttr2)

    attr1Scalar = isinstance(inAttr1, (int,float))
    attr2Scalar = isinstance(inAttr2, (int,float))

    ns = ""
    if not attr1Scalar:
        ns = str(inAttr1.node().namespace())
    elif not attr2Scalar:
        ns = str(inAttr2.node().namespace())

    attr1Name = formatScalar(inAttr1) if attr1Scalar else formatAttr(inAttr1, True)
    attr2Name = formatScalar(inAttr2) if attr2Scalar else formatAttr(inAttr2, True)

    nodeName = inName or ns + reduceName(POW_FORMAT.format(attr1Name, attr2Name))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outputX

    node = create("multiplyDivide", nodeName, **kwargs)
    node.operation.set(3)#power

    if attr1Scalar:
        node.input1X.set(inAttr1)
    else:
        inAttr1 >> node.input1X

    if attr2Scalar:
        node.input2X.set(inAttr2)
    else:
        inAttr2 >> node.input2X

    return node.outputX

@profiled
def div(inAttr1, inAttr2, inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)
    inAttr2 = getNode(inAttr2)

    attr1Scalar = isinstance(inAttr1, (int,float))
    attr2Scalar = isinstance(inAttr2, (int,float))

    ns = ""
    if not attr1Scalar:
        ns = str(inAttr1.node().namespace())
    elif not attr2Scalar:
        ns = str(inAttr2.node().namespace())

    attr1Name = formatScalar(inAttr1) if attr1Scalar else formatAttr(inAttr1, True)
    attr2Name = formatScalar(inAttr2) if attr2Scalar else formatAttr(inAttr2, True)

    nodeName = inName or ns + reduceName(DIVIDE_FORMAT.format(attr1Name, attr2Name))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outputX

    node = create("multiplyDivide", nodeName, **kwargs)
    node.operation.set(2)#Divide

    #Todo manage vector or scalar types (considered scalar as it is)
    if attr1Scalar:
        node.input1X.set(inAttr1)
    else:
        inAttr1 >> node.input1X

    if attr2Scalar:
        node.input2X.set(inAttr2)
    else:
        inAttr2 >> node.input2X

    return node.outputX

@profiled
def clamp(inAttr, inMin=0.0, inMax=1.0, inName=None, **kwargs):
    inAttr = getNode(inAttr)
    inMin = getNode(inMin)
    inMax = getNode(inMax)

    inAttrScalar = isinstance(inAttr, (int,float))
    attrMinScalar = isinstance(inMin, (int,float))
    attrMaxScalar = isinstance(inMax, (int,float))

    nodeName = inName or reduceName(CLAMP_FORMAT.format(formatScalar(inAttr) if inAttrScalar else formatAttr(inAttr), formatScalar(inMin) if attrMinScalar else formatAttr(inMin), formatScalar(inMax) if attrMaxScalar else formatAttr(inMax)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outputR

    node = create("clamp", nodeName, **kwargs)

    if attrMinScalar:
        node.minR.set(inMin)
    else:
        inMin >> node.minR

    if attrMaxScalar:
        node.maxR.set(inMax)
    else:
        inMax >> node.maxR

    if inAttrScalar:
        node.inputR.set(inAttr)
    else:
        inAttr >> node.inputR

    return node.outputR

@profiled
def reverse(inAttr, inName=None, **kwargs):
    inAttr = getNode(inAttr)

    nodeName = inName or reduceName(REVERSE_FORMAT.format(formatAttr(inAttr)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outputX

    revNode = create("reverse", nodeName, **kwargs)
    inAttr >> revNode.inputX

    return revNode.outputX

@profiled
def sin(inAttr, inName=None, **kwargs):
    inAttr = getNode(inAttr)

    nodeName = inName or reduceName(SIN_FORMAT.format(formatAttr(inAttr)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output

    node = create("tkSin", nodeName, **kwargs)
    inAttr >> node.input

    return node.output

@profiled
def cos(inAttr, inName=None, **kwargs):
    inAttr = getNode(inAttr)

    nodeName = inName or reduceName(COS_FORMAT.format(formatAttr(inAttr)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output

    node = create("tkCos", nodeName, **kwargs)
    inAttr >> node.input

    return node.output

@profiled
def mod(inAttr1, inAttr2, inName=None, **kwargs):
    inAttr1 = getNode(inAttr1)
    inAttr2 = getNode(inAttr2)

    attr1Scalar = isinstance(inAttr1, (int,float))
    attr2Scalar = isinstance(inAttr2, (int,float))

    ns = ""
    if not attr1Scalar:
        ns = str(inAttr1.node().namespace())
    elif not attr2Scalar:
        ns = str(inAttr2.node().namespace())

    attr1Name = formatScalar(inAttr1) if attr1Scalar else formatAttr(inAttr1, True)
    attr2Name = formatScalar(inAttr2) if attr2Scalar else formatAttr(inAttr2, True)

    nodeName = inName or ns + reduceName(MOD_FORMAT.format(attr1Name, attr2Name))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output

    node = create("tkMod", nodeName, **kwargs)

    #Todo manage vector or scalar types (considered scalar as it is)
    if attr1Scalar:
        node.input1.set(inAttr1)
    else:
        inAttr1 >> node.input1

    if attr2Scalar:
        node.input2.set(inAttr2)
    else:
        inAttr2 >> node.input2

    return node.output

# Vectors / Matrices
#################################################################################
""" DEPRECATE
@profiled
def composeMatrix(inTranslation, inRotation, inName=None, **kwargs):
    inTranslation = getNode(inTranslation)
    inRotation = getNode(inRotation)

    nodeName = inName or reduceName(COMPMAT_FORMAT.format(inTranslation.node().name()))
    if pc.objExists(nodeName):
        return pc.PyNode(nodeName).outputMatrix
    
    node = create("composeMatrix", nodeName, **kwargs)
    inTranslation >> node.inputTranslate
    inRotation >> node.inputRotate
    
    return node.outputMatrix
"""
@profiled
def fourByFourMatrix(   in00=1.0, in01=0.0, in02=0.0, in03=0.0,
                        in10=0.0, in11=1.0, in12=0.0, in13=0.0,
                        in20=0.0, in21=0.0, in22=1.0, in23=0.0,
                        in30=0.0, in31=0.0, in32=0.0, in33=1.0,
                        inName=None, **kwargs):
    kwargs = dict(locals())

    fbf = create("fourByFourMatrix", inName or "fourByFourMatrix")

    for key, value in kwargs.iteritems():
        if key == "inName" or not key.startswith("in"):
            continue

        if isinstance(value, (float, int)):#isScalar
            fbf.attr(key).set(value)
        else:
            value >> fbf.attr(key)

    return fbf.output

@profiled
def composeMatrix(inT, inR, inS, inScale=[1.0,1.0,1.0], inName=None, **kwargs):
    inTAttr = getNode(inT)
    inRAttr = getNode(inR)
    inSAttr  = getNode(inS)

    inTScalar = isinstance(inTAttr, (list,tuple))
    inRScalar = isinstance(inRAttr, (list,tuple))
    inSScalar = isinstance(inSAttr, (list,tuple))

    nodeName = inName

    if inName is None:
        inTName = formatScalar(inTAttr) if inTScalar else formatAttr(inTAttr)
        inRName = formatScalar(inRAttr) if inRScalar else formatAttr(inRAttr)
        inSName = formatScalar(inSAttr) if inSScalar else formatAttr(inSAttr)

        nodeName = reduceName(COMPMAT_FORMAT.format("{0}_{1}_{2}".format(inTName, inRName, inSName)))

    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outputMatrix
    
    compose = create("composeMatrix", nodeName, **kwargs)

    if inTScalar:
        compose.inputTranslate.set(inTAttr)
    else:
        inTAttr >> compose.inputTranslate

    if inRScalar:
        compose.inputRotate.set(inRAttr)
    else:
        inRAttr >> compose.inputRotate
    
    if inSScalar:
        compose.inputScale.set(inSAttr)
    else:
        inSAttr >> compose.inputScale

    return compose.outputMatrix

@profiled
def decomposeMatrix(inAttr, inName=None, **kwargs):
    inAttr = getNode(inAttr)

    nodeName = inName or reduceName(DECMAT_FORMAT.format(formatAttr(inAttr)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName)
    
    node = create("decomposeMatrix", nodeName, **kwargs)
    inAttr >> node.inputMatrix
    
    return node

@profiled
def worldMatrix(inObj, inName=None, **kwargs):
    inObj = getNode(inObj)

    if inObj.type() != "transform":
        return decomposeMatrix(inObj)

    return decomposeMatrix(inObj.worldMatrix[0])

@profiled
def vector(inSource, inDestination, inWorld=True, inName=None, **kwargs):
    inSource = getNode(inSource)
    inDestination = getNode(inDestination)

    nodeName = inName or reduceName(VECTOR_FORMAT.format(formatAttr(inSource), formatAttr(inDestination, True), WORLD if inWorld else LOCAL))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName)

    sourceNode = worldMatrix(inSource) if inWorld else inSource
    destNode = worldMatrix(inDestination) if inWorld else inDestination 
    
    node = create("plusMinusAverage", nodeName, **kwargs)
    node.operation.set(2)#Substract
    
    get3DOut(sourceNode) >> node.input3D[0]
    get3DOut(destNode) >> node.input3D[1]

    return node.output3D

@profiled
def vectorMag(inVector, inName=None, **kwargs):
    inVector = getNode(inVector)

    nodeName = inName or reduceName(MAGNITUDE_FORMAT.format(formatAttr(inVector)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).distance

    node = create("distanceBetween", nodeName, **kwargs)
    get3DOut(inVector) >> node.point2

    return node.distance

@profiled
def distance(inSource, inDestination, inWorld=True, inName=None, **kwargs):
    inSource = getNode(inSource)
    inDestination = getNode(inDestination)

    nodeName = inName or reduceName(DISTANCE_FORMAT.format(formatAttr(inSource), formatAttr(inDestination, True), WORLD if inWorld else LOCAL))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).distance

    sourceNode = inSource if not inWorld else worldMatrix(inSource)
    destNode = inDestination if not inWorld else worldMatrix(inDestination)
    
    node = create("distanceBetween", nodeName, **kwargs)

    get3DOut(sourceNode) >> node.point1
    get3DOut(destNode) >> node.point2

    return node.distance

@profiled
def dot(inVec1, inVec2, inNormalize=False, inName=None, **kwargs):
    vec1Scalar = isinstance(inVec1, (list, tuple, dt.Vector))
    vec2Scalar = isinstance(inVec2, (list, tuple, dt.Vector))

    if not vec1Scalar:
        inVec1 = getNode(inVec1)
    if not vec2Scalar:
        inVec2 = getNode(inVec2)

    vec1Name = formatScalar(inVec1) if vec1Scalar else formatAttr(inVec1)
    vec2Name = formatScalar(inVec2) if vec2Scalar else formatAttr(inVec2, not vec1Scalar)

    nodeName = inName or reduceName(DOT_FORMAT.format(vec1Name, vec2Name))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).outputX

    node = create("vectorProduct", nodeName, **kwargs)
    if inNormalize:
        node.normalizeOutput.set(True)

    if vec2Scalar:
        node.input1.set(inVec2)
    else:
        get3DOut(inVec2) >> node.input1
    if vec1Scalar:
        node.input2.set(inVec1)
    else:
        get3DOut(inVec1) >> node.input2

    return node.outputX

@profiled
def cross(inVec1, inVec2, inNormalize=False, inName=None, **kwargs):
    vec1Scalar = isinstance(inVec1, (list, tuple, dt.Vector))
    vec2Scalar = isinstance(inVec2, (list, tuple, dt.Vector))

    if not vec1Scalar:
        inVec1 = getNode(inVec1)
    if not vec2Scalar:
        inVec2 = getNode(inVec2)

    vec1Name = formatScalar(inVec1) if vec1Scalar else formatAttr(inVec1)
    vec2Name = formatScalar(inVec2) if vec2Scalar else formatAttr(inVec2, not vec1Scalar)

    nodeName = inName or reduceName(CROSS_FORMAT.format(vec1Name, vec2Name))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output

    node = create("vectorProduct", nodeName, **kwargs)
    node.operation.set(2)#Cross
    if inNormalize:
        node.normalizeOutput.set(True)

    if vec1Scalar:
        node.input1.set(inVec1)
    else:
        get3DOut(inVec1) >> node.input1
    if vec2Scalar:
        node.input2.set(inVec2)
    else:
        get3DOut(inVec2) >> node.input2

    return node.output

@profiled
def pairBlend(inTranslate1, inRotate1, inTranslate2, inRotate2, inWeight=0, inName=None, **kwargs):
    inTranslate1 = getNode(inTranslate1)
    inRotate1 = getNode(inRotate1)

    inTranslate2 = getNode(inTranslate2)
    inRotate2 = getNode(inRotate2)

    weightScalar = isinstance(inWeight, (int,float))
    if not weightScalar:
        inWeight = getNode(inWeight)

    weightName = formatScalar(inWeight) if weightScalar else formatAttr(inWeight, True)
    nodeName = inName or reduceName(BLEND_FORMAT.format(inTranslate1.node().name(), weightName, inTranslate2.node().stripNamespace()))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName)

    node = create("pairBlend", nodeName, **kwargs)

    inTranslate1 >> node.inTranslate1
    inRotate1 >> node.inRotate1

    inTranslate2 >> node.inTranslate2
    inRotate2 >> node.inRotate2

    if weightScalar:
        node.weight.set(inWeight)
    else:
        inWeight >> node.weight

    return node

@profiled
def getAxis(inObj, inLocalVec=(0.0, 1.0, 0.0)):

    return None

# Curves
#################################################################################

@profiled
def getCurveInfo(inCurve, inName=None, **kwargs):
    inCurve = getNode(inCurve)

    if inCurve.type() == "transform":
        inCurve = inCurve.getShape()
        
    nodeName = inName or reduceName(CURVEINFO_FORMAT.format(inCurve.name()))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName)

    node = create("curveInfo", nodeName, **kwargs)
    inCurve.worldSpace[0] >> node.inputCurve
    
    return node

@profiled
def getClosestPoint(inCurve, inPositionNode, inWorld=True, inName=None, **kwargs):
    inCurve = getNode(inCurve)
    inPositionNode = getNode(inPositionNode)

    if inCurve.type() == "transform":
        inCurve = inCurve.getShape()

    nodeName = inName or reduceName(CLOSESTPOINT_FORMAT.format(inCurve.name(), inPositionNode.stripNamespace()))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName)

    node = create("nearestPointOnCurve", nodeName, **kwargs)
    inCurve.worldSpace[0] >> node.inputCurve

    inPositionNode = inPositionNode if not inWorld else worldMatrix(inPositionNode)

    inCurve.worldSpace[0] >> node.inputCurve
    get3DOut(inPositionNode) >> node.inPosition

    return node

@profiled
def pointOnCurve(inCurve, inAsPerc=True, inParam=0.5, inName=None, **kwargs):
    inCurve = getNode(inCurve)
    
    asPercScalar = isinstance(inAsPerc, (bool))
    paramScalar = isinstance(inAsPerc, (float, int))

    percName = formatScalar(inAsPerc) if asPercScalar else formatAttr(inAsPerc, True)
    paramName = formatScalar(inParam) if paramScalar else formatAttr(inParam, True)

    nodeName = inName or reduceName(POINTONCURVE_FORMAT.format(inCurve.name(), percName, paramName))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName)

    node = create("pointOnCurveInfo", nodeName, **kwargs)
    inCurve.worldSpace[0] >> node.inputCurve

    if asPercScalar:
        node.turnOnPercentage.set(inAsPerc)
    else:
        inAsPerc >> node.turnOnPercentage

    if paramScalar:
        node.parameter.set(inParam)
    else:
        inParam >> node.parameter

    return node

# Custom
#################################################################################
@profiled
def keep(inAttr, inName=None, **kwargs):
    inAttr = getNode(inAttr)

    types = {
        "double":0,
        "doubleLinear":0,
        "float":0,
        "double3":1,
        "matrix":2,
        None:2,
        "long":0
        }

    valueType = types.get(inAttr.type())

    if valueType is None:
        raise ValueError("Unmanaged type {0}".format(inAttr.type()))

    nodeName = inName or reduceName(KEEP_FORMAT.format(formatAttr(inAttr)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        if valueType == 0:#number
            return pc.PyNode(nodeName).outputX
        elif valueType == 1:#double3
            return pc.PyNode(nodeName).output
        else:#matrix
            return pc.PyNode(nodeName).outputMat

    node = create("tkKeep", nodeName, **kwargs)

    for key, value in kwargs.iteritems():
        if pc.attributeQuery(key, node=node, exists=True):
            if isinstance(value, pc.general.Attribute):
                value >> node.attr(key)
            else:
                node.attr(key).set(value)

    pc.PyNode("time1").outTime >> node.time

    inputAttr = None;
    outputAttr = None;

    if valueType == 0:#number
        inputAttr = node.inputX
        outputAttr = node.outputX
    elif valueType == 1:#double3
        inputAttr = node.input
        outputAttr = node.output
    else:#matrix
        inputAttr = node.inputMat
        outputAttr = node.outputMat

    inAttr >> inputAttr
    return outputAttr

@profiled
def accu(inAttr, inName=None, **kwargs):
    inAttr = getNode(inAttr)

    nodeName = inName or reduceName(ACCU_FORMAT.format(formatAttr(inAttr)))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output

    node = create("tkAccu", nodeName, **kwargs)

    pc.PyNode("time1").outTime >> node.time

    inAttr >> node.input

    return node.output

#################################################################################
#                           MACROS                                              #
#################################################################################


@profiled
def velocity(inObj, **kwargs):
    nodeName = reduceName(VELOCITY_FORMAT.format(inObj.name()))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output3D

    keptMat = keep(inObj.worldMatrix[0])
    keptMatDec = decomposeMatrix(keptMat)
    objMatDec = decomposeMatrix(inObj.worldMatrix[0])

    vel = sub(objMatDec.outputTranslate, keptMatDec.outputTranslate, nodeName)

    return vel

@profiled
def angularVelocity(inObj, **kwargs):
    nodeName = reduceName(ANGVELOCITY_FORMAT.format(inObj.name()))
    if pc.objExists(nodeName) and (not SAFE_FACTORISATION or not "___" in nodeName):
        return pc.PyNode(nodeName).output3D

    keptMat = keep(inObj.worldMatrix[0])
    keptMatDec = decomposeMatrix(keptMat)
    objMatDec = decomposeMatrix(inObj.worldMatrix[0])

    vel = sub(objMatDec.outputRotate, keptMatDec.outputRotate, nodeName)

    return vel

@profiled
def createAccumulatedVelocity(inObj, **kwargs):
    vel = velocity(inObj)
    mag = vectorMag(vel)
    acc = accu(mag)

    return acc

@profiled
def createExtremumSystem(inAttrs, inMinimum=True, **kwargs):
    previousAttr = None
    previousCondition = None

    cond = None

    counter = 0
    for inAttr in inAttrs:
        if not previousAttr is None:
            cond = None

            if previousCondition is None:
                cond = condition(previousAttr, inAttr, 4 if inMinimum else 2, inName="{0}_firstCond".format(formatAttr(inAttr))).node()
                cond.colorIfTrueR.set(counter-1)
                previousAttr >> cond.colorIfTrueG

                #print "previousCondition is None", previousAttr.node(), ">>", cond
            else:
                cond = condition(previousCondition.outColorG, inAttr, 4 if inMinimum else 2, inName="{0}_Cond".format(formatAttr(inAttr))).node()
                previousCondition.outColorR >> cond.colorIfTrueR
                previousCondition.outColorG >> cond.colorIfTrueG

                #print "else", previousCondition, ">>", cond

            cond.colorIfFalseR.set(counter)
            "always", inAttr >> cond.colorIfFalseG

            #print inAttr.node(), ">>", cond
        previousCondition = cond
        previousAttr = inAttr
        counter += 1

    return cond

@profiled
def createBlendExtremumSystem(inAttrs, inInputAttrs, inName, inMinimum=True, **kwargs):
    outCond = createExtremumSystem(inAttrs, inMinimum=inMinimum)

    inputDegree = 1 if not isinstance(inInputAttrs[0], (list, tuple)) else len(inInputAttrs[0])

    blends = []

    if inputDegree == 1:
        blends.append(create("blendTwoAttr", inName))
    else:
        for i in range(inputDegree):
            blends.append(create("blendTwoAttr", reduceName("{0}_{1}".format(inName, i))))

    counter = 0
    for inputAttr in inInputAttrs:
        if inputDegree == 1:
            inputAttr >> blends[0].attr("input[{0}]".format(counter))
        else:
            for i in range(inputDegree):
                inputAttr[i] >> blends[i].attr("input[{0}]".format(counter))

        counter += 1

    return blends

@profiled
def createProximitiesCompound(inObj, inStart, inEnd, inDist=False, **kwargs):
    startToObjVec = vector(inStart, inObj)
    startToEndVec = vector(inStart, inEnd)
    ObjOnLocDot = dot(startToObjVec, startToEndVec)

    startToEndDist = distance(inStart, inEnd)
    distPow = npow(startToEndDist)
    
    normDivide = div(ObjOnLocDot, distPow)
    rsltClamp = clamp(normDivide)
    rsltReverse = reverse(rsltClamp)

    rslts = {
            "startToObjVec":startToObjVec,
            "startToEndVec":startToEndVec,
            "startToEndDist":startToEndDist,
            "distPow":distPow,
            "ObjOnLocDot":ObjOnLocDot,
            "normDivide":normDivide,
            "rsltClamp":rsltClamp,
            "rsltReverse":rsltReverse,
            }

    if inDist:
        endToStartVec = vector(inEnd, inStart)
        endToObjVec = vector(inEnd, inObj)
        ObjOnLocDot2 = dot(endToObjVec, endToStartVec)

        norm1Abs = nabs(ObjOnLocDot)
        norm2Abs = nabs(ObjOnLocDot2)

        dist = add(norm1Abs, norm2Abs)

        minusDist = sub(dist, distPow)
        
        crossP = cross(startToEndVec, startToObjVec)
        mag = vectorMag(crossP)
        magClamp = clamp(mag, inMin=0.0001, inMax=OMEGA)
        rslts["dist"] = add(minusDist, magClamp)

    return rslts

"""
kwargs awaits :
-inResultObjName (string : default "RESULTS")
-inResultAttrFormat (string with a format token : default "Loc{0}")
-inCurve (curve name or PyNode : default None)
"""
@profiled
def createProximitiesSystem(inObj, *inCheckPoints, **kwargs):
    inResultObjName = kwargs.get("inResultObjName", "RESULTS")
    inResultAttrFormat = kwargs.get("inResultAttrFormat", "Loc{0}")

    inCurve = kwargs.get("inCurve", None)

    if not inCurve is None:
        curveNodes = []
        for checkPoint in inCheckPoints:
            curveNodes.append(getClosestPoint(inCurve, checkPoint, inWorld=False))
        inCheckPoints = curveNodes

    firstIter = True
    lastIter = False

    lenCheckPoints = len(inCheckPoints)

    #Prepare result obj
    resultObj = None
    if not pc.objExists(inResultObjName):
        resultObj = create("transform", inResultObjName, **kwargs)
    else:
        resultObj = pc.PyNode(inResultObjName)

    for i in range(lenCheckPoints):
        attrName = inResultAttrFormat.format(i+1)
        if not pc.attributeQuery(attrName, node=resultObj, exists=True):
            pc.select(resultObj)
            pc.addAttr(longName=attrName, defaultValue=0.0, minValue=0.0, maxValue=1.0)

    #Actually do the nodeling
    intermediateResults = []
    distanceResults = []

    firstOutput = None
    secondOutput = None
    bigger0 = None
    for i in range(lenCheckPoints - 1):
        start = inCheckPoints[i]
        end = inCheckPoints[i+1]

        curCompound = createProximitiesCompound(inObj, start, end, inDist=lenCheckPoints > 2)
        
        if lenCheckPoints == 2:
            #This is the simple case, simply connect outputs from reverse and clamp
            curCompound["rsltReverse"] >> resultObj.attr(inResultAttrFormat.format(i+1))
            curCompound["rsltClamp"] >> resultObj.attr(inResultAttrFormat.format(i+2))
        else:
            intermediateResults.append((curCompound["rsltReverse"], curCompound["rsltClamp"]))
            distanceResults.append(curCompound["dist"])

    if lenCheckPoints > 2:
        segmentsCond = []

        lastSegmentCond = None
        firstIter = True

        extremum = createExtremumSystem(distanceResults)

        counter = 0
        for first, second in intermediateResults:

            segmentCond = create("condition", reduceName("segment_{0}_Cond".format(counter)), **kwargs)
            segmentsCond.append(segmentCond)
            segmentCond.operation.set(0)
            extremum.outColorR >> segmentCond.firstTerm
            segmentCond.secondTerm.set(counter)

            segmentCond.colorIfFalse.set([0, 0, 0])
            segmentCond.colorIfTrueB.set(1)

            first >> segmentCond.colorIfTrueR
            second >> segmentCond.colorIfTrueG

            if firstIter:
                #First iteration
                segmentCond.outColorR >> resultObj.attr(inResultAttrFormat.format(counter+1))
                firstIter = False

            else:
                #Random iteration
                firstSegmentCond = create("condition", reduceName("firstSegment_{0}_Cond".format(counter)), **kwargs)
                firstSegmentCond.operation.set(0)
                firstSegmentCond.firstTerm.set(1)
                lastSegmentCond.outColorB >> firstSegmentCond.secondTerm

                lastSegmentCond.outColorG >> firstSegmentCond.colorIfTrueR

                
                secondSegmentCond = create("condition", reduceName("secondSegment_{0}_Cond".format(counter)), **kwargs)
                secondSegmentCond.operation.set(0)
                secondSegmentCond.firstTerm.set(1)
                secondSegmentCond.colorIfFalseR.set(0)
                segmentCond.outColorB >> secondSegmentCond.secondTerm

                segmentCond.outColorR >> secondSegmentCond.colorIfTrueR
                secondSegmentCond.outColorR >> firstSegmentCond.colorIfFalseR

                firstSegmentCond.outColorR >> resultObj.attr(inResultAttrFormat.format(counter+1))

                if counter == len(intermediateResults) -1:
                    #Last iteration
                    segmentCond.outColorG >> resultObj.attr(inResultAttrFormat.format(counter+2))

            counter += 1
            lastSegmentCond = segmentCond

def createProximitiesSystemOnSelection(inResultObjName="RESULTS", inResultAttrFormat="Loc{0}", **kwargs):
    sel = pc.selected()

    if len(sel) < 3:
        pc.warning("Cannot create a proximities system with less than 3 elements !")
        return

    createProximitiesSystem(sel[0], *sel[1:], inResultObjName=inResultObjName, inResultAttrFormat=inResultAttrFormat)


#################################################################################
#                           EXPRESSIONS                                         #
#################################################################################

EXPR_INSTANCE = None
RESULT_RE = re.compile("^\s*([^= ]*)\s*=\s*")
IF_RE = re.compile("\s*if\s*\(\s*(.*)\s*\)[\S\s]*?({)")

def findEnclosed(inString, inStart, inStartChar ="{", inEndChar ="}"):
    lenString = len(inString)
    caret = inStart
    drop = 0
    while(caret < lenString):
        curChar = inString[caret]
        if curChar == inEndChar:
            if drop == 0:
                return caret
            else:
                drop += -1
        elif curChar == inStartChar:
            drop += 1

        caret += 1
    
    return -1

def convertIf(inString, inStartChar ="{", inEndChar ="}"):
    matches = IF_RE.search(inString)
    if matches:
        #Get if condition and first trailing "{"
        condition, endChar = matches.groups()

        condition = condition.strip(" \t\n\r")

        #Get firstTerm
        startFirst = matches.end(2)
        endFirst = findEnclosed(inString, startFirst, inStartChar, inEndChar)
        if endFirst == -1:
            raise ValueError("Can't find 'firstTerm' closing bracket !")

        firstTerm = inString[startFirst:endFirst].strip(" \t\n\r")
        firstTerm = convertIf(firstTerm, inStartChar, inEndChar)

        firstSplit = firstTerm.split("=")
        firstInput = firstSplit[0].strip(" \t\n\r")
        firstOutput = firstSplit[1].strip(" \t\n\r;")

        #Get secondTerm
        startSecond = inString.find(inStartChar, endFirst)
        if startSecond == -1:
            raise ValueError("Can't find 'else' opening bracket !")

        startSecond += 1
        endSecond = findEnclosed(inString, startSecond, inStartChar, inEndChar)
        if endSecond == -1:
            raise ValueError("Can't find 'secondTerm' closing bracket !")

        secondTerm = inString[startSecond:endSecond].strip(" \t\n\r")
        secondTerm = convertIf(secondTerm, inStartChar, inEndChar)

        secondSplit = secondTerm.split("=")
        secondInput = secondSplit[0].strip(" \t\n\r")
        secondOutput = secondSplit[1].strip(" \t\n\r;")

        if firstInput != secondInput:
            raise ValueError("Can't convert 'if's when its cases affect different inputs ({0} != {1}) !".format(firstInput, secondInput))

        #print "start",start,inString[start-1:start+1]
        #print "end",end,inString[end-1:end+1]
        #print "---"
        #print "condition",condition
        #print "firstTerm",firstTerm
        #print "secondTerm",secondTerm
        #print "---"
        #print "{0} = cond({1}, {2}, {3})".format(firstInput, condition, firstOutput, secondOutput)

        return "{0} = cond({1}, {2}, {3})".format(firstInput, condition, firstOutput, secondOutput)

    return inString

def convertNot(inString):
    return re.sub("!(?!=)", "~", inString)

class NodalTerm(tke.Term):

    def __init__(self, value=None):
        super(NodalTerm, self).__init__(value)

        self.value = getNode(self.value)

    def get(self):
        if isinstance(self.value , pc.general.Attribute):
            return NodalTerm(self.value.get())

        return self.value

    #Unary
    def neg(self):
        return neg(self.value)

    def abs(self):
        return nabs(self.value)

    #Binary
    def add(self, other):
        return add(self.value, other.value)

    def sub(self, other):
        return sub(self.value, other.value)

    def mul(self, other):
        return mul(self.value, other.value)

    def div(self, other):
        return div(self.value, other.value)

    def pow(self, other):
        return npow(self.value, other.value)

    def mod(self, other):
        return mod(self.value, other.value)

    #Functions
    def reverse(self):
        return reverse(self.value)

    def cos(self):
        return cos(self.value)

    def sin(self):
        return sin(self.value)

    def clamp(self, otherMin, otherMax):
        return clamp(self.value, otherMin.value, otherMax.value)

    def cond(self, criterion, secondTerm, ifTrue, ifFalse):
        return condition(self.value, secondTerm.value, criterion, ifTrue.value, ifFalse.value)

class NodalExpr(tke.Expr):
    logger = tke.logger

    def __init__(self):
        super(NodalExpr, self).__init__(NodalTerm, sys.modules[self.__module__])

    def compile(self, inExpr, inDeleteUnused=False):
        result = None
        regResult = RESULT_RE.match(inExpr)
        if not regResult is None:
            result = getNode(regResult.groups()[0])
            inExpr = inExpr[len(regResult.group()):]

            NodalExpr.logger.debug("Result found : {0}".format(result))
            NodalExpr.logger.debug("Expression is now : {0}".format(inExpr))
        else:
            NodalExpr.logger.debug("Result not found")

        startProfiling()

        output = super(NodalExpr, self).compile(inExpr)

        if not result is None:
            output >> result

        if inDeleteUnused:
            deleteUnusedNodes()

        return stopProfiling()

def compileNodes(inExpr, inDeleteUnused=False):
    global EXPR_INSTANCE

    if EXPR_INSTANCE == None:
        EXPR_INSTANCE = NodalExpr()

    return EXPR_INSTANCE.compile(inExpr, inDeleteUnused)

def convertExpressionString(inString, inDeleteUnused=False):
    exprs = convertIf(inString)

    exprs = [expr.strip(os.linesep) for expr in exprs.split(";") if len(expr) > 1]

    NodalExpr.logger.debug("{0} exprs :\n{1}".format(len(exprs), "\n".join(exprs)))

    nodes = []

    for expr in exprs:
        nodes.append(compileNodes(convertNot(expr)))

    if inDeleteUnused:
        deleteUnusedNodes()

    return nodes

def convertExpression(inExpr, inDeleteUnused=False, inVerbose=False):
    inExpr = getNode(inExpr)

    if inExpr.type() != "expression":
        pc.warning("Cannot convert {0} to nodes (Not an expression !)".format(inExpr))
        return

    exprString = inExpr.getString()

    cons = inExpr.output[0].listConnections(plugs=True)
    if len(cons) != 1:
        if inVerbose:
            print "Can't convert, no output ! ({0}, '{1}'')".format(inExpr,exprString)
        return []

    lock = cons[0].isLocked()
    if lock:
        cons[0].setLocked(False)

    if ".O[0]" in exprString:
        exprString = exprString.replace(".O[0]", cons[0])

    nodes = []

    try:
        nodes = convertExpressionString(exprString)
        pc.delete(inExpr)
    except Exception as e:
        if inVerbose:
            pc.warning("Can't convert : '" + exprString + "'\n" + str(e))

    if lock:
        cons[0].setLocked(True)

    if inDeleteUnused:
        deleteUnusedNodes()

    return nodes