import random
import time
import math
import sys
import os
import pprint             as pp
import multiprocessing    as mp
import concurrent.futures as cf
import pandas
###########################

# Calculate crude birth rate, return new dataframe.
# Argument is the input pandas dataframe.
def crude_br_calc(df):
    # Crude birth rate = (number of births in a year / tot population ) * 1000
    df['CRUDE_BIRTHRATE_2023'] = ( df['BIRTHS2023']
                                                   .div(df['POPESTIMATE2023'])
                                                   .mul(1000)
                                                   )
    return df
###########################

def pandaWorker( procName, chunkedLstSection ): # One instance per core.

    # Adjust options.
    optsSetToNone = ['max_rows','max_colwidth','max_columns','width']
    [pandas.set_option('display.{}'.format(el),None) for el in optsSetToNone]

    # Create arguments to .read_cvs.
    userDtype = { 'SUMLEV': 'string', 'REGION':'string', 'DIVISION':'string',
                  'STATE':  'string', 'COUNTY':'string', 'STNAME':  'string',
                  'CTYNAME':'string', 
                  'ESTIMATESBASE2020':'Int64' }

    years   = list(range(2020,2023+1))  # <- Change to process different years.

    bases   = [ 'POPESTIMATE', 'NPOPCHG', 'BIRTHS', 'DEATHS', 'NATURALCHG',
                'INTERNATIONALMIG', 'DOMESTICMIG',  'NETMIG' ]

    concat  = [ b+str(y)  for b in bases for y in years ]
    tmpDict = { c:'Int64' for c in concat }
    userDtype.update(tmpDict) # Manually verified == orig hard-coded dtype.
    cols    = list(userDtype.keys())

    # Process each file in the list.
    answer = {}
    for el in chunkedLstSection:
        inp        = pandas.read_csv( el,                  # csv file.
                                      usecols = cols,      # Generated above.
                                      dtype   = userDtype, # Generated above.
                                      encoding_errors = 
                                       'backslashreplace') # RE: ~idiots.

        inp        = crude_br_calc(inp)
        outTxtFile = el.rsplit('.', 1)[0] + '_county_analysis.txt' # Construct unique out fname.
        origSysOut = sys.stdout           # Save orig sys.stdout.
        sys.stdout = open(outTxtFile,'w') # Set sys.stdout to out f name.

        print(inp[['STNAME','CTYNAME', 'BIRTHS2023', 
                   'POPESTIMATE2023',  'CRUDE_BIRTHRATE_2023']])

        sys.stdout = origSysOut           # Restore sys.stdout to orig.

        # Since worker runs fast already, add a sleep to make the
        # improvment noticable.  Remove when a cpu intensive func run.
        sleepTime = round(random.uniform(0.1, 1.0),1)
        time.sleep(sleepTime)

        inFileBaseName  = os.path.basename(el)
        outFileBaseName = os.path.basename(outTxtFile)
        answer.update({inFileBaseName:{'ProcName':procName, '  result':outFileBaseName}})
    return answer
#############################################################################

def chunkify( inLst, numChunks ):
    # chunkify([ 'a','b','c','d','e','f','g','h' ], 3) =
    # [ ['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h'] ]

    # chunkify([ 'a','b','c','d','e','f','g','h' ], 1] =
    # [ [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' ] ]

    chunkSize = int(math.ceil(len(inLst)/numChunks))

    chunks = [ inLst[x:x+chunkSize] for x in \
               range(0, len(inLst), chunkSize)
             ]
    return chunks
#############################################################################

if __name__ == '__main__':

    # Set numProc and print user intro text.
    VER = '\n Version 0.4. 30-Dec-2024.'
    numCores = mp.cpu_count() # Just FYI.
    numProc  = 5     # <-- Change as desired.
    print(VER)
    print(' Num Cores Available = {}.'.format(numCores))
    print(' Num Cores Requested = {:2}.\n'.format(numProc))
    #############################################################

    if 0 < numProc <= numCores: # Num procs should be <= numCores.

        # Get/Make a flat list of files and chunkify it.
        dirPath = './csvFiles' # Relative to dir this file is in.
        flatIterable = [
            '{}/{}'.format(dirPath,f) for f in os.listdir(dirPath) if \
            os.path.isfile(os.path.join(dirPath, f)) and f.endswith('csv') ]

        chunkedIter = chunkify( flatIterable, numProc )
        #############################################################

        # Concurrently run numProc instances of function pandaWorker.
        # Each instance will run on a different core and work on a
        # different chunk of the chunkedIterable.  Print results.
        kStart = time.time()
        with cf.ProcessPoolExecutor() as executor:
            results =  [                        # Results from all
              executor.submit(                  #   submits auto-collected.  Cool.
                pandaWorker,                    # Worker Func for spawns.
                'e{}'.format(ii),               #   arg: All spawns get a unique Proc Name.
                chunkedIter[ii] )               #   arg: A chunk of flatIterable.
              for ii in range(len(chunkedIter)) # Num instances of Worker Func to create,
            ]                                   #   could be < numProc if numProc>len(flatIter)
                                                #   ref para [LATENT BUG FIXED] in info.txt.

            for f in cf.as_completed(results):  # Print all collected results.
                pp.pprint(f.result())           # Each result is a dictionary.
                print()
            print(' Execution Time = {:5.1f}\n'.format(time.time() - kStart))
    else:
        print(' ERROR')
        print()
#############################################################################
