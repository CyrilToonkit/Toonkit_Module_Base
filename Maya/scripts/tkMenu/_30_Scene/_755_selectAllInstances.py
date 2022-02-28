"""
Select and logs all shape instances found in the scene
"""
import tkMayaCore as tkc
import pymel.core as pc

sel = pc.selected()

instancesDic = tkc.getInstances(inLog=True)

uniqueInstances = []

for instanceName, instances in instancesDic.items():
	uniqueInstances.extend(instances)

pc.select(uniqueInstances)