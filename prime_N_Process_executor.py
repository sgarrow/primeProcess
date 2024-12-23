import time
import multiprocessing    as mp
import concurrent.futures as cf
import getStartStopLst    as gssl
import primeAlgorithm     as pa

def prime_N_Process_executor( ssInLst, numProc ):

    kStart = time.time()
    m     = mp.Manager()
    mmpQ  = m.Queue() # mp.Manager queue must be used here.
    ssLst = gssl.getStartStopLst(ssInLst,numProc)

    with cf.ProcessPoolExecutor() as executor:


        results = [ executor.submit( pa.numPrimesBetween,
                                     'e{}'.format(ii), # Process Name.
                                     mmpQ,             # Queue.
                                     ssLst[ii] )       # Iterable.
                    for ii in range(numProc)
                  ]

        np1 = 0
        # Can access return value (sort of) directly.
        for f in cf.as_completed(results):
            np1 += f.result()

    np = 0
    while not mmpQ.empty():
        np += mmpQ.get()

    # numPrimesBetween returns num primes found in 2 ways; (1)
    # directly (return) and (2) by placing it in a queue.
    # Both ways are doable via this method so they should agree.
    if np1 != np:
        print('Error in prime_N_Process_executor.')

    exeTime = time.time() - kStart
    return np, exeTime
