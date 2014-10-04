import os, sys, shutil
from os import listdir
from os.path import isfile, join

direc=sys.argv[1].rstrip('/')

f=open('graphcluster.input','w')
count=0
for files in listdir(direc):
    if count == 20:
        break;
    count+=1
    f_input=open(direc+'/'+files,'r')
    lines=f_input.readlines()
    f_input.close()
    n_node=0
    n_edge=0
    for line in lines:
        line=line.split()
        if line[0]=='v':
            n_node+=1
        if line[0]=='e':
            n_edge+=1
    print n_node,n_edge,files
    f.write('#'+files+'\n')
    f.write(str(n_node)+'\n')
    for line in lines:
        line=line.split()
        if line[0]=='v':
            f.write(line[2]+'\n')
        if line[0]=='e':
            break
    f.write(str(n_edge)+'\n')
    for line in lines:
        line=line.split()
        if line[0]=='v':
            continue
        if line[0]=='e':
            f.write(line[1]+' '+line[2]+'\n')
    f.write('\n\n')

f.close()    
