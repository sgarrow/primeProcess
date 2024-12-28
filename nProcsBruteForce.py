import time
import multiprocessing as mp
import worker          as wk
#######################################################################

def nProcsBruteForce( ssInLst, numProc, q ):

    kStart  = time.time()
    ssLst   = wk.chunkify(ssInLst,numProc)
    procLst = []

    for ii in range(numProc):
        # Cannot access return value from proc directly.
        proc = mp.Process( target = wk.worker,
                           args   = ( 'p{}'.format(ii), # Process Name.
                                      q,                # Queue.
                                      ssLst[ii] ))      # Iterable.
        proc.start()
        procLst.append(proc)

    for p in procLst:
        p.join()

    return time.time() - kStart 
#######################################################################
