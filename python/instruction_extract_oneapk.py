import fileinput,shlex,subprocess
import os, sys, shutil
import filecmp
import time
import signal
import datetime
from math import sqrt
from os import listdir
from os.path import isfile, join
from operator import add
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.core.analysis import analysis

apk_name=sys.argv[1]

a=apk.APK(apk_name)
d = dvm.DalvikVMFormat(a.get_dex())
x = analysis.VMAnalysis(d)
for method in d.get_methods():
    g = x.get_method(method)

    if method.get_code() == None:
      continue

    #print method.get_class_name(), method.get_name(), method.get_descriptor()

    idx = 0
    for i in g.get_basic_blocks().get(): 
        #print "\tbasic block: %s %x %x" % (i.name, i.start, i.end), '[ NEXT = ', ', '.join( "%x-%x-%s" % (j[0], j[1], j[2].get_name()) for j in i.get_next() ), ']', '[ PREV = ', ', '.join( j[2].get_name() for j in i.get_prev() ), ']'

        for ins in i.get_instructions():
            #print "\t\tinstruction: %x" % idx, ins.get_name(), ins.get_output()
            print ins.get_name()
            idx += ins.get_length()

        #print ""
