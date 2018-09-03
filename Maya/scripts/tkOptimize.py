import os
import re

import OscarZmqMayaString as ozms

import pymel.core as pc
import tkMayaCore as tkc
import tkDevHelpers as tkdev
import tkNodeling as tkn

#BENCHMARKING
#---------------------------------------------------
def evaluate(inFrames=100):
    fps = 100.0 / tkc.benchIt(tkdev.evaluate, inFrames)[0]
    print "{0} fps, {1} ms".format(fps, 1000.0/fps)

    return fps

"""
def createConstraintsBenchmark(inNumber=100):
    objs = []

    for i in range(inNumber):
        objs.append(pc.spaceLocator())

    xOffset = 1.0
    i = 0
    for obj in objs:
        if i > 0:
            #move
            obj.tx.set(i*xOffset)
            
            #parent
            #tkc.constrain(obj, objs[i-1])
            fakeConstrain2(obj, objs[i-1])

        i += 1
"""

#tkc
def getAllConnections(inAttr):
    cons = inAttr.listConnections(source=True, destination=True, plugs=True, connections=True)

    if len(cons) == 0 and inAttr.isCompound():
        childAttrs = inAttr.children()
        for childAttr in childAttrs:
            cons.extend(childAttr.listConnections(source=True, destination=True, plugs=True, connections=True))

    return cons

#tkc
def getConstraintConnections(inCns):
    cons = []

    if inCns.type() == "parentConstraint":
        cons.extend(getAllConnections(inCns.target[0].targetOffsetTranslate))
        cons.extend(getAllConnections(inCns.target[0].targetOffsetRotate))
    elif inCns.type() == "scaleConstraint":
        cons.extend(getAllConnections(inCns.offset))

    return cons

def matrixConstrain(inTarget, inSource, inScale=True, inOffsetT=None, inOffsetR=None, inOffsetS=None, inForceOffset=False):
    createdNodes = []

    matrixOut = None

    offsets = [inOffsetT or [0.0,0.0,0.0], inOffsetR or [0.0,0.0,0.0], inOffsetS or [1.0,1.0,1.0]]

    autodetect = inOffsetT is None or inOffsetR is None or (inScale and inOffsetS is None)
    if autodetect:
        offset = pc.group(name=inSource + "_offset_MARKER", empty=True)
        inSource.addChild(offset)
        tkc.matchTRS(offset, inTarget)
    
        offsets = [inOffsetT or list(offset.getTranslation()), inOffsetR or list(ozms.getPymelRotation(offset)), inOffsetS or list(offset.getScale())]

        pc.delete(offset)

    offseted = inForceOffset or not (tkc.listsBarelyEquals(offsets[0], [0.0,0.0,0.0]) and
                tkc.listsBarelyEquals(offsets[1], [0.0,0.0,0.0]) and
                tkc.listsBarelyEquals(offsets[2], [1.0,1.0,1.0]))

    if not tkc.listsBarelyEquals(offsets[2], [1.0,1.0,1.0]):
        print inSource,">>",inTarget,"have scale offsets",offsets[2]

    if offseted:
        composeOut = tkn.composeMatrix(offsets[0], offsets[1], offsets[2])
        createdNodes.append(composeOut.node())
        matrixOut = tkn.mul(composeOut, inSource.worldMatrix[0])#offset_Mul.matrixSum
        createdNodes.append(matrixOut.node())
    else:
        matrixOut = inSource.worldMatrix[0]

    invertMul = tkn.mul(matrixOut, inTarget.parentInverseMatrix[0])
    createdNodes.append(invertMul.node())

    decompMatrix = tkn.decomposeMatrix(invertMul)
    createdNodes.append(decompMatrix)

    decompMatrix.outputTranslate >> inTarget.translate
    decompMatrix.outputRotate >> inTarget.rotate
    if inScale:
        decompMatrix.outputScale >> inTarget.scale

    return createdNodes

CONS_LINKS = {
    "targetOffsetTranslate":"inputTranslate",

    "targetOffsetTranslateX":"inputTranslateX",
    "targetOffsetTranslateY":"inputTranslateY",
    "targetOffsetTranslateZ":"inputTranslateZ",

    "targetOffsetRotate":"inputRotate",
    "targetOffsetRotateX":"inputRotateX",
    "targetOffsetRotateY":"inputRotateY",
    "targetOffsetRotateZ":"inputRotateZ",

    "offset":"inputScale",
    "offsetX":"inputScaleX",
    "offsetY":"inputScaleY",
    "offsetZ":"inputScaleZ"
}

def replaceConstraint(inConstraint, inTarget=None, inSource=None):

    inSource = inSource or tkc.getConstraintTargets(inConstraint)[0]
    inTarget = inTarget or tkc.getConstraintOwner(inConstraint)[0]

    offsets = [list(inConstraint.target[0].targetOffsetTranslate.get()), list(inConstraint.target[0].targetOffsetRotate.get()), [1.0,1.0,1.0]]

    cons = getConstraintConnections(inConstraint)
    sclCons = []

    pc.delete(inConstraint)

    haveScale = False
    constraints = tkc.getConstraints(inTarget)
    for constraint in constraints:
        if constraint.type() == "scaleConstraint" and inSource in tkc.getConstraintTargets(constraint):
            haveScale = True
            #Search if weight is not 1.0 and/or connected
            udParams = tkc.getParameters(constraint)
            for udParam in udParams:
                if re.match("^w[0-9]+$", udParam):#It's a weight !
                    if not tkc.doubleBarelyEquals(constraint.attr(udParam).get(), 1.0) or len(constraint.attr(udParam).listConnections()) > 0: 
                        haveScale = False

            if haveScale:
                #offsets[2] = list(constraint.offset.get())
                sclCons = getConstraintConnections(constraint)
                pc.delete(constraint)

            break

    haveConnections = (len(cons) + len(sclCons)) > 0

    #createdNodes = matrixConstrain(inTarget, inSource, haveScale, offsets[0], offsets[1], offsets[2], inForceOffset=haveConnections)
    createdNodes = matrixConstrain(inTarget, inSource, haveScale, inForceOffset=haveConnections)

    #Re-link offset connections
    if haveConnections:
        for linkInput, linkOutput in cons:
            newInput = CONS_LINKS.get(linkInput.split(".")[-1])
            if not newInput is None:
                linkOutput >> createdNodes[0].attr(newInput)
            else:
                pc.warning("Can't reconnect {0} >> {1}".format(linkOutput, linkInput))

        for linkInput, linkOutput in sclCons:
            newInput = CONS_LINKS.get(linkInput.split(".")[-1])
            if not newInput is None:
                linkOutput >> createdNodes[0].attr(newInput)
            else:
                pc.warning("Can't reconnect {0} >> {1}".format(linkOutput, linkInput))

def replaceConstraints(inDebugFolder=None):
    debugCounter = 0

    if not inDebugFolder is None:
        if not os.path.isdir(inDebugFolder):
            os.makedirs(inDebugFolder)
        else:
            tkc.emptyDirectory(inDebugFolder)
        print "DEBUG MODE ACTIVATED ({})".format(inDebugFolder)
        tkc.capture(os.path.join(inDebugFolder, "{0:04d}_ORIGINAL.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
        debugCounter = debugCounter + 1

    parentCons = pc.ls(type="parentConstraint")
    print "parentCons", len(parentCons)
    
    replaced = []

    for parentCon in parentCons:
        owner = tkc.getConstraintOwner(parentCon)[0]
        targets = tkc.getConstraintTargets(parentCon)

        if len(targets) == 1:

            if owner.type() != "joint":

                replaced.append(owner)
                replaceConstraint(parentCon, owner, targets[0])

                if not inDebugFolder is None:
                    tkc.capture(os.path.join(inDebugFolder, "{0:04d}_replaceCns_{1}.jpg".format(debugCounter, parentCon.name().replace("|", "("))), start=1, end=1, width=1280, height=720)
                    debugCounter = debugCounter + 1

            else:
                print "Cannot replace (owner is scaled joint): ",parentCon,"on",owner
        else:
            print "Cannot replace (multiple targets): ",parentCon,"on",owner

    print "replaced",len(replaced),replaced

#EXPRESSION REPLACEMENT
#---------------------------------------------------
#tkn.convertExpression(inExpr)
def convertExpressions():
    invalidItems = ["sin(",
                    "cos("]

    replaced = []

    exprs = pc.ls(type="expression")
    print "exprs", len(exprs)
    for expr in exprs:
        #print "Expr",expr
        #print "-cons",len(expr.listConnections()),expr.listConnections()

        valid = True
        exprString = expr.getString()
        #print "-exprString",exprString

        for invalidItem in invalidItems:
            if invalidItem in exprString:
                valid = False
                break

        if valid:
            replaced.append(expr)
            tkn.convertExpression(expr)
        else:
            print "Cannot replace (invalid item): ",expr,exprString
        
    print "replaced",len(replaced),replaced