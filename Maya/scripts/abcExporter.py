import os

import pymel.core as pc

import Toonkit_Core.tkCore as tc
import tkMayaCore as tkc

def writeJobArgs(inJobDict):
    jobFlags = []

    for argName, argValue in inJobDict.items():
        if isinstance(argValue, bool):
            if not argValue:
                continue

            jobFlags.append("-{}".format(argName))
        else:
            if isinstance(argValue, (list, tuple)):
                if argName == "root":
                    argsValue = argValue[0]
                    if len(argValue) > 1:
                        argsValue += " " + " ".join(["-{0} {1}".format(argName, v) for v in argValue[1:]])
                    argValue = argsValue
                else:
                    argValue = " ".join([str(v) for v in argValue])

            jobFlags.append("-{0} {1}".format(argName, argValue))

    return " ".join(jobFlags)

META_SUFFIX = "meta__"

ABC_DEFAULT = {
    "dataFormat":"ogawa",

    "verbose"           :False,
    "noNormals"         :False,
    "ro"                :False,#Renderable Only
    "stripNamespaces"   :False,
    "uvWrite"           :True,
    "writeColorSets"    :True,
    "writeFaceSets"     :False,
    "wholeFrameGeo"     :False,
    "worldSpace"        :True,
    "writeVisibility"   :True,
    "eulerFilter"       :False,
    "autoSubd"          :False,#Write Creases ?
    "writeUVSets"       :True,

    "attr"              :False,
    "attrPrefix"        :False,

    "frameRange"        :None,

    "pythonPerFrameCallback":False,

    META_SUFFIX + "Folder"  :None,
    META_SUFFIX + "Pattern" :"{}.abc",
}

def getGeoSet(inNs, inAssetName):
    selSet = tkc.getNode("{0}:{1}_geo_selset".format(inNs, inAssetName))
    return selSet.flattened() if not selSet is None else []

def getAllMeshesT():
    return [m.getParent() for m in pc.ls(type="mesh")]

def getCamera():
    cameras = [m.getParent() for m in pc.ls(type="camera")]

    for camera in cameras:
        if not camera.stripNamespace() in ["persp", "top", "front", "side"]:
            return [camera]

    return [cameras[0]] if len(cameras) > 0 else []


ABC_PRESETS = {
    "all":{"def":getAllMeshesT, "args":[], "overrides":{}}
}

def abcPrepare(inFolder=None, inCachePresets=ABC_PRESETS, inDefaults=ABC_DEFAULT, inSetName="ABC_Export", **inKwargs):
    """Prepare an abc export with a set hierarchy"""

    #Top container
    #-------------------------------------------------------------------------------------

    #pack base preset
    basePreset = inDefaults.copy()
    basePreset.update(inKwargs)

    #By default set timeRange to scene info
    if basePreset.get("frameRange") is None:
        basePreset["frameRange"] = (pc.playbackOptions(query=True, animationStartTime=True),
                                    pc.playbackOptions(query=True, animationEndTime=True))

    #By default set meta__Folder to inFolder
    if basePreset.get(META_SUFFIX + "Folder") is None:
        basePreset[META_SUFFIX + "Folder"] = inFolder

    #Fail if we still have undefined (None) values at this point
    noneValues = [key for key, value in basePreset.items() if value is None]
    assert len(noneValues) == 0, "Preset contains undefined values ! ({0})".format(",".join(noneValues))

    #Delete old preparation if exists
    if pc.objExists(inSetName):
        oldSet = pc.PyNode(inSetName)
        pc.delete(oldSet.members())
        try:
            pc.delete(oldSet)
        except:
            pass

    #Create root set 
    mayaSet = pc.sets(empty=True, name=inSetName)
    tkc.decorate(mayaSet, basePreset)

    #Sub-sets
    #-------------------------------------------------------------------------------------
    for cachePresetName, cachePresetProc in inCachePresets.items():
        proc = cachePresetProc.get("def")

        objs = proc(*cachePresetProc["args"]) if not proc is None else cachePresetProc.get("args", [])

        if len(objs) > 0:
            subSet = pc.sets(empty=True, name=cachePresetName)
            subSet.addMembers(objs)

            tkc.decorate(subSet, cachePresetProc.get("overrides", {}))

            pc.sets(mayaSet, forceElement=subSet)
        else:
            pc.warning('cache Preset {} return no objects'.format(cachePresetName))

    return mayaSet

def abcExport(inSetName="ABC_Export", inClean=False, inDryRun=False):
    """Export alembic caches from prepared sets (see abcPrepare)"""
    assert pc.objExists(inSetName), "Can't find export set '{0}'".format(inSetName)

    jobs = []
    files = []

    mayaSet = pc.PyNode(inSetName)
    basePreset = tkc.readDecoration(mayaSet)

    for cachePresetSet in mayaSet.members():
        specPreset = basePreset.copy()
        specPreset.update(tkc.readDecoration(cachePresetSet))

        specPreset["file"] = os.path.join(
            specPreset[META_SUFFIX + "Folder"],
            specPreset[META_SUFFIX + "Pattern"].format(cachePresetSet.name())
            )

        files.append(specPreset["file"])

        keys = list(specPreset.keys())
        for key in keys:
            if key.startswith(META_SUFFIX):
                del specPreset[key]

        specPreset["root"] = cachePresetSet.members(cachePresetSet)

        jobs.append(writeJobArgs(specPreset))

    if inDryRun:
        print( "DRY RUN : {0} JOBS :\n".format(len(jobs)),"\n".join(jobs))
    else:
        if len(jobs) > 0:

            #Parallel evaluation is still uncertain for this task (especially in batch)
            mode = pc.evaluationManager(query=True, mode=True)
            if mode != ["off"]:
                pc.evaluationManager(mode="off")
            else:
                mode = None

            pc.AbcExport(j=jobs)

            if not mode is None:
                pc.evaluationManager(mode=mode[0])

            print( "EXPORTED :\n","\n".join(files))
        else:
            pc.warning("Nothing exported !")

    if inClean:
        for cachePresetSet in mayaSet.members():
            pc.delete(cachePresetSet)
        
        try:
            pc.delete(mayaSet)
        except:
            pass

    return files