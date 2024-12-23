import time
import multiprocessing as mp
import getStartStopLst as gssl
import primeAlgorithm  as pa

def prime_N_Process_bruteForce( ssInLst, numProc ):

    numCpus = mp.cpu_count() # Just FYI.
    print(' Num cpus = {}\n '.format(numCpus))

    kStart  = time.time()
    mpQ     = mp.Queue() # mp queue must be used here.
    ssLst   = gssl.getStartStopLst(ssInLst,numProc)
    procLst = []

    for ii in range(numProc):
        # Cannot access return value from proc directly.
        proc = mp.Process( target = pa.numPrimesBetween,
                           args   = ( 'p{}'.format(ii), # Process Name.
                                      mpQ,              # Queue.
                                      ssLst[ii] ))      # Iterable.
        proc.start()
        procLst.append(proc)

    for p in procLst:
        p.join()

    # Directly returning vals from .Process isn't possible
    # in the same way as from a regular func. So the worker
    # funcs all put their rtn vals in the same (shared) queue.
    np = 0
    while not mpQ.empty():
        np += mpQ.get()
    exeTime = time.time() - kStart
    return np, exeTime
