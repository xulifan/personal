import sys
import numpy
import glob
import matplotlib.pyplot as plt

#input:
#   python build_hist.py "./1111m_4276b_main/bad*" "./1111m_4276b_main/good*" 20
#

files1 = glob.glob(sys.argv[1])
files2 = glob.glob(sys.argv[2])
numbers1 = [0] * len(files1)
numbers2 = [0] * len(files2)
for i in range(len(files1)):
	fid = open(files1[i], 'rt')
	numbers1[i] = int(fid.readline().split()[0])
	fid.close()
for i in range(len(files2)):
	fid = open(files2[i], 'rt')
	numbers2[i] = int(fid.readline().split()[0])
	fid.close()
print "min1:", min(numbers1)
print "max1:", max(numbers1)
print "mean1:", sum(numbers1)/float(len(numbers1))
print "min2:", min(numbers2)
print "max2:", max(numbers2)
print "mean2:", sum(numbers2)/float(len(numbers2))
bins=numpy.linspace(0,200,int(sys.argv[3]))
fig=plt.figure(1)
plt.hist(numbers1, bins,alpha=0.5,color='b',label=sys.argv[1])
plt.hist(numbers2, bins,alpha=0.5,color='g',label=sys.argv[2])
plt.xlabel("Number of Nodes")
plt.ylabel("Frequency")
plt.title("Histogram for " + sys.argv[1] + " and "+sys.argv[2])
plt.legend([sys.argv[1],sys.argv[2]])
#plt.show()
print sys.argv[1].split('/')[-2]
fig.savefig('nodehist_'+sys.argv[1].split('/')[-2],  bbox_inches='tight')
