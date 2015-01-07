import os, sys, shutil
from os import listdir
from os.path import isfile, join



input=sys.argv[1]
output=sys.argv[2]
input=input.rstrip('/')
output=output.rstrip('/')
if(os.path.isdir(output)!=True):
    os.mkdir(output,0755)
names=[]
for dirs in listdir(input):
    if dirs[0] != '.':
        names.append(dirs)
names.sort()
print names
i=0
while i < len(names):
    #print i
    length=len(names[i])
    if i < len(names)-1 and names[i][0:length-5] == names[i+1][0:length-5] and int(names[i][-5]) < int(names[i+1][-5]):
        print 'remove ',names[i],i
    else:
        print 'copy   ',names[i],i
        shutil.copy2(input+'/'+names[i],output+'/')
    i+=1
'''
    new_dir=output+"/"+dirs
    cat_dir=input+"/"+dirs
    os.mkdir(new_dir,0755)
    for f in listdir(cat_dir):
        if f[0:6]=="image_":
            fsplit=f.split("_")
            new_name=dirs+"_"+fsplit[1]
            shutil.copy2(cat_dir+"/"+f,new_dir+"/"+new_name)
            print fsplit, new_name
    #print dirs
'''
