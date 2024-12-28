import time
import math
import pprint as pp
#############################################################################

def chunkify(inLst, numChunks):

    chunkSize = int(math.ceil(len(inLst)/numChunks))
    chunks = [inLst[x:x+chunkSize] for x in range(0, len(inLst), chunkSize)]

    #print()
    #print('numChunks',numChunks)
    #print('chunkSize',chunkSize)
    #print()
    #pp.pprint(inLst)
    #print()
    #for el in chunks:
    #    print(el)
    #print(chunks)
    #print()

    return chunks
#############################################################################

def worker(procName,q,iterableLst): # inclusive of endpoints.
    for el in iterableLst:
        s = el[0]
        e = el[1]
        np = 0
        for num in range(s, e+1):
            if num > 1:
                isPrime = True
                for i in range(2, num):
                    if (num % i) == 0:
                        isPrime = False
                        break
                if isPrime:
                    #print(' {:3}: {:4} is     prime'.format(procName,num))
                    np += 1
                else:
                    pass
                    #print(' {:3}: {:4} is not prime'.format(procName,num))
            else:
                pass
                #print(' {:3}: {:4} is not prime'.format(procName,num))
        answer = [iterableLst, np]
        q.put( answer )
        time.sleep(.1)
    return answer
#############################################################################
