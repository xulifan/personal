import os, sys, shutil
from os import listdir
from os.path import isfile, join
from operator import add

#
# python normalize.py ./lifan/interaction/1260m_1260b/
#
input=sys.argv[1]
input=input.rstrip('/')
output=open(input[input.rfind('/')+1:]+'_normalize.txt','w')
if input[-1:]!='/':
    input += '/'

for dirs in listdir(input):
    if dirs[-4:]==".txt":
        
        f=open(input + dirs,'r')
        label=dirs.split('_')[0]
        line=f.readline()
        line=line.split()
        n_nodes=int(line[0])
        output.write(label+' '+str(n_nodes)+' ')
        n_feats=int(line[1])
        feat=[0.0 for i in range (n_feats)]
        temp=0       
        featsum=0 
        while temp<n_nodes:
            temp+=1
            line=f.readline()
            line=line.split()
            line=[float(i) for i in line]
            feat=map(add,feat,line)
            #print line
            #if featsum != 0:
            #    line=[round(i/featsum,4) for i in line]
            #print line
        featsum=sum(feat)
        if featsum != 0:
            feat=[round(i/featsum,5) for i in feat]
        feat=[str(i) for i in feat]
        line=" ".join(feat)
        output.write(line)
        output.write("\n")
            
            
