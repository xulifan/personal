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

svm_train="/home/lifan/Software/libsvm-3.18/svm-train"
input_folder=[]
for i in range(len(sys.argv)-1):
    input_folder.append(sys.argv[i+1])
print input_folder

n_fold=5
C_value=[0.25, 0.5, 1.0, 2.0,4.0,8.0,16.0,32.0,64.0,128.0,256.0,512.0,1024.0,2048.0,4096.0]

for folder in input_folder:
    folder=folder.rstrip('/')
    for file_name in listdir(folder):
        #print file_name[-21:]
        if file_name[-21:]==".precomputedsvmformat":
            print file_name
            svm_input=folder+'/'+file_name
            for C in C_value:
                
                test=subprocess.check_output(svm_train+" -q -t 4 -c "+str(C) +" -v "+str(n_fold)+" "+svm_input,stderr=subprocess.STDOUT,shell=True)
                accuracy=test.rstrip().split()[-1]
                accuracy=float(accuracy.rstrip('%'))/100
                print "Overall 1x"+str(n_fold)+"-fold CV Acc for "+file_name[0:-21]+" on "+folder+" with C ("+str(C)+"):  "+str(accuracy)
                #print test



