import tkBlendShapes
import pymel.core as pc

UINAME = "matchPointPositionsOptionWD"

def wmIndexedToFlat(inWm, inNbPoints=None, inGeo=None, inNeutralValue=0.0):
    assert inNbPoints is not None or inGeo is not None, "inNbPoints and inGeo can't both be None !"

    if inNbPoints is None:
        inNbPoints = tkc.getPointsCount(tkc.getNode(inGeo))

    return [inWm.get(i, inNeutralValue) for i in range(inNbPoints)]

def wmFlatToIndexed(inWm, inNeutralValue=0.0):
    return {i:v for i, v in enumerate(inWm) if v != inNeutralValue}

def matchPointPositions(*args):#I'll take scope:string(All, LeftOnly, RightOnly), treshold:float

    richSel = tkc.getSoftSelections()

    if len(richSel) > 1:
        sided = False
        rightToLeft=False
        treshold=2.0

        if len(args) > 1:
            if args[1] == "Right only":
                sided = True
                rightToLeft = True
            elif args[1] == "Left only":
                sided = True

        if len(args) > 2:
            treshold = args[2]

        for richSelObj, richSelComps in richSel[:-1]:
            if sided or richSelComps is None:
                tkBlendShapes.matchPointPositions(tkc.getNode(richSel[-1][0]), tkc.getNode(richSelObj), sided, rightToLeft, treshold)
            else:
                tkBlendShapes._matchPointPositions(tkc.getNode(richSel[-1][0]), tkc.getNode(richSelObj), inMap=wmIndexedToFlat(richSelComps, inGeo=richSelObj))
    else:
        pc.error("Please select at least two objects (any number of meshes to receive point positions, then a \"Reference\" mesh) !")

def matchPointPositionsClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    matchPointPositions(True, pc.optionMenu("matchOptionScope",query=True, value=True), pc.floatSliderGrp("matchOptionTreshold",query=True, value=True), pc.floatSliderGrp("matchOptionOffset",query=True, value=True))

def matchPointPositionsOption(*args):
    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("matchPointPositionsOptionWD", title='Match point positions')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select any number of meshes to match first, then the ref mesh')

    pc.optionMenu("matchOptionScope", label='Scope')
    pc.menuItem("All", label="All")
    pc.menuItem("LeftOnly", label="Left only")
    pc.menuItem("RightOnly", label="Right only")
    pc.floatSliderGrp("matchOptionTreshold", label='Center treshold', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=0.0, fieldMaxValue=1000000, value=2.0)
    pc.floatSliderGrp("matchOptionOffset", label='Center offset', field=True,pre=2, minValue=-50.0, maxValue=50.0, fieldMinValue=-1000000, fieldMaxValue=1000000, value=0.0)

    pc.button(label='Apply', c=matchPointPositionsClick, width=177)

    pc.showWindow(UINAME)

matchPointPositionsOption()
