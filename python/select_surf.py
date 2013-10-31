import os, sys, shutil, random
from os import listdir
from os.path import isfile, join

input=sys.argv[1]
n_words=int(sys.argv[2])

output=input.rstrip('/')
output=output[output.rfind('/')+1:]
output+='_'+str(n_words)+'w'

print 'output to ',output
if n_words>0:
    f=open(input,'r')
    line=f.readline()
    line=line.split()
    n_points_all=int(line[0])
    n_feat_all=int(line[1])
    if n_words>=n_points_all:
        print 'More words than points,quit\n'
        sys.exit(0)
        
        
    print n_words,n_points_all
    lines=f.readlines()
    word_output=open(output,'w');
    word_output.write(str(n_words))
    word_output.write(' ')
    word_output.write(str(n_feat_all))
    word_output.write('\n')
    select_words=random.sample(lines,n_words)
    #print select_words
    for item in select_words:
        word_output.write(item)
    word_output.close()
