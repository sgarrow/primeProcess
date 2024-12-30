import os
import queue
import pprint           as pp
import multiprocessing  as mp
import oneProc          as op
import nProcsBruteForce as npb
import nProcsExecutor   as npe
import nProcsPool       as npp

import worker           as wrk
import county_summary   as pWrk

VER = '\n Version 1.16. 29-Dec-2024.'
#############################################################################

def printResults( fName, inQ, inExeTime ):
    while not inQ.empty():
        qEl = inQ.get()
        print(' {}\n'.format(pp.pformat(qEl)))
    print( ' {} execution time = {:5.1f} sec.\n'.format(fName,inExeTime))
    print('********************************')
#############################################################################

def doWrk( inNumProc, inFlatIterable, inWrkFunc ):
    status = ' SUCCESS\n'
    if 0 < numProc <= numCores:
        q = queue.Queue() # Simple queue can be used here.
        exeTime = op.oneProc( inFlatIterable, 1, q, inWrkFunc )
        printResults( 'oneProc', q, exeTime )
    
        q = mp.Queue()    # mp queue must be used here.
        exeTime = npb.nProcsBruteForce(inFlatIterable,inNumProc,q,inWrkFunc)
        printResults( 'nProcsBruteForce', q, exeTime )
    
        m = mp.Manager()
        q = m.Queue()     # mp.Manager queue must be used here.
        exeTime = npe.nProcsExecutor(inFlatIterable,inNumProc,q,inWrkFunc)
        printResults( 'nProcsExecutor', q, exeTime )
    
        m = mp.Manager()
        q = m.Queue()     # mp.Manager queue must be used here.
        exeTime = npp.nProcsPool(inFlatIterable,inNumProc,q,inWrkFunc)
        printResults( 'nProcsPool', q, exeTime )
    else:
        status = ' FAIL\n'
    return status
#############################################################################

if __name__ == '__main__':

    status = ' SUCCESS\n'
    numCores = mp.cpu_count() # Just FYI.
    numProc  = 5 # Change value of numProcs as desired up to numCores.

    print(VER)
    print(' Num Cores Available = {}'.format(numCores))
    print(' Num Cores Requested = {}\n'.format(numProc))

    ################ Find number of primes between limits (inclucivce)
    #flatIterable = [ [    1,  5000], [ 5001, 10000], [10001, 15000],
    #                 [15001, 20000], [20001, 25000], [25001, 30000],
    #                 [30001, 35000], [35001, 40000], [40001, 45000],
    #                 [45001, 50000]
    #               ]
    #wrkFunc = wrk.primeWorker
    #status = doWrk( numProc, flatIterable, wrkFunc )
    #print(status)
    #
    ################ Simulate processing a list of text files.
    #flatIterable = [ 'f0.txt',  'f1.txt',  'f2.txt', 'f3.txt',
    #                 'f4.txt',  'f5.txt',  'f6.txt', 'f7.txt',
    #                 'f8.txt',  'f9.txt',  'f10.txt','f11.txt'
    #               ]
    #wrkFunc = wrk.fileWorker
    #status = doWrk( numProc, flatIterable, wrkFunc )
    #print(status)
    #
    ############### Process a list of panda files.
    dirPath = './csvFiles'
    flatIterable = [
        '{}/{}'.format(dirPath,f) for f in os.listdir(dirPath) if \
        os.path.isfile(os.path.join(dirPath, f)) and f.endswith('csv') ]

    #pp.pprint(flatIterable)

    wrkFunc = pWrk.pandaWorker
    status = doWrk( numProc, flatIterable, wrkFunc )
    print(status)

#############################################################################
