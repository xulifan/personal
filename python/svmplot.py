import sys
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

input=sys.argv[1]

f=open(input,'r')
plotdata=[]

for line in f:
    line=line.strip()
    parse=line.split()
    c_idx=0
    while c_idx<len(parse):
        if parse[c_idx][0] == '(' and parse[c_idx][-1:]==':' :
            break
        c_idx+=1
    kernel_idx=0
    while kernel_idx<len(parse):
        if len(parse[kernel_idx])>7 and parse[kernel_idx][-7:]==".kernel":
            break
        kernel_idx+=1
    acc_idx=len(parse)-1

    parse[c_idx]=parse[c_idx].lstrip('(')
    parse[c_idx]=parse[c_idx].rstrip(':')
    parse[c_idx]=parse[c_idx].rstrip(')')

    parse[kernel_idx]=parse[kernel_idx].rstrip('.kernel')
    parse[acc_idx]=float(parse[acc_idx])
    parse[c_idx]=float(parse[c_idx])
    trim=[parse[kernel_idx],parse[c_idx],parse[acc_idx]]
    #print trim
    #print parse[kernel_idx][0:7]
    #if parse[kernel_idx][0:7] != 'GAUSS-1':
    #    plotdata.append(trim)
    plotdata.append(trim)
    #print parse,c_idx,kernel_idx
print plotdata



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
plt.ylim([0.6,1.0])
plt.title(input)
plt.xticks(ticks,c_values,rotation=70)
#plt.show()
fig.savefig(input+'_fig', bbox_extra_artists=(lgd,), bbox_inches='tight')
#pdf=PdfPages(input+'_fig.pdf')
#pdf.savefig(fig)
#pdf.close()


