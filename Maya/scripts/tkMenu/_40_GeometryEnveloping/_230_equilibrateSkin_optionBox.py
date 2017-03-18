import tkMayaCore as tkc
import pymel.core as pc

UINAME = "equilibrateSkinOptionWD"

def equilibrateSkinClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    strPrefixes = pc.textFieldGrp("equilibrateSkinOptionPrefixes",query=True, text=True)
    prefixes = ["Left","Right"]
    splitPrefixes = strPrefixes.split(",")
    if splitPrefixes[0] != "":
        prefixes[0] = splitPrefixes[0]
    if len(splitPrefixes) > 1 and splitPrefixes[1] != "" and splitPrefixes[1] != prefixes[0]:
        prefixes[1] = splitPrefixes[1]

    tkc.equilibrateSelPointsWeights(pc.checkBox("equilibrateSkinOptionRightToLeft", query=True, value=False), inPrefixes = prefixes)

def equilibrateSkinOption(*args):
    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("equilibrateSkinOptionWD", title='EquilibrateSkin')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select center loop points of a skinned mesh')

    pc.checkBox("equilibrateSkinOptionRightToLeft", label='Right to left', value=False)
    pc.textFieldGrp("equilibrateSkinOptionPrefixes", label='Prefixes', text="Left,Right")
    pc.button(label='Apply', c=equilibrateSkinClick, width=177)

    pc.showWindow(UINAME)

equilibrateSkinOption()