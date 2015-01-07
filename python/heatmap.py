import matplotlib.pyplot as plt
import os, sys, shutil

f=open(sys.argv[1],'r')

similarity=[]
for line in f:
    line=line.rstrip()
    line=line.split()
    sim=[float(x) for x in line]
    similarity.append(sim)

#print similarity
plt.imshow(similarity)
plt.jet()
plt.colorbar()
plt.show()
