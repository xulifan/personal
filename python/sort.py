import os, sys, shutil
from os import listdir
from os.path import isfile, join

label=sys.argv[1]
feat=sys.argv[2]

f_label=open(label,'r')
f_feat=open(feat,'r')
line=f_feat.readline()
line=line.split()
n_img=int(line[0])
n_feat=int(line[1])
print n_img,n_feat


labels=f_label.readlines()
feats=f_feat.readlines()



zipped=zip(labels,feats)
zipped.sort(key = lambda t: t[0])

f_label.close()
f_feat.close()

f_label=open('filename_sorted','w')
f_feat=open('gist_sorted','w')
first_line=str(n_img)+' '+str(n_feat)+'\n'
f_feat.write(first_line)
for a in zipped:
    f_label.write(a[0])
    f_feat.write(a[1])

f_label.close()
f_feat.close()
#print zipped

