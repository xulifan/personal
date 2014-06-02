import os, sys, shutil
from os import listdir
from os.path import isfile, join

files=sys.argv[1]
input=sys.argv[2]
output=sys.argv[3]
input.rstrip('/')
output.rstrip('/')

if os.path.isdir(output) != True:
    os.mkdir(output,0755)

f=open(files)
for line in f.readlines():
    line=line.rstrip()
    print line
    if os.path.isdir(input+'/'+line):
        shutil.copytree(input+'/'+line,output+'/'+line)

