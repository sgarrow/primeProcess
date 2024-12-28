import time
import multiprocessing    as mp
import concurrent.futures as cf
import worker             as wk
######################################################################

def nProcsExecutor( ssInLst, numProc, q ):

    kStart = time.time()
    ssLst  = wk.chunkify(ssInLst,numProc)

    with cf.ProcessPoolExecutor() as executor:


        results = [ executor.submit( wk.worker,
                                     'e{}'.format(ii), # Process Name.
                                     q,                # Queue.
                                     ssLst[ii] )       # Iterable.
                    for ii in range(numProc)
                  ]

        # Can access return value (sort of) directly.
        for f in cf.as_completed(results):
            pass
            #print(f.result())

    return time.time() - kStart 
######################################################################
