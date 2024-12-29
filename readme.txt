To run this project: python main.py
It (the worker function) finds the number of prime numbers < 50,001.

Most Python scripts run on a single core, but PCs have multiple cores. It's 
possible to write Python scripts that divide up the work and have each of
those divisions run simultaneously on separate cores.  This project 
demonstrates three different ways of doing just that.  Assume you have a list
(an iterable) of say 10 files and you want to process each one of them with a
function called "worker".  

Normally it would be done like this: for ii in length(fList): 
                                          worker(fList[ii])    

CONCEPTUALLY: By using multiple, say, 2 cores can be done like this:

On core1:                         simultaneously on core2:
--------------------------------  ------------------------------------------
for ii in range(0,len(fList)/2):  for ii in range(len(fList)/2, len(fList)):
    worker(fList[ii])                 worker(fList[ii])

IN PRACTICE: You take your (flat) iterable and divide it into a number of
"chunks".  The number of chunks you divide it up into is the number of cores
you want to run on.  The more cores the faster everything gets done.  My i7
has 28 cores!!

Here's an example of chunking a (flat) iterable into three chunks.

chunkify([ a, b, c, d, e, f, g, h ], 3) =
[ [a, b, c], [d, e, f], [g, h] ]

When you run this program the iterable will be handled the "normal" way and
all multi-core ways that I've called: brute-force, executor and pool.  Each
way has pros and cons.  Each of the 4 ways give the same answer. Whew.

Each of the multi-core ways have (basically) the same execution time so
that's not one of their distinguishing characteristics.

If your iterable has 10 things and you run on 10 cores, then each core will
process 10/10=1 thing.  If you run on 5 cores, then each core will process
10/5=2 things.  If you run on 20 cores, it won't crash but, in fact only 10
cores will be used (as you run out of data after 10 cores - each processing
1 item in the iterable).

I've tried to write everything such that you should only have to change 2
things to port to your use-case: (1) the function "worker" in file
worker.py and variable "flatIterable" in file main.py.

A summary/comparison of the three multi-core methods follows.

                                      bruteForce  executor  pool
            Number of lines of code:  18          16        11
        Can return results directly:  NO          YES       YES
Can give each process a unique name:  YES         YES       NO

During development I recommend getting your use case running via all 3
methods and verify that each gives the same answer.  Then, if I had to
which one to go to production with, go with executor.

Note, in particular, the worker function's result (returned value, if any)
cannot be returned with the bruteForce method.  So, what worker functions
do is place anything it wants to return in a "queue".  The q is passed 
from the top process (main) all the way down to the worker and then back up.

Be aware that if 10 processes are running then they will/may be writing to the q
simultaneously! That's okay, the q's are thread/process safe.  It's amazing.

Note also that the pool method cannot assign a unique name to each of the 
(identical) instances of the process (worker).  Each line of the printed
result begins with the name of the process that provided that particular
result.  So, the pool process names are all identical even though they are
really (probably) different processes.
