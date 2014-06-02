import os, sys, shutil
import csv
from os import listdir
from os.path import isfile, join

#
#   python assign_family_for_csv.py virustotal-search-20131105-104345.csv unique_malware_families > malware_sha256_name_family
#

family_f=open(sys.argv[2],'r')
family_uni=[]
for line in family_f.readlines():
    line=line.rstrip()
    family_uni.append(line)
    #print line
family_uni.append('unknown')

family_count=[0 for i in range(len(family_uni))]

filter_content=[]


with open(sys.argv[1],'rb') as csvfile:
    csv_content=csv.reader(csvfile)
    for line in csv_content:
        #print line
        if 'Search' in line[0]:
            continue
        sha256=line[0]
        name = line[1][line[1].rfind('\\')+1:]
        if name[-4:] == '.apk' or name[-4:] == '.APK':
            name=name[0:-4]
        item=line[5]
        family=''
        if '#' not in item:
            family = 'unknown'
            filter_content.append(name+' '+family)
            family_count[-1]+=1
            print sha256,name,family
            continue
            
        item=item.split('#')
        item=item[1]
        item=item.lower()
        for family_temp in family_uni:
            if family_temp in item:
                if len(family) != 0:
                    #
                    #   TODO
                    #
                    family=family
                    #print line[6],item,family,family_temp
                else:
                    family=family_temp
                break;
        if family not in family_uni:
            family = 'unknown'
            family_count[-1]+=1
            #print line[6],item,name
        else:
            family_count[family_uni.index(family)]+=1
        filter_content.append(name+' '+family)
        print sha256,name,family
       
#filter_content.pop(0)
#print filter_content
#for item in filter_content:
#    print item

family_statistics=zip(family_uni,family_count)

sorted_list=sorted(family_statistics,key=lambda x: x[1],reverse=True)

#for item in sorted_list:
#    print item[0],item[1]
