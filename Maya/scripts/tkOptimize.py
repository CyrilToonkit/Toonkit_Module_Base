import os
import re

import OscarZmqMayaString as ozms

import pymel.core as pc
import tkMayaCore as tkc
import tkRig
import tkDevHelpers as tkdev
import tkNodeling as tkn

"""
#IN ORDER

import tkMayaCore as tkc
import tkDevHelpers as tkdev
import tkNodeling as tkn
import tkExpressions as tke
import tkOptimize as tko

reload(tkc)
reload(tkdev)
reload(tkn)
reload(tke)
reload(tko)

#Diagnose
tko.diagnose()

#Evaluate
tko.evaluate()


#ConvertExpressions
tko.convertExpressions()

#PTTransforms
tko.deletePTTransforms()

#ConvertConstraints
tko.replaceConstraints()

#PTAttributes
tko.deletePTAttributes("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")

#UselessTransforms
tko.deleteUselessTransforms("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")

#UnusedNodes++
tkc.deleteUnusedNodes()
"""


#BENCHMARKING
#---------------------------------------------------
def diagnose(inProps=["Objects",
        "Transforms",
        "Locators",
        "Joints",
        "Curves",
        "Expressions",
        "Expressions Characters",
        "Constraints",
        "parentConstraints",
        "aimConstraints",
        "orientConstraints",
        "scaleConstraints",
        "pointConstraints",
        "poleVectorConstraints",
        "motionPaths",
        "Utilities"]):
    
    values = tkdev.Tester("SomeRig", "SomePath").getValues(*inProps)

    for i in range(len(inProps)):
        print "{0} : {1}".format(inProps[i],values[i])

def evaluate(inFrames=100):
    fps = 100.0 / tkc.benchIt(tkdev.evaluate, inFrames)[0]
    print "{0} fps, {1} ms".format(fps, 1000.0/fps)

    return fps

def createConstraintsBenchmark(inNumber=100):
    objs = []

    for i in range(inNumber):
        objs.append(pc.spaceLocator())

    xOffset = 1.0
    i = 0
    for obj in objs:
        if i > 0:
            #move
            #obj.tx.set(i*xOffset)
            
            #parent
            tkc.constrain(obj, objs[i-1], "Position")
            #matrixPointConstrain(obj, objs[i-1], [0.0,0.0,0.0])
        i += 1

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

#Does not work with offsets !!
def matrixPointConstrain(inTarget, inSource, inOffsetT=None, inForceOffset=False):
    createdNodes = []

    matrixOut = None

    offset = inOffsetT or [0.0,0.0,0.0]

    autodetect = inOffsetT is None
    if autodetect:
        offset = pc.group(name=inSource + "_offset_MARKER", empty=True)
        offsetChild = pc.group(name=inSource + "_offset_MARKER_CHILD", empty=True)

        offset.addChild(offsetChild)
        tkc.matchT(offset, inSource)
        tkc.matchT(offsetChild, inTarget)

        offset = list(offsetChild.getTranslation())

        pc.delete(offset)

    offseted = inForceOffset or not tkc.listsBarelyEquals(offset, [0.0,0.0,0.0])

    if offseted:
        composeOut = tkn.composeMatrix(offset, [0.0,0.0,0.0], [1.0,1.0,1.0])
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
                    if not tkc.doubleBarelyEquals(constraint.attr(udParam).get(), 1.0) or len(constraint.attr(udParam).listConnections()) > 1: 
                        #print "!! haveScale = False",constraint.attr(udParam).get(), tkc.doubleBarelyEquals(constraint.attr(udParam).get(), 1.0), constraint.attr(udParam).listConnections()
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

    parentCons = pc.ls(type=["parentConstraint","pointConstraint"])
    print "Constraints", len(parentCons)
    
    replaced = []

    for parentCon in parentCons:
        conName = parentCon.name().replace("|", "(")

        owner = tkc.getConstraintOwner(parentCon)[0]
        targets = tkc.getConstraintTargets(parentCon)

        if len(targets) == 0:
            print "Cannot replace (NO TARGETS): ",parentCon,"on",owner
            continue

        if parentCon.type() == "pointConstraint":
            #TODO : replace anyway
            if len(targets) > 1:
                #print "Cannot replace (multiple targets): ",parentCon,"on",owner
                continue

            #TODO : replace anyway
            if len(parentCon.offset.listConnections()) > 0:
                #print "Cannot replace (position offset with connections): ",parentCon,"on",owner
                continue

            #TODO : replace anyway
            if not tkc.listsBarelyEquals(parentCon.offset.get(), [0.0,0.0,0.0]):
                #print "Cannot replace (position with offset): ",parentCon,"on",owner
                continue

            replaced.append(owner.name())
            pc.delete(parentCon)
            matrixPointConstrain(owner, targets[0], [0.0,0.0,0.0])
        elif parentCon.type() == "parentConstraint":
            #TODO : replace anyway
            if len(targets) > 1:
                #print "Cannot replace (multiple targets): ",parentCon,"on",owner
                continue

            #TODO : replace if joint have no scale ?
            if owner.type() == "joint":
                #print "Cannot replace (owner is joint): ",parentCon,"on",owner
                continue

            if not tkc.listsBarelyEquals(list(owner.rp.get()), [0.0,0.0,0.0]):
                print "Cannot replace (owner have scale pivots): ",parentCon,"on",owner
                continue

            targetPivots=False
            for target in targets:
                if not tkc.listsBarelyEquals(list(target.rp.get()), [0.0,0.0,0.0]):
                    print "Cannot replace (target {0} have scale pivots): ".format(target),parentCon,"on",owner,
                    targetPivots=True

            if targetPivots:
                continue

            replaced.append(owner.name())
            replaceConstraint(parentCon, owner, targets[0])

        #Reparent
        #------------------
        """
        constraints = tkc.getConstraints(owner)
        for constraint in constraints:
            if constraint.type() == "scaleConstraint" and targets[0] in tkc.getConstraintTargets(constraint):
                pc.delete(constraint)
                break

        pc.delete(parentCon)

        #Unlock the Transforms
        attrs = ["tx","ty", "tz", "rx","ry","rz","sx","sy","sz"]
        for attr in attrs:
           owner.attr(attr).setLocked(False) 

        if owner.getParent() != targets[0]:
            targets[0].addChild(owner)
        """
        #------------------

        if not inDebugFolder is None:
            tkc.capture(os.path.join(inDebugFolder, "{0:04d}_replaceCns_{1}.jpg".format(debugCounter, conName)), start=1, end=1, width=1280, height=720)
            debugCounter = debugCounter + 1

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
            replaced.append(expr.name())
            tkn.convertExpression(expr)
        else:
            print "Cannot replace (invalid item): ",expr,exprString

    print "replaced",len(replaced),replaced


def getUselessTransforms(inExceptPattern=None):
    uselessTransforms = []
    
    ts = pc.ls( exactType=["transform", "joint"])
    
    print len(ts)
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        #Children
        if len(t.getChildren()) > 0:
            continue

        #Connections
        if len(t.listConnections(source=False, destination=True)) > 0:
            print t,t.listConnections(source=False, destination=True)
            continue
    
        uselessTransforms.append(t)
        
    return uselessTransforms

def deleteUselessTransforms(inExceptPattern=None):
    MAXITER = 7

    deleted = []

    uts = getUselessTransforms(inExceptPattern)
    
    if len(uts) == 0:
        return 0

    curIter = 0

    while curIter < MAXITER:
        nUts = len(uts)
        deleted.extend([n.name() for n in uts])
        pc.delete(uts)
        uts = getUselessTransforms(inExceptPattern)

        if nUts == 0:
            print "deleteUselessTransforms",len(uts),uts
            return deleted

    print "deleteUselessTransforms",len(deleted),deleted
    pc.warning("delete useless trasforms : Max iterations reached ({0})".format(MAXITER))
    return deleted

def deletePTTransforms(inExceptPattern=None):
    uselessTransforms = []
    
    ts = pc.ls(exactType=["transform"])
    
    print len(ts)
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        #Children
        if len([c for c in t.getChildren() if not c.type().endswith("Constraint")]) > 0:
            continue

        #Constraints
        cons = [c for c in tkc.getConstraints(t) if c.type() in ["parentConstraint", "scaleConstraint"]]
        otherCons = [c for c in tkc.getConstraintsUsing(t) if c.type() in ["parentConstraint", "scaleConstraint"]]
        
        if len(cons) > 0 and len(otherCons) > 0:
            if len(list(set(t.listConnections()))) != len(list(set(cons + otherCons))):
                print "PTTransforms : Other connections :",t,list(set(t.listConnections())),list(set(cons + otherCons))
                continue

            if len(getConstraintConnections(inCns)) > 0:
                print "PTTransforms : Input connections :",getConstraintConnections(inCns)
                continue

            outputCons = False
            for otherCon in otherCons:
                if len(getConstraintConnections(otherCon)) > 0:
                    print "PTTransforms : Output connections :",getConstraintConnections(otherCon)
                    outputCons=True
                    break

            if outputCons:
                continue

            uselessTransforms.append(t.name())

    print "deletePTTransforms",len(uselessTransforms),uselessTransforms
    return uselessTransforms

def deletePTAttributes(inExceptPattern=None, inDropStaticValues=True):
    uselessAttributes = []
    
    ts = pc.ls(exactType=["transform"])
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        uds = tkc.getParameters(t)
        for ud in uds:

            attr = t.attr(ud)

            #Connections
            cons = attr.listConnections(source=True, destination=False, plugs=True)
            otherCons = attr.listConnections(source=False, destination=True, plugs=True)

            haveExpr = False
            for con in cons + otherCons:
                if con.node().type() == "expression":
                    print "Attribute '{0}' still have expression ('{1}') !".format(attr, con.node())
                    haveExpr = True
                    break

            if haveExpr:
                continue

            if len(cons) > 0 and len(otherCons) > 0:
                uselessAttributes.append(attr.name())

                for otherCon in otherCons:
                    lock = otherCon.isLocked()
                    if lock:
                        otherCon.setLocked(False)

                    cons[0] >> otherCon

                    if lock:
                        otherCon.setLocked(True)

                try:
                    pc.deleteAttr(attr)
                    uselessAttributes.append(attr.name())
                except:
                    pass

            elif inDropStaticValues and not tkRig.isControl(t):
                if len(otherCons) > 0:
                    allSettable = True
                    #Should be useless to filter expressions because filtered before
                    """
                    for otherCon in otherCons:
                        if otherCon.node().type() == "expression":
                            allSettable = False
                            break
                    """

                    if allSettable:
                        value = attr.get()
                        for otherCon in otherCons:
                            attr.disconnect(otherCon)
                            otherCon.set(value)

                        try:
                            pc.deleteAttr(attr)
                            uselessAttributes.append(attr.name())
                        except:
                            pass
                else:
                    try:
                        pc.deleteAttr(attr)
                        uselessAttributes.append(attr.name())
                    except:
                        pass

    print "deletePTAttributes",len(uselessAttributes),uselessAttributes

    return uselessAttributes

def setDeactivator(inAttr, inRoots, inDeactivateValue=1):
    inAttr = tkc.getNode(inAttr)

    cond = tkn.condition(inAttr, inDeactivateValue, "==", 1.0, 0.0)
    condVis = tkn.condition(inAttr, inDeactivateValue, "==", 1.0, 0.0)

    for root in inRoots:
        locked = root.v.isLocked()
        if locked:
            root.v.setLocked(False)

        #TODO compound condition if already connected (and / or ?)
        cond >> root.v

        if locked:
            root.v.setLocked(True)

    cns = tkc.getExternalConstraints(inRoots, inSource=True, inDestination=True)
    for cn in cns:
        #TODO compound condition if already connected (and / or ?)
        cond >> cn.nodeState
"""
def getExternalLinks(inRoot):
    CONSTRAINT_TYPES = ["parentConstraint", "pointConstraint", "scaleConstraint", "orientConstraint"]

    extInputs = []
    extOutputs = []

    if not isinstance(inRoot,(list,tuple)):
        inRoot = [inRoot]

    allChildren = []
    for root in inRoot:
        allChildren.extend(root.getChildren(allDescendents=True, type="transform"))
    allChildren.extend(inRoot)

    for child in allChildren:
        if child.type() in CONSTRAINT_TYPES:
            continue

        cons = child.listConnections(source=True, destination=False, plugs=True, connections=True)
        for con in cons:
            if con[0].type() in CONSTRAINT_TYPES or con[1].type() in CONSTRAINT_TYPES:
                continue

            if con[1].type() == "transform" and con[1].node() in allChildren:
                continue

            extInputs.append(con)

        cons = child.listConnections(source=False, destination=True, plugs=True, connections=True)
        for con in cons:
            if con[0].type() in CONSTRAINT_TYPES or con[1].type() in CONSTRAINT_TYPES:
                continue

            if con[0].type() == "transform" and con[0].node() in allChildren:
                continue

            extOutputs.append(con)

    return (extInputs, extOutputs)

def getExternalLinks3(inRoot):
    CONSTRAINT_TYPES = ["parentConstraint", "pointConstraint", "scaleConstraint", "orientConstraint"]

    extInputs = []
    extOutputs = []

    if not isinstance(inRoot,(list,tuple)):
        inRoot = [inRoot]

    allChildren = []
    for root in inRoot:
        allChildren.extend(root.getChildren(allDescendents=True, type="transform"))
    allChildren.extend(inRoot)

    for child in allChildren:
        if child.type() in CONSTRAINT_TYPES:
            continue

        cons = child.listHistory(future=True)
        for con in cons:
            if con.type() in CONSTRAINT_TYPES:
                continue

            if con.type() == "transform" and con in allChildren:
                continue

            extInputs.append(con)

        cons = child.listHistory()
        for con in cons:
            if con[0].type() in CONSTRAINT_TYPES or con[1].type() in CONSTRAINT_TYPES:
                continue

            if con[0].type() == "transform" and con[0].node() in allChildren:
                continue

            extOutputs.append(con)

    return (extInputs, extOutputs)



setActivator("Left_Hand_ParamHolder_Main_Ctrl.IkFk")



cns = tkc.getExternalConstraints(pc.selected()[0])



uts = getUselessTransforms("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")
print len(uts),uts

print deleteUselessTransforms("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")
"""