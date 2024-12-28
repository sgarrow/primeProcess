import time
import worker as wk
#############################################################

def oneProc(inIterable, numProc, q):

    kStart       = time.time()
    iterableElem = wk.chunkify(inIterable,1)
    results = []
    for el in iterableElem:
        rtnLst = wk.worker( 'f0', # Process Name.
                            q,    # Queue.
                            el )  # Element.
        results.append(rtnLst)    # [iterableElem, numPrimes]
    return time.time() - kStart 
#############################################################
