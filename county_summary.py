import pandas 
#import numpy                     # shg. commented out, not needed.
import sys 
#from sklearn import linear_model # shg. commented out, not needed. 
import random                     # shg. added this, can eventually remove.
import time                       # shg. added this, can eventually remove. 

#########################################
# output to log file
#########################################
# shg. moved to bottom.
#sys.stdout = open('county_analysis.txt','w')

############################################# shg. added for readability.

#calculate crude birth rate, return new dataframe
#First argument is the input dataframe
def crude_br_calc(df):
    #crude birth rate = (number of births in a year / tot population ) * 1000
    df["CRUDE_BIRTHRATE_2023"] = ( df["BIRTHS2023"]
                                                   .div(df["POPESTIMATE2023"])
                                                   .mul(1000)
                                                   )
    return df
############################################# shg. added for readability.

def pandaWorker( procName, q, iterableLst ):

    #################### shg. orig code start.
    #========================================
    # Adjust options 
    #========================================
    pandas.set_option('display.max_rows'    , None)
    pandas.set_option('display.max_colwidth', None)
    pandas.set_option('display.max_columns' , None) 
    pandas.set_option('display.width', None)

    # shg. compressed, easier scrolling.
    cols =[ "SUMLEV",               "REGION",               "DIVISION",             "STATE",
            "COUNTY",               "STNAME",               "CTYNAME",              "ESTIMATESBASE2020",
            "POPESTIMATE2020" ,     "POPESTIMATE2021" ,     "POPESTIMATE2022" ,     "POPESTIMATE2023" ,
            "NPOPCHG2020",          "NPOPCHG2021",          "NPOPCHG2022",          "NPOPCHG2023",
            "BIRTHS2020",           "BIRTHS2021",           "BIRTHS2022",           "BIRTHS2023",
            "DEATHS2020",           "DEATHS2021",           "DEATHS2022",           "DEATHS2023",
            "NATURALCHG2020",       "NATURALCHG2021",       "NATURALCHG2022",       "NATURALCHG2023",
            "INTERNATIONALMIG2020", "INTERNATIONALMIG2021", "INTERNATIONALMIG2022", "INTERNATIONALMIG2023",
            "DOMESTICMIG2020",      "DOMESTICMIG2021",      "DOMESTICMIG2022",      "DOMESTICMIG2023",
            "NETMIG2020",           "NETMIG2021",           "NETMIG2022",           "NETMIG2023"]
    #################### shg. orig code end.

    for el in iterableLst:
        #################### shg. orig code start.
        # shg. compressed, easier scrolling, input file (el) now a parameter.
        inp = pandas.read_csv( el, usecols= cols , 
            dtype={ "SUMLEV":"string",               "REGION":"string",              "DIVISION":"string",             "STATE":"string",
                    "COUNTY":"string",               "STNAME":"string",              "CTYNAME":"string",              "ESTIMATESBASE2020":"Int64",
                    "POPESTIMATE2020":"Int64",       "POPESTIMATE2021":"Int64",      "POPESTIMATE2022":"Int64",       "POPESTIMATE2023":"Int64",
                    "NPOPCHG2020":"Int64",           "NPOPCHG2021":"Int64",          "NPOPCHG2022":"Int64",           "NPOPCHG2023":"Int64",
                    "BIRTHS2020":"Int64",            "BIRTHS2021":"Int64",           "BIRTHS2022":"Int64",            "BIRTHS2023":"Int64",
                    "DEATHS2020":"Int64",            "DEATHS2021":"Int64",           "DEATHS2022":"Int64",            "DEATHS2023":"Int64",
                    "NATURALCHG2020":"Int64",        "NATURALCHG2021":"Int64",       "NATURALCHG2022":"Int64",        "NATURALCHG2023":"Int64",
                    "INTERNATIONALMIG2020":"Int64",  "INTERNATIONALMIG2021":"Int64", "INTERNATIONALMIG2022":"Int64",  "INTERNATIONALMIG2023":"Int64",
                    "DOMESTICMIG2020":"Int64",       "DOMESTICMIG2021":"Int64",      "DOMESTICMIG2022":"Int64",       "DOMESTICMIG2023":"Int64",
                    "NETMIG2020":"Int64",            "NETMIG2021":"Int64",           "NETMIG2022":"Int64",            "NETMIG2023":"Int64"} , 

            #fix the encoding error. Those idiots in pop division actually put a tildy (~)
            #in the public use file. 
            encoding_errors ='backslashreplace')

        inp  = crude_br_calc(inp)

        outTxtFile = el.rsplit('.', 1)[0] + '_county_analysis' + '.txt'  # shg. construct unique out file name.
        origSysOut = sys.stdout            # shg. save orig sys.stdout.
        sys.stdout = open(outTxtFile,'w')  # shg. set sys.stdout to constructed out file name.
        print(inp[["STNAME","CTYNAME", "BIRTHS2023", "POPESTIMATE2023", "CRUDE_BIRTHRATE_2023"]])
        sys.stdout = origSysOut            # shg. restore sys.stdout.
        #################### orig code end

        # shg. since the script runs so fast already I added a sleep to make
        # the improvment more noticable.  Eventually this needs to be removed.
        sleepTime = round(random.uniform(0.1, 1.0),1)
        time.sleep(sleepTime)

        answer = {'ProcName':procName, 'item':el, 'result':outTxtFile}
        q.put( answer )   # Put the answer in the q
    return answer         # and return it directly.
