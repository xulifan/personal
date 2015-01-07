import os, sys, shutil, hashlib, subprocess
from os import listdir
from os.path import isfile, join

input_direc=sys.argv[1]
input_direc.rstrip('/')

#f_output=open('MD5_packagename_filename.txt','w')
aapt='/home/lifan/Software/genymotion-2.3.0/genymotion/tools/aapt'
for item in os.listdir(input_direc):
    filename=item
    md5=''
    packagename=''
    if 'VirusShare' in filename:
        md5=filename.lstrip('VirusShare_')
    else:
        md5=hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest()
    packagename=subprocess.check_output(aapt+" dump badging "+input_direc+'/'+item+" | grep package",stderr=subprocess.STDOUT,shell=True)
    packagename=packagename.strip().split()[1]
    packagename=packagename.lstrip("name=\'")
    packagename=packagename.rstrip("\'")
    print md5,packagename,filename
