import sys
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

input=sys.argv[1]

f=open(input,'r')
plotdata=[]
for line in f:
    line=line.strip()
    parse=line.split()
    parse[8]=parse[8].lstrip('(')
    parse[8]=parse[8].rstrip(':')
    parse[8]=parse[8].rstrip(')')
    parse[5]=parse[5].rstrip('.kernel')
    parse[9]=float(parse[9])
    parse[8]=float(parse[8])
    trim=[parse[5],parse[8],parse[9]]
    plotdata.append(trim)
    #print trim
#print plotdata
num_rec = len(plotdata)
print "total number of records is", num_rec

num_c_vals=1
for i in range(0,num_rec):
    if plotdata[i][0] == plotdata[i+1][0]:
        num_c_vals+=1
    else:
        break

print "different C values is", num_c_vals

num_gks=num_rec/num_c_vals

if num_rec%num_c_vals !=0 :
    print "Error!"
    exit(0)

print "totla number of kernels is", num_gks

gk_names=[]
for i in range(0,num_gks):
    gk_names.append(plotdata[i*num_c_vals][0])

print gk_names

c_values=[]
for i in range(0,num_c_vals):
    c_values.append(plotdata[i][1])
print c_values

zipped=zip(*plotdata)
accuracy=zipped[2]
print accuracy

#get ticks for x axis
ticks=[]
for i in range(0,num_c_vals):
    ticks.append(i)
fig=plt.figure(1)

#get different colors
colors = ['b','g','r','c','m','y','k']
num_colors=len(colors)

#get different markers
markers = []
for m in Line2D.markers:
    try:
        if len(m) == 1 and m != ' ' and m != '_' and m != ',':
            markers.append(m)
    except TypeError:
        pass
num_markers=len(markers)
#print markers,num_markers

#plot for each graph kernel
for i in range(0,num_gks):
    plt.plot(ticks,accuracy[i*num_c_vals:(i+1)*num_c_vals],linestyle='-',marker=markers[i%num_markers],color=colors[i%num_colors],label=gk_names[i])

lgd=plt.legend(bbox_to_anchor=(1.5, 1.0),fancybox=True, shadow=True)
plt.ylabel('Accuracy')
plt.xlabel('C values')
plt.xticks(ticks,c_values)
#plt.show()
fig.savefig(input+'_fig', bbox_extra_artists=(lgd,), bbox_inches='tight')


