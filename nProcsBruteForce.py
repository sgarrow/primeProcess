import time
import multiprocessing as mp
import worker          as wk
#######################################################################

def nProcsBruteForce( inIterable, numProc, q ):

    kStart      = time.time()
    iterableElem = wk.chunkify(inIterable,numProc)
    procLst     = []

    for ii in range(len(iterableElem)):
        # Cannot access return value from proc directly.
        proc = mp.Process( target = wk.worker,
                           args   = ( 'bf{}'.format(ii), # Process Name.
                                      q,                 # Queue.
                                      iterableElem[ii] )) # Iterable.
        proc.start()
        procLst.append(proc)

    for p in procLst:
        p.join()

    return time.time() - kStart 
#######################################################################
