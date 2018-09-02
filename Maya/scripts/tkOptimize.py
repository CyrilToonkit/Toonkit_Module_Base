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

def matrixConstrain(inTarget, inSource):

    matrixOut = None

    offset = pc.group(name=inSource + "_offset_MARKER", empty=True)
    inSource.addChild(offset)
    tkc.matchTRS(offset, inTarget)
    
    offseted = not (tkc.listsBarelyEquals(offset.getTranslation(), [0.0,0.0,0.0]) and
                tkc.listsBarelyEquals(ozms.getPymelRotation(offset), [0.0,0.0,0.0]) and
                tkc.listsBarelyEquals(offset.getScale(), [1.0,1.0,1.0]))

    if offseted:
        composeOut = tkn.composeMatrix(list(offset.t.get()), list(offset.r.get()), list(offset.s.get()))

        """
        offset_Mul = tkn.create("multMatrix", inSource + "_offset_Mul")
        compose.outputMatrix >> offset_Mul.matrixIn[0]
        inSource.worldMatrix[0] >> offset_Mul.matrixIn[1]
        """
        matrixOut = tkn.mul(composeOut, inSource.worldMatrix[0])#offset_Mul.matrixSum
    else:
        matrixOut = inSource.worldMatrix[0]

    pc.delete(offset)

    """
    multInvParent = tkn.create("multMatrix", inTarget + "_multInvParent")
    matrixOut >> multInvParent.matrixIn[0]
    inTarget.parentInverseMatrix[0] >> multInvParent.matrixIn[1]
    """

    decompMatrix = tkn.decomposeMatrix(tkn.mul(matrixOut, inTarget.parentInverseMatrix[0]))#multInvParent.matrixSum)
    
    decompMatrix.outputTranslate >> inTarget.translate
    decompMatrix.outputRotate >> inTarget.rotate
    decompMatrix.outputScale >> inTarget.scale

def replaceConstraint(inConstraint, inTarget, inSource):
    pc.delete(inConstraint)

    constraints = tkc.getConstraints(inTarget)
    for constraint in constraints:
        if constraint.type() == "scaleConstraint" and inSource in tkc.getConstraintTargets(constraint):
            pc.delete(constraint)
            break

    matrixConstrain(inTarget, inSource)

def replaceConstraints():
    parentCons = pc.ls(type="parentConstraint")
    print "parentCons", len(parentCons)
    
    replaced = []

    for parentCon in parentCons:
        owner = tkc.getConstraintOwner(parentCon)[0]
        
        targets = tkc.getConstraintTargets(parentCon)
        if len(targets) == 1:
            replaced.append(owner)
            replaceConstraint(parentCon, owner, targets[0])
        else:
            print "Cannot replace : ",parentCon,"on",owner

    print "replaced",replaced

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
            print "Cannot replace : ",expr,exprString
        
    print "replaced",replaced