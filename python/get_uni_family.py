import os, sys, shutil
import csv
from os import listdir
from os.path import isfile, join

filter_content=[]
family_uni=[]
family_uni2=[]
family_uni3=[]
family_uni4=[]
with open(sys.argv[1],'rb') as csvfile:
    csv_content=csv.reader(csvfile)
    for line in csv_content:
        #print line
        name = line[1][line[1].rfind('\\')+1:]
        #
        #   TODO
        #
        family=line[6]
        if len(family)!=0:
            if family not in family_uni:
                family_uni.append(family)


family_uni.pop(0)
for item in family_uni:
    item = item.split('#')
    #print item[0],item[1]
    if len(item)<2:
        print 'ERROR ',item
    else:
        if item[0] == 'F-Secure':
            #if len(item[1].split('.'))<4:
            #    print item[0],item[1]
            if '/' in item[1]:
                item[1]=item[1][item[1].rfind('/')+1:]
                if '.' in item[1]:
                    item[1]=item[1][0:item[1].rfind('.')]
            if len(item[1].split('.')) == 4:
                item[1]=item[1].split('.')[2]
            if len(item[1].split('.')) == 5:
                item[1]=item[1].split('.')[3]
                
            item[1]=item[1].lower()
            if item[1] not in family_uni2:
                family_uni2.append(item[1])
                #print item[0],item[1]
                
        elif item[0] == 'Microsoft':
            #if len(item[1].split('.'))<4:
            #    print item[0],item[1]
            
            
            if '/' in item[1]:
                item[1]=item[1].split('/')[1]
                if '.' in item[1]:
                    item[1]=item[1][0:item[1].rfind('.')]
            
            item[1]=item[1].lower()
            if item[1] not in family_uni2:
                family_uni2.append(item[1])
                #print item[0],item[1]
                
        elif item[0] == 'Symantec':
            #if len(item[1].split('.'))<4:
            #    print item[0],item[1]
            
            if '.' in item[1]:
                item[1]=item[1].split('.')[1]
            
            
            item[1]=item[1].lower()
            if item[1] not in family_uni2:
                family_uni2.append(item[1])
                #print item[0],item[1]
        
        else:
            print 'ERROR with wrong company ',item
        
    #print item

if 'android' in family_uni2:
    family_uni2.remove('android')
if 'android.a' in family_uni2:    
    family_uni2.remove('android.a')

family_uni2.sort(reverse=True)
for item in family_uni2:
    print item


'''
for item in family_uni2:
    if '/' in item:
        item=item.split('/')
        item=item[1]
        item=item.split('.')[0]
    if item not in family_uni3:
        family_uni3.append(item)
    #print item
    
for item in family_uni3:
    item=item.split('.')
    if len(item[-1])==1:
        item=item[-2]
    elif len(item) > 3 and len(item[-1]) == 2:
        item=item[-2]
    elif len(item)==1:
        item=item[0]
    
    else:
        if 'Android' in item:
            item.remove('Android')
        if 'Malware' in item:
            item.remove('Malware')
        if len(item) == 1:
            item=item[0]
        else:
            item=item[1]
        #item=item[2]
    item=item.lower()
    if item not in family_uni4:
        family_uni4.append(item)
    #print item

family_uni4.sort()    
for item in family_uni4:
    print item
'''
