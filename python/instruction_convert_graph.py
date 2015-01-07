import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python convert_apkinfo_to_feat_vect.py ./original_data_from_jose/malware 0
#


instruction=['add-double', 'add-float', 'add-int', 'add-long', 'aget', 'aget-boolean', 'aget-byte', 'aget-char', 'aget-object', 'aget-short', 'aget-wide', 'and-int', 'and-long', 'aput', 'aput-boolean', 'aput-byte', 'aput-char', 'aput-object', 'aput-short', 'aput-wide', 'array-length', 'check-cast', 'cmp-long', 'cmpg-double', 'cmpg-float', 'cmpl-double', 'cmpl-float', 'const', 'const-class', 'const-string', 'const-wide', 'div-double', 'div-float', 'div-int', 'div-long', 'double-to-float', 'double-to-int', 'double-to-long', 'fill-array-data', 'fill-array-data-payload', 'filled-new-array', 'float-to-double', 'float-to-int', 'float-to-long', 'goto', 'if-eq', 'if-eqz', 'if-ge', 'if-gez', 'if-gt', 'if-gtz', 'if-le', 'if-lez', 'if-lt', 'if-ltz', 'if-ne', 'if-nez', 'iget', 'iget-boolean', 'iget-byte', 'iget-char', 'iget-object', 'iget-short', 'iget-wide', 'instance-of', 'int-to-byte', 'int-to-char', 'int-to-double', 'int-to-float', 'int-to-long', 'int-to-short', 'invoke-direct', 'invoke-interface', 'invoke-static', 'invoke-super', 'invoke-virtual', 'iput', 'iput-boolean', 'iput-byte', 'iput-char', 'iput-object', 'iput-short', 'iput-wide', 'long-to-double', 'long-to-float', 'long-to-int', 'monitor-enter', 'monitor-exit', 'move', 'move-exception', 'move-object', 'move-result', 'move-result-object', 'move-result-wide', 'move-wide', 'mul-double', 'mul-float', 'mul-int', 'mul-long', 'neg-double', 'neg-float', 'neg-int', 'neg-long', 'new-array', 'new-instance', 'nop', 'not-int', 'not-long', 'or-int', 'or-long', 'packed-switch', 'packed-switch-payload', 'rem-double', 'rem-float', 'rem-int', 'rem-long', 'return', 'return-object', 'return-void', 'return-wide', 'rsub-int', 'sget', 'sget-boolean', 'sget-byte', 'sget-char', 'sget-object', 'sget-short', 'sget-wide', 'shl-int', 'shl-long', 'shr-int', 'shr-long', 'sparse-switch', 'sparse-switch-payload', 'sput', 'sput-boolean', 'sput-byte', 'sput-char', 'sput-object', 'sput-short', 'sput-wide', 'sub-double', 'sub-float', 'sub-int', 'sub-long', 'throw', 'unresolved', 'ushr-int', 'ushr-long', 'xor-int', 'xor-long']

n_feat=len(instruction)

input=sys.argv[1]
output=sys.argv[2]
input=input.rstrip('/')
output=output.rstrip('/')
if(os.path.isdir(output)!=True):
    os.mkdir(output,0755)
    
label=sys.argv[3]

for dirs in listdir(input):
    #print dirs
    apk_dir=input+'/'+dirs
    if os.path.isdir(apk_dir):
        files=listdir(apk_dir)
        feat_vect=[0 for i in range(n_feat)]
        
        if 'instruction.out' in files:
            f=open(apk_dir+'/instruction.out','r')
            lines=f.readlines()
            f.close()
            
            for line in lines:
                line=line.strip()
                line=line.split('/')
                real_instruction = line[0]
                
                if real_instruction in instruction:
                    feat_vect[instruction.index(real_instruction)]=1
                else:
                    print apk_dir,real_instruction
            
            
            output_filename=output+'/'+label+'_'+dirs+'.txt'
            f_output=open(output_filename,'w')
            f_output.write("1 ")
            f_output.write(str(n_feat))
            f_output.write("\n")
            f_output.write(' '.join(str(i) for i in feat_vect))
            f_output.write("\n")
            f_output.write("0\n")
            f_output.close()
                    #print line

#instruction_all.sort()
#print instruction_all

#print len(instruction_all)



              
            
    
    


