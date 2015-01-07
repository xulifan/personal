import os, sys, shutil
from math import sqrt
from os import listdir
from os.path import isfile, join
from operator import add

n_input=int(sys.argv[1])

input_name=[]
ratio=[]

for i in range(len(sys.argv)):
    print sys.argv[i]

for i in range(n_input):
    input_name.append(sys.argv[2+i])
    ratio.append(int(sys.argv[2+n_input+i]))
print input_name
print ratio

f=open(input_name[0],'r')
line=f.readlines()
n_node=len(line)
f.close
print n_node

results=[[0 for j in range(n_node)] for i in range(n_node)]
results_norm=[[0 for j in range(n_node)] for i in range(n_node)]
#print results
for i in range(n_input):
    f=open(input_name[i],'r')
    for j in range(n_node):
        line=f.readline()
        line=line.split()
        line=[float(k) for k in line]
        #print line
        line=[k*ratio[i] for k in line]
        #print line
        results[j]=map(add,results[j],line)
    f.close()
#print results

for i in range(n_node):
    for j in range(n_node):
        results_norm[i][j]=round(results[i][j]/sqrt(results[i][i]*results[j][j]),4) 
#print results_norm

output_name='./MKL/'
for i in range(n_input):
    output_name+=str(ratio[i])
    output_name+='-'
    print output_name
    name_temp=input_name[i]
    name_temp=name_temp[name_temp.rfind('/')+1:]
    print name_temp
    name_temp=name_temp[0:name_temp.find('.kernel')]
    print name_temp
    output_name+=name_temp
    if i != n_input-1:
        output_name+='__'
output_name+='.kernel'
print output_name

if '.original' in input_name[0]:
    shutil.copy2(input_name[0][0:input_name[0].rfind('.original')]+'.fnames',output_name+'.fnames')
    shutil.copy2(input_name[0][0:input_name[0].rfind('.original')]+'.labels',output_name+'.labels')
else:
    shutil.copy2(input_name[0]+'.fnames',output_name+'.fnames')
    shutil.copy2(input_name[0]+'.labels',output_name+'.labels')


f=open(output_name,'w')
for i in range(n_node):
    line=results_norm[i]
    line=[str(j) for j in line]
    line=" ".join(line)
    f.write(line)
    f.write('\n')
f.close()

f=open(output_name+'.original','w')
for i in range(n_node):
    line=results[i]
    line=[str(j) for j in line]
    line=" ".join(line)
    f.write(line)
    f.write('\n')
f.close()
    
'''
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
            
'''
            
