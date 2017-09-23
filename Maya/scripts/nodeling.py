import pymel.core as pc

#Todo for "create" nodes, reuse if possible

"""
locs = ["mod:motionPathRig_Loc_00","mod:motionPathRig_Loc_01","mod:motionPathRig_Loc_02","mod:motionPathRig_Loc_03","mod:motionPathRig_Loc_04","mod:motionPathRig_Loc_05","mod:motionPathRig_Loc_06","mod:motionPathRig_Loc_07","mod:motionPathRig_Loc_08","mod:motionPathRig_Loc_09","mod:motionPathRig_Loc_10","mod:motionPathRig_Loc_11","mod:motionPathRig_Loc_12","mod:motionPathRig_Loc_13","mod:motionPathRig_Loc_14","mod:motionPathRig_Loc_15","mod:motionPathRig_Loc_16","mod:motionPathRig_Loc_17","mod:motionPathRig_Loc_18","mod:motionPathRig_Loc_19","mod:motionPathRig_Loc_20","mod:motionPathRig_Loc_21","mod:motionPathRig_Loc_22","mod:motionPathRig_Loc_23","mod:motionPathRig_Loc_24","mod:motionPathRig_Loc_25","mod:motionPathRig_Loc_26","mod:motionPathRig_Loc_27","mod:motionPathRig_Loc_28","mod:motionPathRig_Loc_29","mod:motionPathRig_Loc_30","mod:motionPathRig_Loc_31","mod:motionPathRig_Loc_32","mod:motionPathRig_Loc_33","mod:motionPathRig_Loc_34","mod:motionPathRig_Loc_35","mod:motionPathRig_Loc_36","mod:motionPathRig_Loc_37","mod:motionPathRig_Loc_38","mod:motionPathRig_Loc_39","mod:motionPathRig_Loc_40","mod:motionPathRig_Loc_41","mod:motionPathRig_Loc_42","mod:motionPathRig_Loc_43","mod:motionPathRig_Loc_44","mod:motionPathRig_Loc_45","mod:motionPathRig_Loc_46","mod:motionPathRig_Loc_47"]
ctrls = ["mod:Path_Curve_Ctrl1","mod:Path_Curve_Ctrl2","mod:Path_Curve_Ctrl3","mod:Path_Curve_Ctrl4","mod:Path_Curve_Ctrl5","mod:Path_Curve_Ctrl6","mod:Path_Curve_Ctrl7","mod:Path_Curve_Ctrl8","mod:Path_Curve_Ctrl9","mod:Path_Curve_Ctrl10","mod:Path_Curve_Ctrl11","mod:Path_Curve_Ctrl12","mod:Path_Curve_Ctrl13","mod:Path_Curve_Ctrl14","mod:Path_Curve_Ctrl15","mod:Path_Curve_Ctrl16","mod:Path_Curve_Ctrl17","mod:Path_Curve_Ctrl18","mod:Path_Curve_Ctrl19","mod:Path_Curve_Ctrl20","mod:Path_Curve_Ctrl21","mod:Path_Curve_Ctrl22","mod:Path_Curve_Ctrl23","mod:Path_Curve_Ctrl24","mod:Path_Curve_Ctrl25","mod:Path_Curve_Ctrl26","mod:Path_Curve_Ctrl27","mod:Path_Curve_Ctrl28","mod:Path_Curve_Ctrl29","mod:Path_Curve_Ctrl30","mod:Path_Curve_Ctrl31","mod:Path_Curve_Ctrl32","mod:Path_Curve_Ctrl33","mod:Path_Curve_Ctrl34","mod:Path_Curve_Ctrl35","mod:Path_Curve_Ctrl36","mod:Path_Curve_Ctrl37","mod:Path_Curve_Ctrl38","mod:Path_Curve_Ctrl39","mod:Path_Curve_Ctrl40","mod:Path_Curve_Ctrl41","mod:Path_Curve_Ctrl42","mod:Path_Curve_Ctrl43","mod:Path_Curve_Ctrl44","mod:Path_Curve_Ctrl45","mod:Path_Curve_Ctrl46","mod:Path_Curve_Ctrl47","mod:Path_Curve_Ctrl48","mod:Path_Curve_Ctrl49","mod:Path_Curve_Ctrl50","mod:Path_Curve_Ctrl51","mod:Path_Curve_Ctrl52","mod:Path_Curve_Ctrl53","mod:Path_Curve_Ctrl54","mod:Path_Curve_Ctrl55","mod:Path_Curve_Ctrl56","mod:Path_Curve_Ctrl57","mod:Path_Curve_Ctrl58","mod:Path_Curve_Ctrl59","mod:Path_Curve_Ctrl60","mod:Path_Curve_Ctrl61","mod:Path_Curve_Ctrl62","mod:Path_Curve_Ctrl63","mod:Path_Curve_Ctrl64","mod:Path_Curve_Ctrl65","mod:Path_Curve_Ctrl66","mod:Path_Curve_Ctrl67","mod:Path_Curve_Ctrl68","mod:Path_Curve_Ctrl69","mod:Path_Curve_Ctrl70","mod:Path_Curve_Ctrl71","mod:Path_Curve_Ctrl72","mod:Path_Curve_Ctrl73","mod:Path_Curve_Ctrl74","mod:Path_Curve_Ctrl75","mod:Path_Curve_Ctrl76"]
ctrlsNodes = [pc.PyNode(n) for n in ctrls]
for loc in locs:
    locNode = pc.PyNode(loc)
    createProximitiesSystem(locNode, *ctrlsNodes, inResultObjName=loc)
"""

WORLD = "World"
LOCAL = "Local"

WORLD_MATRIX_FORMAT = "{0}_WorldMatrix"
VECTOR_FORMAT = "{0}_TO_{1}_{2}Space_Vec"
DISTANCE_FORMAT = "{0}_TO_{1}_{2}Space_Dist"
POW_FORMAT = "{0}_Pow"
DOT_FORMAT = "{0}_ON_{1}_Dot"
DIVIDE_FORMAT = "{0}_OVER_{1}_Div"
CLAMP_FORMAT = "{0}_{1}_{2}_Clamp"
REVERSE_FORMAT = "{0}_Reverse"

OUT3DS = {
    "plusMinusAverage":"output3D"
}

def get3DOut(inObj):
    return inObj.attr(OUT3DS.get(inObj.type(), "t"))

def getWorldMatrix(inObj):
    worldName = WORLD_MATRIX_FORMAT.format(inObj.name())
    if pc.objExists(worldName):
        return pc.PyNode(worldName)
        
    worldNode = pc.createNode("decomposeMatrix", name=worldName)
    inObj.worldMatrix[0] >> worldNode.inputMatrix
    
    return worldNode

def getVector(inSource, inDestination, inWorld=True):
    ns = str(inSource.namespace())
    vectorName = ns + VECTOR_FORMAT.format(inSource.stripNamespace(), inDestination.stripNamespace(), WORLD if inWorld else LOCAL)
    if pc.objExists(vectorName):
        return pc.PyNode(vectorName)

    sourceNode = inSource if not inWorld else getWorldMatrix(inSource)
    destNode = inDestination if not inWorld else getWorldMatrix(inDestination)
    
    vectorNode = pc.createNode("plusMinusAverage", name=vectorName)
    vectorNode.operation.set(2)#Substract
    sourceTranslate = sourceNode.outputTranslate if inWorld else source.t
    destTranslate = destNode.outputTranslate if inWorld else destNode.t

    destTranslate  >> vectorNode.input3D[0]
    sourceTranslate >> vectorNode.input3D[1]

    return vectorNode

def getDistance(inSource, inDestination, inWorld=True):
    ns = str(inSource.namespace())
    distanceName = ns + DISTANCE_FORMAT.format(inSource.stripNamespace(), inDestination.stripNamespace(), WORLD if inWorld else LOCAL)
    if pc.objExists(distanceName):
        return pc.PyNode(distanceName)

    sourceNode = inSource if not inWorld else getWorldMatrix(inSource)
    destNode = inDestination if not inWorld else getWorldMatrix(inDestination)
    
    distanceNode = pc.createNode("distanceBetween", name=distanceName)
    sourceTranslate = sourceNode.outputTranslate if inWorld else source.t
    destTranslate = destNode.outputTranslate if inWorld else destNode.t

    sourceTranslate >> distanceNode.point1
    destTranslate >> distanceNode.point2

    return distanceNode

def createPow(inAttr):
    powNode = pc.createNode("multDoubleLinear", name=POW_FORMAT.format(inAttr.node()))
    inAttr >> powNode.input1
    inAttr >> powNode.input2

    return powNode

def createDotProduct(inVec1, inVec2, inNormalize=False):
    ns = str(inVec1.namespace())

    dotNode = pc.createNode("vectorProduct", name=ns + DOT_FORMAT.format(inVec1.stripNamespace(), inVec2.stripNamespace()))
    if inNormalize:
        dotNode.normalizeOutput.set(True)

    get3DOut(inVec2) >> dotNode.input1
    get3DOut(inVec1) >> dotNode.input2

    return dotNode

def createDivide(inAttr1, inAttr2, inName=None):
    ns = str(inAttr1.node().namespace())

    name = inName or ns + DIVIDE_FORMAT.format(inAttr1.node().stripNamespace(), inAttr2.node().stripNamespace())

    divNode = pc.createNode("multiplyDivide", name=name)
    divNode.operation.set(2)#Divide

    #Todo manage vector or scalar types (considered scalar as it is)

    inAttr1 >> divNode.input1X
    inAttr2 >> divNode.input2X

    return divNode

def createClamp(inAttr, inMin=0.0, inMax=1.0, inName=None):
    name = inName or CLAMP_FORMAT.format(inAttr.node().name(), inMin, inMax)

    clampNode = pc.createNode("clamp", name=name)
    clampNode.minR.set(inMin)
    clampNode.maxR.set(inMax)

    inAttr >> clampNode.inputR

    return clampNode

def createReverse(inAttr, inName=None):
    name = inName or REVERSE_FORMAT.format(inAttr.node().name())

    revNode = pc.createNode("reverse", name=name)

    inAttr >> revNode.inputX

    return revNode

def createProximitiesCompound(inObj, inStart, inEnd):
    startToObjVec = getVector(inStart, inObj)

    startToEndVec = getVector(inStart, inEnd)

    startToEndDist = getDistance(inStart, inEnd)

    distPow = createPow(startToEndDist.distance)

    ObjOnLocDot = createDotProduct(startToObjVec, startToEndVec)

    normDivide = createDivide(ObjOnLocDot.outputX, distPow.output)

    rsltClamp = createClamp(normDivide.outputX)

    rsltReverse = createReverse(rsltClamp.outputR)

    return {
            "startToObjVec":startToObjVec,
            "startToEndVec":startToEndVec,
            "startToEndDist":startToEndDist,
            "distPow":distPow,
            "ObjOnLocDot":ObjOnLocDot,
            "normDivide":normDivide,
            "rsltClamp":rsltClamp,
            "rsltReverse":rsltReverse
            }

"""
kwargs awaits : inResultObjName (string : default "RESULTS"), inResultAttrFormat (string with a format token : default "Loc{0}")
"""
def createProximitiesSystem(inObj, *inCheckPoints, **kwargs):
    inResultObjName = kwargs.get("inResultObjName", "RESULTS")
    inResultAttrFormat = kwargs.get("inResultAttrFormat", "Loc{0}")

    firstIter = True
    lastIter = False

    lenCheckPoints = len(inCheckPoints)

    #Prepare result obj
    resultObj = None
    if not pc.objExists(inResultObjName):
        resultObj = pc.createNode("transform", name=inResultObjName)
    else:
        resultObj = pc.PyNode(inResultObjName)

    for i in range(lenCheckPoints):
        attrName = inResultAttrFormat.format(i+1)
        if not pc.attributeQuery(attrName, node=resultObj, exists=True):
            pc.select(resultObj)
            pc.addAttr(longName=attrName, defaultValue=0.0, minValue=0.0, maxValue=1.0)

    #Actually do the nodeling
    firstOutput = None
    secondOutput = None
    bigger0 = None
    for i in range(lenCheckPoints - 1):
        start = inCheckPoints[i]
        end = inCheckPoints[i+1]

        curCompound = createProximitiesCompound(inObj, start, end)
        
        if lenCheckPoints == 2:
            #This is the simple case, simply connect outputs from reverse and clamp
            curCompound["rsltReverse"].outputX >> resultObj.attr(inResultAttrFormat.format(i+1))
            curCompound["rsltClamp"].outputR >> resultObj.attr(inResultAttrFormat.format(i+2))
        else:
            if firstIter:
                firstIter = False
                #At first iteration we can connect first "Loc" directly
                firstOutput = curCompound["rsltReverse"].outputX
            else:
                if i == lenCheckPoints - 2:
                    lastIter = True
                #else connect the ports from last condition
                curCompound["rsltReverse"].outputX >> bigger0.colorIfTrueR
                curCompound["rsltClamp"].outputR >> bigger0.firstTerm
                curCompound["rsltClamp"].outputR >> bigger0.colorIfTrueG

                firstOutput = bigger0.outColorR
                secondOutput = bigger0.outColorG

            if not lastIter:
                bigger0 = pc.createNode("condition", name="BiggerThan0_{0}".format(i+1))
                bigger0.operation.set(2)#Greater than
                bigger0.secondTerm.set(0)
                bigger0.colorIfFalseG.set(0)
                curCompound["rsltClamp"].outputR >> bigger0.colorIfFalseR

            firstOutput >> resultObj.attr(inResultAttrFormat.format(i+1))
            if secondOutput is not None:
                secondOutput >> resultObj.attr(inResultAttrFormat.format(i+2))
            
def createProximitiesSystemOnSelection(inResultObjName="RESULTS", inResultAttrFormat="Loc{0}"):
    sel = pc.selected()

    if len(sel) < 3:
        pc.warning("Cannot create a proximities system with less than 3 elements !")
        return

    createProximitiesSystem(sel[0], *sel[1:], inResultObjName=inResultObjName, inResultAttrFormat=inResultAttrFormat)