import os, sys, shutil
from os import listdir
from os.path import isfile, join

#
#   python ./python_scripts/select_same_filename.py 3 ./representation/instruction/2013_2014_benign.filename ./representation/permission/684f/2013_2014_benign.filename ./representation/graph/23f/10s_all_test_precomputedsvmformat/SPGK-INTERSECT.kernel.fnames > selected_2013_2014_benign.filename
#

def select_check(item,target_list):
    check=0
    for i in range (len(target_list)):
        if item in target_list[i]:
            check=1
            break
    return check
    
n_input=int(sys.argv[1])
input_filename=[]
for i in range(n_input):
    input_filename.append(sys.argv[2+i])
filenames=[]

for i in range(n_input):
    filenames_temp=[]
    f=open(input_filename[i],'r')
    lines=f.readlines()
    f.close()
    for line in lines:
        line=line.strip()
        filenames_temp.append(line)
    filenames.append(filenames_temp)

#print filenames

for i in range(len(filenames[0])):
    item=filenames[0][i]
    select=0
    for j in range (n_input-1):
        if select_check(item,filenames[j+1])==1:
            select=0
            continue
        else:
            select=1
            break
    if select==0:
        print item
