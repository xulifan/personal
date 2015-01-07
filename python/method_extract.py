import fileinput,subprocess
import os, sys, shutil
import filecmp
import time
import signal
import datetime
from math import sqrt
from os import listdir
from os.path import isfile, join
from operator import add

#
#   python method_extract.py ~/Desktop/Data/Malware/VirusShare/2013 ~/Software/genymotion-2.3.0/genymotion/tools/output_2013_10s/
#

input_direc=sys.argv[1].rstrip('/')
output_direc=sys.argv[2].rstrip('/')

extract_script="/home/lifan/Desktop/Data/Malware/python_scripts/method_extract_oneapk.py"

if os.path.isdir(output_direc) != True:
    os.mkdir(output_direc,0755)


for item in listdir(input_direc):

    sys.stdout.flush()
    
    test_apk=input_direc+'/'+item
    apk_out_direc=output_direc+'/'+item
    
    if os.path.isdir(apk_out_direc) != True:
        #os.mkdir(apk_out_direc,0755)
        continue
    
    
    print item
    method_file=apk_out_direc+'/method.out'
    
    
    subprocess.call("python "+extract_script+" "+test_apk+" > method.out",stderr=subprocess.STDOUT,shell=True)
    subprocess.call("mv method.out "+apk_out_direc,stderr=subprocess.STDOUT,shell=True)
    



