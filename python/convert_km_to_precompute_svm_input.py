import os, sys, shutil
from os import listdir
from os.path import isfile, join

input=sys.argv[1]
input=input.rstrip('/')

output=input+'_precomputedsvmformat'
print 'input directory is '+input
print 'output directory is '+output

if(os.path.isdir(output)!=True):
    os.mkdir(output,0755)

for files in listdir(input):
    #print files[-7:]
    label_uni=[]
    label=[]
    if files[-7:]=='.kernel':
        print files
        label_file=files+'.labels'
        f=open(input+'/'+label_file,'r');
        lines=f.readlines()
        f.close()
        for line in lines:
            line=line.rstrip()
            label.append(line)
            if line not in label_uni:
                label_uni.append(line)
        print label_uni
        
        f=open(input+'/'+files,'r')
        lines=f.readlines()
        f.close()
        
        f=open(output+'/'+files+'.precomputedsvmformat','w')
        index=0
        for line in lines:
            #print index
            write_line=str(label_uni.index(label[index]))+' 0:'+str(index+1)
            line=line.rstrip()
            line=line.split()
            for i in range(len(line)):
                write_line+=' '
                write_line+=str(i+1)+':'+line[i]
            index+=1
            f.write(write_line)
            f.write('\n')
        f.close()
        
