import tkBlendShapes as tkBs
import pymel.core as pc

sel = pc.selected()

infs = [n for n in sel if n.type() == "joint"]
meshes = [n for n in sel if n.type() == "transform" and n.getShape() != None and n.getShape().type() == "mesh"]

assert len(meshes) >= 2, "Please select at least two meshes, first the target to modulate, then the base reference"
assert len(infs) >= 1, "Please select at least one joint to modulate positions from its influence"

ref = meshes[-1]
meshes = meshes[:-1]

for mesh in meshes:
    tkBs.cutBsFromInfluences(ref, mesh, infs)