import os, sys, shutil
from os import listdir
from os.path import isfile, join

#
#   python cp_same_sha256.py drebin.sha256 6117b_6930m.sha256 same_malwre_with_drebin
#

sha_file=sys.argv[1]
time_file=sys.argv[2]

sha1=[]
file1=[]
f=open(sha_file,'r')
for line in f.readlines():
    line=line.rstrip().split()
    sha1.append(line[0])
    file1.append(line[1])
f.close()

year_uni=[]
year_count=[]
f=open(time_file,'r')
lines=f.readlines()
for line in lines:
    line=line.rstrip().split()
    sha_temp=line[0]
    year=line[1].split('-')
    if year[0].isdigit():
        if year[0] not in year_uni:
            year_uni.append(year[0])
            year_count.append(0)
        year_count[year_uni.index(year[0])]+=1
        #print sha_temp,year[0]
f.close()
print year_uni
print year_count

for year in year_uni:
    if os.path.isdir(year) != True:
        os.mkdir(year,0755)
for line in lines:
    line=line.rstrip().split()
    sha_temp=line[0]
    for i in range(len(sha1)):
        if sha1[i]==sha_temp:
            filename=file1[i]
            year=line[1].split('-')
            if year[0].isdigit():
                #print 'cp ',filename,' to ',year[0]
                shutil.copy2(filename,year[0])


    


'''
drebin_sha_file=sys.argv[1]
our_sha_file=sys.argv[2]
output=sys.argv[3]
output.rstrip('/')

if os.path.isdir(output) != True:
    os.mkdir(output,0755)

drebin_sha=[]
f=open(drebin_sha_file,'r')
for line in f.readlines():
    line=line.rstrip()
    drebin_sha.append(line)
f.close()

f=open(our_sha_file,'r')
for line in f.readlines():
    line=line.rstrip()
    line=line.split()
    if line[0] in drebin_sha:
        print line[1]
        shutil.copy(line[1],output)
'''

