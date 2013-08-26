import os, sys, shutil
from os import listdir
from os.path import isfile, join
from collections import Counter

label=sys.argv[1]
cluster=sys.argv[2]

f_label=open(label,'r')
f_cluster=open(cluster,'r')


labels=f_label.readlines()
clusters=f_cluster.readlines()

count = Counter()
for label_temp in labels:
    count[label_temp] +=1

#print count
#print len(count)
n_labels=len(count)

count = Counter()
for label_temp in clusters:
    count[label_temp] +=1

#print count
#print len(count)
n_clusters=len(count)

print "num of labels "+str(n_labels)+" num of clusters "+str(n_clusters)+"\n"
zipped=zip(labels,clusters)
zipped.sort(key = lambda t: t[0])

#print zipped

count2 = Counter()
for zip_temp in zipped:
    count2[zip_temp] +=1

#print count2
#print len(count2)
x = [[0 for _ in range(n_clusters+1)] for _ in range(n_labels)]

for item in count2:
    num=count2[item]
    label_temp=item[0]
    cluster_temp=item[1]
    label_temp=label_temp.rstrip('\n')
    cluster_temp=cluster_temp.rstrip('\n')
    #print label_temp,cluster_temp, num
    for i in range(n_labels):
        if x[i][0] == 0 or x[i][0] == label_temp:
            x[i][0] = label_temp
            x[i][int(cluster_temp)+1]=num
            break


for i in range(n_labels):
    #print x[i][1:n_clusters+1],x[i][0]
    for j in range(1,n_clusters+1):
        print repr(x[i][j]).rjust(3),
    print x[i][0]
