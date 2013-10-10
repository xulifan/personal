import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

input_file=sys.argv[1]

f=open(input_file,'r')

line_count=0
line_20=[]
data=[]
kernels=[]
for line in f:
    line_count+=1
    if line_count < 20:
        continue
    elif line_count == 20:
        line_20=line
    else:
        line=line.strip()
        parse=line.split()
        for i in range(0,len(parse)):
            parse[i]=parse[i].rstrip(',')
            parse[i]=parse[i].rstrip('}')
            parse[i]=parse[i].lstrip('{')
            #print parse[i]
        #del parse[7]
        parse_rm_empty=[x for x in parse if x!= '']
        kernel_name_parse=parse_rm_empty[0].split('__')
        real_kernel_name=kernel_name_parse[0]
        parse_rm_empty[0]=kernel_name_parse[0]
        if real_kernel_name not in kernels:
            kernels.append(real_kernel_name)
        #print parse
        data.append(parse_rm_empty)
print data
print kernels
n_col=len(data[0])
#print n_col

n_kernel=len(kernels)
print "num of kernrels is ",n_kernel," : ",kernels

output=[[ 0 for x in range(n_col)] for y in range(n_kernel) ]
kernel_count=[ 0 for x in range(n_kernel)]

for i in range(0,n_kernel):
    output[i][0]=kernels[i]
#print output

LocalSizeNull=0

for record in data:
    kernel_index=kernels.index(record[0])
    kernel_count[kernel_index]+=1
    #print record, kernel_index
    for j in range(1,n_col):
        if record[j] == 'NULL':
            LocalSizeNull=1
        if record[j] != 'NA' and record[j] != 'NULL':
            if '.' not in record[j]:
                #print record[j]
                output[kernel_index][j] += int(record[j])
            else:
                output[kernel_index][j] += float(record[j])
        else:
            output[kernel_index][j] = record[j]
            
for i in range(n_kernel):
    for j in range (1,n_col):
        if output[i][j] != 'NA' and record[j] != 'NULL':
            output[i][j]/= kernel_count[i]


line_20=line_20.rstrip('\n')
line_20+=', extra1, extra2\n'

output_name=input_file[0:-4]+'_csv_output.csv'
print 'output to ', output_name
f_output=open(output_name,'w')
f_output.write(str(line_20))

#print "Local Size is NULL? ",LocalSizeNull

for i in range(n_kernel):
    j=0
    Time=0
    VALUInsts=0
    VFetchInsts=0
    VWriteInsts=0
    VALUUtilization=0
    FetchSize=0
    WriteSize=0
        
    if LocalSizeNull==0:
        while j < n_col:
            if j==4:
                f_output.write('{'+str(output[i][4])+','+str(output[i][5])+','+str(output[i][6])+'}')
                j+=2
            elif j==7:
                f_output.write('{'+str(output[i][7])+','+str(output[i][8])+','+str(output[i][9])+'}')
                j+=2
            else:
                f_output.write(str(output[i][j]))
            f_output.write(' ')
            j+=1
        Time=output[i][10]
        VALUInsts=output[i][17]
        VFetchInsts=output[i][19]
        VWriteInsts=output[i][21]
        VALUUtilization=output[i][23]
        FetchSize=output[i][26]
        WriteSize=output[i][32]
    else:
        while j < n_col:
            if j==4:
                f_output.write('{'+str(output[i][4])+','+str(output[i][5])+','+str(output[i][6])+'}')
                j+=2
            else:
                f_output.write(str(output[i][j]))
            f_output.write(' ')
            j+=1
        Time=output[i][8]
        VALUInsts=output[i][15]
        VFetchInsts=output[i][17]
        VWriteInsts=output[i][19]
        VALUUtilization=output[i][21]
        FetchSize=output[i][24]
        WriteSize=output[i][30]
        
    temp1=VALUInsts/(VFetchInsts+VWriteInsts)
    temp2=(FetchSize+WriteSize)/Time
    print output[i][0],Time,VALUInsts,VFetchInsts,VWriteInsts,VALUUtilization,FetchSize,WriteSize,temp1,temp2
    f_output.write(str(temp1))
    f_output.write(' ')
    f_output.write(str(temp2))
    f_output.write('\n')
f_output.closed
'''
f_output=open('csv_output.csv','wb')
writer=csv.writer(f_output)
writer.writerow(str(line_20))
f_output.close()
'''

#print output
#print line_20

