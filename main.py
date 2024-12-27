import oneProc           as op
import nProcs_bruteForce as npb
import nProcs_executor   as npe
import nProcs_pool       as npp
VER = '\n Version 1.06. 27-Dec-2024.\n'
#############################################################################

def printResults( fName, start, end, np, exeTime ):
    print( fName )
    print(' Num primes  from {:,} to {:,} = {:,}'.format(start, end, np))
    print(' Execution Time: {:5.1f} sec\n'.format(exeTime))
#############################################################################

if __name__ == '__main__':

    print(VER)

    start   = 1
    end     = 100000
    numProc = 10

    np,exeTime = op.oneProc(            [start,end]             )
    printResults( ' oneProc',           start, end, np, exeTime )
    
    np,exeTime = npb.nProcs_bruteForce( [start,end], numProc    )
    printResults( ' nProcs_bruteForce', start, end, np, exeTime )
    
    np,exeTime = npe.nProcs_executor(   [start,end], numProc    )
    printResults( ' nProcs_executor',   start, end, np, exeTime )

    np,exeTime = npp.nProcs_pool(       [start,end], numProc    )
    printResults( ' nProcs_pool',       start, end, np, exeTime )
#############################################################################
