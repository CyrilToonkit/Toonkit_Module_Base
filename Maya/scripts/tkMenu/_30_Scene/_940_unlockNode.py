import pymel.core as pc

sel = pc.selected()

if len(sel) == 0 and pc.confirmDialog(title='Nothing selected', message="Do you want to unlock everything ?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No') == "Yes":
    sel = pc.ls()

for node in sel:
    try:
        pc.lockNode(node, lock=False)

        node.t.setLocked(False)
        node.tx.setLocked(False)
        node.ty.setLocked(False)
        node.tz.setLocked(False)

        node.r.setLocked(False)
        node.rx.setLocked(False)
        node.ry.setLocked(False)
        node.rz.setLocked(False)

        node.s.setLocked(False)
        node.sx.setLocked(False)
        node.sy.setLocked(False)
        node.sz.setLocked(False)
    except:
        pass