import os, sys, shutil
import csv
from os import listdir
from os.path import isfile, join

#
#   python assign_family_for_graph.py ../6117b_6930m/SPGK-INTERSECT.kernel.fnames malware_sha256_name_family
#

graph_fnames=sys.argv[1]
family_file=sys.argv[2]

fp=open(family_file,'r')

sha256=[]
files=[]
family=[]
for line in fp.readlines():
    line=line.split()
    if len(line) != 3:
        print line
        continue
    sha256.append(line[0])
    files.append(line[1])
    family.append(line[2])
fp.close()

family_uni=[]
for item in family:
    if item not in family_uni:
        family_uni.append(item)
family_uni.append('benign')
if 'unknown' not in family_uni:
    family_uni.append('unknown')
family_count=[0 for i in range(len(family_uni))]

fp=open(graph_fnames,'r')
family_output=graph_fnames[:graph_fnames.rfind('/')]
family_output=family_output[family_output.rfind('/')+1:]
sha256_output=family_output+'.sha256'
family_statistics_name=family_output+'.statistics'
family_output+='.family'
f_family_output=open(family_output,'w')
f_sha256_output=open(sha256_output,'w')
for line in fp.readlines():
    line=line.rstrip()
    item=line.split('/')[-1]
    #print item
    graph_family=''
    if item[-4:]=='.txt':
        
        if item[:5]=='good_':
            #print item
            graph_family='benign'
            family_count[family_uni.index('benign')]+=1
        elif item[0:4]=='bad_':
            graph=item[4:]
            graph=graph[0:-4]
            if graph[-4:]=='.apk' or graph[-4:]=='.APK':
                graph=graph[0:-4]
            
            file_index=-1
            for i in range(len(files)):
                if graph.lower() in files[i].lower():
                    file_index=i
                    break
            if file_index != -1:        
                graph_family=family[file_index]
                sha256_temp=sha256[file_index]
                f_sha256_output.write(sha256_temp+' '+line+'\n')
                family_count[family_uni.index(graph_family)]+=1
            else:
                graph_family='unknown'
                print item,graph
                #print files
                f_sha256_output.write('unknown'+' '+line+'\n')
                family_count[family_uni.index('unknown')]+=1
        f_family_output.write(graph_family)
        f_family_output.write('\n')
        
f_family_output.close()
f_sha256_output.close()
fp.close()

family_statistics=zip(family_uni,family_count)
sorted_list=sorted(family_statistics,key=lambda x: x[1],reverse=True)
fp=open(family_statistics_name,'w')
for item in sorted_list:
    fp.write(str(item[0])+' '+str(item[1]))
    fp.write('\n')
fp.close()

