import os, sys, shutil
from os import listdir
from os.path import isfile, join
from operator import add

#
# python extract_and_normalize_all_graphs_into_svm_feature_vector.py ./6117b_6930m
#
input=sys.argv[1]
input=input.rstrip('/')
output=open(input[input.rfind('/')+1:]+'_normalize_svm.txt','w')
output_filename=open(input[input.rfind('/')+1:]+'_normalize_svm_filename.txt','w')
if input[-1:]!='/':
    input += '/'

for dirs in listdir(input):
    if dirs[-4:]==".txt":
        output_filename.write(dirs+'\n')
        f=open(input + dirs,'r')
        label=dirs.split('_')[0]
        if label=='bad':
            label='0'
        if label=='good':
            label='1'
        line=f.readline()
        line=line.split()
        n_nodes=int(line[0])
        output.write(label)
        #output.write(' 1:'+str(n_nodes))
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
        #feat=[str(i) for i in feat]
        for i in range(n_feats):
            output.write(' '+str(i+1)+':'+str(feat[i]))
            #output.write(' '+str(i+2)+':'+str(feat[i]))
            #output.write(' '+str(feat[i]))
        output.write("\n")
output.close()
output_filename.close()
            
            
