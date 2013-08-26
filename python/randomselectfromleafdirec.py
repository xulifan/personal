import os, sys, shutil, random
from os import listdir
from os.path import isfile, isdir, join



input=sys.argv[1]
output=sys.argv[2]
input=input.rstrip('/')
output=output.rstrip('/')
n=int(sys.argv[3])
if(os.path.isdir(output)!=True):
    os.mkdir(output,0755)

f_direc=open(input,'r')
leaf_direcs=f_direc.readlines()
for leaf_direc in leaf_direcs:
    leaf_direc=leaf_direc.rstrip('\n')
    img_list=random.sample(listdir(leaf_direc),n)
    i=0
    print leaf_direc
    for img in img_list:       
        shutil.copy2(leaf_direc+"/"+img,output+"/"+img)
        i+=1
        print i,img

'''
for dirs in listdir(input):
    new_dir=output+"/"+dirs
    cat_dir=input+"/"+dirs
    os.mkdir(new_dir,0755)
    file_list=random.sample(listdir(cat_dir),n)
    #print file_list
    i=0
    for file in file_list:
        shutil.copy2(cat_dir+"/"+file,new_dir+"/"+file)
        i+=1
        print i,file
'''
