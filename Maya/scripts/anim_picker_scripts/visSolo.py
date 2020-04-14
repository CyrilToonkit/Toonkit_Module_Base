import pymel.core as pc

import tkOptimize as tko

def do(inNs):
    attrName = "Global"

    globalAttrs = pc.ls(inNs + "*." + attrName)

    inNss = [inNs]

    if len(globalAttrs) > 0:
        val = globalAttrs[0].get()
        solo=True

        if val:
            globalAttrsAll = pc.ls(["*." + attrName, "*:*." + attrName, "*:*:*." + attrName])
            globalAttrsAll.remove(globalAttrs[0])

            if len(globalAttrsAll) > 0:
                if globalAttrsAll[0].get() != val:
                    inNss=[str(n.namespace()) for n in globalAttrsAll + globalAttrs]
                    solo = False

        tko.setLOD(1, inNss, inAttrs=[attrName], inSolo=solo)