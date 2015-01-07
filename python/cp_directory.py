import os, sys, shutil, subprocess
from os import listdir
from os.path import isfile, join

inputfile=sys.argv[1]
extractdirec=sys.argv[2]
outputdirec=sys.argv[3]

extractdirec=extractdirec.rstrip('/')
outputdirec=outputdirec.rstrip('/')

f=open(inputfile,'r')
lines=f.readlines()

for line in lines:
    line=line.rstrip()
    line=line.lstrip('bad_')
    line=line.lstrip('good_')
    line=line.rstrip('.txt')
    #print line
    target=extractdirec+'/'+line
    subprocess.call("cp -r "+target+" "+outputdirec,shell=True)
    
    
    

