import os, sys, shutil
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

#
#   python plot_system_call.py system_calls_statistics_benign_sorted 20
#

input=sys.argv[1]
topk=int(sys.argv[2])

f=open(input,'r')

sys_calls=[]
sys_calls_count=[]

for line in f.readlines():
    line=line.rstrip().split()
    sys_calls.append(line[0])
    sys_calls_count.append(float(line[1]))
    
f.close()

sys_calls_statistics=zip(sys_calls,sys_calls_count)
sorted_list=sorted(sys_calls_statistics,key=lambda x: x[1],reverse=True)
print sorted_list

topk_calls=sorted_list[0:topk]

topk_sys_calls=[ item[0] for item in topk_calls]
topk_sys_calls_count= [ float(item[1]) for item in topk_calls]

topk_sys_calls.reverse()
topk_sys_calls_count.reverse()


print topk_sys_calls
print topk_sys_calls_count

fig=plt.figure(1)

y_pos=np.arange(len(topk_sys_calls))
plt.ylim(-0.5,topk)
plt.barh(y_pos,topk_sys_calls_count,align='center')
plt.yticks(y_pos,topk_sys_calls)
plt.xlabel('Average Number of Calls per Application')
plt.title('Top '+sys.argv[2]+' system calls for '+sys.argv[1])
#plt.show()

fig.savefig(input+'_fig', bbox_inches='tight')



