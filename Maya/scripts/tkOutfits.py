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
import os
import re

import maya.cmds as mc
import pymel.core as pc

import tkMayaCore as tkc
import mayaexecpythonfile

__author__ = "Cyril GIBAUD - Toonkit"

"""

Example usage for Zombie :
import os
os.environ["ZOMB_TEXTURE_PATH"]="Z:\\0023_Zombillenium"

import tkOutfits
reload(tkOutfits)
tkOutfits.showUI()

tkOutfits.getOverrides(pc.selected()[0])
tkOutfits.refreshOverrides(pc.selected()[0])

print tkOutfits.getCurrent(pc.selected()[0], 'variation')
tkOutfits.setCurrent(pc.selected()[0], 'variation', 'cheveuxTshirt')

tkOutfits.createOutfits(pc.selected()[0], in_sTag="set_outfit", in_sSearch="set_outfit_", in_sReplace="Outfits_variation_", in_sLayerTag="layer", in_sLayerSearch="layer_", in_sLayerReplace="Outfits_variation_", inMembershipsFromLayers=True)

tkOutfits.removeOutfits(pc.selected()[0])

outfits = tkOutfits.getOutfits(pc.selected()[0])

tkOutfits.getOutfits(pc.selected()[0]
"""

UINAME = "tkOutfitsUI"
TOPNODE = None
SHADERTYPES = mc.listNodeTypes('shader')#["lambert","blinn","phong", "surfaceShader", "layeredShader", "useBackground", "rampShader", "dmnToon"]
OUTFIT_TAG = "Outfits"
CURRENTSCENEFOLDER = "$CURRENTSCENEFOLDER"
CURRENTSCENENAME = "$CURRENTSCENENAME"
PRESET = "$PRESET"

def getNamespace(inName):
    if not ":" in inName:
        return ""

    return inName.split(":")[0] + ":"

def getLongestName(inNode):
    return inNode.fullPath() if isinstance(inNode, pc.nodetypes.DagNode) else inNode.name()

def getShortestName(inNodeLongestName):
    if not '|' in inNodeLongestName:
        return inNodeLongestName

    ns = getNamespace(inNodeLongestName)
    
    dagPathSplit = list(filter(None, inNodeLongestName.split('|')))
    shortestName = ""
    
    for i in range(len(dagPathSplit) -1, -1, -1):
        shortestName = dagPathSplit[i] + ("|" if not shortestName == "" else "") + shortestName
        results = mc.ls(shortestName)
        if len(results) == 1:
            break

    return shortestName

def removeAllLocks(ins_name=None, ina_types=None):
    nodes = []

    if ins_name != None:
        nodes = mc.ls(ins_name, [] if ina_types == None else ina_types)
    else:
        nodes = mc.ls([] if ina_types == None else ina_types)

    if len(nodes) > 0:
        mc.lockNode(nodes, lock=False)

def getActiveIDs(inArrayAttr):
    arrayIDs = []
    arrayAttrs = pc.listAttr(inArrayAttr, multi=True)
    for arrayAttr in arrayAttrs:
        if "." in arrayAttr:
            continue

        firstIndex = arrayAttr.find("[")
        lastIndex = arrayAttr.find("]")
        if firstIndex == -1 or lastIndex == -1 or firstIndex >= lastIndex:
            print ("Can't get brackets indices for "+ arrayAttr +"!")
            continue
        
        arrayIDs.append(int(arrayAttr[firstIndex+1:lastIndex]))

    return arrayIDs

def getProperty(in_nAsset, in_nName):
    fullName = in_nAsset.namespace() + in_nName
    if mc.objExists(fullName):
        return pc.PyNode(fullName)

    return None

def assignShader(inMaterial, inObj, inSG=None):
    #print "assignShader(%s, %s, %s, %s)" % (str(inMaterial), str(inObj), str(inSG), str(inMultiUVs))
    #return None
    shape = inObj
    if inObj.type() == "transform":
        shapes = inObj.getShapes(noIntermediate=True)
        if len(shapes) > 0:
            shape = shapes[0]
        else:
            pc.warning("Can't find any shapes on object %s" % inObj.name())

    shadingGroup = None

    if inSG != None:
        shadingGroup = inSG
    else:
        nodes = pc.listHistory(inMaterial, future=True, levels=1)
        
        for node in nodes:
            if not "initialParticleSE" in node.name() and (node.type() == "shadingEngine" or node.type() == "materialFacade"):
                shadingGroup = node
                break

        #No shading group ?
        if shadingGroup == None:
            shadingGroup = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name=inMaterial.name()+"SG")
            pc.connectAttr(inMaterial.name() + ".outColor", shadingGroup.name() + ".surfaceShader")

    pc.sets(shadingGroup, edit=True, forceElement=shape)

    return shadingGroup

def getShaders(inObj, inFirstOnly=True):
    shaders = []
    shapes = [inObj]
    if inObj.type() == "transform":
        shapes = inObj.getShapes(noIntermediate=True)
   
    for shape in shapes:
        shadingGroups = pc.listConnections(shape, type="shadingEngine")
        for sGroup in shadingGroups:
            if "initialParticleSE" in sGroup.name():
                continue
            cons = pc.listConnections(sGroup, destination=False)
            for con in cons:
                if con.type() in SHADERTYPES:
                    shaders.append(con)
                    if inFirstOnly:
                        return shaders
                    break
    
    return shaders

def getInheritedVisibility(inObj):
    if not mc.getAttr("{0}.visibility".format(inObj)):
        return False
    
    obj = inObj
    objParent = mc.listRelatives(obj, parent=True)
    if objParent != None:
        objParent = objParent[0]
        
    while objParent != None:
        if not mc.getAttr("{0}.visibility".format(objParent)):
            return False
        
        objParent = mc.listRelatives(objParent, parent=True)
        if objParent != None:
            objParent = objParent[0]
            
    return True

def getLayerAdjustments(inLayer):
    nodesDic = {}
    
    memberships = pc.editRenderLayerMembers(inLayer, query=True, fullNames=True)
    
    if memberships != None:
        for member in memberships:
            nodesDic[member] = {}
    
    #adjs = pc.editRenderLayerAdjustment(inLayer, query=True, layer=True)
    #print "{0} ({1})".format(adjs, len(adjs))

    #Materials
    adjustIndices = getActiveIDs(inLayer + '.outAdjustments')
    for index in adjustIndices:
        nodes = pc.listConnections(inLayer + '.outAdjustments[{0}].outPlug'.format(index))

        if len(nodes) > 0:
            nodeName = getLongestName(nodes[0])
            sgName = pc.listConnections(inLayer + '.outAdjustments[{0}].outValue'.format(index))[0].name()
            
            matName = None
           
            #Get material from shadingGroup
            cons = pc.listConnections(sgName, destination=False)
            for con in cons:
                if con.type() in SHADERTYPES:
                    matName = con.name()
            
            if matName == None:
                pc.warning("Can't get shader from shading group {0}".format(sgName))
            
            if not nodeName in nodesDic:
                nodesDic[nodeName] = {}
            
            nodesDic[nodeName]["shader"] = matName

    #Plugs
    adjustIndices = getActiveIDs(inLayer + '.adjustments')
    for index in adjustIndices:
        attr = pc.listConnections(inLayer + '.adjustments[{0}].plug'.format(index), plugs=True)[0]
        nodeName = getLongestName(attr.node())
        attrname = attr.name(includeNode=False, longName=True)

        if 'instObjGroups[0]' in attrname:
            print ('Material related attribute ignored "{0}"'.format(attrname))
            continue

        if not nodeName in nodesDic:
            nodesDic[nodeName] = {}

        alias = pc.aliasAttr("{0}.{1}".format(nodeName, attrname), query=True)
        #print "alias", alias
        if alias != None and alias != "":
            attrname = alias
        
        nodesDic[nodeName][attrname] = pc.getAttr(inLayer + '.adjustments[{0}].value'.format(index))
        
    return nodesDic

def getAllLayers(inNamePattern=""):
    layersAdjusts = {}

    filteredLayers = []
    layers = []
    if inNamePattern == "":
        layers = mc.ls(type="renderLayer")
    else:
        layers = mc.ls(inNamePattern, type="renderLayer")

    for layer in layers:
        if layer == "defaultRenderLayer":
            continue
        filteredLayers.append(layer)

    return filteredLayers

def getAllLayersAdjustments(inNamePattern=""):
    layersAdjusts = {}

    layers = getAllLayers(inNamePattern)

    for layer in layers:
        overrides = getLayerAdjustments(layer)

        if len(overrides) > 0:
             layersAdjusts[layer] = overrides

    return layersAdjusts

def getLayerOrphanMeshes(inNamePattern="", excludeInvisible=True):
    print ("getLayerOrphanMeshes("+str(inNamePattern)+", "+str(excludeInvisible)+")")
    meshes = pc.ls(type="mesh")
    meshesT = [mesh.getParent().fullPath() for mesh in meshes]

    allMembers = []
    layers = getAllLayers(inNamePattern)

    for layer in layers:
        members = pc.editRenderLayerMembers(layer, query=True, fullNames=True)
        for member in members:
            if not member in allMembers:
                allMembers.append(member)

    unfound = []

    for meshT in meshesT:
        if not meshT in allMembers:
            if not excludeInvisible or getInheritedVisibility(meshT):
                unfound.append(pc.PyNode(meshT))

    return unfound

def getOutfitsSetup(in_sNs="", in_bClean=False, in_sTag=None, in_sSearch="", in_sReplace="", in_sLayerTag=None, in_sLayerSearch="", in_sLayerReplace="", inMembershipsFromLayers=False):
    outfits = {}

    if in_sTag == None:
        in_sTag = OUTFIT_TAG

    if in_sLayerTag == None:
        in_sLayerTag = OUTFIT_TAG

    tag = in_sLayerTag if inMembershipsFromLayers else in_sTag

    search = in_sLayerSearch if inMembershipsFromLayers else in_sSearch
    replace = in_sLayerReplace if inMembershipsFromLayers else in_sReplace

    if inMembershipsFromLayers:
        orphans = getLayerOrphanMeshes(in_sNs + tag + "_*")
        if len(orphans) > 0:
            message = 'Some geometries are visible by default, but are not present in any layer :\r\n' + "\r\n".join([orphan.name() for orphan in orphans])
            rslt = mc.confirmDialog( title='Geometries not present in any layer', message=message, button=['Always exclude (most likely)','Always include', 'Cancel'], defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
            print ("\r\n" + message + "\r\n")

            if rslt == "Cancel":
                return outfits

            if rslt == "Always exclude (most likely)":
                for orphan in orphans:
                    mc.setAttr("{0}.visibility".format(orphan.name()), 0)

    #Collect outfit sets (could be cool to be able to override that)
    outfitSets = mc.ls(in_sNs + tag + "_*", type="objectSet" if not inMembershipsFromLayers else "renderLayer")  

    if len(outfitSets) == 0:
        mc.warning('No outfits sets found ({0})'.format(in_sNs + tag + "_*"))
        return {}

    #Set default layer as active
    mc.editRenderLayerGlobals(currentRenderLayer="defaultRenderLayer")

    #If we use layers we could have to force objects to be added (attributes overrides)
    layerAdjustments = {}

    forcedObjects = []

    for outfitSet in outfitSets:
        layer = outfitSet if inMembershipsFromLayers else outfitSet.replace(in_sTag, in_sLayerTag)
        if mc.objExists(layer):
            layerAdjustments[layer] = getLayerAdjustments(layer)

            for obj in layerAdjustments[layer].keys():
                if not obj in forcedObjects:
                    for adj in layerAdjustments[layer][obj].keys():
                        if adj == None:
                            continue
                        if adj == "shader":
                            continue
                        if adj == "visibility":
                            continue
                        
                        forcedObjects.append(pc.PyNode(obj))

    for outfitSet in outfitSets:
        outfitRealName = outfitSet.split(":")[-1]
        if search != "":
            outfitRealName = outfitRealName.replace(search, replace)

        aSplitName = outfitRealName.split("_")
        if len(aSplitName) != 3:
            mc.warning("Set have incorrect name and will be ignored : '{0}'".format(outfitRealName))
            continue

        tag, outfitCateg, outfitValue = aSplitName

        if not outfitCateg in outfits:
            outfits[outfitCateg] = {}

        objsDics = {}
        objs = []

        layer = outfitSet if inMembershipsFromLayers else outfitSet.replace(in_sTag, in_sLayerTag)
        
        adjustments = {}
        if mc.objExists(layer):
            adjustments = getLayerAdjustments(layer)

        if inMembershipsFromLayers and mc.objExists(layer):
            members = pc.editRenderLayerMembers(layer, query=True, fullNames=True)
            for member in members:
                node = pc.PyNode(member)

                #Reject memberships that hides this node
                if not "visibility" in adjustments[node.fullPath()] or adjustments[node.fullPath()]["visibility"] == 1:
                    if not node in objs:
                        objs.append(node)
            for adjustment in adjustments.keys():
                adjNode = pc.PyNode(adjustment)
                #If node is not a dag node, it cannot be added to memberships, so consider any override as a membership
                if adjNode.name() == "chr_zombie1_default_modeling_TK:geo_jawA":
                    print ("/!\\ ", adjNode.name(), " is dag ? " ,isinstance(adjNode, pc.nodetypes.DagNode))
                if not isinstance(adjNode, pc.nodetypes.DagNode):
                    if not adjustment in members and not adjNode in objs:
                        objs.append(adjNode)
        else:
            objs = pc.sets(outfitSet, query=True) or []

        #Add forced objects (that have arbitrary attributes)
        for obj in forcedObjects:
            if not obj in objs:
                objs.append(obj)

        #remove hidden by default
        hiddenObjs = []
        for i in range(len(objs)):
            if pc.attributeQuery("visibility",node=objs[i], exists=True) and not getInheritedVisibility(getLongestName(objs[i])):
                hiddenObjs.append(i)

        indices = sorted(hiddenObjs, reverse=True)
        for index in indices:
            del objs[index]

        #Add all shapes of visible dagnodes
        objsDupe = objs[:]
        for objDupe in objsDupe:
            if objDupe.type() == "transform":
                shapes = objDupe.getShapes()
                for shape in shapes:
                    if not shape in objs:
                        objs.append(shape)

        print (outfitSet, objs)

        for obj in objs:
            objDic = {}
            objDic["node"] = obj
            objDic["name"] = obj.name()
            objDic["longName"] = getLongestName(obj)
            
            if objDic["longName"] in adjustments:
                if "shader" in adjustments[objDic["longName"]]:
                    objDic["shader"] = adjustments[objDic["longName"]]["shader"]

                #arbitrary attributes
                attrs = None
                for key in adjustments[objDic["longName"]].keys():
                    if key == None:
                        continue
                    if key == "shader":
                        continue
                    if key == "visibility":
                        continue
                    if attrs == None:
                        attrs = {}

                    attrs[key] = adjustments[objDic["longName"]][key]

                if attrs != None and len(attrs) > 0:
                    objDic["attrs"] = attrs

            objsDics[objDic["name"]] = objDic

        outfits[outfitCateg][outfitValue] = objsDics
    #print outfits
    return outfits

def getOutfits(in_nAsset):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    outfits = {}

    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)

    if outfitsProperty == None:
        return None

    outfitAttrs = tkc.getParameters(outfitsProperty, customOnly=True, keyableOnly=True)
    
    for attr in outfitAttrs:
        if attr.startswith(OUTFIT_TAG):
            shortName = attr[len(OUTFIT_TAG)+1:]
            outfits[shortName] = []
            enumValues = pc.attributeQuery(attr, node=outfitsProperty, listEnum=True)[0].split(":")
            for i in range(1, len(enumValues)):
                outfits[shortName].append(enumValues[i])

    return outfits

def getOverrides(in_nAsset):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    overrides = None

    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
    if outfitsProperty != None:
        return eval(pc.getAttr(outfitsProperty.name() + ".tk_overrides"))

    return overrides

def getIncludedObjects(in_nAsset, inOutfits=None):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    ns = in_nAsset.namespace()

    outfits = getOutfits(in_nAsset)
    objectsOverrides = getOverrides(in_nAsset)

    cases = []

    if inOutfits !=None:
        for outfit,current in inOutfits.iteritems():
            cases.append("tk_"+outfit+"_is_"+current)
    else:
        for outfit in outfits.keys():
            current = getCurrent(in_nAsset, outfit)
            if current == "Debug":
                continue
            cases.append("tk_"+outfit+"_is_"+current)

    concernedObjects = []

    if len(cases) == 0:
        #All is debug, select All
        concernedObjects = objectsOverrides.keys()
    else:
        for objectsOverride in objectsOverrides:
            if objectsOverride in concernedObjects:
                continue
            for case in cases:
                if case in objectsOverrides[objectsOverride]:
                    concernedObjects.append(objectsOverride)

    actualObjects = []

    for concernedObject in concernedObjects:
        if pc.objExists(ns + concernedObject):
            actualObjects.append(ns + concernedObject)
        else:
            pc.warning(ns + concernedObject + " does not exists !!")

    return actualObjects

def getExcludedObjects(in_nAsset):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    ns = in_nAsset.namespace()

    outfits = getOutfits(in_nAsset)
    objectsOverrides = getOverrides(in_nAsset)

    cases = []

    for outfit in outfits.keys():
        current = getCurrent(in_nAsset, outfit)
        if current == "Debug":
            continue
        cases.append("tk_"+outfit+"_is_"+current)

    excludedObjects = []

    if len(cases) == 0:
        #All is debug, return Nothing
        return []
    else:
        allObjs = [ns + k for k in objectsOverrides.keys()]
        concernedObjects = getIncludedObjects(in_nAsset)

        for obj in allObjs:
            if not obj in concernedObjects:
                if pc.objExists(obj):
                    excludedObjects.append(obj)
                else:
                    pc.warning(obj + " does not exists !!")

    return excludedObjects

def setOverrides(in_nAsset, inOverrides):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
    if outfitsProperty != None:
        pc.setAttr(outfitsProperty.name() + ".tk_overrides", str(inOverrides))

def findShader(in_sNs, in_sRawName):
    shader = None
    #try with in_sNs (most probable)
    shaders = mc.ls(in_sNs+in_sRawName,type=SHADERTYPES)
    if len(shaders) > 0:
        shader = shaders[0]
    elif in_sNs != "":
        #Ok, so without in_sNs if any ?
        shaders = mc.ls(in_sRawName,type=SHADERTYPES)
        if len(shaders) > 0:
            shader = shaders[0]

    return shader

def collectUsedShaders(in_nAsset):
    shaders = []

    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return

    ns = in_nAsset.namespace()
    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
    if outfitsProperty == None:
        return []

    outfits = getOutfits(in_nAsset)
    objectsOverrides = getOverrides(in_nAsset)

    cases = []

    for outfit in outfits.keys():
        current = getCurrent(in_nAsset, outfit)
        if current == "Debug":
            continue
        cases.append("tk_"+outfit+"_is_"+current)

    for obj in objectsOverrides.keys():
        overrides = objectsOverrides[obj]
        objName = ns+obj
        managed=False
        for case in cases:
            if case in overrides:
                curOverrides = overrides[case]
                for curOverride in curOverrides.keys():
                    if curOverride == "shader":
                        if curOverrides[curOverride] != "":
                            managed = True
                            shader=None
                            if mc.objExists(curOverrides[curOverride]):
                                shader=curOverrides[curOverride]
                            elif  mc.objExists(ns+curOverrides[curOverride]):
                                shader=ns+curOverrides[curOverride]

                            if shader != None and not shader in shaders:
                                shaders.append(shader)
                        break

        if not managed:
            if "defaultShader" in overrides:
                shader=None
                if mc.objExists(overrides["defaultShader"]):
                    shader=overrides["defaultShader"]
                elif  mc.objExists(ns+overrides["defaultShader"]):
                    shader=ns+overrides["defaultShader"]

                if shader != None and not shader in shaders:
                    shaders.append(shader)
            else:
                pc.warning(objName + "defaultShader can't be found !")

    return shaders

def refreshOverrides(in_nAsset, asOverrides=False):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return

    ns = in_nAsset.namespace()
    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
    if outfitsProperty == None:
        return

    outfits = getOutfits(in_nAsset)
    objectsOverrides = getOverrides(in_nAsset)
    #print objectsOverrides
    cases = []

    for outfit in outfits.keys():
        current = getCurrent(in_nAsset, outfit)
        if current == "Debug":
            continue
        cases.append("tk_"+outfit+"_is_"+current)

    for obj in objectsOverrides.keys():
        overrides = objectsOverrides[obj]
        objName = ns+obj
        if not mc.objExists(objName):
            objName = obj
        if mc.objExists(objName):
            managed=False
            if "defaultAttrs" in overrides:
                for attr in overrides["defaultAttrs"].keys():
                    mc.setAttr("{0}.{1}".format(objName, attr), overrides["defaultAttrs"][attr])
            for case in cases:
                if case in overrides:
                    managed = True
                    curOverrides = overrides[case]
                    for curOverride in curOverrides.keys():
                        if curOverride == "visibility":
                            if mc.attributeQuery("visibility",node=objName, exists=True):
                                if mc.getAttr(objName + ".visibility", settable=True):
                                    mc.setAttr(objName + ".visibility", 1)#curOverrides[curOverride])
                                else:
                                    pc.warning(objName + ".visibility not settable")
                        elif curOverride == "shader":
                            if curOverrides[curOverride] != "":
                                shader=None
                                if mc.objExists(curOverrides[curOverride]):
                                    shader=curOverrides[curOverride]
                                elif  mc.objExists(ns+curOverrides[curOverride]):
                                    shader=ns+curOverrides[curOverride]

                                if shader != None:
                                    assignShader(pc.PyNode(shader), pc.PyNode(objName))
                                else:
                                    pc.warning("Can't find override shader : " + curOverrides[curOverride])
                        elif curOverride == "attrs":
                            if not mc.objExists(objName):
                                objName = obj
                            if mc.objExists(objName):
                                for attrKey in curOverrides[curOverride].keys():
                                    if attrKey != None and attrKey != "None":
                                        if mc.attributeQuery(attrKey,node=objName, exists=True):
                                            attr="{0}.{1}".format(objName, attrKey)
                                            mc.setAttr(attr, curOverrides[curOverride][attrKey])
                                            if asOverrides:
                                                pc.editRenderLayerAdjustment(attr)
                        else:
                            pc.warning("Unmanaged override : " + curOverride)
                    break

            #print obj, managed

            if not managed:
                if mc.objExists(objName):
                    if mc.attributeQuery("visibility",node=objName, exists=True):
                        if mc.getAttr(objName + ".visibility", settable=True):
                            mc.setAttr(objName + ".visibility", 0)
                        else:
                            pc.warning(objName + ".visibility not settable")
        else:
            pc.warning(objName + " can't be found !")

    #At last override with debug values
    for outfit in outfits.keys():
        current = getCurrent(in_nAsset, outfit)
        if current == "Debug":
            for obj in objectsOverrides.keys():
                for overrideKey in objectsOverrides[obj]:
                    if overrideKey.startswith("tk_"+outfit+"_is_"):
                        objName = ns+obj
                        if not mc.objExists(objName):
                            objName = obj
                        if mc.objExists(objName):
                            objNode = pc.PyNode(objName)
                            if mc.attributeQuery("visibility",node=objName, exists=True):
                                if mc.getAttr(objName + ".visibility", settable=True):
                                    mc.setAttr(objName + ".visibility", 1)
                            
                            if objectsOverrides[obj]["defaultShader"] != "":

                                shader=None
                                if mc.objExists(objectsOverrides[obj]["defaultShader"]):
                                    shader=objectsOverrides[obj]["defaultShader"]
                                elif  mc.objExists(ns+objectsOverrides[obj]["defaultShader"]):
                                    shader=ns+objectsOverrides[obj]["defaultShader"]

                                if shader != None:
                                    assignShader(pc.PyNode(shader), objNode)
                                else:
                                    pc.warning("Can't find default shader : " + objectsOverrides[obj]["defaultShader"])
                            
                            if "defaultAttrs" in objectsOverrides[obj]:
                                for attr in objectsOverrides[obj]["defaultAttrs"].keys():
                                    mc.setAttr("{0}.{1}".format(objNode.name(), attr), objectsOverrides[obj]["defaultAttrs"][attr])
                        break

def getCurrent(in_nAsset, in_sOutfit):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)

    if outfitsProperty != None:
        if mc.attributeQuery(OUTFIT_TAG + "_" + in_sOutfit, node=outfitsProperty.name(), exists=True):
            enumValues = pc.attributeQuery(OUTFIT_TAG + "_" + in_sOutfit, node=outfitsProperty, listEnum=True)[0].split(":")
            return enumValues[pc.getAttr(outfitsProperty.name() + "." + OUTFIT_TAG + "_" + in_sOutfit)]

    return None

def setCurrent(in_nAsset, in_sOutfit, in_sValue, refresh=False, asOverrides=False):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)

    if outfitsProperty != None:
        if mc.attributeQuery(OUTFIT_TAG + "_" + in_sOutfit, node=outfitsProperty.name(), exists=True):
            enumValues = pc.attributeQuery(OUTFIT_TAG + "_" + in_sOutfit, node=outfitsProperty, listEnum=True)[0].split(":")
            if in_sValue in enumValues:
                pc.setAttr(outfitsProperty.name() + "." + OUTFIT_TAG + "_" + in_sOutfit, enumValues.index(in_sValue))

                if refresh:
                    refreshOverrides(in_nAsset)

def removeOutfits(in_nAsset):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return None

    outfits = getOutfits(in_nAsset)

    if outfits != None:
        outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)

        #Store value of attributes linked to "tk_.+_is_.+" to reset the values after deletion
        storedValues = {}
        attrs = tkc.getParameters(outfitsProperty)
        filteredCons = []
        for attr in attrs:
            if re.match("tk_.+_is_.+", attr):
                cons = pc.listConnections("{0}.{1}".format(outfitsProperty, attr), plugs=True, source=False, destination=True)
                for con in cons:
                    if not re.match(".+_casesChain.*\.input", con.name()) and not re.match(".*tkOutfits_visibilities\.", con.name()):
                        filteredCons.append(con)

        for con in filteredCons:
            storedValues[con] = con.get()

        for outfitKey in outfits.keys():
            mc.setAttr("{0}.{1}".format(outfitsProperty, OUTFIT_TAG+"_"+outfitKey), 0)

        pc.delete(outfitsProperty)

        for attr, attrValue in storedValues.iteritems():
            try:
                attr.set(attrValue)
                attr.lock()
            except:
                pass

    return None

def connectVisibilities(in_nAsset):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return

    ns = in_nAsset.namespace()
    outfits = getOutfits(in_nAsset)

    if outfits != None:
        outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
        outfitsVis = tkc.getProperty(outfitsProperty, 'visibilities')

        visAttrs = tkc.getParameters(outfitsVis, customOnly=True, keyableOnly=False)

        for attr in visAttrs:
            obj, attribute = attr.split("__")

            if mc.objExists(ns + obj):
                pc.connectAttr("{0}.{1}".format(outfitsVis.name(), attr), "{0}.{1}".format(ns + obj, attribute), f=True)
            else:
                pc.warning("Can't find '" + ns + obj + "'")

def getPresets(in_nAsset):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return {}

    presets = {}
    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
    if outfitsProperty != None:
        outfitsPresets = tkc.getProperty(outfitsProperty, 'tkpresets')
        if outfitsPresets != None:
            presetAttrs = tkc.getParameters(outfitsPresets, customOnly=True, keyableOnly=False)

            for presetAttr in presetAttrs:
                presets[presetAttr] = eval(pc.getAttr(outfitsPresets.name() + "." + presetAttr))

    return presets

def savePresets(in_nAsset, in_dPresets):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return

    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
    if outfitsProperty != None:
        outfitsPresets = tkc.getProperty(outfitsProperty, 'tkpresets')
        if outfitsPresets != None:
            mc.delete(outfitsPresets.name())

        for presetKey in in_dPresets.keys():
            tkc.addParameter(outfitsProperty, presetKey , inType="string", default=str(in_dPresets[presetKey]), containerName='tkpresets')

def addPreset(in_nAsset, in_sPresetName, in_dPresetValues):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return

    presets = getPresets(in_nAsset)
    presets[in_sPresetName] = in_dPresetValues

    savePresets(in_nAsset, presets)

def createOutfits(in_nAsset, in_bClean=True, in_sTag=None, in_sSearch="", in_sReplace="", in_sLayerTag=None, in_sLayerSearch="", in_sLayerReplace="", inMembershipsFromLayers=False):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return

    ns = in_nAsset.namespace()

    outfits = getOutfitsSetup(ns, in_bClean, in_sTag, in_sSearch, in_sReplace, in_sLayerTag, in_sLayerSearch, in_sLayerReplace, inMembershipsFromLayers)

    if len(outfits) == 0:
        mc.warning("No outfits returned !!")
        return
    
    removeOutfits(in_nAsset)

    objectsSetup = {}

    #We will collect shading groups to be able to lock them at the end
    allShadingGroups = []

    sortedKeys = sorted(outfits.keys())

    defaultAttrs = {}

    for outfitKey in sortedKeys:
        outfit = outfits[outfitKey]
        sortedValuesKeys = sorted(outfit.keys())
        for valueKey in sortedValuesKeys:
            objects = outfit[valueKey]
            for obj in objects:
                if "attrs" in objects[obj]:
                    for attr in objects[obj]["attrs"].keys():
                        if not obj in defaultAttrs:
                            defaultAttrs[obj] = {}

                        defaultAttrs[obj][attr] = pc.getAttr("{0}.{1}".format(obj, attr))

    for outfitKey in sortedKeys:
        outfit = outfits[outfitKey]
        sortedValuesKeys = sorted(outfit.keys())

        enumValues = ['Debug']
        enumValues.extend(sortedValuesKeys)

        outfitEnum = tkc.addParameter(in_nAsset, '{0}_{1}'.format(OUTFIT_TAG, outfitKey) , inType="enum;"+':'.join(enumValues), default=enumValues[0], containerName='tk'+OUTFIT_TAG)
        
        debugNode = pc.createNode('condition', name=ns + outfitKey + '_debug_cond')
        debugNode.setAttr('operation', 1)
        mc.connectAttr(outfitEnum, debugNode.name() + '.secondTerm')

        cnt = 1
        for valueKey in sortedValuesKeys:
            caseName = 'tk_{0}_is_{1}'.format(outfitKey, valueKey)
            attr = tkc.addParameter(in_nAsset, caseName, inType="bool", containerName='tk'+OUTFIT_TAG, expose=False)
            node = pc.createNode('condition', name=ns + caseName + '_cond')
            node.setAttr('operation', 1)
            node.setAttr('firstTerm', cnt)
            mc.connectAttr(outfitEnum, node.name() + '.secondTerm')

            addDebugNode = pc.createNode('addDoubleLinear', name=ns + caseName + '_debugAdd')
            mc.connectAttr(node.name() + ".outColorR", addDebugNode.name() + '.input1')
            mc.connectAttr(debugNode.name() + ".outColorR", addDebugNode.name() + '.input2')

            mc.connectAttr(addDebugNode.name() + ".output", attr)
            
            objects = outfit[valueKey]

            for obj in objects.keys():
                objName = obj.split(":")[-1]
                if not objName in objectsSetup:
                    shader=""
                    if objects[obj]["node"].type() == "transform":
                        shaders = getShaders(objects[obj]["node"])
                        if len(shaders) > 0:
                            shadingGroups = pc.listConnections(shaders[0], type="shadingEngine")

                            if len(shadingGroups) > 0 and not shadingGroups[0].name() in allShadingGroups:
                                allShadingGroups.append(shadingGroups[0].name())

                            shader = shaders[0].name()
                            shader = shader.split(":")[-1]
                        else:
                            pc.warning("Can't find default shader : " + obj)

                    objectsSetup[objName] = {"defaultShader":shader, caseName:{"visibility":True}}
                elif not caseName in objectsSetup[objName]:
                    objectsSetup[objName][caseName] = {"visibility":True}   

                if "attrs" in objects[obj]:
                    objectsSetup[objName][caseName]["attrs"] = objects[obj]["attrs"]

                if obj in defaultAttrs:
                    if not "defaultAttrs" in objectsSetup[objName]:
                        objectsSetup[objName]["defaultAttrs"] = {}
                    for defaultAttr in defaultAttrs[obj].keys():
                        objectsSetup[objName]["defaultAttrs"][defaultAttr] = defaultAttrs[obj][defaultAttr]
     
                if "shader" in objects[obj]:
                    shadingGroups = pc.listConnections(objects[obj]["shader"], type="shadingEngine")

                    if len(shadingGroups) > 0 and not shadingGroups[0].name() in allShadingGroups:
                        allShadingGroups.append(shadingGroups[0].name())

                    objectsSetup[objName][caseName]["shader"] = objects[obj]["shader"].split(":")[-1]
                else:
                    objectsSetup[objName][caseName]["shader"] = objectsSetup[objName]["defaultShader"]

            cnt += 1

    #Remove property prefix
    mc.rename(in_nAsset.name() + "_tk"+OUTFIT_TAG, ns+"tk"+OUTFIT_TAG)

    #create visibility PlaceHolders
    outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)

    for obj in objectsSetup.keys():
        attr = tkc.addParameter(outfitsProperty, '{0}__{1}'.format(obj, "visibility"), inType="bool", containerName='visibilities', expose=False)

        cases = objectsSetup[obj].keys()

        if len(cases) > 2:
            freePlug = None
            for case in cases:
                if case != "defaultShader" and case != "defaultAttrs":
                    if freePlug == None:
                        freePlug = outfitsProperty.name() + "." + case
                    else:
                        addNode = pc.createNode('addDoubleLinear', name=ns+obj + '_casesChain')
                        mc.connectAttr(freePlug, addNode.input1.name())
                        mc.connectAttr(outfitsProperty.name() + "." + case, addNode.input2.name())
                        freePlug = addNode.output.name()
            mc.connectAttr(freePlug, attr)
        else:
            if cases[0] != "defaultShader":
                mc.connectAttr(outfitsProperty.name() + "." + cases[0], attr)
            else:
                mc.connectAttr(outfitsProperty.name() + "." + cases[1], attr)

    #connectVisibilities(in_nAsset)

    #create shadingGroups PlaceHolders
    #print "allShadingGroups : ", len(allShadingGroups), allShadingGroups
    if len(allShadingGroups) > 0:
        attr = tkc.addParameter(outfitsProperty, "shadingGroups", inType="bool", containerName="shadingGroups", expose=False)
        holder = tkc.getProperty(outfitsProperty,"shadingGroups")

        for shadingGroup in allShadingGroups:
            facet = mc.polyCreateFacet(name="{0}_placeholder".format(ns+shadingGroup.split(":")[-1]), p=[(0.0, 0.0, 0.0), (0.001, 0.0, 0.0), (0, 0.001, 0.0)] )
            pc.mel.eval("DeleteHistory " + facet[0])
            #print "mc.sets(", shadingGroup,", edit=True, forceElement=",facet[0],")"
            pc.sets(shadingGroup, edit=True, forceElement=facet[0])
            mc.parent(facet[0], holder.name())
            tkc.addParameter(pc.PyNode(facet[0]), "exclude", inType="bool", default=True, containerName="OscarAttributes")

    #Automate presets creation when we have only one outfit
    if len(sortedKeys) == 1:
        outfit = outfits[sortedKeys[0]]
        sortedValuesKeys = sorted(outfit.keys())

        for sortedValuesKey in sortedValuesKeys:
            addPreset(in_nAsset, sortedValuesKey, {sortedKeys[0]:sortedValuesKey})

    tkc.addParameter(outfitsProperty, "tk_overrides", inType="string", default=str(objectsSetup), expose=False)

def applyPreset(in_nAsset, preset, asOverrides=False):
    presets = getPresets(in_nAsset)
    if not preset in presets:
        mc.warning(preset + "does not exists")
        return False

    for outfitValue in presets[preset].keys():
        setCurrent(in_nAsset, outfitValue, presets[preset][outfitValue])

    refreshOverrides(in_nAsset, asOverrides)

def cleanCurrent(in_nAsset, asBatch=False, alternateRoots=None):
    if in_nAsset == None:
        sel = pc.selected()
        if len(sel) > 0:
            in_nAsset = pc.selected()[0]
        else:
            pc.warning("Top node undefined, please select it !")
            return

    ns = in_nAsset.namespace()
    outfits = getOutfits(in_nAsset)

    deletedObjs = []

    if outfits != None:
        values = []

        presets = getPresets(in_nAsset)

        for outfit in outfits.keys():
            current = getCurrent(in_nAsset, outfit)
            if current == "Debug":
                continue
            values.append(current)

        outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)

        objects = getExcludedObjects(in_nAsset)
        for obj in objects:
            deletedObjs.append(obj)
            if pc.objExists(obj):
                tkc.freeze(obj)
                pc.delete(obj)

        #rename objects in Geometries if they end with the variation name      
        toRename = {}
        outfitsProperty = getProperty(in_nAsset, 'tk'+OUTFIT_TAG)
        if outfitsProperty != None:
            parent = outfitsProperty.getParent()
            geoObjs = tkc.getChildren(parent, True)

            if alternateRoots:
                for alternateRoot in alternateRoots:
                    if pc.objExists(alternateRoot):
                        geoObjs.extend(tkc.getChildren(pc.PyNode(alternateRoot), True))

            for geoObj in geoObjs:
                origName = geoObj.name()
                for value in values:
                    if "_"+value in origName:
                        if not origName in toRename:
                            toRename[origName] = geoObj
                        presetKeys = sorted(presets.keys(), key=lambda v: -len(v))
                        for preset in presetKeys:
                            if "_"+preset in geoObj.name():
                                geoObj.rename(geoObj.name().replace("_"+preset, ""))

        if len(toRename) > 0:
            renamedObjs = ["{0} => {1}".format(key, value) for key, value in toRename.iteritems()]
            pc.warning("{0} objects were containing outift name and were renamed :\n{1}".format(len(toRename), "\n".join(renamedObjs)))

        #rename outfit specific materials if possible
        usedShaders = collectUsedShaders(in_nAsset)

        removeOutfits(in_nAsset)

        #Delete elements from rig if *_Root_Oscar_Attributes.GenerationTags is found and does not match
        props = mc.ls("*_Root_OSCAR_Attributes", transforms=True)
        #print "props", props
        attrName = "GenerationTags"

        toDelete = []
        outfitFound = False
        for prop in props:
            outfitFound = False
            if mc.attributeQuery(attrName, node=prop, exists=True):
                tags = mc.getAttr("{0}.{1}".format(prop, attrName)).split(",")
                for tag in tags:
                    if tag == "":
                        continue
                    for value in values:
                        if tag == value:
                            outfitFound = True
                            break

                    if outfitFound:
                        break

                if not outfitFound:
                    toDelete.append(prop)

        for toDeleteObj in toDelete:
            if mc.objExists(toDeleteObj):
                actualObj = pc.listRelatives(toDeleteObj, parent=True)[0]
                deletedObjs.append(actualObj.name())
                externalCns = tkc.getExternalConstraintsOnHierarchy(actualObj)
                if len(externalCns) > 0:
                    pc.delete(externalCns)
                pc.delete(actualObj)

        pc.mel.eval("MLdeleteUnused")

        for usedShader in usedShaders:
            for value in values:
                if usedShader.endswith("_"+value):
                    shortName = usedShader[:-len("_"+value)]
                    if not mc.objExists(shortName):
                        mc.rename(usedShader, shortName)
                    else:
                        pc.warning("Cannot rename " + usedShader + "," + shortName + " already exists !")

        #Execute variation postscript
        if not asBatch:
            pc.warning("You way have variation postscript to apply by hand !")

        print ("{0} objects were deleted:\n{1}".format(len(deletedObjs), "\r\n".join(deletedObjs)))

def replaceVariables(in_sPath, in_sPreset="", in_iDropFirst=0, in_iDropLast=0, in_sDropSeparator="_", in_sForcedPostFix=""):
    postFix = ""

    replaced = in_sPath

    currentScene = os.path.abspath(mc.file(q=True, sn=True))

    if CURRENTSCENEFOLDER in replaced:
        if not os.path.isfile(currentScene):
            mc.warning("Scene not saved, cannot use '{0}'".format(CURRENTSCENEFOLDER))
            return None

        replaced = replaced.replace(CURRENTSCENEFOLDER, os.path.dirname(currentScene))

    if CURRENTSCENENAME in replaced:
        if not os.path.isfile(currentScene):
            mc.warning("Scene not saved, cannot use '{0}'".format(CURRENTSCENENAME))
            return None

        path, ext = os.path.splitext(currentScene)
        if ext != "":
            postFix = ext
            currentScene = currentScene.replace(ext, "")

        currentScene = os.path.basename(currentScene)

        if in_iDropFirst + in_iDropLast > 0 and in_sDropSeparator in currentScene:
            splitScene = currentScene.split(in_sDropSeparator)
            if len(splitScene) > in_iDropFirst:
                splitScene = splitScene[in_iDropFirst:]
            else:
                mc.warning("Scene name too short to drop {0} first elements with separator {1} ({2})".format(in_iDropFirst, in_sDropSeparator, currentScene))

            if len(splitScene) > in_iDropLast:
                splitScene = splitScene[:-in_iDropLast]
            else:
                mc.warning("Scene name too short to drop {0} last elements with separator {1} ({2})".format(in_iDropLast, in_sDropSeparator, currentScene))

            currentScene = in_sDropSeparator.join(splitScene)

        replaced = replaced.replace(CURRENTSCENENAME, currentScene)

    if PRESET in replaced:
        replaced = replaced.replace(PRESET, in_sPreset)

    if postFix == "" and not "." in replaced:
        postFix = in_sForcedPostFix

    return replaced + postFix

def exportVariations(in_nAsset, in_sSourcePath, in_sExportPath, in_sExportFileName, in_iDropFirst=0, in_iDropLast=0, in_sDropSeparator="_", in_bSimulate=True, in_lAlternateRoots=None):
    print ("exportVariations(in_nAsset={0}, in_sSourcePath={1}, in_sExportPath={2}, in_sExportFileName={3}, in_iDropFirst*={4}, in_iDropLast*={5}, in_sDropSeparator*={6}, in_bSimulate=*{7})".format(in_nAsset.name(),
                                                                            in_sSourcePath,
                                                                            in_sExportPath,
                                                                            in_sExportFileName,
                                                                            in_iDropFirst,
                                                                            in_iDropLast,
                                                                            in_sDropSeparator,
                                                                            in_bSimulate
                                                                            ))
    exports = []
    assetName = in_nAsset.name()

    presets = getPresets(in_nAsset)
    if len(presets) > 0:
        sourcePath = replaceVariables(in_sSourcePath)
        
        if sourcePath == None or not os.path.isfile(sourcePath):
            pc.warning("Source path cannot be found : " + str(sourcePath) + "(" + in_sSourcePath + ")")
            return exports

        for preset in presets.keys():
            if not in_bSimulate:
                mc.file(sourcePath, open=True, force=True)
            in_nAsset = pc.PyNode(assetName)

            exportFolder = replaceVariables(in_sExportPath, preset)
            exportFileName = replaceVariables(in_sExportFileName, preset, in_iDropFirst, in_iDropLast, in_sDropSeparator, ".ma")

            if exportFolder == None:
                pc.warning("Export folder cannot be resolved : " + str(exportFolder) + "(" + in_sExportPath + ")")
            elif exportFileName == None:
                pc.warning("Export file name cannot be resolved : " + str(exportFileName) + "(" + in_sExportFileName + ")")
            else:
                applyPreset(in_nAsset, preset)

                if not in_bSimulate:
                    exportPath = os.path.join(exportFolder, exportFileName)
                    cleanCurrent(in_nAsset, True, in_lAlternateRoots)

                    #Execute variation postscript
                    postScriptPath = os.path.join(exportFolder, preset + ".py")
                    
                    if os.path.isfile(postScriptPath):
                        mayaexecpythonfile.execpythonfile(postScriptPath)
                        print ("Variation postScript executed : '{0}'",postScriptPath)
                    else:
                        print ("No variation postScript found ('{0}')",postScriptPath)

                    if not os.path.isdir(exportFolder):
                        os.makedirs(exportFolder)

                    mc.file(rename=exportPath)
                    mc.file(force=True, save=True, type='mayaAscii')
                    exports.append((preset, exportPath))
                print ("preset '{0}' {1}exported to : {2}".format(preset, ("WILL BE " if in_bSimulate else ""), exportPath))
    
    return exports

def changed(*args):
    pass

def exportVariationsClick(*args):
    exportVariations(TOPNODE,   mc.textFieldGrp("tk"+OUTFIT_TAG + "_sourceScene", query=True,text=True),
                                mc.textFieldGrp("tk"+OUTFIT_TAG + "_exportPath", query=True, text=True),
                                mc.textFieldGrp("tk"+OUTFIT_TAG + "_exportFileName", query=True, text=True),
                                mc.intSliderGrp("tk"+OUTFIT_TAG + "_dropFirst", query=True, value=True),
                                mc.intSliderGrp("tk"+OUTFIT_TAG + "_dropLast", query=True, value=True),
                                mc.textFieldGrp("tk"+OUTFIT_TAG + "_dropSep", query=True, text=True),
                                False )

def simulateVariationsClick(*args):
    exportVariations(TOPNODE,   mc.textFieldGrp("tk"+OUTFIT_TAG + "_sourceScene", query=True,text=True),
                                mc.textFieldGrp("tk"+OUTFIT_TAG + "_exportPath", query=True, text=True),
                                mc.textFieldGrp("tk"+OUTFIT_TAG + "_exportFileName", query=True, text=True),
                                mc.intSliderGrp("tk"+OUTFIT_TAG + "_dropFirst", query=True, value=True),
                                mc.intSliderGrp("tk"+OUTFIT_TAG + "_dropLast", query=True, value=True),
                                mc.textFieldGrp("tk"+OUTFIT_TAG + "_dropSep", query=True, text=True),
                                True )

def selInClick(*args):
    pc.select(getIncludedObjects(TOPNODE))

def selExClick(*args):
    pc.select(getExcludedObjects(TOPNODE))

def addSelClick(*args):
    ns = TOPNODE.namespace()
    outfitsProperty = getProperty(TOPNODE, 'tk'+OUTFIT_TAG)
    if outfitsProperty == None:
        return

    sel = pc.ls(sl=True)

    if len(sel) == 0:
        pc.warning("Please select some objects to add to current outfits")
        return

    outfits = getOutfits(TOPNODE)
    objectsOverrides = getOverrides(TOPNODE)
    #print objectsOverrides
    cases = []

    for outfit in outfits.keys():
        current = getCurrent(TOPNODE, outfit)
        if current == "Debug":
            continue
        cases.append("tk_"+outfit+"_is_"+current)

    if len(cases) == 0:
        pc.warning("No outfits selected to add objects (debug is not a correct entry) !")
        return

    #print "outfits", outfits
    #print "objectsOverrides", objectsOverrides

    overridesModified = False

    for selObjMaster in sel:
        selObjs = [selObjMaster]
        if selObjMaster.type() == "transform":
            shapes = selObjMaster.getShapes()
            for shape in shapes:
                selObjs.append(shape)

        for selObj in selObjs:
            shortName = selObj.stripNamespace()[:]
            shader = ""

            if shortName in objectsOverrides:
                print (shortName, "found :", objectsOverrides[shortName])
                shader = objectsOverrides[shortName]["defaultShader"]
            else:
                print (shortName, "NOT found")
                #We will have to add 'defaultShader' fake case
                shaders = getShaders(selObj)
                if len(shaders) > 0:
                    shader = shaders[0].name().split(":")[-1]

                objectsOverrides[shortName] = {'defaultShader':shader}
                overridesModified = True

            for case in cases:
                if case in objectsOverrides[shortName]:
                    mc.warning(shortName + " already belongs to '"+ case +"' !")
                else:
                    objectsOverrides[shortName][case] = {"shader":shader, "visibility":True}
                    overridesModified = True
                    print (shortName, " added to case '"+ case +"'")

    if overridesModified:
        print ("Overrides updated !")
        setOverrides(TOPNODE, objectsOverrides)
        outfitChanged()
    else:
        mc.warning("No modifications in overrides !")

def rebuildLayersClick(*args):
    outfits = getOutfits(TOPNODE)

    #Reset to debug and defaultRenderLayer
    if outfits != None:
        for outfit in outfits.keys():
            setCurrent(TOPNODE, outfit, "Debug", True)
        pc.editRenderLayerGlobals(currentRenderLayer="defaultRenderLayer")

        presets = getPresets(TOPNODE)
        if len(presets) > 0:
            for preset, outfits in presets.iteritems():
                objs = getIncludedObjects(TOPNODE, outfits)

                newLayer = pc.createRenderLayer(name=TOPNODE.namespace()+"layer_"+preset, makeCurrent=True, empty=True)
                pc.editRenderLayerMembers(newLayer, objs, noRecurse=True)
                applyPreset(TOPNODE, preset, True)

                #Reset to debug and defaultRenderLayer
                for outfit in outfits.keys():
                    setCurrent(TOPNODE, outfit, "Debug", True)
                pc.editRenderLayerGlobals(currentRenderLayer="defaultRenderLayer")

        if pc.checkBox("tk"+OUTFIT_TAG + "_cleanOutfits", query=True, value=True):
           remove()

def remSelClick(*args):
    ns = TOPNODE.namespace()
    outfitsProperty = getProperty(TOPNODE, 'tk'+OUTFIT_TAG)
    if outfitsProperty == None:
        return

    sel = pc.ls(sl=True)

    if len(sel) == 0:
        pc.warning("Please select some objects to add to current outfits")
        return

    outfits = getOutfits(TOPNODE)
    objectsOverrides = getOverrides(TOPNODE)
    #print objectsOverrides
    cases = []

    for outfit in outfits.keys():
        current = getCurrent(TOPNODE, outfit)
        if current == "Debug":
            continue
        cases.append("tk_"+outfit+"_is_"+current)


    if len(cases) == 0:
        pc.warning("No outfits selected to add objects (debug is not a correct entry) !")
        return

    #print "outfits", outfits
    #print "objectsOverrides", objectsOverrides

    overridesModified = False

    for selObjMaster in sel:
        selObjs = [selObjMaster]
        if selObjMaster.type() == "transform":
            shapes = selObjMaster.getShapes()
            for shape in shapes:
                selObjs.append(shape)

        for selObj in selObjs:
            shortName = selObj.stripNamespace()

            if shortName in objectsOverrides:
                print (shortName, "found :", objectsOverrides[shortName])
                for case in cases:
                    if case in objectsOverrides[shortName]:
                        del objectsOverrides[shortName][case]
                        print (shortName, " removed from case '"+ case +"'")
                        overridesModified = True
                    else:
                        mc.warning(shortName + " does not belong to '"+ case +"' !")
            else:
                mc.warning(shortName + " not present in overrides !")

    if overridesModified:
        print ("Overrides updated !")
        setOverrides(TOPNODE, objectsOverrides)
        outfitChanged()
    else:
        mc.warning("No modifications in overrides !")

def create(*args):
    createOutfits(TOPNODE, in_sTag="set_outfit", in_sSearch="set_outfit_", in_sReplace="Outfits_variation_", in_sLayerTag="layer", in_sLayerSearch="layer_", in_sLayerReplace="Outfits_variation_", inMembershipsFromLayers=True)
    showUI(TOPNODE)

def remove(*args):
    removeOutfits(TOPNODE)
    showUI(TOPNODE)

def clean(*args):
    cleanCurrent(TOPNODE)
    if mc.control(UINAME, query=True, exists=True):
        mc.deleteUI(UINAME, control=True)

def addPresetClick(*args):
    print ("addPreset")

def showHelp(*args):
    pc.showHelp("https://docs.google.com/document/d/1q_aRS0SVRLwTaLVA8Zm6DHvS6vEcjPFptFu--1kXoe0/pub#h.ktt003ljt55u", absolute=True)

def outfitChanged(*args):
    outfits = getOutfits(TOPNODE)

    if outfits != None:
        for outfit in outfits.keys():
            setCurrent(TOPNODE, outfit, mc.optionMenu("tk"+OUTFIT_TAG + "_" + outfit, query=True, value=True))
        
        refreshOverrides(TOPNODE)

def getOutfitProp(inNs=None):
    outfitProp = 'tk'+OUTFIT_TAG

    if inNs != None:
        outfitProp = inNs + 'tk'+OUTFIT_TAG

    if pc.objExists(outfitProp):
        return pc.PyNode(outfitProp)

    nodes = pc.ls("*:" + 'tk'+OUTFIT_TAG)

    if len(nodes) > 0:
        return nodes[0]

    return None

def showUI(inTopNode=None):
    global UINAME
    global TOPNODE

    ns = ""

    if inTopNode == None:
        sel = pc.selected()
        if len(sel) > 0:
            ns = sel[0].namespace()

        outfitProp = getOutfitProp(ns)

        if outfitProp != None:
            TOPNODE = outfitProp.getParent()
        elif len(sel) == 0:
            pc.warning("Please select an asset top node")
            return
        else:
            TOPNODE = sel[0]
    else:
        TOPNODE = inTopNode

    if mc.control(UINAME, query=True, exists=True):
        mc.deleteUI(UINAME, control=True)

    UINAME = mc.window(UINAME, title='Outfits Manager : ' + TOPNODE.name())
    
    colLayout = mc.columnLayout()

    mc.rowLayout(numberOfColumns=3, columnWidth3=[177,177,30])
    mc.button(label='Store outfits', c=create, width=177)
    mc.button(label='Remove outfits', c=remove, width=177)
    mc.button(label='Help', c=showHelp, width=30)
    mc.setParent(colLayout)

    outfits = getOutfits(TOPNODE)

    mc.frameLayout(label="Outfits", collapsable=True, width=390)

    if outfits != None:
        for outfit in outfits.keys():
            current = getCurrent(TOPNODE, outfit)
            mc.rowLayout(numberOfColumns=2, columnWidth2=[192,192])
            mc.text(label=outfit)
            mc.optionMenu("tk"+OUTFIT_TAG + "_" + outfit, cc=outfitChanged, width=192)
            mc.menuItem(outfit + "_Debug", label="Debug")
            for outfitValue in outfits[outfit]:
                mc.menuItem(outfit + "_" + outfitValue, label=outfitValue)
            mc.optionMenu("tk"+OUTFIT_TAG + "_" + outfit, edit=True, value=current)
            mc.setParent(colLayout)

        if len(outfits) > 1:
            mc.rowLayout(numberOfColumns=2)#, columnWidth3=[110,110,28])
            mc.textFieldGrp( label='Name : ', text='preset1' )
            mc.button(label='Add preset', c=addPresetClick)#, width=110)
            mc.setParent(colLayout)

        mc.setParent(colLayout)
        editLayout = mc.frameLayout(label="Edit", collapsable=True)
        mc.rowLayout(numberOfColumns=2)
        mc.button(label='Select included', c=selInClick, width=192)
        mc.button(label='Select excluded', c=selExClick, width=192)
        mc.setParent(colLayout)
        mc.rowLayout(numberOfColumns=2)
        mc.button(label='Add selection', c=addSelClick, width=192)
        mc.button(label='Remove selection', c=remSelClick, width=192)

        mc.setParent(colLayout)
        mc.rowLayout(numberOfColumns=2)
        mc.button(label='Rebuild layers', c=rebuildLayersClick, width=192)
        pc.checkBox("tk"+OUTFIT_TAG + "_cleanOutfits", label='Clean Outfits', value=True)
        mc.setParent(colLayout)
        mc.button(label='Clean current variation', c=clean, width=384)

        presets = getPresets(TOPNODE)

        if len(presets) > 0:
            if outfits != None and len(outfits) > 1:
                mc.frameLayout(label="Presets", collapsable=True)
                mc.textScrollList("tk"+OUTFIT_TAG + "_presets", append=presets.keys())

            mc.setParent(colLayout)

            colLayout = mc.frameLayout(label="Export", collapsable=True)
            mc.textFieldGrp("tk"+OUTFIT_TAG + "_sourceScene", label='Source scene', text=CURRENTSCENEFOLDER + "\\" + CURRENTSCENENAME)

            mc.textFieldGrp("tk"+OUTFIT_TAG + "_exportPath", label='Export path', text=CURRENTSCENEFOLDER + "\\variations")
            mc.textFieldGrp("tk"+OUTFIT_TAG + "_exportFileName", label='Export filename', text=CURRENTSCENENAME + '_' + PRESET)

            mc.frameLayout(label="Modify file name", collapsable=True, collapse=True)
            mc.intSliderGrp("tk"+OUTFIT_TAG + "_dropFirst", label="Drop first", minValue=0, maxValue=3, fieldMinValue=0, fieldMaxValue=100, field=True, value=0)
            mc.intSliderGrp("tk"+OUTFIT_TAG + "_dropLast", label="Drop last", minValue=0, maxValue=3, fieldMinValue=0, fieldMaxValue=100, field=True, value=1)
            mc.textFieldGrp("tk"+OUTFIT_TAG + "_dropSep", label="Separator", text="_")

            mc.setParent(colLayout)

            mc.rowLayout(numberOfColumns=2)
            mc.button(label='Simulate export', c=simulateVariationsClick, width=192)
            mc.button(label='Export variations', c=exportVariationsClick, width=192)
    else:
        mc.text(label='No outfits created yet...Try "Store outfits"')

    mc.showWindow(UINAME)