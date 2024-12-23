import time

def numPrimesBetween(n,q,ss): # inclusive of endpoints.
    s = ss[0]
    e = ss[1]
    np = 0
    for num in range(s, e+1):
        if num > 1:
            isPrime = True
            for i in range(2, num):
                if (num % i) == 0:
                    isPrime = False
                    break
            if isPrime:
                #print(' {:3}: {:4} is     prime'.format(n,num))
                ## Convert the number to a string
                #n_str = str(num)
                #if n_str == n_str[::-1]:
                #    print(' {:3}: {:4} is     prime'.format(n,num))
                np += 1
            else:
                pass
                #print(' {:3}: {:4} is not prime'.format(n,num))
        else:
            pass
            #print(' {:3}: {:4} is not prime'.format(n,num))
    q.put(np)
    time.sleep(.1)
    #print(' {}: Num primes numbers from {:4} to {:4} = {:4}'.format(n,s, e, np))
    return np
#############################################################################
