import pymel.core as pc
import tkOutfits

def getLongestName(inNode):
    return inNode.fullPath() if isinstance(inNode, pc.nodetypes.DagNode) else inNode.name()


selObjs = pc.ls(sl=True)

selArray = [getLongestName(selObj) for selObj in selObjs]

layersAdjusts = tkOutfits.getAllLayersAdjustments()

objectsOverrides = {}

for layersAdjust in layersAdjusts.keys():
    for objectAdjust in layersAdjusts[layersAdjust].keys():
        overrides = layersAdjusts[layersAdjust][objectAdjust]
        for key in overrides.keys():
            if key == None:
                continue

            if not objectAdjust in objectsOverrides:
                objectsOverrides[objectAdjust] = {}

            if not layersAdjust in objectsOverrides[objectAdjust]:
                objectsOverrides[objectAdjust][layersAdjust] = {}

            objectsOverrides[objectAdjust][layersAdjust][key] = overrides[key]

for objectAdjust in objectsOverrides.keys():
    if len(selObjs) == 0 or objectAdjust in selArray:
        obj = pc.PyNode(objectAdjust)
        print "\r\n *** {0} ***".format(obj.name())
        for layerAdjust in objectsOverrides[objectAdjust]:
            print " - {0}".format(layerAdjust)
            overrides = objectsOverrides[objectAdjust][layerAdjust]
            for override in overrides.keys():
                print "   - {0}.{1} : {2}".format(obj.name(), override, overrides[override])
