import time
import functools       as ft
import multiprocessing as mp
import worker          as wk
###################################################

def nProcsPool( ssInLst, numProc, q ):

    kStart  = time.time()
    ssLst  = wk.chunkify(ssInLst,numProc)
    newFunc = ft.partial( wk.worker, 'pN', q )
    with mp.Pool( numProc ) as aPool:
        results = aPool.map( newFunc, ssLst )
    #print(results)

    return time.time() - kStart 
