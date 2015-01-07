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
#   python svm_test.py ../representation/10s_2014_precomputedsvmformat/training_km/SPGK-INTERSECT.kernel.precomputedsvmformat ../representation/10s_2014_precomputedsvmformat/training_km/SPGK-INTERSECT.kernel.fnames ~/Software/libsvm-3.18/svm-predict ../representation/10s_2014_precomputedsvmformat/training_km/libsvmtrain.model
#

precomputed_svm_file=sys.argv[1]
fnames_file=sys.argv[2]
svm_predict=sys.argv[3]
svm_model=sys.argv[4]

f=open(precomputed_svm_file,'r')
lines=f.readlines()
f.close()

precomputed_svm=[]
for line in lines:
    line=line.strip()
    precomputed_svm.append(line)
 
f=open(fnames_file,'r')
lines=f.readlines()
f.close()

fnames=[]
for line in lines:
    line=line.strip()
    fnames.append(line)
    
#print precomputed_svm
#print fnames

f_output=open('prediction_error.output','w')

for i in range(len(fnames)):
    file_name=fnames[i]
    sim=precomputed_svm[i].split()
    target=sim[0]
    sim[1]='0:0'
    f=open('query_test','w')
    f.write(' '.join(sim))
    f.close()
    predict_result=subprocess.check_output(svm_predict+" query_test "+svm_model+" svm_output",stderr=subprocess.STDOUT,shell=True)
    predict_result=predict_result.strip().split()
    
    #print predict_result[2]
    if predict_result[2] != '100%':
        f_output.write(str(i)+' ')
        f_output.write(file_name)
        f_output.write('\n')
        print i,file_name,predict_result[2]
f_output.close()

    
