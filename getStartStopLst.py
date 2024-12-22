import pprint as pp

def getStartStopLst( ssInLst, numProc ):
    start = ssInLst[0]
    end   = ssInLst[1]
    ssLst = []
    chunkSize  = (end-start)//numProc
    for ii in range(numProc):
        chunkStart = ii*chunkSize + start + ii
        if chunkStart > end:
            break
        chunkEnd   = chunkStart + chunkSize
        if chunkEnd > end:
            chunkEnd = end
        ssLst.append([chunkStart,chunkEnd])
    #pp.pprint(ssLst)
    return ssLst
