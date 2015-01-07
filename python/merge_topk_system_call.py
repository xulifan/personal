import os, sys, shutil
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

#
#   ./python_scripts/merge_topk_system_call.py 3 20 ./representation/information/sys_count_2013_10s ./representation/information/sys_count_2014_10s ./representation/information/sys_count_benign_10s
#

n_input=int(sys.argv[1])

topk=int(sys.argv[2])

sys_call_files=[]
for i in range(n_input):
    sys_call_files.append(sys.argv[3+i])

sys_call_all=[]    
for item in sys_call_files:    
    f=open(item,'r')

    sys_calls=[]
    sys_calls_count=[]

    for line in f.readlines():
        line=line.rstrip().split()
        sys_calls.append(line[0])
        sys_calls_count.append(float(line[1]))
        
    f.close()

    sys_calls_statistics=zip(sys_calls,sys_calls_count)
    sorted_list=sorted(sys_calls_statistics,key=lambda x: x[1],reverse=True)
    #print sorted_list

    topk_calls=sorted_list[0:topk]

    topk_sys_calls=[ item[0] for item in topk_calls]
    topk_sys_calls_count= [ float(item[1]) for item in topk_calls]

    topk_sys_calls.reverse()
    topk_sys_calls_count.reverse()

    for syscall in topk_sys_calls:
        if syscall not in sys_call_all:
            sys_call_all.append(syscall)

    #print topk_sys_calls
    #print topk_sys_calls_count

print sys_call_all
print len(sys_call_all)



