import time
import queue
import primeAlgorithm as pa
def prime_1_Process(ssLst):

    kStart = time.time()
    q      = queue.Queue() # Simple queue can be used here.
    np1    = pa.numPrimesBetween(ssLst,q,'f0')
    np     = 0

    while not q.empty():
        np += q.get()

    # numPrimesBetween returns num primes found in 2 ways; (1)
    # directly (return) and (2) by placing it in a queue.
    # Both ways are doable via this method so they should agree.
    if np1 != np:
        print('Error in primt_1_Propress.')

    exeTime = time.time() - kStart
    return np, exeTime
