import pymel.core as pc

sel = pc.selected()

if len(sel) == 0 and pc.confirmDialog(title='Nothing selected', message="Do you want to lock everything ?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No') == "Yes":
    sel = pc.ls()

for node in sel:
    try:
        pc.lockNode(node, lock=True)
    except:
        pass