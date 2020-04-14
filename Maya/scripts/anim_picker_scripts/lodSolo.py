import pymel.core as pc

import tkOptimize as tko

def do(inNs):
    attrName = "Body_LOD"

    globalAttrs = pc.ls(inNs + "*." + attrName)

    inNss = [inNs]

    if len(globalAttrs) > 0:
        val = globalAttrs[0].get()
        solo=True

        if val == 0:
            globalAttrsAll = pc.ls(["*." + attrName, "*:*." + attrName, "*:*:*." + attrName])
            globalAttrsAll.remove(globalAttrs[0])

            if len(globalAttrsAll) > 0:
                if globalAttrsAll[0].get() != val:
                    inNss=[str(n.namespace()) for n in globalAttrsAll + globalAttrs]
                    solo = False

        print "setLOD",0,inNss,[attrName],solo
        tko.setLOD(0, inNss, inAttrs=[attrName], inSolo=solo)