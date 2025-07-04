import os
import re

import OscarZmqMayaString as ozms

import pymel.core as pc
import tkMayaCore as tkc
import tkRig
import tkDevHelpers as tkdev
import tkNodeling as tkn
import tkTagTool as tkt
import tkBlendShapes as tkb
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
        print ("{0} : {1}".format(inProps[i],values[i]))

def evaluate(inFrames=100):
    fps = 100.0 / tkc.benchIt(tkdev.evaluate, inFrames)[0]
    print ("{0} fps, {1} ms".format(fps, 1000.0/fps))

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

    #As we may change local transformations (world ones stayiong the same), and maya constraints being dependant on locals,
    #(because of contraints being separated parent + scale) we'll store output contraints on the objects and reapply them afterwards
    storedCons = [c for c in tkc.getConstraintsUsing(inTarget) if c.type() in ["parentConstraint", "scaleConstraint"]]
    storedConsInfo = [(c.type(), tkc.getConstraintOwner(c)[0].name(), c.name()) for c in storedCons]
    pc.delete(storedCons)

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

    #Reapply old output contraints
    for storedCon in storedConsInfo:
        cnsType, cnsTarget, cnsName = storedCon

        print ("inTarget",inTarget)
        print ("cnsTarget",cnsTarget)

        try:
            if cnsType == "parentConstraint":
                newCns = pc.parentConstraint(inTarget, cnsTarget, name=cnsName.split("|")[-1], maintainOffset=True)
            else:
                newCns = pc.scaleConstraint(inTarget, cnsTarget, name=cnsName.split("|")[-1], maintainOffset=True)
        except:
            pass

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
    cons = [(linkInput.name(), linkOutput) for linkInput, linkOutput in cons]

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
                sclCons = [(linkInput.name(), linkOutput) for linkInput, linkOutput in sclCons]

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

def replaceConstraints(inExclude=None, inDebugFolder=None, inVerbose=False):
    inExclude = inExclude or []
    inExclude = tkc.getNodes(inExclude)

    debugCounter = 0

    if not inDebugFolder is None:
        if not os.path.isdir(inDebugFolder):
            os.makedirs(inDebugFolder)
        else:
            tkc.emptyDirectory(inDebugFolder)
        print ("DEBUG MODE ACTIVATED ({})".format(inDebugFolder))
        tkc.capture(os.path.join(inDebugFolder, "{0:04d}_ORIGINAL.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
        debugCounter = debugCounter + 1

    parentCons = [c.name() for c in pc.ls(type=["parentConstraint","pointConstraint"])]
    
    if inVerbose:
        print ("Constraints", len(parentCons))
        print (parentCons)
    
    replaced = []

    for parentCon in parentCons:
        try:
            parentCon = pc.PyNode(parentCon)
        except:
            continue

        conName = parentCon.name().replace("|", "(")

        owners = tkc.getConstraintOwner(parentCon)
        if len(owners) == 0:
            pc.warning("Disconected constraint : " + parentCon.name())
            #pc.delete(parentCon)
            continue

        owner = tkc.getConstraintOwner(parentCon)[0]
        targets = tkc.getConstraintTargets(parentCon)

        if len(targets) == 0:
            if inVerbose:
                print ("Cannot replace (NO TARGETS): ",parentCon,"on",owner)
            continue

        skip = False

        for target in targets:
            #print "target",target,inExclude
            if target in inExclude:
                print ("Constraint '{0}'' is on an excluded object ({1}), skip...".format(parentCon, target))
                skip = True
                break

        if skip:
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
                    print ("Cannot replace (owner have scale pivots): ",parentCon,"on",owner)
                continue

            if not tkc.listsBarelyEquals(list(owner.s.get()), [1.0,1.0,1.0]):
                if inVerbose:
                    print ("Cannot replace (owner {0} have non-uniform scaling): ".format(owner),parentCon,"on",owner)
                continue

            targetPivots=False
            targetNonUniformScale=False
            for target in targets:
                if not tkc.listsBarelyEquals(list(target.rp.get()), [0.0,0.0,0.0]):
                    if inVerbose:
                        print ("Cannot replace (target {0} have scale pivots): ".format(target),parentCon,"on",owner)
                    targetPivots=True

                if not tkc.listsBarelyEquals(list(target.s.get()), [1.0,1.0,1.0]):
                    if inVerbose:
                        print ("Cannot replace (target {0} have non-uniform scaling): ".format(target),parentCon,"on",owner)
                    targetNonUniformScale=True

            if targetPivots or targetNonUniformScale:
                continue

            #Check if we have contraints using replaced object that are not replaceable
            storedCons = [c for c in tkc.getConstraintsUsing(owner) if c.type() in ["parentConstraint", "scaleConstraint"]]
            incompatible = False
            for storedCon in storedCons:
                if len([c for c in storedCon.listConnections() if not isinstance(c, pc.nodetypes.Transform)]) > 0:
                    incompatible = True
                    print ("Cannot replace (constraints on owner with connections): ",owner,storedCon)
                    break

            if incompatible:
                continue

            replaced.append(owner.name())
            replaceConstraint(parentCon, owner, targets[0])

        if not inDebugFolder is None:
            tkc.capture(os.path.join(inDebugFolder, "{0:04d}_replaceCns_{1}.jpg".format(debugCounter, conName)), start=1, end=1, width=1280, height=720)
            debugCounter = debugCounter + 1

    if inVerbose:
        print ("replaced",len(replaced),replaced)

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
        print ("exprs", len(exprs))
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
            print ("Cannot replace (invalid item): ",expr,exprString)

    if inVerbose:
        print ("convertExpressions replaced",len(replaced),replaced)

    return replaced

CONSTRAINT_TYPES = ["parentConstraint",
                    "aimConstraint",
                    "orientConstraint",
                    "scaleConstraint",
                    "pointConstraint",
                    "poleVectorConstraint"]

def isUselessTransform(inTransform,  inVerbose=False):
    #Children
    children = inTransform.getChildren()
    constraints = [tc for tc in children if tc.type() in CONSTRAINT_TYPES]
    for c in constraints:
        children.remove(c)
    lenChildren = len(children)

    if lenChildren > 1:
        return False

    #If child starts with the same name, have no connections and no children, consider it can go with its parent
    if ( lenChildren == 1 and (
            not children[0].name().startswith(inTransform.name()) or
            len(children[0].getChildren()) > 0 or
            len(children[0].listConnections(source=False, destination=True)) > 0
                )
        ):
        return False

    #Connections
    if len([c for c in inTransform.listConnections(source=False, destination=True) if not c in constraints]) > 0:
        if inVerbose:
            print (inTransform,[c for c in inTransform.listConnections(source=False, destination=True) if not c in constraints])
        return False

    return True

def getUselessTransforms(inExceptPattern=None, inVerbose=False,
                        inExceptTypes=["ikHandle"],
                        inExceptShapes=["camera"]):
    uselessTransforms = []
    
    ts = pc.ls(transforms=True)

    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        #Type
        if not inExceptTypes is None and len(inExceptTypes) > 0:
            if t.type() in inExceptTypes:
                continue

        #Shape
        if not inExceptShapes is None and len(inExceptShapes) > 0:
            shape = t.getShape()
            if not shape is None and shape.type() in inExceptShapes:
                continue

        if isUselessTransform(t, inVerbose=inVerbose):
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
                print ("deleteUselessTransforms",len(uts),uts)
            return deleted

        curIter += 1

    if inVerbose:
        print ("deleteUselessTransforms",len(deleted),deleted)

    pc.warning("delete useless trasforms : Max iterations reached ({0})".format(MAXITER))
    return deleted

def deletePTTransforms(inExceptPattern=None):
    uselessTransforms = []
    
    ts = pc.ls(exactType=["transform"])
    
    print (len(ts))
    
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
                print ("PTTransforms : Other connections :",t,list(set(t.listConnections())),list(set(cons + otherCons)))
                continue

            if len(getConstraintConnections(inCns)) > 0:
                print ("PTTransforms : Input connections :",getConstraintConnections(inCns))
                continue

            outputCons = False
            for otherCon in otherCons:
                if len(getConstraintConnections(otherCon)) > 0:
                    print ("PTTransforms : Output connections :",getConstraintConnections(otherCon))
                    outputCons=True
                    break

            if outputCons:
                continue

            uselessTransforms.append(t.name())

    print ("deletePTTransforms",len(uselessTransforms),uselessTransforms)
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

            try:
                attr = t.attr(ud)
            except:
                continue

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
        print ("deletePTAttributes",len(uselessAttributes),uselessAttributes)

    return uselessAttributes

def deactivate(inObj, inCond=None, inCondVis=None, inExceptTypes=None, inKeepVisible=False, inKeepActive=None, inRecur=0, inDeactivated=None):
    #print " " * inRecur + "DEACTIVATE",inObj,inCond,inCondVis,inExceptTypes
    if not inKeepActive is None and inObj.name() in inKeepActive:
        return

    inDeactivated = inDeactivated if not inDeactivated is None else []

    if isinstance(inObj, pc.nodetypes.Transform):
        if not inKeepVisible:
            if inCondVis is None:
                inObj.v.set(0)
            else:
                if not inObj.v.name() in inDeactivated:
                    tkn.conditionAnd(inObj.v, inCondVis)
                    inDeactivated.append(inObj.v.name())

        for shape in inObj.getShapes():
            deactivate(shape, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inKeepActive=inKeepActive, inRecur=inRecur+1, inDeactivated=inDeactivated)

    elif isinstance(inObj, pc.nodetypes.Mesh):
        if not inKeepVisible:
            if inCondVis is None:
                inObj.v.set(0)
            else:
                if not inObj.v in inDeactivated:
                    tkn.conditionAnd(inObj.v, inCondVis)
                    inDeactivated.append(inObj.v)

        defs = pc.listHistory(inObj, gl=True, pdo=True, lf=True, f=False, il=2)
        if defs != None:
            for deform in defs:
                if pc.attributeQuery("envelope" , node=deform, exists=True):
                    if inExceptTypes is None or not deform.type() in inExceptTypes:
                        deactivate(deform, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inKeepActive=inKeepActive, inRecur=inRecur+1, inDeactivated=inDeactivated)

    if inCond is None:
        inObj.nodeState.set(2)
    else:
        if not inObj.nodeState.name() in inDeactivated:
            tkn.conditionAnd(inObj.nodeState, inCond)
            inDeactivated.append(inObj.nodeState.name())

def setDeactivator(inAttr, inRootsKeep=None, inRootsRemove=None, inDeactivateValue=1, inName=None, inReplaceDeformers=None, inIgnoreTags=["hd"], inKeepOrphans=None, inForceProxy=None, inDropProxy=None, inExistingProxies=None, inKeepActive=None, inPolyReduceMin=0, inPolyReduceMax=0, inHide=True, inNeedProxies=True, **kwargs):
    if inRootsKeep is None and inRootsRemove is None:
        raise ValueError("inRootsKeep and inRootsRemove can't both be None !")

    deactivated = []

    inKeepOrphans = inKeepOrphans or []

    inRoots = inRootsKeep or inRootsRemove
    nodesRootToRemove, nodesRootToKeep, allGivenNodes = [None,None,None]

    if not inRootsKeep is None:
        nodesRootToRemove, nodesRootToKeep, allGivenNodes = tkRig.OscarSplitNodes(inRootsKeep)
    else:
        nodesRootToKeep, nodesRootToRemove, allGivenNodes = tkRig.OscarSplitNodes(inRootsRemove)

    print ("nodesRootToRemove",len(nodesRootToRemove),nodesRootToRemove)
    print ("nodesRootToKeep",len(nodesRootToKeep),nodesRootToKeep)

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
    print (" Constraints :",len(cns),cns)

    for cn in cnsAll:
        #DEACTTIVATE CONSTRAINT
        deactivate(cn, cond, condVis, inKeepActive=inKeepActive, inDeactivated=deactivated)

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
    geos = []
    for skin in skinClusters:
        skinGeos = skin.getGeometry()
        if len(skinGeos) > 0:
            geos.append(skinGeos[0])
        else:
            pc.warning("SkinCluster '{0}' is not bound to a geometry !".format(skin))

    deformersRemaining = []

    #Find remaining deformers 
    for nodeRoot in nodesRootToKeep:
        deformers = nodeRoot.getChildren(allDescendents=True, type='joint')
        deformersRemaining.extend([n.name() for n in deformers])

    replacingDeformers = []

    if not inReplaceDeformers is None:
        for replaceDeformer in inReplaceDeformers:
            print (" deformersRemaining","replaceDeformer",replaceDeformer, replaceDeformer,"deformersRemaining",len(deformersRemaining),deformersRemaining)
            replaceDeformerList = pc.ls(["*:"+replaceDeformer, replaceDeformer])

            if len(replaceDeformerList) > 0 and replaceDeformerList[0].name() in deformersRemaining:
                replacingDeformers.append(pc.PyNode(replaceDeformerList[0]))

    print (" deformersRemaining",len(deformersRemaining),deformersRemaining)

    print (" replacingDeformers",len(replacingDeformers),replacingDeformers)

    #Find and add "siblings" geo (geo deformed by an existing one)
    siblingsGeos = []
    for geo in geos:
        histos = geo.listHistory(future=True, type="mesh")
        for histo in histos:
            if not histo in siblingsGeos and not histo in geos:
                siblingsGeos.append(histo)
                print (" siblingsGeo OK :",geo,"=>",histo)

    geos.extend(siblingsGeos)

    if inNeedProxies:
        #Find and hide "forcedProxies"
        if not inForceProxy is None:
            for forcedProxy in inForceProxy:
                forcedProxyList = pc.ls(["*:"+forcedProxy, forcedProxy])
                if len(forcedProxyList) > 0:
                    node = forcedProxyList[0]
                    if node.type() == "transform":
                        node = node.getShape()
                    if not node in geos:
                        geos.append(node)

        forcedOrphans = []
        #Find and exclude "droppedProxies"
        if not inDropProxy is None:
            for droppedProxy in inDropProxy:
                droppedProxyList = pc.ls(["*:"+droppedProxy, droppedProxy])

                if len(droppedProxyList) > 0:
                    node = droppedProxyList[0]

                    forcedOrphans.append(node)
                    forcedOrphans.extend(node.getShapes())

    proxies = []

    for geo in geos:
        print ("-",geo,geo.type())

        if not isinstance(geo, pc.nodetypes.DagNode):
            deactivate(geo, cond, condVis, inDeactivated=deactivated)
            continue

        underGeo = None

        if inNeedProxies:
            transform = geo.getParent()
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
                print ("blendShape",blendShape)

                if pc.objExists(blendShape):
                    cons = pc.listConnections(blendShape, source=True, destination=False, type="mesh")
                    for con in cons:
                        skin = tkc.getSkinCluster(con)
                        if not skin is None:
                            BSinfs = skin.influenceObjects()
                            #Determine if most of the influences are kept or dropped
                            keptInfs = [inf for inf in BSinfs if inf.name() in deformersRemaining]

                            print ("keptInfs", len(keptInfs),keptInfs)
                            print ("remainingTopInfs", len(remainingTopInfs),remainingTopInfs)                       

                            if len(keptInfs) > len(remainingTopInfs):
                                underGeo = con
                                break

            isOrphanGeo = len(remainingTopInfs) == 0 and len(replacingDeformers) == 0 and underGeo is None 

            if isOrphanGeo:
                if transform.stripNamespace() in inKeepOrphans:
                    isOrphanGeo  = False
            elif geo in forcedOrphans:
                isOrphanGeo  = True

            print (" isOrphanGeo",isOrphanGeo)
            print (" underGeo",underGeo)
            print (" inIgnoreTags",len(inIgnoreTags),inIgnoreTags)
            print (" len(tkt.getTags([geo], inIgnoreTags))",len(tkt.getTags([transform], inIgnoreTags)))
            print (" visible",tkc.isVisibleAfterAll(geo))
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
                        proxy = None

                        shortName = transform.stripNamespace()
                        if shortName in inExistingProxies:
                            existingProxy = inExistingProxies[shortName]

                            existingProxyTransforms = pc.ls(["*:"+existingProxy, existingProxy])
                            if len(existingProxyTransforms) > 0:
                                proxy = existingProxyTransforms[0]

                        if proxy is None:
                            #Create geometry proxy
                            #------------------------
                            proxy = tkc.getNode(tkc.duplicateAndClean(transform.name(), inTargetName=("$REF_dupe" if inName is None else "$REF_" + inName), inMuteDeformers=False, inResetDisplayType=False))
                            
                            #Copy visibility connections
                            tkc.matchConnections(proxy, transform, "visibility", "overrideEnabled", "overrideVisibility", inSource=True, inDestination=False, inShape=True)

                            if inPolyReduceMin < inPolyReduceMax:
                                tkc.polyReduceComplexity(proxy, inPolyReduceMin, inPolyReduceMax)

                            infsLeft = len(keptTopInfs) - len(infsToRemove)

                            newSkin = None
                            if not underGeo is None:
                                print (" Proxy",proxy,"created with gator under",underGeo,"approach" )
                                tkc.gator([proxy], underGeo)
                                newSkin = tkc.getSkinCluster(proxy)
                                dupeInfs = newSkin.influenceObjects()

                                infsToRemove = []

                                for inf in dupeInfs:
                                    if inf in removedDeformers:
                                        infsToRemove.append(inf)

                                if len(infsToRemove) > 0:
                                    print ("infsToRemove", len(infsToRemove),infsToRemove)
                                pc.skinCluster(newSkin,e=True,ri=infsToRemove)
                            elif infsLeft == 0:
                                if len(replacingDeformers) > 0:
                                    print (" Proxy",proxy,"created with replacingDeformers approach",proxy,replacingDeformers)
                                    newSkin = pc.skinCluster(proxy,replacingDeformers, name=proxy.name() + "_skinCluster", toSelectedBones=True)
                                elif len(deformersRemaining) > 0:
                                    print (" Proxy",proxy,"created with deformersRemaining approach" ,proxy,deformersRemaining)
                                    newSkin = pc.skinCluster(proxy,deformersRemaining, name=proxy.name() + "_skinCluster", toSelectedBones=True)
                            else:
                                print (" Proxy",proxy,"created with gator",geo,"approach" )
                                tkc.gator([proxy], geo)
                                newSkin = tkc.getSkinCluster(proxy)
                                pc.skinCluster(newSkin,e=True,ri=infsToRemove)

                            tkRig.hammerCenter(proxy, inThreshold=kwargs.get("inThreshold", 10.0))
                            pc.skinPercent(newSkin, proxy, pruneWeights=0.005 )
                            removedInfs = tkc.removeUnusedInfs(newSkin)

                        proxies.append(proxy)
                        deactivate(proxy, inverse, inverseVis, inKeepVisible=not inHide, inKeepActive=inKeepActive, inDeactivated=deactivated)
                        #------------------------

        #Connect "old" geometry
        #------------------------
        deactivate(geo, cond, condVis, inKeepVisible=not inHide or not tkc.isVisibleAfterAll(geo), inKeepActive=inKeepActive, inDeactivated=deactivated)

        if underGeo is not None:
            #DEACTTIVATE GEOMETRY
            deactivate(underGeo, cond, condVis, inKeepVisible=not inHide or not tkc.isVisibleAfterAll(underGeo), inKeepActive=inKeepActive, inDeactivated=deactivated)

    print ("geos",len(geos),geos)
    print ("proxies",len(proxies),proxies)
    print ("deactivated",len(deactivated),deactivated)

def storeShapeConversions(inShapeConversions, inShapeAliases=None, inName="TK_SHAPE_CONVERSIONS", inDisconnectConflicting=False, inRecut=True, inRecutTreshold=2.0, inUseTopLevel=False):
    if inShapeAliases is None:
        inShapeAliases = {}

    root = pc.group(empty=True, world=True, name=inName)
    root.v.set(False)

    if inRecut:
        for object, shapes in inShapeConversions.items():
            newDict = {}
            orphans = []
            for poseName, poseData in shapes.items():
                if "Right" in poseName:
                    if poseName in orphans:
                        orphans.remove(poseName)
                    else:
                        orphans.append(poseName)

                elif "Left" in poseName and poseName.replace("Left", "Right") in shapes:
                    otherName = poseName.replace("Left", "Right")
                    newDict["TKRECUT_"+poseName] = [poseData, shapes[otherName]]
                    if otherName in orphans:
                        orphans.remove(otherName)
                    else:
                        orphans.append(otherName)
                else:
                    newDict[poseName] = poseData

            for orphan in orphans:
                #print "orphan",orphan
                newDict[orphan] = shapes[orphan]

            inShapeConversions[object] = newDict

    for object, shapes in inShapeConversions.items():

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

        sourceObject = object
        if inUseTopLevel:
            objectNode = pc.PyNode(object)
            #If we want to use 'top level', search a mesh using 'object' as live blendShape target
            outBss = objectNode.getShape().listConnections(source=False, destination=True, type="blendShape")
            if len(outBss) > 0:
                outBs = outBss[0]
                topLevelMeshes = outBs.listHistory(future=True, type="mesh")
                if len(topLevelMeshes) > 0:
                    sourceObject = topLevelMeshes[0].getParent().name()

        #Here we may have existing blendShape targets in conflict that will be disconnected
        toDisconnects = []
        #Get blendShape targets attributes at 0 that are connected to something
        bsAttrs = []
        if inDisconnectConflicting:
            for bs in pc.listHistory(object, type="blendShape"):
                arrayAttrs = pc.listAttr("{0}.weight".format(bs), multi=True)

                for arrayAttr in arrayAttrs:
                    bsAttr = bs.attr(arrayAttr)
                    if bsAttr.get() < 0.001 and len(bsAttr.listConnections()) > 0:
                        bsAttrs.append(bsAttr)

        objectRoot = pc.group(empty=True, parent=root, name="{0}_{1}".format(object, inName))
        for poseName, poseData in shapes.items():

            poseNames = [poseName]
            poseDatas = [poseData]

            isRecut = False
            refObj = None
            if poseName.startswith("TKRECUT_"):
                isRecut = True
                poseNames = [poseName[8:], poseName[8:].replace("Left", "Right")]
                poseDatas = [poseData[0], poseData[1]]
                refObj = tkc.duplicateAndClean(sourceObject, inMuteDeformers=True, inResetDisplayType=False)

            i = 0
            oldValues = {}
            channelNiceNames = {}
            outputValues = {}
            channels = {}
            values = {}
            for poseName in poseNames:
                poseData = poseDatas[i]
                i += 1

                channel = None
                value = None
                outputChannel = None
                outputValue = None

                #print "poseData",len(poseData),poseData

                if len(poseData) == 2:
                    channel, value = poseData
                    outputChannel = channel
                    outputValue = value
                else:
                    channel, value, outputChannel, outputValue = poseData

                if not pc.objExists(channel):
                    pc.warning("Can't find channel {0}".format(channel))
                    continue

                channelNode = pc.PyNode(channel)
                channelNiceName = outputChannel.replace(".", "_DOT_")

                channelNiceNames[poseName] = channelNiceName
                outputValues[poseName] = outputValue
                channels[poseName] = channel
                values[poseName] = value
                #print "channelNiceName",channelNiceName
                #print "outputValue",outputValue

                oldValue = pc.getAttr(channel)
                if not channel in oldValues:
                    oldValues[channel] = oldValue

                pc.setAttr(channel, value)

                if not isRecut:
                    #Verify if some of our blendShapes get activated
                    for bsAttr in bsAttrs:
                        if bsAttr.get() >= 0.1:
                            toDisconnects.append(bsAttr)

                    dupe = pc.PyNode(tkc.duplicateAndClean(sourceObject, inMuteDeformers=False, inResetDisplayType=False))
                    dupe.rename("{0}_{1}".format(object, poseName))
                    tkc.addParameter(dupe, channelNiceName, default=outputValue, containerName=inName)
                    if len(poseData) == 4:
                        tkc.addParameter(dupe, channel.replace(".", "_DOT_"), default=value, containerName=inName)

                    objectRoot.addChild(dupe)
                    
                    pc.setAttr(channel, oldValue)

            if isRecut:
                #Verify if some of our blendShapes get activated
                for bsAttr in bsAttrs:
                    if bsAttr.get() >= 0.1:
                        toDisconnects.append(bsAttr)
                
                dupe = pc.PyNode(tkc.duplicateAndClean(sourceObject, inMuteDeformers=False, inResetDisplayType=False))
                tkb.cutLeftRight(refObj, dupe, treshold=inRecutTreshold)


                node = pc.PyNode(dupe.name() + "_Left")
                node.rename("{0}_{1}".format(object, poseNames[0]))
                if poseNames[0] in channelNiceNames:
                    tkc.addParameter(node, channelNiceNames[poseNames[0]], default=outputValues[poseNames[0]], containerName=inName)
                    if len(poseDatas[0]) == 4:
                        tkc.addParameter(node, channels[poseNames[0]].replace(".", "_DOT_"), default=values[poseNames[0]], containerName=inName)
                objectRoot.addChild(node)

                node = pc.PyNode(dupe.name() + "_Right")
                node.rename("{0}_{1}".format(object, poseNames[1]))
                if poseNames[1] in channelNiceNames:
                    tkc.addParameter(node, channelNiceNames[poseNames[1]], default=outputValues[poseNames[1]], containerName=inName)
                    if len(poseDatas[1]) == 4:
                        tkc.addParameter(node, channels[poseNames[1]].replace(".", "_DOT_"), default=values[poseNames[1]], containerName=inName)
                objectRoot.addChild(node)
                
                pc.delete(dupe)

                i = 0
                for poseName in poseNames:
                    poseData = poseDatas[i]
                    i += 1

                    channel = None
                    value = None
                    outputChannel = None
                    outputValue = None

                    if len(poseData) == 2:
                        channel, value = poseData
                        outputChannel = channel
                        outputValue = value
                    else:
                        channel, value, outputChannel, outputValue = poseData

                    if not pc.objExists(channel):
                        pc.warning("Can't find channel {0}".format(channel))
                        continue

                    pc.setAttr(channel, oldValues[channel])

                pc.delete(refObj)

        #We are done with the object, disconnect conflicting blendShapes
        for toDisconnect in toDisconnects:
            toDisconnect.disconnect()

def applyShapeConversions(inDelete=True, inName="TK_SHAPE_CONVERSIONS", inCustomMeshSuffix=None):
    if pc.objExists(inName):
        root = pc.PyNode(inName)

        for child in root.getChildren():
            object = child.name()[:-len(inName)-1]
            objectNodeName = object if inCustomMeshSuffix is None else object + inCustomMeshSuffix

            print ("applyShapeConversions searching for :",object,objectNodeName)

            if not pc.objExists(objectNodeName):
                pc.warning("Can't find object '{0}'".format(objectNodeName))
                continue

            objectNode = pc.PyNode(objectNodeName)
            
            bs = child.getChildren()

            #Extract deltas
            objectSkin = tkc.getSkinCluster(objectNode)
            if not objectSkin is None:
                newBS = []
                for bsObj in bs:
                    channels = tkc.getParameters(bsObj, containerName=inName)
                    if len(channels) > 0:
                        channel = channels[-1]
                        controller, attribute = channel.split("_DOT_")
                        attrNode = pc.PyNode(controller).attr(attribute)

                        oldValue = attrNode.get()
                        value = tkc.getProperty(bsObj, inName).attr(channel).get()
                        attrNode.set(value)

                        deltaMesh = None
                        try:
                            print ("extractDeltas",objectNode,bsObj)
                            deltaMesh = pc.extractDeltas(s=objectNode, c=bsObj)
                        except:
                            pass

                        if not deltaMesh is None:
                            deltaNode = pc.PyNode(deltaMesh)

                            bsObj.getParent().addChild(deltaNode)
                            for child in bsObj.getChildren():
                                deltaNode.addChild(child)

                            name = bsObj.name()
                            pc.delete(bsObj)
                            deltaNode.rename(name)
                            newBS.append(deltaNode)
                        else:
                            newBS.append(bsObj)

                        attrNode.set(oldValue)

                bs = newBS

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
                bsNode = pc.blendShape(bsArgs, name="{0}_BS".format(objectNodeName))[0]
                tkc.reorderDeformers(objectNodeName)
            
            for bsObj in bs:
                channels = tkc.getParameters(bsObj, containerName=inName)
                channel = channels[0]

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

def moveControl(inControl, inJoint, inSurfaceMesh, inRoot, inRootUnder="TK_RootUnder_Main_Ctrl", inSurfaceOffset=None):
    #print "moveControl",inControl, inJoint, inSurfaceMesh, inRoot, inSurfaceOffset

    newNodeName = inControl.name() + "_REPLACING"

    relativeDeformerPath = os.path.join(tkc.oscarmodulepath, r"Standalones\OSCAR\Data\Rigs\RelativeDeformer\RelativeDeformer.ma")
    importedObjects = tkc.importFile(relativeDeformerPath, newNodeName)

    baseName = "{0}:{0}".format(newNodeName)

    root = pc.PyNode(baseName + "_Root")
    setupParams = pc.PyNode(baseName + "_Root_SetupParameters")
    newControl = pc.PyNode(baseName + "_Main_Ctrl")
    newDeformer = pc.PyNode(baseName + "_Main_Deform")

    tkc.matchTRS(root, inControl)
    root.s.set([1.0 if root.sx.get() > 0 else -1.0,
                1.0 if root.sy.get() > 0 else -1.0,
                1.0 if root.sz.get() > 0 else -1.0])

    setupParams.RelativeDeformer_initTx.set(root.tx.get())
    setupParams.RelativeDeformer_initTy.set(root.ty.get())
    setupParams.RelativeDeformer_initTz.set(root.tz.get())

    setupParams.RelativeDeformer_initRx.set(root.rx.get())
    setupParams.RelativeDeformer_initRy.set(root.ry.get())
    setupParams.RelativeDeformer_initRz.set(root.rz.get())

    setupParams.RelativeDeformer_initSx.set(root.sx.get())
    setupParams.RelativeDeformer_initSy.set(root.sy.get())
    setupParams.RelativeDeformer_initSz.set(root.sz.get())

    inRoot.addChild(root)

    #external constraints
    """
    extCons = tkc.getConstraintsUsing(inControl)

    owners = []
    for extCon in extCons:
        owner = tkc.getConstraintOwner(extCon)[0]
        
        if not owner in owners:
            owners.append(owner)

    storedCons = []
    for owner in owners:
        storedCons.append(tkc.storeConstraints([owner], inRemove=True))

    #print "!! storedCons",storedCons
    """

    ctrlName = inControl.name()
    inControl.rename(ctrlName + "_REPLACED")
    newControl.rename(ctrlName)

    for child in inControl.getChildren():
        if child.type() == "transform":
            newControl.addChild(child)

    #Shape
    origShape = newControl.getShape()
    if not origShape is None:
        pc.delete(origShape)

    pc.parent(inControl.getShape(), newControl, shape=True, add=True)

    #Transform
    tkc.matchConnections(newControl, inControl, "visibility", "drawOverride", "overrideVisibility")

    #Deformer
    tkc.matchConnections(newDeformer, inJoint, "visibility", "drawOverride", "overrideVisibility")

    #Sets
    tkc.matchSets(newControl, inControl)

    #Create surface constraint
    under = tkc.getNode(inSurfaceMesh)

    rootParent = pc.group(empty=True, name=root.name() + "_Constrainer_Parent")
    tkc.matchTRS(rootParent, root)
    inRoot.addChild(rootParent)
    if pc.objExists(inRootUnder):
        rootUnder = pc.PyNode(inRootUnder)
        tkc.constrain(rootParent, rootUnder)
        tkc.constrain(rootParent, rootUnder, "Scaling")
    else:
        pc.warning("Can't find root under to reconstrain ({0}) !!".format(inRootUnder))

    rootConstrainer = pc.group(empty=True, name=root.name() + "_Constrainer")
    tkc.matchTRS(rootConstrainer, rootParent)
    rootParent.addChild(rootConstrainer)

    if not inSurfaceOffset is None:
        pc.move(inSurfaceOffset[0], inSurfaceOffset[1], inSurfaceOffset[2], rootConstrainer, objectSpace=True, r=True, wd=True)

    surfCns = tkc.constrain(rootConstrainer, under, 'Surface')

    tkc.constrain(root, rootConstrainer)
    tkc.constrain(root, rootConstrainer, "Scaling")

    #reapply constraints
    """
    for cns in storedCons:
        tkc.loadConstraints(cns)
    """

    pc.delete(importedObjects[0])
    #"{0}:Controls".format(newNodeName),"{0}:Connected".format(newNodeName), "{0}:Guide".format(newNodeName), "{0}:Unselectable".format(newNodeName)
    pc.delete([ "{0}:Deformers".format(newNodeName), "{0}:Hidden".format(newNodeName)])

    pc.namespace(removeNamespace=newNodeName, mergeNamespaceWithRoot=True)

    tkRig.OscarHide([surfCns.name()])

    return (newControl, newDeformer)

def convertToBlendShapes(inShapeConversions, inNodesToRemove, inDefaultReskin, inRootParent, inRootName="MovedControllers", inReskin=None, inControlsToMove=None, inNewSkinCluster=None, inRootUnder="TK_RootUnder_Main_Ctrl", inShapeAliases=None, inPostSmooths=None, inPostSmoothGrows=1, inSurfaceOffset=[0.0, 0.0, 0.47], inDeletePosed=None, inKeptRoots=None, inPostSmoothSteps=30, inPostSmoothSize=0.15):
    if not pc.objExists(inDefaultReskin):
        pc.warning("Can't find 'inDefaultReskin' " + inDefaultReskin)
        return

    if not pc.objExists(inRootParent):
        pc.warning("Can't find 'inRootParent' " + inRootParent)
        return

    inRootParent = tkc.getNode(inRootParent)

    storeShapeConversions(inShapeConversions, inShapeAliases=inShapeAliases, inDisconnectConflicting=True, inUseTopLevel=(not inDeletePosed is None))

    if not inDeletePosed is None:
        for posesToDelete in inDeletePosed:
            if not pc.objExists(posesToDelete):
                pc.warning("Can't find posed object to delete '{0}'".format(posesToDelete))
                continue

            #Disconnect poses
            posesToDeleteNodeParent = pc.PyNode(posesToDelete).getParent()

            posesToDeleteNodeParent.tx.disconnect()
            posesToDeleteNodeParent.ty.disconnect()
            posesToDeleteNodeParent.tz.disconnect()

            posesToDeleteNodeParent.rx.disconnect()
            posesToDeleteNodeParent.ry.disconnect()
            posesToDeleteNodeParent.rz.disconnect()

            posesToDeleteNodeParent.sx.disconnect()
            posesToDeleteNodeParent.sy.disconnect()
            posesToDeleteNodeParent.sz.disconnect()

    inNodesToRemove = tkc.getNodes(inNodesToRemove)

    deformersToReplace = []

    controlsToMove = {}
    newSkinCluster = None
    #Find deformers to replace
    if not inControlsToMove is None:
        candidates = inNewSkinCluster or []

        for candidate in candidates:
            if pc.objExists(candidate):
                newSkinCluster = tkc.getNode(candidate)
                break

        if newSkinCluster is None:
            pc.warning("inNewSkinCluster must be defined to a valid mesh if we want to move controllers !")
        else:
            for nodeRoot in inNodesToRemove:
                joints = nodeRoot.getChildren(allDescendents=True, type='joint')
                deformersToReplace.extend(joints)

                #Here we may have to check if joint is not under a controller we want to keep !
                for joint in joints:
                    parents = joint.getAllParents()

                    for parent in parents:
                        if parent == nodeRoot:
                            break

                        if parent.name() in inControlsToMove:
                            skins = joint.listHistory(future=True, type="skinCluster")

                            skinnedObjs = {}
                            for skin in skins:
                                infs = skin.influenceObjects()

                                geo = skin.getGeometry()[0] if len(skin.getGeometry()) > 0 else None
                                if not geo is None and not geo in skinnedObjs:
                                    if joint in infs:
                                        skinnedObjs[geo] = tkc.getWeights(geo, joint)
                                    else:
                                        pc.warning("Joint {0} is not in {1} infs ({2})".format(joint, geo, infs))

                            if len(skinnedObjs) > 0:
                                controlsToMove[parent] = (joint, skinnedObjs)

    #print "controlsToMove",controlsToMove

    defaultReskin = inDefaultReskin

    skinningReplacements = {}

    for deformerToReplace in deformersToReplace:
        reskinner = defaultReskin
        if not inReskin is None and deformerToReplace.name() in inReskin and pc.objExists(inReskin[deformerToReplace.name()]):
            reskinner = inReskin[deformerToReplace.name()]
        if reskinner in skinningReplacements:
            skinningReplacements[reskinner].append(deformerToReplace)
        else:
            skinningReplacements[reskinner] = [deformerToReplace]

    if len(skinningReplacements) > 0:

        postSmooths = {}
        if not inPostSmooths is None:
            for mesh, deformers in inPostSmooths.items():
                if pc.objExists(mesh):
                    meshNode = pc.PyNode(mesh)
                    postSmooths[meshNode] = tkc.getInfluencedPoints(meshNode, deformers)

        #Filter skinClusters that affects meshes
        skins = pc.ls(type="skinCluster")
        meshSkins = [skin for skin in skins if len(skin.getGeometry()) > 0 and skin.getGeometry()[0].type() == "mesh"]

        gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

        pc.progressBar( gMainProgressBar,
        edit=True,
        beginProgress=True,
        isInterruptable=True,
        status="Replacing deformers",
        maxValue=len(skinningReplacements))

        for newDef, oldDefs in skinningReplacements.items():
            pc.progressBar(gMainProgressBar, edit=True, step=1)
            print ("replaceDeformers",oldDefs,newDef,meshSkins)
            tkc.replaceDeformers(oldDefs, tkc.getNode(newDef), inSkins=meshSkins)

        pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

        for mesh, points in postSmooths.items():
            pc.select(points)
            for i in range(inPostSmoothGrows):
                pc.mel.eval("GrowPolygonSelectionRegion")

            try:
                pc.ngSkinRelax(numSteps=inPostSmoothSteps, stepSize=inPostSmoothSize)
            except:
                pass

    pc.select(clear=True)

    #Move controls
    addSkinData = {}

    neededTransforms = []

    nVertsNewSkinCluster = pc.polyEvaluate(newSkinCluster, vertex=True)

    root = None
    TerriblyArbitraryTmpName = "TerriblyArbitraryTmpName"
    if pc.objExists(TerriblyArbitraryTmpName):
        root = pc.PyNode(TerriblyArbitraryTmpName)
    else:
        root = pc.group(empty=True, name=TerriblyArbitraryTmpName)
        inRootParent.addChild(root)

    for control, jointData in controlsToMove.items():
        joint, meshesData = jointData

        surfaceMesh = None
        #Find the good mesh to connect the moved controls to
        for mesh, meshData in meshesData.items():
            if "under" in mesh.name() and pc.polyEvaluate(mesh, vertex=True) == nVertsNewSkinCluster:
                surfaceMesh = mesh

        if not surfaceMesh is None:
            #print "MOVE",control,"meshesData",meshesData,"surface ?",meshesData.keys()[0].getParent()
            controller, deformer = moveControl(control, joint, surfaceMesh.getParent(), root, inRootUnder=inRootUnder, inSurfaceOffset=inSurfaceOffset)
        else:
            pc.warning("!! surfaceMesh can't be found for " + control)

        #Add source transforms in neededTransforms
        neededTransforms.extend(list(set(controller.listHistory(type="transform") + controller.getShape().listHistory(type="transform"))))

        for mesh, weights in meshesData.items():
            if not mesh in addSkinData:
                addSkinData[mesh] = [[deformer], [weights]]
            else:
                addSkinData[mesh][0].append(deformer)
                addSkinData[mesh][1].append(weights)

    
    for mesh, jointData in addSkinData.items():
        if pc.polyEvaluate(mesh, vertex=True) == nVertsNewSkinCluster:
            tkc.addWeights(newSkinCluster, jointData[0], jointData[1])
            break

    #before removing make sure we carry on what we need
    allRemovedTrans = []
    for nodeToRemove in inNodesToRemove:
        allRemovedTrans.extend([t for t in nodeToRemove.getChildren(allDescendents=True, type="transform")])

    neededTransforms = list(set(neededTransforms))
    allRemovedTrans = list(set(allRemovedTrans))

    #Reparent needed objects
    for neededTransform in neededTransforms:
        if neededTransform in allRemovedTrans:
            root.addChild(neededTransform)

    #actually delete
    for nodeToRemove in inNodesToRemove:
        if pc.objExists(nodeToRemove):
            node = pc.PyNode(nodeToRemove)

            if not inKeptRoots is None and nodeToRemove in inKeptRoots:
                vAttr = node.v
                locked = vAttr.isLocked()
                if locked:
                    vAttr.setLocked(False)

                vAttr.set(0)

                if locked:
                    vAttr.setLocked(True)

                pc.rename(nodeToRemove, nodeToRemove + "_KEPT")
            else:
                pc.delete(nodeToRemove)

    #ApplyShapeConversions
    applyShapeConversions()

    if not inRootName is None:
        root.rename(inRootName)

    tkc.deleteUnusedNodes()

"""
#We're losing:
#Left_Lip_Zip
#Right_Lip_Zip
#Sticky_Lip

mouth_shape_aliases = {
    "head_under_geo":         ["body_under_geo"],
}

mouth_conversions = {
    "head_under_geo":
        {
            "Upperlip_Center_Up"    :("Mouth_Upperlip_Center.ty", 1),

            "Upperlip_Center_Up_Left":("Left_Mouth_Upperlip_1.ty", 1),

            "Upperlip_Center_Up_Right":("Right_Mouth_Upperlip_1.ty", 1),


            "Lowerlip_Center_Up"    :("Mouth_Lowerlip_Center.ty", -1),

            "Lowerlip_Center_Up_Left":("Left_Mouth_Lowerlip_1.ty", -1),

            "Lowerlip_Center_Up_Right":("Right_Mouth_Lowerlip_1.ty", -1),


            "Bulge_Upperlip_Pos"     :("Mouth_Bulge_Upperlip.tx", 1),
            "Bulge_Upperlip_Neg"     :("Mouth_Bulge_Upperlip.tx", -1),

            "Bulge_Lowerlip_Pos"     :("Mouth_Bulge_Lowerlip.tx", 1),
            "Bulge_Lowerlip_Neg"     :("Mouth_Bulge_Lowerlip.tx", -1),


            "Jaw_Up"                :("Jaw_Move.ty", 1),
            "Jaw_Down"              :("Jaw_FK.rz", -33, "TK_Jaw_Open_Params_Root_SetupParameters.Jaw_Open_Params_Jaw_Open", 1),
            "Jaw_L"                 :("Jaw_Move.tx", 1),
            "Jaw_R"                 :("Jaw_Move.tx", -1),


            "Left_Smile"            :("Left_Mouth.ty", 1),
            "Left_Frown"            :("Left_Mouth.ty", -1),
            "Left_Wide"             :("Left_Mouth.tx", 1),
            "Left_Narrow"           :("Left_Mouth.tx", -1),


            "Right_Smile"            :("Right_Mouth.ty", 1),
            "Right_Frown"            :("Right_Mouth.ty", -1),
            "Right_Wide"             :("Right_Mouth.tx", 1),
            "Right_Narrow"           :("Right_Mouth.tx", -1),


            "Mouth_Up"                :("Mouth_Move.ty", 1),
            "Mouth_Down"              :("Mouth_Move.ty", -1),
            "Mouth_L"                 :("Mouth_Move.tx", 1),
            "Mouth_R"                 :("Mouth_Move.tx", -1),


            "Cheek_Up_Left"            :("Left_Eye_Up_Cheek.ty", 1),
            "Cheek_Dwn_Left"           :("Left_Eye_Up_Cheek.ty", -1),

            "Cheek_Up_Right"            :("Right_Eye_Up_Cheek.ty", 1),
            "Cheek_Dwn_Right"           :("Right_Eye_Up_Cheek.ty", -1),


            "Curl_Upperlip_Out"       :("Curl_Upperlip.tx", 1),
            "Curl_Upperlip_In"        :("Curl_Upperlip.tx", -1),

            "Curl_Lowerlip_Out"       :("Curl_Lowerlip.tx", 1),
            "Curl_Lowerlip_In"        :("Curl_Lowerlip.tx", -1),


            "Puff_Upperlip_Out"       :("Puff_Upperlip.tx", 1),
            "Puff_Upperlip_In"        :("Puff_Upperlip.tx", -1),

            "Puff_Lowerlip_Out"       :("Puff_Lowerlip.tx", 1),
            "Puff_Lowerlip_In"        :("Puff_Lowerlip.tx", -1),


            "Left_Pinch_Corner_Up"    :("Left_Pinch_Corner.ty", 1),
            "Left_Pinch_Corner_Dwn"   :("Left_Pinch_Corner.ty", -1),

            "Right_Pinch_Corner_Up"    :("Right_Pinch_Corner.ty", 1),
            "Right_Pinch_Corner_Dwn"   :("Right_Pinch_Corner.ty", -1),


            "Left_Curl_Corner_Up"    :("Left_Curl_Corner.ty", 1),
            "Left_Curl_Corner_Dwn"   :("Left_Curl_Corner.ty", -1),

            "Right_Curl_Corner_Up"    :("Right_Curl_Corner.ty", 1),
            "Right_Curl_Corner_Dwn"   :("Right_Curl_Corner.ty", -1),


            "Left_Cheek_Inflate_Up"    :("Left_Cheek_Inflate.ty", 1),
            "Left_Cheek_Inflate_Dwn"   :("Left_Cheek_Inflate.ty", -1),

            "Right_Cheek_Inflate_Up"    :("Right_Cheek_Inflate.ty", 1),
            "Right_Cheek_Inflate_Dwn"   :("Right_Cheek_Inflate.ty", -1),


            "Left_Puff_Up"    :("Left_Puff.ty", 1),
            "Left_Puff_Dwn"   :("Left_Puff.ty", -1),

            "Right_Puff_Up"    :("Right_Puff.ty", 1),
            "Right_Puff_Dwn"   :("Right_Puff.ty", -1),


            "Mouth_Up_Lat_Left"       :("Left_Mouth_Lat_Upperlip_Ctrl.ty", 1),

            "Mouth_Down_Lat_Left"     :("Left_Mouth_Lat_Lowerlip_Ctrl.ty", 1),

            "Mouth_Up_Lat_Right"       :("Right_Mouth_Lat_Upperlip_Ctrl.ty", 1),

            "Mouth_Down_Lat_Right"     :("Right_Mouth_Lat_Lowerlip_Ctrl.ty", 1),
        }
}

controlsToMove = ["Right_Mouth_Deform","Right_Mouth_Down_2_Deform","Right_Mouth_Up_2_Deform",
                    "Right_Mouth_Up_1_Deform","Right_Mouth_Down_1_Deform","Right_Mouth_Up_0_Deform",
                    "Right_Mouth_Down_0_Deform","Center_Down_Deform","Center_Up_Deform",
                    "Left_Mouth_Down_0_Deform","Left_Mouth_Up_0_Deform","Left_Mouth_Up_1_Deform",
                    "Left_Mouth_Down_1_Deform","Left_Mouth_Down_2_Deform","Left_Mouth_Up_2_Deform",
                    "Left_Mouth_Deform",
                    "Left_Cheekbone_Main_Ctrl", "Right_Cheekbone_Main_Ctrl"]

defaultReplaceDeformer = "TK_Head_Ctrl_0_Deform"

reskin = {
    "TK_Mouth_Center_Down_Deform":"TK_Jaw_0_Deform",
    "TK_Chin_0_Deform":"TK_Jaw_0_Deform",
    "TK_Depressor_Center_Deform":"TK_Jaw_0_Deform",

    "TK_Left_Depressor_Deform":"TK_Jaw_0_Deform",
    "TK_Mouth_Left_Down_0_Deform":"TK_Jaw_0_Deform",
    "TK_Mouth_Left_Down_1_Deform":"TK_Jaw_0_Deform",
    "TK_Mouth_Left_Down_2_Deform":"TK_Jaw_0_Deform",

    "TK_Right_Depressor_Deform":"TK_Jaw_0_Deform",
    "TK_Mouth_Right_Down_0_Deform":"TK_Jaw_0_Deform",
    "TK_Mouth_Right_Down_1_Deform":"TK_Jaw_0_Deform",
    "TK_Mouth_Right_Down_2_Deform":"TK_Jaw_0_Deform",
}

remove_roots = [    "TK_Mouth_Root",
                    "TK_Chin_Root",
                    "TK_Depressor_Center_Root",
                    "TK_Center_Levator_Root",

                    "TK_Left_Cheekbone_Root",
                    "TK_Left_UpperLid_Root",
                    "TK_Left_Riso_Root",
                    "TK_Left_Zygo_Root",
                    "TK_Left_Levator_Root",
                    "TK_Left_Depressor_Root",
                    "TK_Left_CheekCtrl_Root",
                    "TK_Left_Lips_Cheek_Switcher_Root",
                    "TK_Left_Cheek_Switcher_Root",
                    "TK_AttenuationCheekBone_ParentSwitcher_Root",

                    "TK_Right_Cheekbone_Root",
                    "TK_Right_UpperLid_Root",
                    "TK_Right_Riso_Root",
                    "TK_Right_Zygo_Root",
                    "TK_Right_Levator_Root",
                    "TK_Right_Depressor_Root",
                    "TK_Right_CheekCtrl_Root",
                    "TK_Right_Lips_Cheek_Switcher_Root",
                    "TK_Right_Cheek_Switcher_Root",
                    "TK_Right_AttenuationCheekBone_ParentSwitcher1_Root",
                ]

import re

import tkMayaCore as tkc
import tkOptimize as tko
import tkNodeling as tkn

reload(tkc)
reload(tko)

#Edit the template in term of jaw opening
exprString = pc.PyNode("Jaw_Open_Params_Root_SetupParameters_Jaw_Open_Params_Jaw_Open_Expr").getString()

divisor = None
divisorPattern = r"\/\s*(-*\s*[0-9]+)\s*;"

matches = re.finditer(divisorPattern, exprString, re.MULTILINE)

for matchNum, match in enumerate(matches):
    divisor = int(match.groups(0)[0])
    if divisor > 0:
        divisor *= -1
    break

if not divisor is None:
    if len(mouth_conversions["head_under_geo"]["Jaw_Down"]) == 2:
        mouth_conversions["head_under_geo"]["Jaw_Down"] = (mouth_conversions["head_under_geo"]["Jaw_Down"][0], divisor)
    else:
        mouth_conversions["head_under_geo"]["Jaw_Down"] = (mouth_conversions["head_under_geo"]["Jaw_Down"][0], divisor, mouth_conversions["head_under_geo"]["Jaw_Down"][2], mouth_conversions["head_under_geo"]["Jaw_Down"][3])
else:
    pc.warning("Can't get mouth opening divisor from 'Jaw_Open_Params_Root_SetupParameters_Jaw_Open_Params_Jaw_Open_Expr'")

smoothInfs = reskin.keys()
addInfs = ["TK_Mouth_Left_Deform", "TK_Mouth_Right_Deform", "TK_Mouth_Left_Up_1_Deform", "TK_Mouth_Right_Up_1_Deform", "TK_Mouth_Left_Up_0_Deform", "TK_Mouth_Right_Up_0_Deform"]
for addInf in addInfs:
    if not addInf in smoothInfs:
        smoothInfs.append(addInf)

postSmooths = {"head_under_geo":smoothInfs,
                "body_under_geo":smoothInfs}

tko.convertToBlendShapes(mouth_conversions, remove_roots, "TK_Head_Ctrl_0_Deform", "TKRig", inRootName="TK_Mouth_Root", inReskin=reskin, inControlsToMove=controlsToMove, inNewSkinCluster=["head_geo", "body_geo"], inShapeAliases=mouth_shape_aliases, inPostSmooths=postSmooths)
"""