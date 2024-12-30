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

def pandaWorker( procName, q, iterableLst ):

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
    for el in iterableLst:

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
        q.put( answer )   # Put the answer in the q
    return answer         # and return it directly.
