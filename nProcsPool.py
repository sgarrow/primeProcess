import time
import functools       as ft
import multiprocessing as mp
import worker          as wk
############################################################

def nProcsPool( flatIterableIn, numProc, q ):

    kStart  = time.time()
    chunkedIterable = wk.chunkify( flatIterableIn, numProc )
    newFunc = ft.partial( wk.worker, 'pN', q )

    with mp.Pool( len(chunkedIterable) ) as aPool:
        results = aPool.map( newFunc, chunkedIterable )
    #print(results)

    return time.time() - kStart
############################################################
