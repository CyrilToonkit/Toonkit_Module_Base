import tkPalette

message = "Please two geometries, the geometry to copy the shaders to first, then the reference."

types = ["mesh"]

sel = pc.selected()

assert len(sel) > 1, message

assert sel[0].type() in types or (not sel[0].getShape() is None and sel[0].getShape().type() in types, message

assert sel[1].type() in types or (not sel[1].getShape() is None and sel[1].getShape().type() in types, message

tkPalette.gatorShaders()