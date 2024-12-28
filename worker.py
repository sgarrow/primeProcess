import time
import math
import pprint as pp
#############################################################################

def chunkify(inLst, numChunks):

    # chunkify([ 'a','b','c','d','e','f','g','h'] , 3) =
    # [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h']]

    chunkSize = int(math.ceil(len(inLst)/numChunks))
    chunks = [inLst[x:x+chunkSize] for x in range(0, len(inLst), chunkSize)]

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
                    np += 1
        answer = [procName, el, np]
        q.put( answer )   # Put the answer in the q
    return answer         # and return it directly.
#############################################################################
