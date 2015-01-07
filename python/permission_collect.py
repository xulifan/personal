import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python permission_collect.py 3 ~/Software/genymotion-2.3.0/genymotion/tools/output_benign_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2014_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2013_10s/
#



uses_permission_all=[]
third_party_permission=[]
permission_all=[]

n_folder=int(sys.argv[1])
input_folder=[]
for i in range(n_folder):
    tmp=sys.argv[2+i].rstrip('/')
    input_folder.append(tmp)

for folder in input_folder:
    for dirs in listdir(folder):
        #print dirs
        apk_dir=folder+'/'+dirs
        if os.path.isdir(apk_dir):
            files=listdir(apk_dir)
            strace_filename=''
            app_name=''
            app_id=-1
            root_num=-1
            
            if 'permission.out' in files:
                f=open(apk_dir+'/permission.out','r')
                lines=f.readlines()
                f.close()
                try:
                    for line in lines:
                        line=line.rstrip()
                        line=line.split()
                        real_permission=line[1].split('.')[-1]
                        
                        if line[0]=='uses-permission:':
                            if line[1] not in uses_permission_all:
                                uses_permission_all.append(line[1])
                        if line[0]=='permission:':
                            if line[1] not in third_party_permission:
                                third_party_permission.append(line[1])
                        if real_permission not in permission_all:
                            print "Add ",line[1],real_permission
                            permission_all.append(real_permission)
                except:
                    print 'Error in ',apk_dir
                    continue                    
            else:
                print 'Cannot find permission.out ! ',folder,dirs
                continue
            
                
            
            
print 'uses-permissions:'
#for item in uses_permission_all:
#    print item
    
print '\nthird party permissions:'
#for item in third_party_permission:
#    print item

permission_all.sort()    
print '\nall permissions:'
#for item in permission_all:
#    print item
    
print '\n'
print permission_all

print len(permission_all)
    


