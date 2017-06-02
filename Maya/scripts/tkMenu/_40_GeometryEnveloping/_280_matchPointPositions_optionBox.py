import tkBlendShapes
import pymel.core as pc

UINAME = "matchPointPositionsOptionWD"

def matchPointPositions(*args):#I'll take scope:string(All, LeftOnly, RightOnly), treshold:float
    print "matchPointPositions(", args
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        sided = False
        rightToLeft=False
        treshold=2.0
        offset=0.0

        if len(args) > 1:
            if args[1] == "Right only":
                sided = True
                rightToLeft = True
            elif args[1] == "Left only":
                sided = True

        if len(args) > 2:
            treshold = args[2]

        if len(args) > 3:
            offset = args[3]
 
        for selObj in sel[:-1]:
            tkBlendShapes.matchPointPositions(sel[-1], selObj, sided, rightToLeft, treshold, offset)

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
