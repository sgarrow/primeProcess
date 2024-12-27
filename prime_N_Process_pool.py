import time
import functools       as ft
import multiprocessing as mp
import primeAlgorithm  as pa

def prime_N_Process_pool( ssInLst, numProc ):

    kStart  = time.time()
    m       = mp.Manager()
    mmpQ    = m.Queue() # mp.Manager queue must be used here.
    ssLst   = pa.getStartStopLst(ssInLst,numProc)
    newFunc = ft.partial( pa.numPrimesBetween, 'pN', mmpQ )
    with mp.Pool( numProc ) as aPool:
        results = aPool.map( newFunc, ssLst )

    np1 = sum(results)
    np  = 0
    while not mmpQ.empty():
        np += mmpQ.get()

    # numPrimesBetween returns num primes found in 2 ways; (1)
    # directly (return) and (2) by placing it in a queue.
    # Both ways are doable via this method so they should agree.
    if np1 != np:
        print('Error in prime_1_Process_pool.')

    exeTime = time.time() - kStart
    return np, exeTime
