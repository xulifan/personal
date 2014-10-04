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
total_process=int(sys.argv[3])
cur_process=int(sys.argv[4])

failed_apks=[]
failed_reasons=[]
strace_time=5

avd_name='AVD'+sys.argv[4]
port_number=5554+cur_process*2
emulator_name='emulator-'+str(port_number)
tmp_dir='temp'+sys.argv[4]

if os.path.isdir(output_direc) != True:
    os.mkdir(output_direc,0755)

if os.path.isdir(tmp_dir) != True:
    os.mkdir(tmp_dir,0755)

count=0
for item in listdir(input_direc):
    count+=1
    if (count-1)%total_process != cur_process:
        continue
    #
    #   start AVD on background
    #
    subprocess.call("~/Software/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator -port "+str(port_number)+" -avd "+ avd_name+" -wipe-data -no-boot-anim -no-window &",shell=True)
    #./emulator -avd AVD2 -wipe-data -no-boot-anim -no-window
    #time.sleep(30)
    
    print 'installing '+str(count)+' '+item
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
            getprop_output=subprocess.check_output("./adb -s "+emulator_name+" shell pm list features",stderr=subprocess.STDOUT,shell=True)
            #print 'getprop_output ',getprop_output
            if 'feature' in getprop_output:
                break;
        except:
            pass
    
    #
    #   get zygote PID
    #
    zygote_id=subprocess.check_output("./adb -s "+emulator_name+" shell ps | grep zygote | awk \'{print$2}\'",stderr=subprocess.STDOUT,shell=True)
    zygote_id=zygote_id.rstrip()


    
    #
    #   try install the package
    #
    install_output=''
    try:
        install_output=subprocess.check_output("./adb -s "+emulator_name+" install "+test_apk,stderr=subprocess.PIPE,shell=True)
        print 'install_output '+install_output
        install_output=install_output.split()[-1]
        if install_output != 'Success':
            failed_apks.append(item)
            print ' Install Fail!!!!'
            print install_output
            if install_output not in failed_reasons:
                failed_reasons.append(install_output)
            subprocess.call("./adb -s "+emulator_name+" emu kill",shell=True)
            continue
    except:
        failed_apks.append(item)
        print 'Fail to install :',install_output,sys.exc_info()[1]
        subprocess.call("./adb -s "+emulator_name+" emu kill",shell=True)
        continue
    
    #print 'strace '+zygote_id
    #
    #   strace zygote
    #    
    #subprocess.call("./adb shell timeout -t "+str(strace_time)+" strace -q -f -t -xx -p"+zygote_id+" > strace.out &",shell=True)
    subprocess.call("./adb -s "+emulator_name+" shell strace -q -f -t -xx -p "+zygote_id+" > "+tmp_dir+"/strace.out &",shell=True)
    
    #print 'start '
    #
    #   try start the application
    #
    try:
        start_output=subprocess.check_output("./adb -s "+emulator_name+" shell am start -n "+pkg+"/"+act,stderr=subprocess.PIPE,shell=True)
    except:
        print 'Fail to start'
        failed_apks.append(item)
        time.sleep(strace_time)
        subprocess.call("./adb -s "+emulator_name+" emu kill",shell=True)
        continue
    
    #print 'sleep'    
    time.sleep(strace_time)
    
    #print 'ps'
    #
    # get zygote PID and application PID
    #
    subprocess.call("./adb -s "+emulator_name+" shell ps > "+tmp_dir+"/ps.out",shell=True)
    strace_id=subprocess.check_output("cat "+tmp_dir+"/ps.out | grep strace | awk \'{print$2}\'",stderr=subprocess.STDOUT,shell=True)
    subprocess.call("./adb -s "+emulator_name+" shell kill "+strace_id,shell=True)
    test_id=subprocess.check_output("cat "+tmp_dir+"/ps.out | grep "+pkg+" | awk \'{print$2}\'",stderr=subprocess.STDOUT,shell=True)
    test_id=test_id.rstrip()
    if test_id == '':
        print 'Cannot get PID!'
        uninstall_output=subprocess.check_output("./adb -s "+emulator_name+" shell pm uninstall "+pkg,stderr=subprocess.PIPE,shell=True)
        failed_apks.append(item)
        subprocess.call("./adb -s "+emulator_name+" emu kill",shell=True)
        continue
        
    test_id=test_id.split()
    #for item in test_id:
    #    print item
    subprocess.call("./adb -s "+emulator_name+" shell kill "+test_id[0],shell=True)
    print 'PID is '+' '.join(test_id)
    
    #
    #   uninstall the application
    #
    uninstall_output=subprocess.check_output("./adb -s "+emulator_name+" shell pm uninstall "+pkg,stderr=subprocess.PIPE,shell=True)
    #print 'uninstall_output '+uninstall_output.split()[-1]
    if uninstall_output.split()[-1] != 'Success':
        print ' Uninstall Fail!!!!'
        print uninstall_output
        subprocess.call("./adb -s "+emulator_name+" emu kill",shell=True)
        continue
    subprocess.check_output("./adb -s "+emulator_name+" shell pm clear "+pkg,stderr=subprocess.PIPE,shell=True)
    
    
    #
    #   output
    #
    f=open(tmp_dir+"/information.out",'w')
    f.write("Package:   "+pkg+'\n')
    f.write("Activity:  "+act+'\n')
    f.write("ZygotePID: "+zygote_id+'\n')
    f.write("AppPID:    "+' '.join(test_id)+'\n')
    f.close()
    
    if os.path.isdir(apk_out_direc) != True:
        os.mkdir(apk_out_direc,0755)
    #print test_apk,apk_out_direc
    subprocess.call("mv "+tmp_dir+"/information.out "+apk_out_direc,shell=True)
    subprocess.call("mv "+tmp_dir+"/strace.out "+apk_out_direc,shell=True)
    subprocess.call("mv "+tmp_dir+"/ps.out "+apk_out_direc,shell=True)
    #print pkg
    #print act
    #print zygote_id
    #print test_id

    #
    #   kill the emulator
    #
    print 'Kill emulator'
    subprocess.call("./adb -s "+emulator_name+" emu kill",shell=True)

print '\n These APKs have failed:'
for item in failed_apks:
    print item

print '\n Reasons:'
for item in failed_reasons:
    print item



