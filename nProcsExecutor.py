import time
import multiprocessing    as mp
import concurrent.futures as cf
import worker             as wk
######################################################################

def nProcsExecutor( inIterable, numProc, q ):

    kStart      = time.time()
    iterableElem = wk.chunkify(inIterable,numProc)

    with cf.ProcessPoolExecutor() as executor:


        results = [ executor.submit( wk.worker,
                                     'e{}'.format(ii), # Process Name.
                                     q,                # Queue.
                                     iterableElem[ii] ) # Iterable.
                    for ii in range(len(inIterable))
                  ]

        # Can access return value (sort of) directly.
        for f in cf.as_completed(results):
            pass
            #print(f.result())

    return time.time() - kStart 
######################################################################
