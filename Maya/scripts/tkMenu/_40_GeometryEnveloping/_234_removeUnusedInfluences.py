import tkMayaCore as tkc

for selObj in pc.selected():
	skinCls = tkc.getSkinCluster(selObj)
	if not skinCls is None:
		tkc.removeUnusedInfs(skinCls)