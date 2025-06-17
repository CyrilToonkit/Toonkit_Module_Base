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
import re
import os
import six
basestring = six.string_types
import fnmatch

import maya.cmds as mc
import pymel.core as pc
from TkApi import maya_api as tkApi
import tkMayaCore as tkc
import tkRig
import tkOutfits

__author__ = "Cyril GIBAUD - Toonkit"

"""
#Copy Point positions on two selected objects, ref first, then target
import tkBlendShapes
reload(tkBlendShapes)

tkBlendShapes.matchPointPositions(pc.selected()[0], pc.selected()[1])
"""

MESH_REF_NAME = "tkBs_{0}_refMesh"

POSE_GRP_NAME = "tkBs_{0}_grp"

EDIT_MESH_NAME = "tkBs_{0}_pose_{1}_editMesh"

DELTA_MESH_NAME = "tkBs_{0}_pose_{1}_corrective"

def getBSTargetFromIndex(inBlendShape, inIndex):
    aliases = mc.aliasAttr(inBlendShape, query=True)

    for i in range(int(len(aliases)/2)):
        alias = [aliases[2*i], aliases[2*i+1]]
        if alias[1] == "weight[{0}]".format(inIndex):
            return alias[0]

    return None

def getBSIndexFromTarget(inBlendShape, inTarget):
    reg = re.compile("weight\\[([0-9]+)\\]")
    aliases = mc.aliasAttr(inBlendShape, query=True)

    for i in range(int(len(aliases)/2)):
        alias = [aliases[2*i], aliases[2*i+1]]
        if alias[0] == inTarget:
            #print alias[1], inTarget
            matchObj = reg.match(alias[1])
            if matchObj:
                return int(matchObj.groups(0)[0])

    return None

def getFirstAvailableIndex(inBlendShape):
    return pc.mel.eval("bsMultiIndexForTarget "+inBlendShape+" "+str(mc.blendShape(inBlendShape, query=True,wc=True)-1)) + 1


def getSource(inBlendShape):
    sourceMeshes = mc.ls(mc.listHistory(inBlendShape, gl=True, lf=True, f=True, il=2), type="mesh")

    if len(sourceMeshes) == 0:
        mc.warning("source Mesh can't be found !")
        return None
    return sourceMeshes[0]

def cleanUpBlendShapeWeights(inBlendShape):
    arrayAttrs = mc.listAttr("{0}.weight".format(inBlendShape), multi=True)
   
    for target in arrayAttrs:
        print (target)
        if re.search("weight\\[.*\\]", target):
            mc.removeMultiInstance(inBlendShape+"."+target)

def editTarget(inBlendShape, inTarget, corrective=None):
    if isinstance(inTarget, basestring):
        inTarget = getBSIndexFromTarget(inBlendShape, inTarget)
        if inTarget == None:
            mc.warning("Can't get index from target {0}".format(inTarget))

    arrayAttrs = mc.listAttr("{0}.weight".format(inBlendShape), multi=True)

    """
    if len(arrayAttrs) <= inTarget:
        mc.warning("Target index wasn't found !")
        return None
    """

    targetMeshes = mc.ls(mc.listConnections("{0}.inputTarget[0].inputTargetGroup[{1}].inputTargetItem[6000].inputGeomTarget".format(inBlendShape, inTarget), shapes=True), type="mesh")
    if targetMeshes != None and len(targetMeshes) > 0:
        print ("Target mesh already connected : {0}".format(targetMeshes[0]))
        return targetMeshes[0]

    vectors =  mc.getAttr("{0}.inputTarget[0].inputTargetGroup[{1}].inputTargetItem[6000].inputPointsTarget".format(inBlendShape, inTarget))

    if vectors == None or len(vectors) == 0:
        mc.warning("Target index is empty !")
        return None

    components = mc.getAttr("{0}.inputTarget[0].inputTargetGroup[{1}].inputTargetItem[6000].inputComponentsTarget".format(inBlendShape, inTarget))

    if components == None or len(components) == 0:
        mc.warning("Target components does not match !")
        return None

    sourceMeshes = mc.ls(mc.listHistory(inBlendShape, gl=True, lf=True, f=True, il=2), type="mesh")

    if len(sourceMeshes) == 0:
        mc.warning("source Mesh can't be found !")
        return None
    sourceMesh = sourceMeshes[0]

    targetName = getBSTargetFromIndex(inBlendShape, inTarget)
    dupe = pc.PyNode(duplicateAndClean(sourceMesh, inTargetName=targetName, inMuteDeformers=True))
    dupeShape = dupe.getShapes()[0]

    targetPoints = dupeShape.getPoints()
    reg = re.compile("vtx\\[([0-9]+)\\]")
    regRange = re.compile("vtx\\[([0-9]+:[0-9]+)\\]")

    curVector = 0
    for i in range(len(components)):
        component = components[i]
        matchObj = reg.match(component)
        if matchObj:
            vtx = int(matchObj.groups(0)[0])
            targetPoints[vtx] = targetPoints[vtx] + vectors[curVector]
            curVector += 1
        else:
            matchObj = regRange.match(component)
            if matchObj:
                vtxBefore, vtxAfter = [int(a) for a in matchObj.groups(0)[0].split(":")]
                for j in range(vtxBefore, vtxAfter+1):
                    targetPoints[j] = targetPoints[j] + vectors[curVector]
                    curVector += 1

    dupeShape.setPoints(targetPoints)

    mc.connectAttr("{0}.worldMesh[0]".format(dupeShape.name()), "{0}.inputTarget[0].inputTargetGroup[{1}].inputTargetItem[6000].inputGeomTarget".format(inBlendShape, inTarget), force=True)
    
    return dupe

def editTargets(inBlendShape):
    targets = []

    arrayAttrs = pc.listAttr("{0}.weight".format(inBlendShape), multi=True)

    for arrayAttr in arrayAttrs:
        target = editTarget(inBlendShape, arrayAttr, corrective=None)
        if target != None:
            targets.append(target)

    return targets

def rebuildAllTargets(inObject, inProgress=True):
    inObject = tkc.getNode(inObject)

    bss = []
    targets = []

    if inObject.type() == "blendShape":
        bss = [inObject]
    else:
        bss = pc.listHistory(inObject, type="blendShape")

    for bs in bss:
        targetCount = pc.blendShape(bs, wc=True, q=True)

        gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')
        if inProgress:
            pc.progressBar( gMainProgressBar,
                edit=True,
                beginProgress=True,
                isInterruptable=True,
                status="Rebuilding shape targets",
                maxValue=targetCount )

        for i in range(targetCount):
            targets.extend(pc.sculptTarget(bs, e=True, regenerate=True, target=i))
            if inProgress:
                pc.progressBar(gMainProgressBar, edit=True, step=1)
            
        if inProgress:
            pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    return targets

def duplicateAndClean(inSourceMesh, inTargetName="$REF_dupe", inMuteDeformers=True, inMaterials=False):
    #Make sure every deformer is at 0 before duplication
    envelopes = {}
    if inMuteDeformers:
        envelopes = muteDeformers(inSourceMesh)
    
    dupe = mc.duplicate(inSourceMesh, rr=True)[0]

    if '$REF' in inTargetName:
        inTargetName = inTargetName.replace('$REF', inSourceMesh)

    dupe = mc.rename(dupe, inTargetName)
    
    shapes = mc.listRelatives(dupe, shapes=True, fullPath=True)
    if shapes != None:
        for shape in shapes:
            if mc.getAttr("{0}.intermediateObject".format(shape)):
                mc.delete(shape)
            else:
                mc.setAttr("{0}.overrideDisplayType".format(shape), 0)

    if inMuteDeformers:
        restoreDeformers(inSourceMesh, envelopes)

    if inMaterials:
        tkOutfits.assignShader(pc.PyNode("lambert1"), pc.PyNode(dupe))

    return dupe

def _matchPointPositions(inRef, inTarget, inMap=None, inRefPoints=None, inTargetPoints=None):
    refShape = None

    VALIDTYPES = ["mesh", "nurbsSurface"]
    refType = None
    targetType = None

    if inRef.type() in VALIDTYPES:
        refType = inRef.type()
        refShape = inRef
    else:
        refShapes = inRef.getShapes(noIntermediate=True)
        for shape in refShapes:
            if shape.type() in VALIDTYPES:
                refType = shape.type()
                refShape = shape
                break
                
        if refShape is None:
            pc.warning(inRef.name() + " is not a valid (must be of type {0}) !!".format(VALIDTYPES))
            return False

    targetShape = None

    if inTarget.type() in VALIDTYPES:
        targetType = inTarget.type()
        targetShape = inTarget
    else:
        targetShapes = inTarget.getShapes(noIntermediate=True)
        for shape in targetShapes:
            if shape.type() in VALIDTYPES:
                targetType = shape.type()
                targetShape = shape
                break
                
        if targetShape is None:
            pc.warning(inTarget.name() + " is not a valid (must be of type {0}) !!".format(VALIDTYPES))
            return False
    refPoints = inRefPoints or tkApi.getPointPositions(inRef.name()) if refType == "mesh" else refShape.getCVs()
    targetPoints = inTargetPoints or tkApi.getPointPositions(inTarget.name()) if targetType == "mesh" else targetShape.getCVs()

    for i in range(len(refPoints)):
        if i >= len(targetPoints):
            break

        if inMap is None or i >= len(inMap):
            targetPoints[i] = refPoints[i]
        elif inMap[i] >= 0.9999:
            targetPoints[i] = refPoints[i]
        elif inMap[i] >= 0.0001:
            targetPoints[i][0] = (1 - inMap[i]) * targetPoints[i][0] + inMap[i] * refPoints[i][0]
            targetPoints[i][1] = (1 - inMap[i]) * targetPoints[i][1] + inMap[i] * refPoints[i][1]
            targetPoints[i][2] = (1 - inMap[i]) * targetPoints[i][2] + inMap[i] * refPoints[i][2]

    if targetType == "mesh":
        tkc.POINT_POSITIONS = targetPoints
        pc.setPointPositions(inTarget.name())
        tkc.POINT_POSITIONS = None
    else:
        targetShape.setCVs(targetPoints)
        targetShape.updateSurface()

    return True

def matchPointPositions(inRef, inTarget, sided=False, rightToLeft=False, treshold=2.0, offset=0.0):
    if not sided:
        return _matchPointPositions(inRef, inTarget)
        
    refShape = None

    if inRef.type() == "mesh":
        refShape = inRef
    else:
        refShapes = inRef.getShapes(noIntermediate=True)
        for shape in refShapes:
            if shape.type() == "mesh":
                refShape = shape
                break
                
        if refShape is None:
            pc.warning(inRef.name() + " is not a mesh !!")
            return False

    targetShape = None

    if inTarget.type() == "mesh":
        targetShape = inTarget
    else:
        targetShapes = inTarget.getShapes(noIntermediate=True)
        for shape in targetShapes:
            if shape.type() == "mesh":
                targetShape = shape
                break
                
        if targetShape is None:
            pc.warning(inTarget.name() + " is not a mesh !!")
            return False

    refPoints = refShape.getPoints()
    targetPoints = targetShape.getPoints()

    weightMap = []

    for i in range(len(refPoints)):
        if i >= len(targetPoints):
            break

        xValue = refPoints[i][0] - offset
        if rightToLeft:
            if xValue < -treshold:
                weightMap.append(1.0)
            elif xValue < treshold:#in treshold
                weightMap.append(1 - ((xValue + treshold) / (2 * treshold)))
            else:
                weightMap.append(0.0)
        else:
            if xValue > treshold:
                weightMap.append(1.0)
            elif xValue > -treshold:#in treshold
                weightMap.append((xValue + treshold) / (2 * treshold))
            else:
                weightMap.append(0.0)

    _matchPointPositions(refShape, targetShape, weightMap, refPoints, targetPoints)

def matchPointPositionsFromInfluences(inRef, inTarget, inInfluences, inSkinGeometry=None):
    if not isinstance(inInfluences, (list, tuple)):
        inInfluences = (inInfluences,)

    skins = pc.listHistory(inInfluences[0], future=True, type="skinCluster")

    assert len(skins) > 0,"No skinning connected to given influences ({0})".format(inInfluences)

    if inSkinGeometry is None:
        inSkinGeometry = inTarget

        shape = inSkinGeometry.getShape()

        skinMatches = False
        for skin in skins:
            geos = skin.getGeometry()
            if shape in geos:
                skinMatches = True
                break

        if not skinMatches:
            inSkinGeometry = skins[0].getGeometry()[0].getParent()

    weightMap = []

    for influence in inInfluences:
        weights = tkc.getWeights(inSkinGeometry, influence)
        i = 0
        for weight in weights:
            if len(weightMap) <= i:
                weightMap.append(weight / 100.0)
            else:
                weightMap[i] += weight / 100.0
            i += 1

    _matchPointPositions(inRef, inTarget, weightMap)

def cutBsFromInfluences(inRef, inTarget, inInfluences, inSkinGeometry=None):
    results = []

    #Use specific "ref" geometry instead of the given one if it exists
    refShortName = inRef.stripNamespace().split("__")[0]
    if not inSkinGeometry is None and not inSkinGeometry.name().startswith(refShortName):
        
        inSkinGeometry = tkc.getNode(refShortName + "_" + inSkinGeometry.name()) or inSkinGeometry
        #print("Spec geo: {} {}".format(refShortName + "_" + inSkinGeometry.name(), inSkinGeometry))

    for influence in inInfluences:
        infMesh = duplicateAndClean(inTarget.name(), "{0}_{1}".format(inRef.name(), str(influence.stripNamespace())))
        node = pc.PyNode(infMesh)
        results.append(node)

        #print("FromInf : {} {} {} {}".format(inRef, node, influence, inSkinGeometry))

        matchPointPositionsFromInfluences(inRef, node, influence, inSkinGeometry=inSkinGeometry)

    return results

#cutLeftRight(pc.selected()[0], pc.selected()[1], 2.0)
def cutLeftRight(inRef, inTarget, treshold=2.0):
    if mc.objExists(inTarget.name() + "_Left"):
        mc.delete(inTarget.name() + "_Left")
    leftMesh = duplicateAndClean(inTarget.name(), inTarget.name() + "_Left")
    matchPointPositions(inRef, pc.PyNode(leftMesh), True, True, treshold=treshold)

    if mc.objExists(inTarget.name() + "_Right"):
        mc.delete(inTarget.name() + "_Right")
    rightMesh = duplicateAndClean(inTarget.name(), inTarget.name() + "_Right")
    matchPointPositions(inRef, pc.PyNode(rightMesh), True, False, treshold=treshold)

    return (leftMesh, rightMesh)

def getCorrectives(inPose=""):
    pattern = POSE_GRP_NAME
    if inPose != "":
        pattern = POSE_GRP_NAME.format(inPose)
    else:
        pattern = POSE_GRP_NAME.format("*")

    groups = mc.ls(pattern, transforms=True)

    correctives = {}

    editPattern = EDIT_MESH_NAME.format("(.*)", "{0}")
    for group in groups:
        poseName = inPose
        if inPose == "":
            searchObj = re.search( pattern.replace("*", "(.*)"), group)
            poseName = searchObj.groups(0)[0]

        correctives[poseName] = []
        children = mc.listRelatives(group, children=True)
        if children != None:
            for child in children:
                searchObj = re.search( editPattern.format(poseName), child)
                if searchObj:
                    meshName = searchObj.groups(0)[0]
                    correctives[poseName].append(meshName)

    return correctives

def getDeltasObjects(inPose=""):
    correctives = getCorrectives(inPose)

    deltas = []

    for pose in correctives.keys():
        for corrective in correctives[pose]:
            correcName = DELTA_MESH_NAME.format(corrective, pose)
            if mc.objExists(correcName + "_Left") or mc.objExists(correcName + "_Right"):
                if mc.objExists(correcName + "_Left"):
                    if not correcName + "_Left" in deltas:
                        deltas.append(correcName + "_Left")
                else:
                    mc.warning("{0} does not exist !!".format(correcName + "_Left"))

                if mc.objExists(correcName + "_Right"):
                    if not correcName + "_Right" in deltas:
                        deltas.append(correcName + "_Right")
                else:
                    mc.warning("{0} does not exist !!".format(correcName + "_Right"))
            else:
                if mc.objExists(correcName):
                    if not correcName in deltas:
                        deltas.append(correcName)
                else:
                    mc.warning("{0} does not exist !!".format(correcName))

    return deltas

def storeConnections(inNode):
    cons = []
    
    couples = pc.listConnections(inNode, connections=True, plugs=True)
    
    for couple in couples:
        inAlias = couple[0].name()
        outAlias = couple[1].name()
        doStore = False

        if ".weight[" in couple[0].name():
            inAlias = pc.aliasAttr(couple[0], query=True)
            if inAlias != "":
                inAlias = couple[0].node().name() + "." + inAlias
                doStore=True
            else:
                pc.warning("Cannot find alias for attribute {0}".format(couple[0].name()))

        if ".weight[" in couple[1].name():
            outAlias = pc.aliasAttr(couple[1], query=True)
            if outAlias != "":
                outAlias = couple[1].node().name() + "." + outAlias
                doStore=True
            else:
                pc.warning("Cannot find alias for attribute {0}".format(couple[1].name()))

        if doStore:
            cons.append((inAlias, outAlias))

    return cons

def resetConnections(inNode, inConnections):
    errors = "" 
    for couple in inConnections:
        try:
            mc.connectAttr(couple[1], couple[0], force=True)
        except Exception as e:
            errors += str(e) + "\r\n"

    return errors

def getRigMesh(inMeshName):
    rigMesh = inMeshName

    matchObj = re.match(EDIT_MESH_NAME.format("(.*)", "(.*)"), rigMesh)
    if matchObj:
        rigMesh = matchObj.groups(0)[0]

    if mc.objExists(rigMesh):
        return rigMesh

    meshes = mc.ls("*:{0}".format(rigMesh))
    if len(meshes) > 0:
        return meshes[0]

    return None

def plugMeshes(shape1, shape2):
    oldCons = mc.listConnections("{0}.inMesh".format(shape2))
    if oldCons == None or len(oldCons) == 0:
        mc.connectAttr("{0}.outMesh".format(shape1), "{0}.inMesh".format(shape2), force=True)

def muteDeformers(inMeshName):
    envelopes = {}
    defs = mc.listHistory(inMeshName, gl=True, pdo=True, lf=True, f=False, il=2)
    if defs != None:
        for deformer in defs:
            if pc.objExists(deformer):
                if mc.attributeQuery("envelope" , node=deformer, exists=True):
                    attrName = "{0}.envelope".format(deformer)
                    envelopes[deformer] = mc.getAttr(attrName)
                    mc.setAttr(attrName, 0.0)

    return envelopes

def restoreDeformers(inMeshName, inDeformers):
    for envelope in inDeformers.keys():
        if envelope != "":
            mc.setAttr("{0}.envelope".format(envelope), inDeformers[envelope])

def getOrCreateRefMesh(inMeshName):
    refMesh = MESH_REF_NAME.format(inMeshName)
    if mc.objExists(refMesh):
        return refMesh

    rigMesh = getRigMesh(inMeshName)
    if rigMesh == None:
        mc.warning("Can't get rig mesh for {0}".format(inMeshName))
        return None

    refMesh = duplicateAndClean(rigMesh, refMesh)
    pc.parent(refMesh, world=True)
    tkc.gator([pc.PyNode(refMesh)], pc.PyNode(rigMesh), inCopyMatrices=True, inDirectCopy=True)
    mc.setAttr("{0}.visibility".format(refMesh), False)

    #Replug in every inMesh ?

    return refMesh

def matchOneOf(inString, inPatterns):
    for pattern in inPatterns:
        if re.match(pattern, inString):
            return True

    return False

"""
import tkBlendShapes
reload(tkBlendShapes)

EYELASHESPOLYS = [941,942,943,944,945,946,947,948,949,950,951,952,953,1022,2114,2115,2116,2117,2118,2119,2120,2121,2122,2123,2124,2125,2126,2141]

tkBlendShapes.copyBS("mod:malik_body_Under_BS", "mod:malik_eyeLash_Under", inCreateBlendShape=False, inBsFilters=[".*Left_Upperblink_Dwn",".*Right_Upperblink_Dwn"], inPolySubSet=EYELASHESPOLYS, inPolySubSetReference="mod:malik_body")
"""

def copyBS(inBlendShape, inTarget, inCreateBlendShape=True, inDeleteTargets=True, inBsFilters=None, inPolySubSet=None, inPolySubSetReference=None, **kwargs):
    mc.undoInfo(openChunk=True)

    sourceMesh = getSource(inBlendShape)
    sourceTransform = mc.listRelatives(sourceMesh, parent=True)[0]
    envelopes = muteDeformers(sourceMesh)
    
    mc.setAttr("{0}.envelope".format(inBlendShape), 1.0)

    aliases = mc.aliasAttr(inBlendShape, query=True)

    #store and remove weight connections if we have any on targets
    weightAttrs = [aliases[i*2] for i in range(len(aliases)/2)]
    inBlendShapeNode = pc.PyNode(inBlendShape)
    cons = tkc.getNodeConnections(inBlendShapeNode, *weightAttrs, inDisconnect=True)

    #reset all targets
    oldValues = {}
    for weightAttr in weightAttrs:
        attrName = "{0}.{1}".format(inBlendShape, weightAttr)
        oldValues[attrName] = mc.getAttr(attrName)
        mc.setAttr(attrName, 0)

    targets = []
    for i in range(len(aliases)/2):
        alias = aliases[i*2]

        if inBsFilters is None or matchOneOf(alias, inBsFilters):
            dupe = duplicateAndClean(inTarget, alias)
            intermediate = None
            wraps = []

            if not inPolySubSet is None:
                sourceRef = inPolySubSetReference or sourceTransform

                nFaces = mc.polyEvaluate(sourceRef, face=True)
                intermediate = duplicateAndClean(sourceRef, sourceRef + "_intermediate")
                mc.delete(["{0}.f[{1}]".format(intermediate, i) for i in range(nFaces) if not i in inPolySubSet])

                #Wrap subset on sourceMesh
                mc.select([intermediate, sourceMesh], replace=True)
                pc.mel.eval("CreateWrap")
                wrap = None
                wraps.extend(mc.ls(mc.listHistory(intermediate, gl=True, pdo=True, lf=True, f=False, il=2), type="wrap"))

                #final Wrap
                mc.select([dupe, intermediate], replace=True)
                pc.mel.eval("CreateWrap")
                wrap = None
                wraps.extend(mc.ls(mc.listHistory(dupe, gl=True, pdo=True, lf=True, f=False, il=2), type="wrap"))
            else:
                mc.select([dupe, sourceMesh], replace=True)
                pc.mel.eval("CreateWrap")
                wrap = None
                wraps.extend(mc.ls(mc.listHistory(dupe, gl=True, pdo=True, lf=True, f=False, il=2), type="wrap"))

            if len(wraps) > 0:
                for wrap in wraps:
                    mc.setAttr("{0}.falloffMode".format(wrap), kwargs.get("falloffMode", 0))
                    mc.setAttr("{0}.autoWeightThreshold".format(wrap), 0)
                    mc.setAttr("{0}.maxDistance".format(wrap), 0)

                attrName = "{0}.{1}".format(inBlendShape, alias)
                mc.setAttr(attrName, 1.0)

                mc.delete(dupe , ch=True)
                if mc.objExists(sourceTransform + "Base"):
                    mc.delete(sourceTransform + "Base")

                if not intermediate is None:
                    mc.delete(intermediate)

                    if mc.objExists(intermediate + "Base"):
                        mc.delete(intermediate + "Base")

                mc.setAttr(attrName, 0.0)
                targets.append(dupe)
            else:
                mc.warning("Cannot find wrap !")
                mc.delete(dupe)

    bsNode = None

    if len(targets) > 0:
        if inCreateBlendShape:
            args = targets[:]
            args.append(inTarget)
            ns = ""
            if ":" in inTarget:
                ns = inTarget.split(":")[0]+":"
            bsNode = mc.blendShape(*args, name=ns + inBlendShape.split(":")[-1])

            if inDeleteTargets:
                mc.delete(targets)
    else:
        mc.warning("Cannot copy any targets !")

    #reset all targets
    for key in oldValues.keys():
        mc.setAttr(key, oldValues[key])

    #Restore weight connections
    tkc.setNodeConnections(cons)

    restoreDeformers(sourceMesh, envelopes)

    mc.undoInfo(closeChunk=True)

    return bsNode if inCreateBlendShape else targets

def editCorrective(inMeshName, inPose, inCharName, inKeySet):
    #drop ns
    inMeshName = inMeshName.split(":")[-1]

    correctives = getCorrectives(inPose="")

    rigMesh = getRigMesh(inMeshName)
    if rigMesh == None:
        mc.warning("Can't get rig mesh for {0}".format(inMeshName))
        return False

    grpName = POSE_GRP_NAME.format(inPose)
    if not inPose in correctives:
        mc.group(name=grpName, empty=True)

    editMeshName = EDIT_MESH_NAME.format(inMeshName, inPose)
    if not mc.objExists(editMeshName):
        #Make sure every controller/deformer is at 0 before duplication
        anim = tkRig.savePose(inCharName, inKeySet)
        tkRig.resetAll(inCharName, inKeySet)
        refMesh = getOrCreateRefMesh(inMeshName)
        
        editMesh = duplicateAndClean(refMesh, editMeshName)
        mc.parent(editMesh, grpName)
        plugMeshes(refMesh, editMesh)
        
        #Show edit mesh
        mc.setAttr("{0}.visibility".format(editMesh), True)

        tkRig.applyPose(anim)
    else:
        mc.select(editMeshName)

    #Manage visibilities
    for pose in correctives:
        mc.setAttr("{0}.visibility".format(POSE_GRP_NAME.format(pose)), pose == inPose)

    #Hide original mesh
    mc.setAttr("{0}.visibility".format(rigMesh), False)

    return True

def storeDeltas(inMeshName, inPose, inTreshold):
    rigMesh = getRigMesh(inMeshName)
    refMesh = getOrCreateRefMesh(inMeshName)

    editMeshName = EDIT_MESH_NAME.format(inMeshName, inPose)
    if not mc.objExists(editMeshName):
        mc.warning("Can't get corrective mesh ({0})".format(editMeshName))
        return False

    dupe = duplicateAndClean(editMeshName, "{0}_dupe".format(editMeshName))

    deltaMeshName = DELTA_MESH_NAME.format(inMeshName, inPose)
    if mc.objExists(deltaMeshName):
        mc.delete(deltaMeshName)

    deltaMesh = pc.extractDeltas(s=refMesh, c=dupe)
    mc.rename(deltaMesh, deltaMeshName)
    try:
        mc.parent(deltaMeshName, POSE_GRP_NAME.format(inPose))
    except:
        pass

    mc.delete(dupe)
    #Cut right/Left
    envelopes = muteDeformers(refMesh)
    cutLeftRight(pc.PyNode(refMesh), pc.PyNode(deltaMeshName), treshold=inTreshold)
    restoreDeformers(refMesh, envelopes)

    return True

def updateBs(inMeshName, suffix="_corrective_TestingBS"):
    rigMesh = getRigMesh(inMeshName)

    connections = []
    blendShapes = mc.ls(mc.listHistory(rigMesh, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
    for blendShape in blendShapes:
        if blendShape == rigMesh+suffix:
            connections = storeConnections(pc.PyNode(blendShape))
            mc.delete(blendShape)
            break

    deltas = getDeltasObjects()

    args = []
    for delta in deltas:
        if re.match(DELTA_MESH_NAME.format(inMeshName, "(.*)"), delta):
            args.append(delta)

    args.append(rigMesh)

    bs = mc.blendShape(*args, name=rigMesh+suffix)
    errors = resetConnections(bs, connections)

    if len(errors) > 0:
        pc.warning(errors)

    tkc.reorderDeformers(rigMesh)

def stopEditCorrective(inMeshName, inPose, inCharName, inKeySet, inTreshold=2.0, inStore=True):
    print ("stopEditCorrective store ?", inStore)
    #drop ns
    inMeshName = inMeshName.split(":")[-1]

    correctives = getCorrectives(inPose="")

    rigMesh = getRigMesh(inMeshName)

    if rigMesh == None:
        mc.warning("Can't get rig mesh for {0}".format(inMeshName))
        return False

    inMeshName = rigMesh.split(":")[-1]

    if not inStore:
        #Manage visibilities
        for pose in correctives:
            mc.setAttr("{0}.visibility".format(POSE_GRP_NAME.format(pose)), False)

        #Show original mesh
        mc.setAttr("{0}.visibility".format(rigMesh), True)
        mc.select(rigMesh)
        return True

    #Store delta
    if not storeDeltas(inMeshName, inPose, inTreshold):
        return False

    #Manage visibilities
    for pose in correctives:
        mc.setAttr("{0}.visibility".format(POSE_GRP_NAME.format(pose)), False)

    #Update/create targets on original mesh
    updateBs(inMeshName)

    #Show original mesh
    mc.setAttr("{0}.visibility".format(rigMesh), True)
    mc.select(rigMesh)

    return True

def exportBS(inCharName, projectPath, assetName, modPattern, skippedAttrList=""):
    print ("tkBlendShapes.exportBS(inCharName='"+inCharName+"', projectPath='"+projectPath+"', assetName='"+assetName+"', modPattern='"+modPattern+"', skippedAttrList='"+skippedAttrList+"')")
    deltas = getDeltasObjects(inPose="")

    if len(deltas) == 0:
        return "Can't find any correctives"

    geoFolder = os.path.join(projectPath, "Assets", assetName, "Data")

    if not os.path.isdir(geoFolder):
        return "Geo folder does not exists !! ({0})".format(geoFolder)

    filePattern = modPattern.replace("$ASSETNAME", assetName)

    geoFile = None
    for fileCandidate in os.listdir(geoFolder):
        if fnmatch.fnmatch(fileCandidate, filePattern):
            geoFile = fileCandidate

    if geoFile == None:
        return "Can't find file with pattern '{0}' in '{1}'".format(filePattern, geoFolder)

    path = os.path.join(geoFolder, geoFile)

    mc.select(deltas)

    ext = os.path.splitext(geoFile)[1]

    pc.system.exportSelected(path.replace(ext, "_CorrectivesDeltas"+ext), type="mayaAscii", force=True, constructionHistory=True, channels=True, constraints=True, expressions=True, shader=True, preserveReferences=True)

    rslt = mc.confirmDialog( title='Geo model opening', message="Geo scene will be opened for integration, do you want to save current scene ?", button=['Yes','No', 'Cancel'], defaultButton='Yes', cancelButton='Cancel', dismissString='Cancel' )
    
    if rslt == "Cancel":
        return "Cancelled by user (Correctives were exported to '{0}')".format(path.replace(ext, "_CorrectivesDeltas"+ext))

    if rslt == "Yes":
        currentScene = os.path.abspath(mc.file(q=True, sn=True))
        if not os.path.isfile(currentScene):
            return "File is not saved ! Exiting  (Correctives were exported to '{0}')".format(path.replace(ext, "_CorrectivesDeltas"+ext))
        
        pc.system.saveAs(currentScene, force=True)

    pc.system.openFile(path, force=True)

    pc.system.importFile(path.replace(ext, "_CorrectivesDeltas"+ext))

    objs_deltas = {}

    ns = os.path.splitext(geoFile)[0]

    cnt = 0
    for delta in deltas:
        matchObj = re.match(DELTA_MESH_NAME.format("(.*)", "(.*)"), delta)
        if matchObj:
            obj = matchObj.groups(0)[0]
            pose = matchObj.groups(0)[1]

            fullName = ns+":"+obj
            if mc.objExists(fullName):
                if not fullName in objs_deltas:
                    objs_deltas[fullName] = {"poses":{}, "name":obj}

                if not pose in objs_deltas[fullName]["poses"]:
                    objs_deltas[fullName]["poses"][pose] = {"deltas":[]}

                objs_deltas[fullName]["poses"][pose]["deltas"].append(delta)
                cnt+=1

    for obj in objs_deltas.keys():
        deltas = objs_deltas[obj]

        connections = []

        bsNode = None

        blendShapes = mc.ls(mc.listHistory(obj, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
        for blendShape in blendShapes:
            if blendShape == obj+"_correctiveBS":
                connections = storeConnections(pc.PyNode(blendShape))
                #pc.delete(blendShape)
                bsNode = blendShape
                break

        shapesNames = []
        for pose in deltas["poses"].keys():
            for i in range(len(deltas["poses"][pose]["deltas"])):
                shapeName = deltas["name"] + "_" + pose
                #print obj, shapeName
                shapeName = deltas["poses"][pose]["deltas"][i].replace(DELTA_MESH_NAME.format(deltas["name"], pose), shapeName)
                shapeName = mc.rename(deltas["poses"][pose]["deltas"][i], shapeName)
                shapesNames.append(shapeName)

        args = shapesNames[:]
        args.append(obj)

        if bsNode == None:
            bsNode = mc.blendShape(*args, name=obj+"_correctiveBS")[0]
        else:
            for shapeName in shapesNames:
                #rename target to avoid name clash
                index = getBSIndexFromTarget(bsNode, shapeName)
                if index != None:#Reuse target
                    #print "Shape",shapeName,"already exists, reuse !"
                    shapeDupeName = mc.rename(shapeName, shapeName + "_RENAMED")
                    shape = editTarget(bsNode, shapeName)
                    matchPointPositions(pc.PyNode(shapeDupeName), pc.PyNode(shape))
                    mc.delete(shape.name())
                    mc.rename(shapeDupeName, shapeName)
                else:#New target
                    #print "Shape",shapeName,"does not exists, create !"
                    nextFreeIndex = getFirstAvailableIndex(bsNode)
                    mc.blendShape(obj, edit=True, target=[obj, nextFreeIndex, shapeName, 1.0])

        mc.delete(shapesNames)

        tkc.reorderDeformers(obj)

        resetConnections(obj+"_correctiveBS", connections)

        rootName = filePattern.split(".")[0]
        skippedAttrs = skippedAttrList.split("|")

        root = pc.PyNode("{0}:{0}_Root".format(rootName))
        for shapeName in shapesNames:
            realAttrName = shapeName.replace(obj.split(":")[-1] + "_", "")
            #print "realAttrName",realAttrName
            if skippedAttrs == None or not realAttrName in skippedAttrs:
                realName = tkc.addParameter(inobject=root, name=ns + "_" + realAttrName, inType="double", default=0, min=-1, max = 2, softmin=0, softmax=1, nicename="", expose=True, containerName="RigParameters", readOnly=False, booleanType=0, skipIfExists=True)
                try:
                    mc.connectAttr(realName, bsNode + "." + shapeName, force=True)
                except:
                    pass

    roots = mc.ls(POSE_GRP_NAME.format("*"), transforms=True)

    if len(roots) > 0:
        mc.delete(roots)

    return "Successfully added {0} blendShape targets on {1} objects ({2})".format(cnt, len(objs_deltas), ",".join(objs_deltas.keys()))

def updateScene(inTreshold=2.0):
    correctives = getCorrectives()

    meshes = []

    nRebuilds = 0

    for poseName, meshList in correctives.items():
        for mesh in meshList:
            nRebuilds += 1
            if not mesh in meshes:
                meshes.append(mesh)

    steps = nRebuilds*2 + len(meshes) * 2

    if steps > 0:
        gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')
        pc.progressBar( gMainProgressBar,
            edit=True,
            beginProgress=True,
            isInterruptable=True,
            status="Rebuilding correctives",
            maxValue=steps )
            
        #Rebuild refMeshes
        print ("Rebuild refMeshes")
        for mesh in meshes:
            refMesh = MESH_REF_NAME.format(mesh)
            rigMesh = getRigMesh(mesh)
            print (" - Rebuild " + MESH_REF_NAME.format(mesh))
            pc.progressBar(gMainProgressBar, edit=True, step=1)
            
            if mc.objExists(refMesh):
                #mc.delete(refMesh)
                tkc.gator([pc.PyNode(refMesh)], pc.PyNode(rigMesh), inCopyMatrices=True, inDirectCopy=True)
            else:
                getOrCreateRefMesh(mesh)

        #Rebuild correctives
        print ("Rebuild correctives")
        for mesh in meshes:
            refMeshName = MESH_REF_NAME.format(mesh)
            for poseName, meshList in correctives.items():
                if mesh in meshList:
                    editMeshName = EDIT_MESH_NAME.format(mesh, poseName)
                    print (" - Rebuild " + editMeshName)
                    plugMeshes(refMeshName, editMeshName)
                    
                    correcName = DELTA_MESH_NAME.format(mesh, poseName)
                    print ("    - Extract " + correcName)
                    pc.progressBar(gMainProgressBar, edit=True, step=2)
                    
                    storeDeltas(mesh, poseName, inTreshold)
            
            pc.progressBar(gMainProgressBar, edit=True, step=1)
            updateBs(mesh)

        pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

#Constants
DEFAULT_SHORT_TRESHOLD = .15
DEFAULT_MID_TRESHOLD = .3
DEFAULT_WIDE_TRESHOLD = 1.3

SHORT_TRESHOLD = DEFAULT_SHORT_TRESHOLD
MID_TRESHOLD = DEFAULT_MID_TRESHOLD
WIDE_TRESHOLD = DEFAULT_WIDE_TRESHOLD

#Constants, functions needs to take strings and not nodes, just an example (from WRT)
'''
BS = [
    {"source":"brow_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_browA"), tkc.getNode("L_browB"), tkc.getNode("L_browC"), tkc.getNode("L_browD"), tkc.getNode("L_browE")), tkc.getNode("L_browCut")), "outputs":[{},{},{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_browA"), tkc.getNode("R_browB"), tkc.getNode("R_browC"), tkc.getNode("R_browD"), tkc.getNode("R_browE")), tkc.getNode("R_browCut")), "outputs":[{},{},{},{},{}]},
    ]},
    {"source":"brow_In",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"brow_Out",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"brow_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_browA"), tkc.getNode("L_browB"), tkc.getNode("L_browC"), tkc.getNode("L_browD"), tkc.getNode("L_browE")), tkc.getNode("L_browCut")), "outputs":[{},{},{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_browA"), tkc.getNode("R_browB"), tkc.getNode("R_browC"), tkc.getNode("R_browD"), tkc.getNode("R_browE")), tkc.getNode("R_browCut")), "outputs":[{},{},{},{},{}]},
    ]},

    {"source":"cheekBone_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_cheekBoneA"), tkc.getNode("L_cheekBoneB"), tkc.getNode("L_cheekBoneC")), tkc.getNode("cheekBoneCut")), "outputs":[{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_cheekBoneA"), tkc.getNode("R_cheekBoneB"), tkc.getNode("R_cheekBoneC")), tkc.getNode("cheekBoneCut")), "outputs":[{},{},{}]},
    ]},
    {"source":"cheekBone_In",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"cheekBone_Out",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"cheekBone_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_cheekBoneA"), tkc.getNode("L_cheekBoneB"), tkc.getNode("L_cheekBoneC")), tkc.getNode("cheekBoneCut")), "outputs":[{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_cheekBoneA"), tkc.getNode("R_cheekBoneB"), tkc.getNode("R_cheekBoneC")), tkc.getNode("cheekBoneCut")), "outputs":[{},{},{}]},
    ]},

    {"source":"cheek_Bw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"cheek_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"cheek_Fw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"cheek_In",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"cheek_Out",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"cheek_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},

    {"source":"chin_Dn" },
    {"source":"chin_Up" },

    {"source":"jawMuscle",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"jawSide_Lft" },
    {"source":"jawSide_Rgt" },
    {"source":"jaw_Bw" },
    {"source":"jaw_Dn" }, 
    {"source":"jaw_Fw" },
    {"source":"jaw_Up" },

    {"source":"lowerEyelid_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_eyeLidA"), tkc.getNode("L_eyeLidB"), tkc.getNode("L_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_eyeLidA"), tkc.getNode("R_eyeLidB"), tkc.getNode("R_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
    ]},
    {"source":"lowerEyelid_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_eyeLidA"), tkc.getNode("L_eyeLidB"), tkc.getNode("L_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_eyeLidA"), tkc.getNode("R_eyeLidB"), tkc.getNode("R_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
    ]},
    
    {"source":"lowerLipCenter_Dn" },
    {"source":"lowerLipCenter_Up" },

    {"source":"lowerLipCorner_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLipCorner_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLipCurl_Bw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLipCurl_Fw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLipPuff_Bw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLipPuff_Fw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLipSide_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLipSide_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},

    {"source":"lowerLip_Bw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    #{"source":"lowerLip_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"lowerLip_Fw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    #{"source":"lowerLip_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},

    {"source":"mouthCorner_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"mouthCorner_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"mouthRot_Ng" },
    {"source":"mouthRot_Ps" },
    {"source":"mouthSide_Lft" },
    {"source":"mouthSide_Rgt" },
    {"source":"mouth_Dn" },
    {"source":"mouth_In",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"mouth_Out",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"mouth_Up" },

    {"source":"neck",      "function":(cutLeftRight, "$targetNode", "$sourceNode", WIDE_TRESHOLD), "outputs":[{},{}]},
    {"source":"neckSide",      "function":(cutLeftRight, "$targetNode", "$sourceNode", WIDE_TRESHOLD), "outputs":[{},{}]},

    {"source":"noseDilate_In",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"noseDilate_Out",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"nose_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"nose_In",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"nose_Out",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"nose_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},

    {"source":"pinch",          "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_pinchA"), tkc.getNode("L_pinchB"), tkc.getNode("L_pinchC"), tkc.getNode("L_pinchD"), tkc.getNode("L_pinchE"), tkc.getNode("L_pinchF"), tkc.getNode("L_pinchG"), tkc.getNode("L_pinchH")), tkc.getNode("L_pinchCut")), "outputs":[{},{},{},{},{},{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_pinchA"), tkc.getNode("R_pinchB"), tkc.getNode("R_pinchC"), tkc.getNode("R_pinchD"), tkc.getNode("R_pinchE"), tkc.getNode("R_pinchF"), tkc.getNode("R_pinchG"), tkc.getNode("R_pinchH")), tkc.getNode("R_pinchCut")), "outputs":[{},{},{},{},{},{},{},{}]},
    ]},

    {"source":"snear_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},
    {"source":"snear_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[{},{}]},

    {"source":"upperEyelid_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_eyeLidA"), tkc.getNode("L_eyeLidB"), tkc.getNode("L_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_eyeLidA"), tkc.getNode("R_eyeLidB"), tkc.getNode("R_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
    ]},
    {"source":"upperEyelid_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", SHORT_TRESHOLD), "outputs":[
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("L_eyeLidA"), tkc.getNode("L_eyeLidB"), tkc.getNode("L_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
        {"function":(cutBsFromInfluences, "$sourceNode", "$targetNode", (tkc.getNode("R_eyeLidA"), tkc.getNode("R_eyeLidB"), tkc.getNode("R_eyeLidC")), tkc.getNode("eyeLidCut")), "outputs":[{},{},{}]},
    ]},

    {"source":"upperLipCenter_Dn" },
    {"source":"upperLipCenter_Up" },

    {"source":"upperLipCorner_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"upperLipCorner_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"upperLipCurl_Bw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"upperLipCurl_Fw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"upperLipPuff_Bw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"upperLipPuff_Fw",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"upperLipSide_Dn",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
    {"source":"upperLipSide_Up",      "function":(cutLeftRight, "$targetNode", "$sourceNode", MID_TRESHOLD), "outputs":[{},{}]},
]
'''

def addBS(inObjects=None, inBetweenName=None, inBetweenValue=0.5, inComboShapes=None, inComboValus=None):
    tkc.storeSelection()
    if inObjects is None:
        inObjects = pc.selected()
    else:
        pc.select(inObjects)

    inTarget = inObjects[-1]
    blenshapes = inObjects[0:-1]
    
    ns = str(inTarget.namespace())
    if ":" in ns:
        ns = ns.replace(":", "")

    rigParamsName = ns + ":" + ns + "_Root_RigParameters"
    rigParams = None

    if not pc.objExists(rigParamsName):
        
        hierarchy = [
            {
            "name"      :ns + ":Geometries",
            "type"      :"locator",
            "parent"    :ns+":"+ns,
            "groups"    :[ns+":Hidden", ns+":Unselectable"],
            },
            {
            "name"      :ns + ":" + ns + "_Root",
            "type"      :"locator",
            "parent"    :ns + ":Geometries",
            "groups"    :[ns+":Hidden", ns+":Unselectable"],
            },
            {
            "name"      :ns + ":" + ns + "_Root_RigParameters",
            "type"      :"transform",
            "parent"    :ns + ":" + ns + "_Root",
            "groups"    :[ns+":Hidden", ns+":Unselectable"],
            "attrs"     :[
                    {"name":"tx", "type":"float", "value":None, "keyable":False},
                    {"name":"ty", "type":"float", "value":None, "keyable":False},
                    {"name":"tz", "type":"float", "value":None, "keyable":False},

                    {"name":"rx", "type":"float", "value":None, "keyable":False},
                    {"name":"ry", "type":"float", "value":None, "keyable":False},
                    {"name":"rz", "type":"float", "value":None, "keyable":False},

                    {"name":"sx", "type":"float", "value":None, "keyable":False},
                    {"name":"sy", "type":"float", "value":None, "keyable":False},
                    {"name":"sz", "type":"float", "value":None, "keyable":False},

                    {"name":"visibility", "type":"bool", "value":False, "keyable":False},
                    {"name":"inheritsTransform", "type":"bool", "value":False, "keyable":False},
                ],
            },
        ]

        hi = tkRig.buildHierarchy(hierarchy)
        rigParams = hi[ns + ":" + ns + "_Root_RigParameters"]["node"]

        pc.select(inObjects)
    else:
        rigParams = pc.PyNode(rigParamsName)

    bsName = inTarget.name() + "_BS"
    bsExists = pc.objExists(bsName)
    bsNode = None
    if not bsExists:

        bsNode = pc.blendShape(name=bsName)[0]
    else:
        bsNode = pc.PyNode(bsName)

    for blenshape in blenshapes:
        if bsExists:
            #Add target

            if not inBetweenName is None:
                #Find in between target
                index = getBSIndexFromTarget(bsName, inBetweenName)
                if index != None:
                    pc.blendShape(bsNode, edit=True, ib=True, t=(inTarget.name(), index, blenshape, inBetweenValue))
                else:
                    pc.warning("Cant find index of target '{0}' on {1}".format(inBetweenName, bsName))
            
            elif not inComboShapes is None:
                # ApplyPose
                pc.setAttr(SHAPES_PARAM_FORMAT.format(rigParamsName, ns, inComboShapes[0]), inComboValus[0])
                pc.setAttr(SHAPES_PARAM_FORMAT.format(rigParamsName, ns, inComboShapes[1]), inComboValus[1])
                # Extract Deltas
                print("extractDelta {} {}".format(inTarget, blenshape))
                deltaMesh = tkc.getNode(pc.extractDeltas(s=inTarget.name(), c=blenshape.name()))
                deltaMesh = deltaMesh.rename(inComboShapes[0]+"_"+inComboShapes[1]+"_Combo")
                # ResetPose
                pc.setAttr(SHAPES_PARAM_FORMAT.format(rigParamsName, ns, inComboShapes[0]), 0)
                pc.setAttr(SHAPES_PARAM_FORMAT.format(rigParamsName, ns, inComboShapes[1]), 0)
                #add Target
                indices = bsNode.weightIndexList()
                index = indices[-1] + 1 if len(indices) > 0 else 0
                pc.blendShape(bsNode, edit=True, t=(inTarget.name(), index, deltaMesh, 1.0))

                # Normalize pose 1 activator if reference value is not 1
                poseAttr1 = SHAPES_PARAM_FORMAT.format(rigParamsName, ns, inComboShapes[0])
                poseAttr1Norm = poseAttr1
                if inComboValus[0] != 1:
                    poseAttr1Norm = tkn.mul(poseAttr1, 1.0 / float(inComboValus[0]))

                poseAttr2 = SHAPES_PARAM_FORMAT.format(rigParamsName, ns, inComboShapes[1])
                poseAttr2Norm = poseAttr2
                if inComboValus[1] != 1:
                    poseAttr2Norm = tkn.mul(poseAttr2, 1.0/ float(inComboValus[1]))
                
                # Create Combinatory weight based on the maximum value of both activators
                combi =  tkn.mul(tkn.clamp(poseAttr1Norm, inMin=0.0, inMax=poseAttr2Norm), -1)
                combi >> bsNode.attr(deltaMesh.name())

            else:
                #Find existing shape index
                index = getBSIndexFromTarget(bsName, blenshape)
                if not index is None:
                    shape = cmds.listRelatives(blenshape.name(), shapes=True, ni=True, path=True)[0]
                    cmds.connectAttr(shape + ".worldMesh[0]", bsName + ".inputTarget[0].inputTargetGroup["+str(index)+"].inputTargetItem[6000].inputGeomTarget", force=True)
                    cmds.disconnectAttr(shape + ".worldMesh[0]", bsName + ".inputTarget[0].inputTargetGroup["+str(index)+"].inputTargetItem[6000].inputGeomTarget")
                else:
                    #First available index
                    indices = bsNode.weightIndexList()
                    index = indices[-1] + 1 if len(indices) > 0 else 0
                    pc.blendShape(bsNode, edit=True, t=(inTarget.name(), index, blenshape, 1.0))
        
        shapeShortName = str(blenshape.stripNamespace())

        bsAttrName = shapeShortName

        if bsAttrName.startswith("{0}__".format(inTarget.stripNamespace())):
            bsAttrName = bsAttrName[len(inTarget.stripNamespace()) + 2:]

        if bsAttrName.startswith("{0}_".format(inTarget.stripNamespace())):
            bsAttrName = bsAttrName[len(inTarget.stripNamespace()) + 1:]

        if inBetweenName is None and inComboShapes is None and not rigParams is None:
            attrName = "{0}.{1}".format(rigParams.name(), ns + "_" + bsAttrName)
            if not pc.objExists(attrName):
                attrName = tkc.addParameter(rigParams, ns + "_" + bsAttrName)
            
            pc.PyNode(attrName) >> bsNode.attr(shapeShortName)

    tkc.loadSelection()

def bsOperations(inPreset, inTarget, inSource=None, inDryRun=False, inSkipCuts=False):
    source = inPreset.get("source", inSource)
    sourceNode = tkc.getNode(source)

    target = inTarget
    targetNode = tkc.getNode(target)

    func = inPreset.get("function")

    results = []

    if not inSkipCuts and not func is None:
        args = list(func[1:])

        for i in range(len(args)):
            if args[i] == "$target":
                args[i] = target
            elif args[i] == "$targetNode":
                args[i] = targetNode
            if args[i] == "$source":
                args[i] = source
            elif args[i] == "$sourceNode":
                args[i] = sourceNode

        outs = []
        outsNumber = len(inPreset["outputs"])
        
        if inDryRun:
            print("DRYRUN | {0}({1}) would have been called and returned {2} results".format(func[0].__name__, ",".join([str(args) for arg in args]), outsNumber))
            outs = [targetNode] * outsNumber
        else:
            outs = func[0](*args)

        for i in range(len(inPreset["outputs"])):
            out = outs[i]
            outPreset = inPreset["outputs"][i]

            results.extend(tkc.getNodes(bsOperations(outPreset, inTarget, inSource=out, inDryRun=inDryRun)))
    else:
        return [tkc.getNode(source)]

    return results

INBETWEEN_PATTERN = r".*__((?:\d_\d+)|\d)"
COMBO_PATTERN = r"(.*)__((?:\d_\d+)|\d)__(.*)__((?:\d_\d+)|\d)"
def integrateBS(inPreset=[], inTargetsDict={}, inVerbose=False, inDryRun=False, inSkipCuts=False):
    inTargetsDict = inTargetsDict or {}

    finalTargets = {}
    
    gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

    pc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Integrate BS...",
    maxValue=len(inPreset) + 1)

    for bsPreset in inPreset:
        source = bsPreset["source"]

        foundAShape = False

        targetCandidates = pc.ls(["*:*__{0}".format(source), "*__{0}".format(source)], transforms=True)

        for targetCandidate in targetCandidates:
            if targetCandidate.getShape() is None:
                continue

            if not targetCandidate.getShape().type() in ["mesh", "nurbsSurface"]:
                continue

            targetName = targetCandidate.name()[:-(len(source) + 2)]
            targetNode = tkc.getNode(targetName, inConsiderNs=True)

            if not targetNode is None:
                target = targetNode.name()

                if not target in finalTargets:
                    finalTargets[target] = []
                
                foundAShape=True

                bsThisPreset = bsPreset.copy()
                bsThisPreset["source"] = targetCandidate.name()
                meshes = bsOperations(bsThisPreset, target, inDryRun=inDryRun, inSkipCuts=inSkipCuts)

                if len(meshes) > 0:
                    finalTargets[target].extend(meshes)

            else:
                pc.warning("Can't find target mesh '{0}'".format(targetName))

            #Autodetect inbetweens and combos
            siblings = pc.ls(targetCandidate.name()+"__*", transforms=True)
            
            for sibling in siblings:
                shortName = sibling.name()[len(targetName) + 2:]
                if re.match(COMBO_PATTERN, shortName) or re.match(INBETWEEN_PATTERN, shortName):
                    subPreset = bsPreset.copy()
                    subPreset["source"] = sibling.name()

                    meshes = bsOperations(subPreset, target, inDryRun=inDryRun, inSkipCuts=inSkipCuts)

                    if len(meshes) > 0:
                        finalTargets[target].extend(meshes)

        if not foundAShape:
            pc.warning("No targets found for shape '{0}'".format(source))

        pc.progressBar(gMainProgressBar, edit=True, step=1)

    for targetName, blendShapes in finalTargets.items():
        target = pc.PyNode(targetName)

        if inDryRun:
            print("DRYRUN | target:{0}, shapes:{1}".format(targetName, blendShapes))
            continue

        renamings = {}

        inBetweens = []
        inCombos = []

        realBlendShapes = []

        for blendShape in blendShapes:
            renamings[blendShape.name()] = blendShape

            for origName, newName in inTargetsDict.items():
                if origName in blendShape.name():
                    blendShape.rename(blendShape.name().replace(origName, newName))
                    break

            #remove target prefix
            blendShape.rename(blendShape.name().replace(str(target.stripNamespace()) + "__", ""))
            inCombosMatch = re.match(COMBO_PATTERN, blendShape.name())
            inBetweenMatch = re.match(INBETWEEN_PATTERN, blendShape.name())
            
            #Manage inBetweens
            if inCombosMatch:
                #print("inCombosMatch")
                if inVerbose:
                    print(" name " + blendShape.name())
                activator1 = inCombosMatch.groups()[0] + blendShape.name()[inCombosMatch.end(4):]
                activator2 = inCombosMatch.groups()[2] + blendShape.name()[inCombosMatch.end(4):]
                value1 = eval(inCombosMatch.groups()[1].replace("_", "."))
                value2 = eval(inCombosMatch.groups()[3].replace("_", "."))
                if inVerbose:
                    print(" Combo from Shape " + activator1 + " " + activator2)
                    print(" values " + str(value1) + " " + str(value2))
                inCombos.append((blendShape, activator1, activator2, value1, value2))
            elif inBetweenMatch:
                print("inBetweenMatch")
                if inVerbose:
                    print(" name" + blendShape.name())
                refBsName = blendShape.name()[:inBetweenMatch.start(1)-2] + blendShape.name()[inBetweenMatch.end(1):]
                if inVerbose:
                    print(" refBs " + refBsName)
                value = eval(inBetweenMatch.groups()[0].replace("_", "."))
                if inVerbose:
                    print(" value " + str(value))
                    print("")
                inBetweens.append((blendShape, refBsName, value))
            else:
                realBlendShapes.append(blendShape)

        addBS(realBlendShapes + [target])

        #Integrate inBetweens
        for inBetween, inBetweenName, inBetweenValue in inBetweens:
            addBS([inBetween, target], inBetweenName, inBetweenValue)

        #Integrate combos
        for inBlendShape, comboShape1, comboShape2, value1, value2 in inCombos:
            addBS([inBlendShape, target], inComboShapes=(comboShape1, comboShape2), inComboValus=(value1, value2))

        #Restore original names
        for origName, mesh in renamings.items():
            mesh.rename(origName)

    pc.progressBar(gMainProgressBar, edit=True, step=1)
    pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

def buildBSScene(inPreset=[], inSourceObjs=None, inOffset=[20.0, 0.0, 0.0]):
    """TODO : cuts ?"""
    if inSourceObjs is None:
        inSourceObjs = [n.name() for n in pc.ls(sl=True)]

    gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')
    pc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Build BS scene",
    maxValue=len(inPreset) * len(inSourceObjs))

    cutsInfo = []

    step = inOffset[:]
    for bsPreset in inPreset:
        source = bsPreset["source"]

        for sourceObj in inSourceObjs:
            targetName = sourceObj + "__" + source
            if not pc.objExists(targetName):
                dupe = tkbs.duplicateAndClean(sourceObj, inTargetName=targetName)
                pc.move(*step, dupe, r=True)

            pc.progressBar(gMainProgressBar, edit=True, step=1)
        
        for i in range(3):
            step[i] += inOffset[i]


    pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

#integrateBS call
'''
result = pc.promptDialog(
        title="Threshold multiplier",
        message="Left/Right cuts presets were set on Heimer, modify this multpiplier if needed",
        text="1.0",
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
if result == 'OK':
    value = pc.promptDialog(query=True, text=True)

    factor = None

    try:
        factor = float(value)
    except:
        pass

    if not factor is None and factor > 0.0:
        SHORT_TRESHOLD = DEFAULT_SHORT_TRESHOLD * factor
        MID_TRESHOLD = DEFAULT_MID_TRESHOLD * factor
        WIDE_TRESHOLD = DEFAULT_WIDE_TRESHOLD * factor

        print("Using thresholds : {} {} {}".format(SHORT_TRESHOLD, MID_TRESHOLD, WIDE_TRESHOLD))
        integrateBS(inPreset=BS, inSkipCuts=False)
    else:
        pc.warning("Can't read value '{0}' as valid float multiplier !. Aborting...")
'''