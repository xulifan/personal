import fileinput,subprocess
import os, sys, shutil
import filecmp
import time
import signal
import datetime
from math import sqrt
from os import listdir
from os.path import isfile, join
from operator import add


#
#   python ./python_scripts/MKL_script.py ./representation/graph/23f/10s_all_test/SPGK-INTERSECT.kernel ./representation/permission/684f/graph/10s_all_test/FV-INTERSECT.kernel
#

input1=sys.argv[1]
input2=sys.argv[2]

ratio=[1,2,4,8]

used_ratio=[]

for i in ratio:
    for j in ratio:
        temp=float(j)/float(i)
        if temp in used_ratio:
            #print "Used ratio ",i,j
            continue
        else:
            used_ratio.append(temp)
            print i,j
            subprocess.call("python /home/lifan/Desktop/Data/Malware/python_scripts/combine_matrix.py 2 "+input1+" "+input2+" "+str(i)+" "+str(j),shell=True)
            
            
#print (len(used_ratio))
                            


