import os, sys, shutil
import csv
from os import listdir
from os.path import isfile, join

#
#   python assign_test_train.py 6117b_6930m.family gappusin
#

family_file=sys.argv[1]
test_target=sys.argv[2]
test_target=test_target.lower()
test_num=0
total_num=0
output=family_file[:family_file.rfind('.')+1]+'testtrain.'+test_target

fp=open(family_file,'r')
fp_write=open(output,'w')
for line in fp.readlines():
    if line.rstrip()==test_target:
        fp_write.write('test\n')
        test_num+=1
        total_num+=1
    else:
        fp_write.write('train\n')
        total_num+=1
fp.close()
fp_write.close()
print output,test_num,total_num

