import os, sys, shutil
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
    line=line.split('/')
    filename=line[-1]
    if isfile(extractdirec+'/'+filename):
        shutil.copy2(extractdirec+'/'+filename,outputdirec)
        #print filename
    else:
        print filename+' not exist'
    
    
'''
input=sys.argv[1]
output=sys.argv[2]
input=input.rstrip('/')
output=output.rstrip('/')
os.mkdir(output,0755);
for dirs in listdir(input):
    new_dir=output+"/"+dirs
    cat_dir=input+"/"+dirs
    os.mkdir(new_dir,0755)
    for f in listdir(cat_dir):
        if f[0:6]=="image_":
            fsplit=f.split("_")
            new_name=dirs+"_"+fsplit[1]
            shutil.copy2(cat_dir+"/"+f,new_dir+"/"+new_name)
            print fsplit, new_name
    #print dirs
'''
