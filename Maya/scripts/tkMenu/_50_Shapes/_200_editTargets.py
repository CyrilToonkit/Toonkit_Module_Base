import tkBlendShapes
import pymel.core as pc

UINAME = "editTargetsWD"

def editTargets(*args):
    bs = None

    selObjs = pc.ls(sl=True)

    for selObj in selObjs:
        if selObj.type() != "blendShape":
            bsOps = pc.ls(pc.listHistory(selObj, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
            if len(bsOps) > 0:
                bs = bsOps[0].name()
        else:
            bs = selObj.name()

    if bs == None:
        pc.warning("No blendShape found in selection !")
        return

    global UINAME
    global UITAG

    UITAG = bs

    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("editTargetsWD", title='Edit blendShape targets')

    colLayout = pc.columnLayout()

    arrayAttrs = pc.listAttr("{0}.weight".format(bs), multi=True)

    pc.optionMenu("editTargetsTargets", label='Targets')
    for arrayAttr in arrayAttrs:
        index = tkBlendShapes.getBSIndexFromTarget(bs, arrayAttr)

        pc.menuItem(arrayAttr, label="{0} ({1})".format(arrayAttr, index + 1))

    pc.rowLayout(numberOfColumns=3)
    pc.button(label='Edit Target', c=editTargetsClick, width=128)
    pc.button(label='Edit all targets', c=editAllTargetsClick, width=128)
    pc.button(label='Remove Target', c=removeTargetsClick, width=128)

    pc.showWindow(UINAME)

def editTargetsClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    if UITAG == None or not pc.objExists(UITAG):
        pc.warning("No blendShape node given !")
        return

    target = pc.optionMenu("editTargetsTargets",query=True, value=True).split(" ")[0]
    shape = tkBlendShapes.editTarget(UITAG, target, corrective=None)

    if shape != None:
        pc.select(shape, replace=True)

def editAllTargetsClick(*args):
    if UITAG == None or not pc.objExists(UITAG):
        pc.warning("No blendShape node given !")
        return

    allTargets = tkBlendShapes.editTargets(UITAG)

    if len(allTargets) > 0:
        pc.select(allTargets, replace=True)

def removeTargetsClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    if UITAG == None or not pc.objExists(UITAG):
        pc.warning("No blendShape node given !")
        return

    target = pc.optionMenu("editTargetsTargets",query=True, value=True).split(" ")[0]
    source = tkBlendShapes.getSource(UITAG)

    shape = tkBlendShapes.editTarget(UITAG, target)
    pc.blendShape(UITAG, edit=True, rm=True, target=[source, 2, target, 1])
    pc.delete(shape)
    pc.select(source, replace=True)
    editTargets()

def cleanTargets(*args):
    selObjs = pc.ls(sl=True)

    for selObj in selObjs:
        if selObj.type() != "blendShape":
            bsOps = pc.ls(pc.listHistory(selObj, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
            for bsOp in bsOps:
                tkBlendShapes.cleanUpBlendShapeWeights(bsOp.name())
        else:
            tkBlendShapes.cleanUpBlendShapeWeights(selObj.name())

editTargets()