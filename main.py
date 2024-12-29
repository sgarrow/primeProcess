import queue
import multiprocessing  as mp
import oneProc          as op
import nProcsBruteForce as npb
import nProcsExecutor   as npe
import nProcsPool       as npp
import worker           as wrk

VER = '\n Version 1.12. 28-Dec-2024.'
#############################################################################

def printResults( fName, inQ, inExeTime ):

    print( '{:<18} execution time = {:5.1f} seconds.'.\
        format(fName,inExeTime))

    totalNumPrimes = 0
    while not inQ.empty():
        qEl = inQ.get()
        totalNumPrimes += qEl[2]

        print(' (proc = {}) Num primes in {} = {:,}'.\
            format(qEl[0], qEl[1], qEl[2]))

    print(' Total primes = {:,}\n'.format(totalNumPrimes))
#############################################################################

def doWrk( inNumProc, inFlatIterable, inWrkFunc ):
    status = ' SUCCESS\n'
    if 0 < numProc <= numCores:
        q = queue.Queue() # Simple queue can be used here.
        exeTime = op.oneProc( inFlatIterable, 1, q, inWrkFunc )
        printResults( ' oneProc', q, exeTime )
    
        q = mp.Queue()    # mp queue must be used here.
        exeTime = npb.nProcsBruteForce(inFlatIterable,inNumProc,q,inWrkFunc)
        printResults( ' nProcsBruteForce', q, exeTime )
    
        m = mp.Manager()
        q = m.Queue()     # mp.Manager queue must be used here.
        exeTime = npe.nProcsExecutor(inFlatIterable,inNumProc,q,inWrkFunc)
        printResults( ' nProcsExecutor', q, exeTime )
    
        m = mp.Manager()
        q = m.Queue()     # mp.Manager queue must be used here.
        exeTime = npp.nProcsPool(inFlatIterable,inNumProc,q,inWrkFunc)
        printResults( ' nProcsPool', q, exeTime )
    else:
        status = ' FAIL\n'
    return status
#############################################################################

if __name__ == '__main__':

    status = ' SUCCESS\n'
    numCores = mp.cpu_count() # Just FYI.
    numProc  = 16 # Change value of numProcs as desired up to numCores.

    print(VER)
    print(' Num Cores Available = {}'.format(numCores))
    print(' Num Cores Requested = {}\n'.format(numProc))

    ###############
    flatIterable = [ [    1,  5000], [ 5001, 10000], [10001, 15000],
                     [15001, 20000], [20001, 25000], [25001, 30000],
                     [30001, 35000], [35001, 40000], [40001, 45000],
                     [45001, 50000]
                   ]
    wrkFunc = wrk.primeWorker
    status = doWrk( numProc, flatIterable, wrkFunc )
    print(status)
    ###############

    ###############
    flatIterable = [ 'f0.txt',  'f1.txt',  'f2.txt', 'f3.txt',
                     'f4.txt',  'f5.txt',  'f6.txt', 'f7.txt',
                     'f8.txt',  'f9.txt',  'f10.txt','f11.txt',
                     'f12.txt', 'f13.txt'
                   ]
    wrkFunc = wrk.fileWorker
    status = doWrk( numProc, flatIterable, wrkFunc )
    print(status)
    ###############

#############################################################################
