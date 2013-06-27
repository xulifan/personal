import os, sys, shutil
from os import listdir
from os.path import isfile, join

input=sys.argv[1]
if input[-1:]!='/':
    input += '/'
for dirs in listdir(input):
    #if dirs[-6:]==".graph":
    if dirs[-4:]==".txt":
        
        f=open(input + dirs,'r')
        line=f.readline()
        line=line.split()
        n_nodes=int(line[0])
        n_feats=int(line[1])
        temp=0        
        while temp<n_nodes:
            temp+=1
            f.readline()
        adjsum=0
        temp=0;
        while temp<n_nodes:
            temp+=1
            line=f.readline()
            line=line.split()
            line=[int(i) for i in line]
            adjsum+=sum(line)
        if(adjsum == 0):
            os.remove(input+dirs)
            print dirs, n_nodes, n_feats,adjsum
            
