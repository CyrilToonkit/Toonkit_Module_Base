#Copy deltaMush Map
DEFORMER = "deltaMush"
allSel = pc.filterExpand(sm=12)

if len(allSel) < 2:
    pc.warning("Please select any number of meshes then the reference one")
else:
    meshesT = allSel[:-1]
    meshRefT = allSel[-1]

    refDeltaMushes = pc.ls(pc.listHistory(meshRefT, gl=True, pdo=True, lf=True, f=False, il=2), type=DEFORMER)

    if len(refDeltaMushes) > 0:
        
        for meshT in meshesT:
            deltaMushes = pc.ls(pc.listHistory(meshT, gl=True, pdo=True, lf=True, f=False, il=2), type=DEFORMER)
            if len(deltaMushes) == 0:
                pc.warning("No {0} found on {1}".format(DEFORMER, meshT))
                continue
                
            pc.copyDeformerWeights(ss=meshRefT, ds=meshT, sd=refDeltaMushes[0]  , dd=deltaMushes[0])
    else:
        pc.warning("No {0} found on {1}".format(DEFORMER, meshRefT))