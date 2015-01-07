import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python ./python_scripts/method_collect.py 3 ~/Software/genymotion-2.3.0/genymotion/tools/output_2013_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2014_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_benign_10s/
#


#
#['add-double', 'add-float', 'add-int', 'add-long', 'aget', 'aget-boolean', 'aget-byte', 'aget-char', 'aget-object', 'aget-short', 'aget-wide', 'and-int', 'and-long', 'aput', 'aput-boolean', 'aput-byte', 'aput-char', 'aput-object', 'aput-short', 'aput-wide', 'array-length', 'check-cast', 'cmp-long', 'cmpg-double', 'cmpg-float', 'cmpl-double', 'cmpl-float', 'const', 'const-class', 'const-string', 'const-wide', 'div-double', 'div-float', 'div-int', 'div-long', 'double-to-float', 'double-to-int', 'double-to-long', 'fill-array-data', 'fill-array-data-payload', 'filled-new-array', 'float-to-double', 'float-to-int', 'float-to-long', 'goto', 'if-eq', 'if-eqz', 'if-ge', 'if-gez', 'if-gt', 'if-gtz', 'if-le', 'if-lez', 'if-lt', 'if-ltz', 'if-ne', 'if-nez', 'iget', 'iget-boolean', 'iget-byte', 'iget-char', 'iget-object', 'iget-short', 'iget-wide', 'instance-of', 'int-to-byte', 'int-to-char', 'int-to-double', 'int-to-float', 'int-to-long', 'int-to-short', 'invoke-direct', 'invoke-interface', 'invoke-static', 'invoke-super', 'invoke-virtual', 'iput', 'iput-boolean', 'iput-byte', 'iput-char', 'iput-object', 'iput-short', 'iput-wide', 'long-to-double', 'long-to-float', 'long-to-int', 'monitor-enter', 'monitor-exit', 'move', 'move-exception', 'move-object', 'move-result', 'move-result-object', 'move-result-wide', 'move-wide', 'mul-double', 'mul-float', 'mul-int', 'mul-long', 'neg-double', 'neg-float', 'neg-int', 'neg-long', 'new-array', 'new-instance', 'nop', 'not-int', 'not-long', 'or-int', 'or-long', 'packed-switch', 'packed-switch-payload', 'rem-double', 'rem-float', 'rem-int', 'rem-long', 'return', 'return-object', 'return-void', 'return-wide', 'rsub-int', 'sget', 'sget-boolean', 'sget-byte', 'sget-char', 'sget-object', 'sget-short', 'sget-wide', 'shl-int', 'shl-long', 'shr-int', 'shr-long', 'sparse-switch', 'sparse-switch-payload', 'sput', 'sput-boolean', 'sput-byte', 'sput-char', 'sput-object', 'sput-short', 'sput-wide', 'sub-double', 'sub-float', 'sub-int', 'sub-long', 'throw', 'unresolved', 'ushr-int', 'ushr-long', 'xor-int', 'xor-long']
#

method_all=[]

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
            
            if 'method.out' in files:
                f=open(apk_dir+'/method.out','r')
                lines=f.readlines()
                f.close()
                try:
                    for line in lines:
                        line=line.strip()
                        line=line.split()
                        if line[1] not in method_all:
                            print "add ",line[1]
                            method_all.append(line[1])
                        
                except:
                    print 'Error in ',apk_dir,sys.exc_info()
                    continue                    
            else:
                print 'Cannot find method.out ! ',folder,dirs
                continue
            
                
            
            


method_all.sort()    
print '\nall method:'
for item in method_all:
    print item
    
print '\n'
print method_all

print len(method_all)
    


