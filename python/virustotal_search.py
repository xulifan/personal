import simplejson
import urllib
import urllib2
import time
import os, sys, shutil
import csv
import requests
from os import listdir
from os.path import isfile, join
from urlparse import urlparse, parse_qs

#
#python virustotal_search.py 6117b_6930m.sha256 > 6117b_6930m.virustotal
#
'''
scanners=['AVG', 'Ad-Aware', 'AegisLab', 'Agnitum', 'AhnLab-V3', 'AntiVir', 'Antiy-AVL', 'Avast', 'Baidu-International', 'BitDefender', 'Bkav', 'CAT-QuickHeal', 'CMC', 'ClamAV', 'Commtouch', 'Comodo', 'DrWeb', 'ESET-NOD32', 'Emsisoft', 'F-Prot', 'F-Secure', 'Fortinet', 'GData', 'Ikarus', 'Jiangmin', 'K7AntiVirus', 'K7GW', 'Kaspersky', 'Kingsoft', 'Malwarebytes', 'McAfee', 'McAfee-GW-Edition', 'MicroWorld-eScan', 'Microsoft', 'NANO-Antivirus', 'Norman', 'Panda', 'Qihoo-360', 'Rising', 'SUPERAntiSpyware', 'Sophos', 'Symantec', 'TheHacker', 'TotalDefense', 'TrendMicro', 'TrendMicro-HouseCall', 'VBA32', 'VIPRE', 'ViRobot', 'Zillya', 'nProtect']
'''

scanners=['Ikarus']

#scanners_all=[]

input_sha256_filename=sys.argv[1]
f=open(input_sha256_filename,'r')

sha256=[]
for line in f.readlines():
    line=line.rstrip()
    line=line.split()
    if line[0] != 'unknown':
        sha256.append(line[0])
f.close()

total_sha256=len(sha256)
print 'Total number of sha256 is ',total_sha256
true_result=[0 for i in range(len(scanners))]
false_result=[0 for i in range(len(scanners))]
no_result=[0 for i in range(len(scanners))]

url = "https://www.virustotal.com/vtapi/v2/file/report"
for index in range(total_sha256):
    item=sha256[index]
    #print index,item
    parameters = {"resource": item, "apikey": "ec11d453bf472a428170c53259317f2287ba7354eaa96382d2b3af2b9a4620a1", "allinfo":1}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json = response.read()
    #print json
    oResult = simplejson.loads(json)
    if 'first_seen' in oResult.keys():
        print item,oResult['first_seen']
    else:
        print item, 'unknown'
    
    
    
    
    #link=oResult['permalink']
    #print link
    #f_link=requests.get(link)
    #print f_link.text
    if oResult['response_code'] == 1:
        scans = []
        for scan in sorted(oResult['scans']):
            #scanners_all.append(scan)
            #print scan
            if ((oResult['scans'][scan]['detected'] == True) and (scan in scanners)):
                true_result[scanners.index(scan)] += 1
                #print scan,oResult['scans'][scan]['detected'],oResult['scans'][scan]['update']
            elif ((oResult['scans'][scan]['detected'] == False) and (scan in scanners)):
                false_result[scanners.index(scan)] += 1
    else:
        #print 'no result'
        no_result=[x+1 for x in no_result]
    
    time.sleep(0.25)

print total_sha256    
print scanners
print true_result
print false_result
print no_result

all_result=[true_result[i]+false_result[i]+no_result[i] for i in range(len(scanners)) ]
print all_result


accuracy=[ float(x)/total_sha256 for x in true_result]
accuracy_temp=[ float(x)/6930 for x in true_result]

print accuracy

#print scanners_all

scanners_statistics=zip(scanners,true_result)
accuracy_statistics=zip(scanners,accuracy)
accuracy_temp_statistics=zip(scanners,accuracy_temp)

#print sys_calls_statistics
sorted_scanners_statistics=sorted(scanners_statistics,key=lambda x: x[1],reverse=True)
sorted_accuracy_statistics=sorted(accuracy_statistics,key=lambda x: x[1],reverse=True)
sorted_accuracy_temp_statistics=sorted(accuracy_temp_statistics,key=lambda x: x[1],reverse=True)

print sorted_scanners_statistics
name=''
number=''
for item in sorted_scanners_statistics:
    name+=item[0]+' & '
    number+=str(item[1])+ ' & '
print name
print number 

name=''
number=''
for item in sorted_accuracy_statistics:
    name+=item[0]+' & '
    number+=str('{:.1%}'.format(item[1]))+ ' & '
print name
print number

name=''
number=''
for item in sorted_accuracy_temp_statistics:
    name+=item[0]+' & '
    number+=str('{:.1%}'.format(item[1]))+ ' & '
print name
print number




