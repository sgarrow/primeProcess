import prime_1_Process            as p1p
import prime_N_Process_bruteForce as pNpbf
import prime_N_Process_executor   as pNpe
import prime_N_Process_pool       as pNpp

if __name__ == '__main__':

    print('\n Version 1.02. 22-Dec-2024.\n')

    start   = 1
    end     = 200000
    numProc = 20

    np,exeTime = p1p.prime_1_Process([start,end])
    #print(' prime_1_Process')
    #print(' Num primes  from {:,} to {:,} = {:,}'.format(start, end, np))
    #print(' Execution Time: {:5.1f} sec\n'.format(exeTime))
    #
    #np,exeTime = pNpbf.prime_N_Process_bruteForce([start,end],numProc)
    #print(' prime_N_Process_bruteForce')
    #print(' Num primes  from {:,} to {:,} = {:,}'.format(start, end, np))
    #print(' Execution Time: {:5.1f} sec\n'.format(exeTime))
    #
    #np,exeTime = pNpe.prime_N_Process_executor([start,end],numProc)
    #print(' prime_N_Process_executor')
    #print(' Num primes  from {:,} to {:,} = {:,}'.format(start, end, np))
    #print(' Execution Time: {:5.1f} sec\n'.format(exeTime))

    np,exeTime = pNpp.prime_N_Process_pool([start,end],numProc)
    print(' prime_N_Process_pool')
    print(' Num primes  from {:,} to {:,} = {:,}'.format(start, end, np))
    print(' Execution Time: {:5.1f} sec\n'.format(exeTime))
