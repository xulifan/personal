import os, sys, shutil
#sys.path.append("/usr/lib64/python2.6/site-packages")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from collections import Counter

input=sys.argv[1]

f=open(input,'r')
alldata=[]
cluster=[]
image=[]
dimension=[]
base_kernel=[]
v2_kernel=[]
v5_kernel=[]
for line in f:
    line=line.strip()
    #print line
    parse=line.split()
    #print parse
    parse[0]=int(parse[0])
    parse[1]=int(parse[1])
    parse[2]=int(parse[2])
    parse[3]=float(parse[3])
    parse[4]=float(parse[4])
    parse[5]=float(parse[5])
    trim=[parse[0],parse[1],parse[2],parse[3],parse[4],parse[5]]
    alldata.append(trim)
    if parse[0] not in cluster:
        cluster.append(parse[0])
    if parse[1] not in image:
        image.append(parse[1])
    if parse[2] not in dimension:
        dimension.append(parse[2])
    if parse[3] not in base_kernel:
        base_kernel.append(parse[3])
    if parse[4] not in v2_kernel:
        v2_kernel.append(parse[4])
    if parse[5] not in v5_kernel:
        v5_kernel.append(parse[5])
    #print trim
#print plotdata
num_rec = len(alldata)
print "total number of records is", num_rec

cluster=sorted(cluster)
dimension=sorted(dimension)
image=sorted(image)
print cluster
print dimension
print image


n_clusters=len(cluster)

n_images=len(image)

n_dimensions=len(dimension)


ticks=[]
for i in range(0,n_images):
    ticks.append(i)


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

labels=["Baseline","V2","V5"]

plotcount=1
fig=plt.figure(1,figsize=(20,10))

for j in range(0,n_dimensions):
    cur_dim=dimension[j]
    for i in range(0,n_clusters):
        cur_cluster=cluster[i]
    
        plt.subplot(n_dimensions,n_clusters,plotcount)
        plotcount+=1
        for k in range(0,3):
            plotdata=[]
            for m in range(0,n_images):
                cur_img=image[m]
                for l in range(0,num_rec):
                    #print alldata[l][0],alldata[l][2]
                    if(alldata[l][0]==cur_cluster and alldata[l][2]==cur_dim and alldata[l][1]==cur_img):
                        plotdata.append(alldata[l][3+k])
            print cur_cluster,cur_dim, plotdata
            plt.plot(ticks,plotdata,linestyle='-',marker=markers[k%num_markers],color=colors[k%num_colors],label=labels[k])
            if i==0:
                plt.ylabel('Dimensions = '+str(cur_dim))
            if j==n_dimensions-1:
                plt.xlabel('Clusters = '+str(cur_cluster))
            #plt.yticks(rotation=45,fontsize=10)
            plt.xticks(ticks,image,rotation=45,fontsize=10)
lgd=plt.legend(bbox_to_anchor=(-1.4, 4),fontsize=15,ncol=n_dimensions)
fig.text(0.5, -0.01, 'Number Images', ha='center', va='center')
fig.text(-0.01, 0.5, 'Time', ha='center', va='center', rotation='vertical')    
fig.tight_layout()    
fig.savefig('output', bbox_inches='tight')



