import os, sys, shutil
from os import listdir
from os.path import isfile, join

#
#   python ./python_scripts/rm_files.py ./representation/graph/23f/precomputedsvm/10s_all_precomputedsvmformat/prediction_error.output ./representation/permission/684f/10s_all_test/
#

rm_file_name=sys.argv[1]
rm_direc=sys.argv[2]

rm_direc.rstrip('/')

f=open(rm_file_name,'r')
lines=f.readlines()
f.close()
for line in lines:
    line=line.split()[1].split('/')[-1]
    print line
    os.remove(rm_direc+'/'+line)
