import os, sys, shutil
from os import listdir
from os.path import isfile, join

input=sys.argv[1]
if input[-1:]!='/':
    input += '/'
output=input.rstrip('/')
output+='_normalized_sepcial/'
os.mkdir(output,0755);

for dirs in listdir(input):
    if dirs[-6:]==".graph":
    #if dirs[-4:]==".txt":
        
        f=open(input + dirs,'r')
        fw=open(output + dirs,'w')
        line=f.readline()
        fw.write(line)
        line=line.split()
        n_nodes=int(line[0])
        n_feats=int(line[1])
        temp=0       
        featsum=0 
        while temp<n_nodes:
            temp+=1
            line=f.readline()
            line=line.split()
            line=[float(i) for i in line]
            n1 = line[-1]
            n2 = line[-2]
            line.pop()
            line.pop()
            featsum=sum(line)
            #print line
            if featsum != 0:
                line=[round(i/featsum,4) for i in line]
            line.append(n1)
            line.append(n2)
            line=[str(i) for i in line]
            #print line
            line=" ".join(line)
            fw.write(line)
            fw.write("\n")
        adjsum=0
        temp=0;
        while temp<n_nodes:
            temp+=1
            line=f.readline()
            fw.write(line)
            
            
