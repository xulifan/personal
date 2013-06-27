import os, sys, shutil
from os import listdir
from os.path import isfile, join



input=sys.argv[1]
output=sys.argv[2]
input=input.rstrip('/')
output=output.rstrip('/')
os.mkdir(output,0755);
for dirs in listdir(input):
    new_dir=output+"/"+dirs
    cat_dir=input+"/"+dirs
    os.mkdir(new_dir,0755)
    count=1
    for f in listdir(cat_dir):
        if f[-4:]==".txt":
            fsplit=f.split("_")
            new_name=fsplit[0]+"_"+str(count)+".graph"
            shutil.copy2(cat_dir+"/"+f,new_dir+"/"+new_name)
            count+=1
            print f, fsplit, new_name
        
    #print dirs
