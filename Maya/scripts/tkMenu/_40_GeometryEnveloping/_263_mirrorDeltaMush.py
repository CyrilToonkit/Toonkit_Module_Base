#Mirror deltaMush Map
DEFORMER = "deltaMush"
meshesT = pc.filterExpand(sm=12)

for meshT in meshesT:
    deltaMushes = pc.ls(pc.listHistory(meshT, gl=True, pdo=True, lf=True, f=False, il=2), type=DEFORMER)

    if len(deltaMushes) == 0:
        pc.warning("No {0} found on {1}".format(DEFORMER, meshT.name()))
        continue

    pc.copyDeformerWeights(ss=meshT, ds=meshT, sd=deltaMushes[0]  , dd=deltaMushes[0]  , mirrorMode='YZ', mirrorInverse=False)