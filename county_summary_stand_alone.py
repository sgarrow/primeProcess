import pandas 
import sys 
import random # shg. added this, can eventually remove.
import time   # shg. added this, can eventually remove. 

###########################

#calculate crude birth rate, return new dataframe
#First argument is the input dataframe
def crude_br_calc(df):
    #crude birth rate = (number of births in a year / tot population ) * 1000
    df["CRUDE_BIRTHRATE_2023"] = ( df["BIRTHS2023"]
                                                   .div(df["POPESTIMATE2023"])
                                                   .mul(1000)
                                                   )
    return df
###########################

def pandaWorker( procName, chunkedLstSection ):

    # Adjust options.
    pandas.set_option('display.max_rows'    , None)
    pandas.set_option('display.max_colwidth', None)
    pandas.set_option('display.max_columns' , None) 
    pandas.set_option('display.width', None)

    # Create arguments to .read_cvs.
    userDtype = { 
    "SUMLEV":"string",             "REGION":"string",             "DIVISION":"string",           "STATE":"string",
    "COUNTY":"string",             "STNAME":"string",             "CTYNAME":"string",            "ESTIMATESBASE2020":"Int64",
    "POPESTIMATE2020":"Int64",     "POPESTIMATE2021":"Int64",     "POPESTIMATE2022":"Int64",     "POPESTIMATE2023":"Int64",
    "NPOPCHG2020":"Int64",         "NPOPCHG2021":"Int64",         "NPOPCHG2022":"Int64",         "NPOPCHG2023":"Int64",
    "BIRTHS2020":"Int64",          "BIRTHS2021":"Int64",          "BIRTHS2022":"Int64",          "BIRTHS2023":"Int64",
    "DEATHS2020":"Int64",          "DEATHS2021":"Int64",          "DEATHS2022":"Int64",          "DEATHS2023":"Int64",
    "NATURALCHG2020":"Int64",      "NATURALCHG2021":"Int64",      "NATURALCHG2022":"Int64",      "NATURALCHG2023":"Int64",
    "INTERNATIONALMIG2020":"Int64","INTERNATIONALMIG2021":"Int64","INTERNATIONALMIG2022":"Int64","INTERNATIONALMIG2023":"Int64",
    "DOMESTICMIG2020":"Int64",     "DOMESTICMIG2021":"Int64",     "DOMESTICMIG2022":"Int64",     "DOMESTICMIG2023":"Int64",
    "NETMIG2020":"Int64",          "NETMIG2021":"Int64",          "NETMIG2022":"Int64",          "NETMIG2023":"Int64"}

    cols = list(userDtype.keys())

    # Process each file in the list.
    for el in chunkedLstSection:

        inp        = pandas.read_csv( el, usecols = cols, dtype = userDtype, encoding_errors = 'backslashreplace')
        inp        = crude_br_calc(inp)
        outTxtFile = el.rsplit('.', 1)[0] + '_county_analysis' + '.txt'  # Construct unique out file name.
        origSysOut = sys.stdout            # save orig sys.stdout.
        sys.stdout = open(outTxtFile,'w')  # set sys.stdout to constructed out file name.
        print(inp[["STNAME","CTYNAME", "BIRTHS2023", "POPESTIMATE2023", "CRUDE_BIRTHRATE_2023"]])
        sys.stdout = origSysOut            # restore sys.stdout to orig.

        # Since the script runs so fast already I added a sleep to make
        # the improvment more noticable.  Eventually this needs to be removed.
        sleepTime = round(random.uniform(0.1, 1.0),1)
        time.sleep(sleepTime)

        answer = {'ProcName':procName, 'item':el, 'result':outTxtFile}
    return answer         # and return it directly.
#############################################################################

import math

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

import os
import multiprocessing    as mp
import concurrent.futures as cf

if __name__ == '__main__':

    # Set numProc and print user intro text.
    VER = '\n Version 0.0. 30-Dec-2024.'
    numCores = mp.cpu_count() # Just FYI.
    numProc  = 5     # <-- Change as desired.
    print(VER)
    print(' Num Cores Available = {}'.format(numCores))
    print(' Num Cores Requested = {}\n'.format(numProc))
    #############################################################

    # Get/Make a flat list of files and chunkify it.
    dirPath = './csvFiles'
    flatIterable = [
        '{}/{}'.format(dirPath,f) for f in os.listdir(dirPath) if \
        os.path.isfile(os.path.join(dirPath, f)) and f.endswith('csv') ]

    chunkedIterable = chunkify( flatIterable, numProc )
    #############################################################

    # Concurrently run numProc instances of function pandaWorker.
    # Each instance will run on a different core and work on a
    # different chunk of the chunkedIterable.  Print results.
    with cf.ProcessPoolExecutor() as executor:
        results = [ executor.submit( pandaWorker,
                                     'e{}'.format(ii),     # Process Name.
                                     chunkedIterable[ii] ) # Iterable.
                    for ii in range(len(chunkedIterable))
                  ]

        for f in cf.as_completed(results):
            print(f.result())
    #############################################################

