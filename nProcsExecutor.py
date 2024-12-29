import time
import concurrent.futures as cf
import worker             as wk
######################################################################

def nProcsExecutor( flatIterableIn, numProc, q, wrkF  ):

    kStart      = time.time()
    chunkedIterable = wk.chunkify( flatIterableIn, numProc )

    with cf.ProcessPoolExecutor() as executor:
        results = [ executor.submit( wrkF,
                                     'e{}'.format(ii), # Process Name.
                                     q,                # Queue.
                                     chunkedIterable[ii] ) # Iterable.
                    for ii in range(len(chunkedIterable))
                  ]

        # Can access return value (sort of) directly.
        for f in cf.as_completed(results):
            pass
            #print(f.result())

    return time.time() - kStart
######################################################################
