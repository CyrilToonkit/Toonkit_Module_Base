import pymel.core as pc

import tkOptimize as tko

def do(inNs):
    attrName = "Body_LOD"

    globalAttrs = pc.ls(inNs + "*." + attrName)

    if len(globalAttrs) > 0:
        val = globalAttrs[0].get()

        tko.setLOD(not val, [inNs], inAttrs=[attrName])