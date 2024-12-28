import time
import worker as wk
#############################################################

def oneProc(inIterable, numProc, q):

    kStart  = time.time()
    ssLst   = wk.chunkify(inIterable,1)
    results = []
    for iterbleElem in ssLst:
        rtnLst = wk.worker( 'f0',         # Process Name.
                            q,            # Queue.
                            iterbleElem ) # Iterable.
        results.append(rtnLst) # [ iterableElem, numPrimes ]
    return time.time() - kStart 
#############################################################
