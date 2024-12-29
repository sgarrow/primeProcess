import time
import multiprocessing as mp
import worker          as wk
################################################################

def nProcsBruteForce( flatIterableIn, numProc, q, wrkF  ):

    kStart      = time.time()
    chunkedIterable = wk.chunkify(flatIterableIn,numProc)
    procLst     = []

    for ii in range(len(chunkedIterable)):
        # Cannot access return value from proc directly.
        proc = mp.Process( 
               target = wrkF,
               args   = ( 'bf{}'.format(ii),     # Process Name.
                          q,                     # Queue.
                          chunkedIterable[ii] )) # Iterable.
        proc.start()
        procLst.append(proc)

    for p in procLst:
        p.join()

    return time.time() - kStart
################################################################
