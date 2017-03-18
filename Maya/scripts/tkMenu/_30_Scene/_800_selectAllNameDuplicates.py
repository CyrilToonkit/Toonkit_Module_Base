import tkMayaCore as tkc
import pymel.core as pc

namesDic = tkc.getDuplicates(inLog=True)

dupObjs = []
for name in namesDic:
    dupObjs.extend(namesDic[name])

pc.select(dupObjs)