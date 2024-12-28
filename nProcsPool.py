import time
import functools       as ft
import multiprocessing as mp
import worker          as wk
###################################################

def nProcsPool( inIterable, numProc, q ):

    kStart      = time.time()
    iterableElem = wk.chunkify(inIterable,numProc)
    newFunc     = ft.partial( wk.worker, 'pN', q )
    with mp.Pool( len(iterableElem) ) as aPool:
        results = aPool.map( newFunc, iterableElem )
    #print(results)

    return time.time() - kStart 
###################################################

