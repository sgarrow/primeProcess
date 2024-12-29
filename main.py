import queue
import multiprocessing  as mp
import oneProc          as op
import nProcsBruteForce as npb
import nProcsExecutor   as npe
import nProcsPool       as npp

VER = '\n Version 1.10. 28-Dec-2024.'
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

if __name__ == '__main__':

    status = ' SUCCESS\n'
    numCores = mp.cpu_count() # Just FYI.
    print(VER)
    print(' Num Cores Available = {}'.format(numCores))


    # Change value of flatIterable as desired.
    flatIterable = [ [    1,  5000], [ 5001, 10000], [10001, 15000],
                     [15001, 20000], [20001, 25000], [25001, 30000],
                     [30001, 35000], [35001, 40000], [40001, 45000],
                     [45001, 50000]
                   ]
    # Change value of numProcs as desired.
    numProc = 7
    #numProc = numCores
    print(' Num Cores Requested = {}\n'.format(numProc))
    
    if 0 < numProc <= numCores:
        q = queue.Queue() # Simple queue can be used here.
        exeTime = op.oneProc( flatIterable, 1, q )
        printResults( ' oneProc', q, exeTime )
    
        q = mp.Queue()    # mp queue must be used here.
        exeTime = npb.nProcsBruteForce( flatIterable, numProc, q )
        printResults( ' nProcsBruteForce', q, exeTime )
    
        m = mp.Manager()
        q = m.Queue()     # mp.Manager queue must be used here.
        exeTime = npe.nProcsExecutor( flatIterable, numProc, q )
        printResults( ' nProcsExecutor', q, exeTime )
    
        m = mp.Manager()
        q = m.Queue()     # mp.Manager queue must be used here.
        exeTime = npp.nProcsPool( flatIterable, numProc, q )
        printResults( ' nProcsPool', q, exeTime )
    else:
        status = ' FAIL\n'
    print(status)
#############################################################################
