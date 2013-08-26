import os, sys, shutil
from os import listdir
from os.path import isfile, isdir, join
from collections import Counter
from subprocess import call

files=sys.argv[1]
dest_direc=sys.argv[2]
dest_direc.rstrip('/')
if(os.path.isdir(dest_direc)!=True):
    os.mkdir(dest_direc,0755)

f_files=open(files,'r')



filenames=f_files.readlines()
for fullname in filenames:   
    fullname=fullname.rstrip('\n')
    original_name=fullname
    fullname=fullname.split('/') 
    #print fullname
    #fullname=fullname[-2]+'_'+fullname[-1]  
    fullname=fullname[-1]    
    target_name=dest_direc+'/'+fullname.replace('.jpg','.ppm')
    #call(["djpeg","-outfile",target_name,original_name ])
    call(["convert",original_name,"-resize","256x256!",target_name ])
    print fullname+" "+target_name
#print dest_direc
