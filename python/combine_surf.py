import os, sys, shutil, random
from os import listdir
from os.path import isfile, join

input=sys.argv[1]
if input[-1:]!='/':
    input += '/'
output=input.rstrip('/')
output=output[output.rfind('/')+1:]
output+='_surfall'
fw=open(output,'w')
print output
n_node_all=0
n_feat_all=0
for dirs in listdir(input):
    if dirs[-5:]==".surf":
    #if dirs[-4:]==".txt":
        
        f=open(input + dirs,'r')
        
        n_feat=int(f.readline())
        n_node=int(f.readline())
        n_node_all+=n_node
        n_feat_all=n_feat
        f.close()
        print dirs,n_feat,n_node
        
fw.write(str(n_node_all))
fw.write(' ')
fw.write(str(n_feat_all))
fw.write('\n')

for dirs in listdir(input):
    if dirs[-5:]==".surf":
    #if dirs[-4:]==".txt":
        
        f=open(input + dirs,'r')
        
        n_feat=int(f.readline())
        n_node=int(f.readline())
        i=0
        while i<n_node:
            i+=1
            line=f.readline()
            line=line.split()
            line=line[6:]
            line_str=" ".join(line)
            #print line_str
            fw.write(line_str)
            fw.write('\n')
        f.close()
fw.close()


    
    

            
