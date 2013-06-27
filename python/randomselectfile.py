import os, sys, shutil, random
from os import listdir
from os.path import isfile, join



input=sys.argv[1]
output=sys.argv[2]
n=int(sys.argv[3])
os.mkdir(output,0755);
i=0;
while i<n:
    i+=1
    file_list=random.sample(listdir(input),n)
    #print file_list
    i=0
    for file in file_list:
        shutil.copy2(input+"/"+file,output+"/"+file)
        i+=1
        print i,file

