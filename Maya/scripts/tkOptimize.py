import os
import re

import OscarZmqMayaString as ozms

import pymel.core as pc
import tkMayaCore as tkc
import tkRig
import tkDevHelpers as tkdev
import tkNodeling as tkn
import tkTagTool as tkt

"""
#IN ORDER

#Diagnose
tko.diagnose()

#Evaluate
tko.evaluate()



#ConvertExpressions
tko.convertExpressions()

#LOD generations should come here (setDeactivator)
#tko.setDeactivator("Global_SRT.Body_LOD", inRootsKeep=all_body, inName="body_low", inDeactivateValue=1, inPolyReduceMin=50, inPolyReduceMax=250)

#ConvertConstraints
tko.replaceConstraints()

#PTAttributes
tko.deletePTAttributes("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")

#UselessTransforms
tko.deleteUselessTransforms("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")

#UnusedNodes++
tkc.deleteUnusedNodes()
"""

def refreshFrame():
    pc.currentTime(pc.currentTime())

#Rigs LOD manipulation
def setLOD(inValue, inNamespaces=None, inAttrs=["Body_LOD", "Facial_LOD", "LOD"], inSolo=False, inUseSelection=True, inInvalidate=True, inReverse=False):
    #print "setLOD(",inValue,",", inNamespaces,",",inAttrs,",", inSolo,",", inUseSelection,",", inInvalidate,",", inReverse,",)"

    changed = False

    namespaces = ["*:", ""]

    if inNamespaces is None:
        if inUseSelection:
            sel = pc.selected()
            if len(sel) > 0:
                namespaces = []
                for sel in pc.selected():
                    ns = sel.namespace()
                    if ns in namespaces:
                        continue

                    namespaces.append(ns)
    else:
        if not inReverse:
            namespaces = inNamespaces

    #print "namespaces",namespaces

    attrsPatterns = []
    #Collect attributes
    for ns in namespaces:
        attrsPatterns.extend(["{0}*.{1}".format(ns, attr) for attr in inAttrs])

    #print "attrsPatterns",attrsPatterns

    attrs = pc.ls(attrsPatterns)

    for attr in attrs:
        if inReverse and attr.namespace() in inNamespaces:
            continue

        thisValue = inValue
        value = attr.get()
        minimum = attr.getMin() or 0
        maximum = attr.getMax() or 2

        if inReverse:
            if abs(thisValue-minimum) > abs(thisValue-maximum):#Closer to maximum
                thisValue = minimum
            else:
                thisValue = maximum

        #enumValues = pc.attributeQuery(attr, node=outfitsProperty, listEnum=True)[0].split(":")

        attrValue = min(max(thisValue,minimum), maximum)
        if attrValue != attr.get():
            attr.set(attrValue)
            changed = True

    if namespaces != ["*:", ""] and inSolo:
        if setLOD(inValue, inNamespaces=namespaces, inAttrs=inAttrs, inInvalidate=False, inReverse=True):
            changed = True

    if changed and inInvalidate:
        pc.evaluationManager(invalidate=True)
        pc.evalDeferred(refreshFrame)

    return changed

#BENCHMARKING
#---------------------------------------------------
def diagnose(inProps=["Objects",
        "Transforms",
        "Locators",
        "Joints",
        "Curves",
        "Meshes",
        "Meshes Points",
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
        "follicles",
        "Utilities",
        "Deformers",
        "skinClusters",
        "blendshapes",
        "clusters",
        "lattices",
        "wraps",
        "shrinkWraps"]):
    
    values = tkdev.Tester("SomeRig", "SomePath").getValues(*inProps)

    for i in range(len(inProps)):
        print "{0} : {1}".format(inProps[i],values[i])

def evaluate(inFrames=100):
    fps = 100.0 / tkc.benchIt(tkdev.evaluate, inFrames)[0]
    print "{0} fps, {1} ms".format(fps, 1000.0/fps)

    return fps

def importMultiple(inPath, inNumber=100):
    pc.openFile(inPath, force=True)
    
    for i in range(inNumber-1):
        pc.importFile(inPath, force=True)

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
        cons.extend(getAllConnections(inCns.nodeState))
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
    "offsetZ":"inputScaleZ",

    "nodeState":"nodeState"
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
            inputName = linkInput.split(".")[-1]
            newInput = CONS_LINKS.get(inputName)
            if not newInput is None:
                linkOutput >> createdNodes[0].attr(newInput) if not "nodeState" in inputName else createdNodes[-1].attr(newInput)
            else:
                pc.warning("Can't reconnect {0} >> {1}".format(linkOutput, linkInput))

        for linkInput, linkOutput in sclCons:
            newInput = CONS_LINKS.get(linkInput.split(".")[-1])
            if not newInput is None:
                if not "nodeState" in linkOutput.name():
                    linkOutput >> createdNodes[0].attr(newInput)
            else:
                pc.warning("Can't reconnect {0} >> {1}".format(linkOutput, linkInput))

def replaceConstraints(inDebugFolder=None, inVerbose=False):
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
    
    if inVerbose:
        print "Constraints", len(parentCons)
    
    replaced = []

    for parentCon in parentCons:
        conName = parentCon.name().replace("|", "(")

        owner = tkc.getConstraintOwner(parentCon)[0]
        targets = tkc.getConstraintTargets(parentCon)

        if len(targets) == 0:
            if inVerbose:
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
                if inVerbose:
                    print "Cannot replace (owner have scale pivots): ",parentCon,"on",owner
                continue

            targetPivots=False
            for target in targets:
                if not tkc.listsBarelyEquals(list(target.rp.get()), [0.0,0.0,0.0]):
                    if inVerbose:
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

    if inVerbose:
        print "replaced",len(replaced),replaced

    return replaced

#EXPRESSION REPLACEMENT
#---------------------------------------------------
#tkn.convertExpression(inExpr)
def convertExpressions(inVerbose=False):
    invalidItems = ["sin(",
                    "cos(",
                    "noise("
                    ]

    replaced = []

    exprs = pc.ls(type="expression")
    if inVerbose:
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
        elif inVerbose:
            print "Cannot replace (invalid item): ",expr,exprString

    if inVerbose:
        print "convertExpressions replaced",len(replaced),replaced

    return replaced

def getUselessTransforms(inExceptPattern=None, inVerbose=False):
    uselessTransforms = []
    
    ts = pc.ls( exactType=["transform", "joint"])
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        #Children
        if len(t.getChildren()) > 0:
            continue

        #Connections
        if len(t.listConnections(source=False, destination=True)) > 0:
            if inVerbose:
                print t,t.listConnections(source=False, destination=True)
            continue
    
        uselessTransforms.append(t)
        
    return uselessTransforms

def deleteUselessTransforms(inExceptPattern=None, inVerbose=False):
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
            if inVerbose:
                print "deleteUselessTransforms",len(uts),uts
            return deleted

    if inVerbose:
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

def deletePTAttributes(inExceptPattern=None, inExceptParamsPattern=None, inDropStaticValues=True, inVerbose=False):
    exceptParams=["ift","smt","dr"]

    uselessAttributes = []
    
    ts = pc.ls(exactType=["transform"])
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        uds = tkc.getParameters(t)
        for ud in uds:

            if ud in exceptParams or (not inExceptParamsPattern is None and re.match(inExceptParamsPattern, ud)):
                continue

            attr = t.attr(ud)

            #Connections
            cons = attr.listConnections(source=True, destination=False, plugs=True)
            otherCons = attr.listConnections(source=False, destination=True, plugs=True)

            haveExpr = False
            for con in cons + otherCons:
                if con.node().type() == "expression":
                    #print "Attribute '{0}' still have expression ('{1}') !".format(attr, con.node())
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

    if inVerbose:
        print "deletePTAttributes",len(uselessAttributes),uselessAttributes

    return uselessAttributes

def deactivate(inObj, inCond=None, inCondVis=None, inExceptTypes=None, inKeepVisible=False, inKeepActive=None, inRecur=0):
    #print " " * inRecur + "DEACTIVATE",inObj,inCond,inCondVis,inExceptTypes
    if not inKeepActive is None and inObj.name() in inKeepActive:
        return

    if isinstance(inObj, pc.nodetypes.Transform):
        if not inKeepVisible:
            if inCondVis is None:
                inObj.v.set(0)
            else:
                tkn.conditionAnd(inObj.v, inCondVis)
        
        for shape in inObj.getShapes():
            deactivate(shape, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inKeepActive=inKeepActive, inRecur=inRecur+1)

    elif isinstance(inObj, pc.nodetypes.Mesh):
        if not inKeepVisible:
            if inCondVis is None:
                inObj.v.set(0)
            else:
                tkn.conditionAnd(inObj.v, inCondVis)

        defs = pc.listHistory(inObj, gl=True, pdo=True, lf=True, f=False, il=2)
        if defs != None:
            for deform in defs:
                if pc.attributeQuery("envelope" , node=deform, exists=True):
                    if inExceptTypes is None or not deform.type() in inExceptTypes:
                        deactivate(deform, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inKeepActive=inKeepActive, inRecur=inRecur+1)
                        deactivate(deform, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inKeepActive=inKeepActive, inRecur=inRecur+1)
    # else:# else:
    #    pc.warning("Don't know how to deactivate {0} of type {1}".format(inObj, type(inObj)))

    if inCond is None:
        inObj.nodeState.set(2)
    else:
        tkn.conditionAnd(inObj.nodeState, inCond)

def setDeactivator(inAttr, inRootsKeep=None, inRootsRemove=None, inDeactivateValue=1, inName=None, inReplaceDeformers=None, inIgnoreTags=["hd"], inKeepOrphans=None, inForceProxy=None, inKeepActive=None, inPolyReduceMin=0, inPolyReduceMax=0, inHide=True):
    if inRootsKeep is None and inRootsRemove is None:
        raise ValueError("inRootsKeep and inRootsRemove can't both be None !")

    inKeepOrphans = inKeepOrphans or []

    inRoots = inRootsKeep or inRootsRemove
    nodesRootToRemove, nodesRootToKeep, allGivenNodes = [None,None,None]

    if not inRootsKeep is None:
        nodesRootToRemove, nodesRootToKeep, allGivenNodes = tkRig.OscarSplitNodes(inRootsKeep)
    else:
        nodesRootToKeep, nodesRootToRemove, allGivenNodes = tkRig.OscarSplitNodes(inRootsRemove)

    print "nodesRootToRemove",len(nodesRootToRemove),nodesRootToRemove
    print "nodesRootToKeep",len(nodesRootToKeep),nodesRootToKeep

    if len(allGivenNodes) > 0:
        pc.warning("{0} nodesNotFound ({1})".format(len(allGivenNodes),allGivenNodes))

    inAttr = tkc.getNode(inAttr)

    cond = tkn.condition(inAttr, inDeactivateValue, "==", 2.0, 0.0)
    condVis = tkn.condition(inAttr, inDeactivateValue, "!=", 1.0, 0.0)

    inverse = tkn.reverse(cond)
    inverseVis = tkn.reverse(condVis)

    #if inHide:
    for root in nodesRootToRemove:
        tkn.conditionAnd(root.v, condVis)

    cns, cnsAll = tkc.getExternalConstraints(nodesRootToRemove, inSource=True, inDestination=True, inReturnAll=True, inProgress=True)

    externalOwners = []
    print " Constraints :",len(cns),cns

    for cn in cnsAll:
        #DEACTTIVATE CONSTRAINT
        deactivate(cn, cond, condVis, inKeepActive=inKeepActive)

    if len(externalOwners) > 0:
        pc.warning("External Owners : {0} {1}".format(len(externalOwners), externalOwners))

    origGeos = [m.getParent() for m in pc.ls(type="mesh") if len(m.getParent().v.listConnections()) > 0 or m.getParent().v.get()]

    deformersToReplace = {}
    #Find deformers to replace

    removedDeformers = []
    skinClusters = []
    for nodeRoot in nodesRootToRemove:
        deformers = nodeRoot.getChildren(allDescendents=True, type='joint')
        removedDeformers.extend(deformers)

        for deformer in deformers:
            #deformersToReplace[deformer.name()] = deformer.getTranslation(space="world")
            skinClusters.extend(deformer.listConnections(type="skinCluster"))

    skinClusters = list(set(skinClusters))
    geos = [skin.getGeometry()[0] for skin in skinClusters]

    deformersRemaining = []

    #Find remaining deformers 
    for nodeRoot in nodesRootToKeep:
        deformers = nodeRoot.getChildren(allDescendents=True, type='joint')
        deformersRemaining.extend([n.name() for n in deformers])

    replacingDeformers = []

    if not inReplaceDeformers is None:
        for replaceDeformer in inReplaceDeformers:
            print " deformersRemaining","replaceDeformer",replaceDeformer, replaceDeformer,"deformersRemaining",len(deformersRemaining),deformersRemaining
            if pc.objExists(replaceDeformer) and replaceDeformer in deformersRemaining:
                replacingDeformers.append(pc.PyNode(replaceDeformer))

    print " deformersRemaining",len(deformersRemaining),deformersRemaining

    print " replacingDeformers",len(replacingDeformers),replacingDeformers

    #Find and add "siblings" geo (geo deformed by an existing one)
    siblingsGeos = []
    for geo in geos:
        histos = geo.listHistory(future=True, type="mesh")
        for histo in histos:
            if not histo in siblingsGeos and not histo in geos:
                siblingsGeos.append(histo)
                print " siblingsGeo OK :",geo,"=>",histo

    geos.extend(siblingsGeos)

    #Find and hide "forcedProxies"
    if not inForceProxy is None:
        for forcedProxy in inForceProxy:
            if pc.objExists(forcedProxy):
                node = tkc.getNode(forcedProxy)
                if node.type() == "transform":
                    node = node.getShape()
                if not node in geos:
                    geos.append(node)

    proxies = []

    for geo in geos:
        print "-",geo,geo.type()
        """
        if not geo.type() == "mesh":
            continue
        """
        if not isinstance(geo, pc.nodetypes.DagNode):
            deactivate(geo, cond, condVis)
            continue

        transform = geo.getParent()
        underGeo = None
        isOrphanGeo = True
        keptTopInfs = []

        geoSkin = tkc.getSkinCluster(geo)
        if not geoSkin is None:
            keptTopInfs = geoSkin.influenceObjects()

            remainingTopInfs = [inf for inf in keptTopInfs if inf.name() in deformersRemaining]

            otherDeformers = [d for d in geo.listHistory() if d.type() in ["blendShape", "wrap"]]


            #'Live' blendshape targets
            #------------------------------------
            blendShapes = geo.listHistory(type="blendShape")
            for blendShape in blendShapes:
                if pc.objExists(blendShape):
                    cons = pc.listConnections(blendShape, source=True, destination=False, type="mesh")
                    for con in cons:
                        skin = tkc.getSkinCluster(con)
                        if not skin is None:
                            BSinfs = skin.influenceObjects()
                            #Determine if most of the influences are kept or dropped
                            keptInfs = [inf for inf in BSinfs if inf.name() in deformersRemaining]

                            if len(keptInfs) > len(remainingTopInfs):
                                underGeo = con
                                break

            isOrphanGeo = len(remainingTopInfs) == 0 and len(replacingDeformers) == 0 and underGeo is None 

        if isOrphanGeo and transform.stripNamespace() in inKeepOrphans:
            isOrphanGeo  = False

        print " isOrphanGeo",isOrphanGeo
        print " underGeo",underGeo
        print " inIgnoreTags",len(inIgnoreTags),inIgnoreTags
        print " len(tkt.getTags([geo], inIgnoreTags))",len(tkt.getTags([transform], inIgnoreTags))
        print " visible",tkc.isVisibleAfterAll(geo)
        isSafe = False

        if inIgnoreTags is None or len(inIgnoreTags) == 0 or len(tkt.getTags([transform], inIgnoreTags)) == 0:
            if not isOrphanGeo and tkc.isVisibleAfterAll(geo):
                infsToRemove = []

                for inf in keptTopInfs:
                    if inf in removedDeformers:
                        infsToRemove.append(inf)

                #print " infs",len(keptTopInfs),keptTopInfs
                #print " infsToRemove",len(infsToRemove),infsToRemove

                if geo.type() == "mesh":
                    #Create geometry proxy
                    #------------------------
                    dupe = tkc.getNode(tkc.duplicateAndClean(transform.name(), inTargetName=("$REF_dupe" if inName is None else "$REF_" + inName), inMuteDeformers=False, inResetDisplayType=False))
                    
                    if inPolyReduceMin < inPolyReduceMax:
                        tkc.polyReduceComplexity(dupe, inPolyReduceMin, inPolyReduceMax)

                    proxies.append(dupe)

                    infsLeft = len(keptTopInfs) - len(infsToRemove)

                    newSkin = None
                    if not underGeo is None:
                        print " Proxy",dupe,"created with gator under",underGeo,"approach" 
                        tkc.gator([dupe], underGeo)
                        newSkin = tkc.getSkinCluster(dupe)
                        dupeInfs = newSkin.influenceObjects()

                        infsToRemove = []

                        for inf in dupeInfs:
                            if inf in removedDeformers:
                                infsToRemove.append(inf)

                        pc.skinCluster(newSkin,e=True,ri=infsToRemove)
                    elif infsLeft == 0:
                        if len(replacingDeformers) > 0:
                            print " Proxy",dupe,"created with replacingDeformers approach",dupe,replacingDeformers
                            newSkin = pc.skinCluster(dupe,replacingDeformers, name=dupe.name() + "_skinCluster", toSelectedBones=True)
                        elif len(deformersRemaining) > 0:
                            print " Proxy",dupe,"created with deformersRemaining approach" ,dupe,deformersRemaining
                            newSkin = pc.skinCluster(dupe,deformersRemaining, name=dupe.name() + "_skinCluster", toSelectedBones=True)
                    else:
                        print " Proxy",dupe,"created with gator",geo,"approach" 
                        tkc.gator([dupe], geo)
                        newSkin = tkc.getSkinCluster(dupe)
                        pc.skinCluster(newSkin,e=True,ri=infsToRemove)

                    tkRig.hammerCenter(dupe)
                    pc.skinPercent(newSkin, dupe, pruneWeights=0.005 )
                    removedInfs = tkc.removeUnusedInfs(newSkin)

                    deactivate(dupe, inverse, inverseVis, inKeepVisible=not inHide, inKeepActive=inKeepActive)
                    #------------------------

        #Connect "old" geometry
        #------------------------
        deactivate(geo, cond, condVis, inKeepVisible=not inHide or not tkc.isVisibleAfterAll(geo), inKeepActive=inKeepActive)

        if underGeo is not None:
            #DEACTTIVATE GEOMETRY
            deactivate(underGeo, cond, condVis, inKeepVisible=not inHide or not tkc.isVisibleAfterAll(underGeo), inKeepActive=inKeepActive)

    print "geos",len(geos),geos
    print "proxies",len(proxies),proxies

def storeShapeConversions(inShapeConversions, inShapeAliases=None, inName="TK_SHAPE_CONVERSIONS"):
    if inShapeAliases is None:
        inShapeAliases = {}

    root = pc.group(empty=True, world=True, name=inName)
    root.v.set(False)

    for object, shapes in inShapeConversions.iteritems():

        origName = object
        if not pc.objExists(object):
            aliases = inShapeAliases.get(object, [])
            object = None
            for alias in aliases:
                if pc.objExists(alias):
                    object = alias
                    break

        if object is None:
            pc.warning("Can't find object '{0}' (and None of its aliases : {1}) !".format(origName, inShapeAliases.get(origName, [])))
            continue

        objectRoot = pc.group(empty=True, parent=root, name="{0}_{1}".format(object, inName))
        for poseName, poseData in shapes.iteritems():
            channel, value = poseData
            channelNode = pc.PyNode(channel)
            channelNiceName = channel.replace(".", "_DOT_")
            
            oldValue = pc.getAttr(channel)
            
            pc.setAttr(channel, value)
            
            dupe = pc.PyNode(tkc.duplicateAndClean(object, inMuteDeformers=False, inResetDisplayType=False))
            dupe.rename("{0}_{1}".format(object, poseName))
            tkc.addParameter(dupe, channelNiceName, default=value, containerName=inName)
            
            objectRoot.addChild(dupe)
            
            pc.setAttr(channel, oldValue)

def applyShapeConversions(inDelete=True, inName="TK_SHAPE_CONVERSIONS", inCustomMeshSuffix=None):
    if pc.objExists(inName):
        root = pc.PyNode(inName)

        for child in root.getChildren():
            object = child.name()[:-len(inName)-1]
            objectNodeName = object if inCustomMeshSuffix is None else object + inCustomMeshSuffix

            print "applyShapeConversions searching for :",object,objectNodeName

            if not pc.objExists(objectNodeName):
                pc.warning("Can't find object '{0}'".format(objectNodeName))
                continue

            objectNode = pc.PyNode(objectNodeName)
            
            bs = child.getChildren()

            bsNode = None

            #Search if a blendShape node already exists
            bsNodes = objectNode.listHistory(type="blendShape")
            if len(bsNodes) > 0:
                bsNode = bsNodes[0]

                #Add targets
                #First available index
                indices = bsNode.weightIndexList()
                index = indices[-1] + 1 if len(indices) > 0 else 0
                for target in bs:
                    pc.blendShape(bsNode, edit=True, t=(objectNodeName, index, target, 1.0))
                    index += 1
            else:
                #Create new blendShape node
                bsArgs = bs + [objectNode]
                print "bsArgs",bsArgs
                bsNode = pc.blendShape(bsArgs, name="{0}_BS".format(objectNodeName))[0]
                tkc.reorderDeformers(objectNodeName)
            
            for bsObj in bs:
                channel = tkc.getParameters(bsObj, containerName=inName)[0]
                controller, attribute = channel.split("_DOT_")
                value = tkc.getProperty(bsObj, inName).attr(channel).get()
                minValue = min(0, value)
                maxValue = max(0, value)
                
                rslt = tkn.clamp(pc.PyNode(controller).attr(attribute), minValue, maxValue)
                
                if abs(value - 1.0) > 0.001:
                    rslt = tkn.mul(rslt, 1/value)

                rslt >> bsNode.attr(bsObj.name())

        if inDelete:
            pc.delete(inName)