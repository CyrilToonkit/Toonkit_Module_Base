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
import fnmatch

import maya.cmds as mc
import pymel.core as pc

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

    for i in range(len(aliases)/2):
        alias = [aliases[2*i], aliases[2*i+1]]
        if alias[1] == "weight[{0}]".format(inIndex):
            return alias[0]

    return None

def getBSIndexFromTarget(inBlendShape, inTarget):
    reg = re.compile("weight\\[([0-9]+)\\]")
    aliases = mc.aliasAttr(inBlendShape, query=True)

    for i in range(len(aliases)/2):
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
        print target
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
        print "Target mesh already connected : {0}".format(targetMeshes[0])
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

def duplicateAndClean(inSourceMesh, inTargetName="$REF_dupe", inMuteDeformers=True, inMaterials=False):
    #Make sure every deformer is at 0 before duplication
    envelopes = {}
    if inMuteDeformers:
        envelopes = muteDeformers(inSourceMesh)
    
    dupe = mc.duplicate(inSourceMesh, rr=True)[0]

    if '$REF' in inTargetName:
        inTargetName = inTargetName.replace('$REF', inSourceMesh)

    dupe = mc.rename(dupe, inTargetName)
    
    shapes = mc.listRelatives(dupe, shapes=True)
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
    if inSkinGeometry is None:
        inSkinGeometry = inTarget

    if not isinstance(inInfluences, (list, tuple)):
        print "inInfluences is not a list !"
        inInfluences = (inInfluences,)

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

def _matchPointPositions(inRef, inTarget, inMap=None, inRefPoints=None, inTargetPoints=None):
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

    refPoints = inRefPoints or refShape.getPoints()
    targetPoints = inTargetPoints or targetShape.getPoints()

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

    targetShape.setPoints(targetPoints)
    return True

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
        except Exception, e:
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

def copyBS(inBlendShape, inTarget):
    mc.undoInfo(openChunk=True)

    sourceMesh = getSource(inBlendShape)
    sourceTransform = mc.listRelatives(sourceMesh, parent=True)[0]
    envelopes = muteDeformers(sourceMesh)
    
    mc.setAttr("{0}.envelope".format(inBlendShape), 1.0)

    aliases = mc.aliasAttr(inBlendShape, query=True)

    #reset all targets
    oldValues = {}
    for i in range(len(aliases)/2):
        attrName = "{0}.{1}".format(inBlendShape, aliases[i*2])
        oldValues[attrName] = mc.getAttr(attrName)
        mc.setAttr(attrName, 0)

    targets = []
    for i in range(len(aliases)/2):
        alias = aliases[i*2]
        dupe = duplicateAndClean(inTarget, alias)
        mc.select([dupe, sourceMesh], replace=True)
        pc.mel.eval("CreateWrap")
        wrap = None
        wraps = mc.ls(mc.listHistory(dupe, gl=True, pdo=True, lf=True, f=False, il=2), type="wrap")
        if len(wraps) > 0:
            wrap = wraps[0]
            mc.setAttr("{0}.falloffMode".format(wrap), 0)
            mc.setAttr("{0}.autoWeightThreshold".format(wrap), 0)
            mc.setAttr("{0}.maxDistance".format(wrap), 0)

            attrName = "{0}.{1}".format(inBlendShape, alias)
            mc.setAttr(attrName, 1.0)
            mc.delete(dupe , ch=True)
            if mc.objExists(sourceTransform + "Base"):
                mc.delete(sourceTransform + "Base")
            mc.setAttr(attrName, 0.0)
            targets.append(dupe)
        else:
            mc.warning("Cannot find wrap !")
            mc.delete(dupe)

    if len(targets) > 0:
        args = targets[:]
        args.append(inTarget)
        ns = ""
        if ":" in inTarget:
            ns = inTarget.split(":")[0]+":"
        mc.blendShape(*args, name=ns + inBlendShape.split(":")[-1])
        mc.delete(targets)
    else:
        mc.warning("Cannot copy any targets !")

    #reset all targets
    for key in oldValues.keys():
        mc.setAttr(key, oldValues[key])

    restoreDeformers(sourceMesh, envelopes)

    mc.undoInfo(closeChunk=True)

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
    print "stopEditCorrective store ?", inStore
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
    print "tkBlendShapes.exportBS(inCharName='"+inCharName+"', projectPath='"+projectPath+"', assetName='"+assetName+"', modPattern='"+modPattern+"', skippedAttrList='"+skippedAttrList+"')"
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

    for poseName, meshList in correctives.iteritems():
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
        print "Rebuild refMeshes"
        for mesh in meshes:
            refMesh = MESH_REF_NAME.format(mesh)
            rigMesh = getRigMesh(mesh)
            print " - Rebuild " + MESH_REF_NAME.format(mesh)
            pc.progressBar(gMainProgressBar, edit=True, step=1)
            
            if mc.objExists(refMesh):
                #mc.delete(refMesh)
                tkc.gator([pc.PyNode(refMesh)], pc.PyNode(rigMesh), inCopyMatrices=True, inDirectCopy=True)
            else:
                getOrCreateRefMesh(mesh)

        #Rebuild correctives
        print "Rebuild correctives"
        for mesh in meshes:
            refMeshName = MESH_REF_NAME.format(mesh)
            for poseName, meshList in correctives.iteritems():
                if mesh in meshList:
                    editMeshName = EDIT_MESH_NAME.format(mesh, poseName)
                    print " - Rebuild " + editMeshName
                    plugMeshes(refMeshName, editMeshName)
                    
                    correcName = DELTA_MESH_NAME.format(mesh, poseName)
                    print "    - Extract " + correcName
                    pc.progressBar(gMainProgressBar, edit=True, step=2)
                    
                    storeDeltas(mesh, poseName, inTreshold)
            
            pc.progressBar(gMainProgressBar, edit=True, step=1)
            updateBs(mesh)

        pc.progressBar(gMainProgressBar, edit=True, endProgress=True)
