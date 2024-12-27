import time
import queue
import worker as wk
#############################################################################

def oneProc(ssLst):

    kStart = time.time()
    q      = queue.Queue() # Simple queue can be used here.
    np1    = wk.worker( 'f0',   # Process Name.
                        q,      # Queue.
                        ssLst ) # Iterable.
    np     = 0

    while not q.empty():
        np += q.get()

    # worker returns num primes found in 2 ways; (1)
    # directly (return) and (2) by placing it in a queue.
    # Both ways are doable via this method so they should agree.
    if np1 != np:
        print('Error in primt_1_Process.')

    exeTime = time.time() - kStart
    return np, exeTime
#############################################################################
