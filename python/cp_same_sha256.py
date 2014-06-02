import os, sys, shutil
from os import listdir
from os.path import isfile, join

#
#   python cp_same_sha256.py drebin.sha256 6117b_6930m.sha256 same_malwre_with_drebin
#

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


