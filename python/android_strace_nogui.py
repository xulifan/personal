import fileinput,subprocess
import os, sys, shutil
import filecmp
import time
from math import sqrt
from os import listdir
from os.path import isfile, join
from operator import add

input_direc=sys.argv[1].rstrip('/')
output_direc=sys.argv[2].rstrip('/')
failed_apks=[]
failed_reasons=[]
strace_time=5

if os.path.isdir(output_direc) != True:
    os.mkdir(output_direc,0755)

count=0
for item in listdir(input_direc):
    
    #
    #   start AVD on background
    #
    subprocess.call("~/Software/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator -avd AVD0 -wipe-data -no-boot-anim -no-window &",shell=True)
    #./emulator -avd AVD2 -wipe-data -no-boot-anim -no-window
    #time.sleep(30)
    
    #
    #   get emulator PID
    #
    emulator_id=subprocess.check_output("ps | grep emulator | awk \'{print$1}\'",stderr=subprocess.STDOUT,shell=True)
    
    print 'installing '+str(count)+' '+item
    count+=1
    test_apk=input_direc+'/'+item
    apk_out_direc=output_direc+'/'+item
    

    #
    #   get package name
    #
    pkg=subprocess.check_output("./aapt dump badging "+test_apk+"|awk -F\" \" \'/package/ {print $2}\'|awk -F\"\'\" \'/name=/ {print $2}\'",stderr=subprocess.STDOUT,shell=True)
    pkg=pkg.rstrip()


    #
    #   get activity
    #
    act=subprocess.check_output("./aapt dump badging "+test_apk+"|awk -F\" \" \'/launchable-activity/ {print $2}\'|awk -F\"\'\" \'/name=/ {print $2}\'",stderr=subprocess.STDOUT,shell=True)
    act=act.rstrip()

    #
    #   check the device is fully loaded 
    #
    while True:
        try:
            #getprop_output=subprocess.check_output("./adb wait-for-device shell getprop init.svc.servicemanager",stderr=subprocess.STDOUT,shell=True)
            #print 'getprop_output ',getprop_output
            #if 'running' in getprop_output:
            #    break;
            
            getprop_output=subprocess.check_output("./adb shell pm list features",stderr=subprocess.STDOUT,shell=True)
            #print 'getprop_output ',getprop_output
            if 'feature' in getprop_output:
                break;
        except:
            pass
    
    #
    #   get zygote PID
    #
    zygote_id=subprocess.check_output("./adb shell ps | grep zygote | awk \'{print$2}\'",stderr=subprocess.STDOUT,shell=True)
    zygote_id=zygote_id.rstrip()


    
    #
    #   try install the package
    #
    install_output=''
    try:
        install_output=subprocess.check_output("./adb install "+test_apk,stderr=subprocess.PIPE,shell=True)
        print 'install_output '+install_output
        install_output=install_output.split()[-1]
        if install_output != 'Success':
            failed_apks.append(item)
            print ' Install Fail!!!!'
            print install_output
            if install_output not in failed_reasons:
                failed_reasons.append(install_output)
            subprocess.call("./adb emu kill",shell=True)
            continue
    except:
        failed_apks.append(item)
        print 'Fail to install :',install_output,sys.exc_info()[1]
        subprocess.call("./adb emu kill",shell=True)
        continue
    
    #print 'strace '+zygote_id
    #
    #   strace zygote
    #    
    #subprocess.call("./adb shell timeout -t "+str(strace_time)+" strace -q -f -t -xx -p"+zygote_id+" > strace.out &",shell=True)
    subprocess.call("./adb shell strace -q -f -t -xx -p "+zygote_id+" > strace.out &",shell=True)
    
    #print 'start '
    #
    #   try start the application
    #
    try:
        start_output=subprocess.check_output("./adb shell am start -n "+pkg+"/"+act,stderr=subprocess.PIPE,shell=True)
    except:
        print 'Fail to start'
        failed_apks.append(item)
        time.sleep(strace_time)
        subprocess.call("./adb emu kill",shell=True)
        continue
    
    #print 'sleep'    
    time.sleep(strace_time)
    
    #print 'ps'
    #
    # get zygote PID and application PID
    #
    subprocess.call("./adb shell ps > ps.out",shell=True)
    strace_id=subprocess.check_output("cat ps.out | grep strace | awk \'{print$2}\'",stderr=subprocess.STDOUT,shell=True)
    subprocess.call("./adb shell kill "+strace_id,shell=True)
    test_id=subprocess.check_output("cat ps.out | grep "+pkg+" | awk \'{print$2}\'",stderr=subprocess.STDOUT,shell=True)
    test_id=test_id.rstrip()
    if test_id == '':
        print 'Cannot get PID!'
        uninstall_output=subprocess.check_output("./adb shell pm uninstall "+pkg,stderr=subprocess.PIPE,shell=True)
        failed_apks.append(item)
        subprocess.call("./adb emu kill",shell=True)
        continue
        
    test_id=test_id.split()
    #for item in test_id:
    #    print item
    subprocess.call("./adb shell kill "+test_id[0],shell=True)
    print 'PID is '+' '.join(test_id)
    
    #
    #   uninstall the application
    #
    #subprocess.call("./adb uninstall "+pkg,shell=True)
    uninstall_output=subprocess.check_output("./adb shell pm uninstall "+pkg,stderr=subprocess.PIPE,shell=True)
    #print 'uninstall_output '+uninstall_output.split()[-1]
    if uninstall_output.split()[-1] != 'Success':
        print ' Uninstall Fail!!!!'
        print uninstall_output
        subprocess.call("./adb emu kill",shell=True)
        continue
    subprocess.check_output("./adb shell pm clear "+pkg,stderr=subprocess.PIPE,shell=True)
    
    
    #
    #   output
    #
    f=open("information.out",'w')
    f.write("Package:   "+pkg+'\n')
    f.write("Activity:  "+act+'\n')
    f.write("ZygotePID: "+zygote_id+'\n')
    f.write("AppPID:    "+' '.join(test_id)+'\n')
    f.close()
    
    if os.path.isdir(apk_out_direc) != True:
        os.mkdir(apk_out_direc,0755)
    #print test_apk,apk_out_direc
    subprocess.call("mv information.out "+apk_out_direc,shell=True)
    subprocess.call("mv strace.out "+apk_out_direc,shell=True)
    subprocess.call("mv ps.out "+apk_out_direc,shell=True)
    #print pkg
    #print act
    #print zygote_id
    #print test_id

    #
    #   kill the emulator
    #
    print 'Kill emulator'
    subprocess.call("./adb emu kill",shell=True)

print '\n These APKs have failed:'
for item in failed_apks:
    print item

print '\n Reasons:'
for item in failed_reasons:
    print item



