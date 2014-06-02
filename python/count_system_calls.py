import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python convert_strace_to_graph_oneapp.py ./original_data_from_DrJose/delaware-benign/all-android-benign-samples-set-14-results/2014.02.11.15.52.10/ ./benign/ good
#


sys_calls=['select', 'ioctl', 'recvmsg', 'recv', 'munmap', 'open', 'pivot_root', 'close', 'sigaction', 'fork', 'mprotect', 'clone', 'syscall_983045', 'prctl', 'SYS_224', 'write', 'setgroups32', 'setgid32', 'fstat64', 'setuid32', 'personality', 'capset', 'setrlimit', 'msgget', 'setpriority', 'getpriority', 'socket', 'pipe', 'getpid', 'connect', 'getsockopt', 'getpgid', 'setpgid', 'sendmsg', 'fcntl64', 'access', 'getuid32', 'ipc_subcall', 'semop', 'semget', 'dup', 'read', 'writev', 'stat64', '_llseek', 'pread', 'gettimeofday', 'mkdir', 'chmod', 'lseek', 'sched_getparam', 'sched_getscheduler', 'syscall_983042', 'sigprocmask', 'getdents64', 'flock', 'nanosleep', 'pwrite', 'fsync', 'unlink', 'ftruncate', 'geteuid32', 'getgid32', 'getegid32', 'socketpair', 'bind', 'rename', 'lstat64', 'setsockopt', 'getsockname', 'rt_sigtimedwait', 'recvfrom', 'poll', 'dup2', 'getrlimit', 'execve', 'wait4', 'uname', 'fchmod', 'msync', 'sched_yield', 'shutdown', 'listen', 'rmdir', 'sigaltstack', 'rt_sigreturn', 'setitimer', 'getpeername', 'msgctl', 'getcwd', 'getgroups32', 'chdir', 'getrusage', 'symlink', 'vfork', 'ftruncate64', 'kill', 'sched_get_priority_min', 'sched_get_priority_max', 'mlock', 'umask', 'fchown32', 'munlock', 'chown32', 'readlink', 'setup', 'setsid', 'getdents', 'fdatasync', 'sendto']
sys_calls_count=[ 0 for i in range(len(sys_calls))]


sys_calls_all=[]

input=sys.argv[1]
input=input.rstrip('/')

n_graphs=0

for dirs in listdir(input):
    #print dirs
    apk_dir=input+'/'+dirs
    if os.path.isdir(apk_dir):
        files=listdir(apk_dir)
        highest_strace=-1
        strace_filename=''
        app_name=''
        app_id=-1
        root_num=-1
        
        if 'strace.txt' in files:
            strace_filename=apk_dir+'/strace.txt'
            apk_activities=''
            
            if os.path.isfile(apk_dir+'/apk-info.txt') != True:
                print 'Cannot open apk info file in ',apk_dir
                continue
            apk_info=open(apk_dir+'/apk-info.txt','r')
            apk_info.readline()
            apk_activities=apk_info.readline().rstrip().split()[0]
            apk_info.close()
            #print apk_activities
            
            
            #
            # get PID of the application in ps-output
            #
            if os.path.isfile(apk_dir+'/ps-output.txt') != True:
                print 'Cannot open ps output file in ',apk_dir
                continue
            ps_output=open(apk_dir+'/ps-output.txt','r')
            ps_content=ps_output.readlines()
            for line in ps_content:
                if len(line)>0:
                    line=line.split()
                    if len(line) == 9:
                        if line[8] == 'zygote':
                            root_num=int(line[1])
                        if line[8] in apk_activities:
                            app_id=int(line[1])
                            break;
            if app_id==-1:
                print 'Cannot get application PID in ',apk_dir,files
                continue
            #print dirs,app_id,apk_activities
        else:
        
            #
            # get highest strace number if there is multiple strace files
            #
            for item in files:
                if item[0:7]=='strace.':
                    strace_num=int(item[7])
                    if strace_num>highest_strace:
                        highest_strace=strace_num
                        strace_filename=apk_dir+'/'+item
            if highest_strace==-1:
                print 'Cannot get strace file in ',apk_dir
                continue
                #sys.exit(0)
                
            #
            # get the application name in app-summary file
            #
            if os.path.isfile(apk_dir+'/app-summary.'+str(highest_strace)+'.txt') != True:
                print 'Cannot open app summary file in ',apk_dir
                continue
            app_summery=open(apk_dir+'/app-summary.'+str(highest_strace)+'.txt','r')
            for line in app_summery.readlines():
                line=line.split()
                if len(line)>0 and line[0]=='package:':
                    app_name=line[1]
            if len(app_name) == 0:
                print 'Cannot get application name in ',apk_dir
                continue
                #sys.exit(0)
                
            #
            # get PID of the application in ps-output
            #
            if os.path.isfile(apk_dir+'/ps-output.'+str(highest_strace)+'.txt') != True:
                print 'Cannot open ps output file in ',apk_dir
                continue
            ps_output=open(apk_dir+'/ps-output.'+str(highest_strace)+'.txt','r')
            for line in ps_output.readlines():
                line=line.split()
                if len(line)>0 and line[-1] == app_name:
                    app_id= int(line[1])
                if len(line)>0 and line[-1] == 'zygote':
                    root_num=int(line[1])
            if app_id==-1 or root_num==-1:
                print 'Cannot get application PID or root number in ',apk_dir,highest_strace,app_name
                continue
                #sys.exit(0)
                
            #print root_num,highest_strace,app_name,app_id,strace_filename
    
    
    
    
        #print 'converting ', dirs
        n_graphs+=1
        strace_fp=open(strace_filename,'r')
        contents=strace_fp.readlines()
        strace_fp.close()
        
        
        for item in contents:
            if 'unfinished' in item:
                continue
            if 'resumed' in item:
                continue
            if item.find('(')==-1:
                continue
            part1_str=item[0:item.find('(')]
            if len(part1_str)==0:
                continue
            result = -1
            if '=' in item.split():
                #print item
                item_split=item.split()
                item_split.reverse()
                result_str=item_split[item_split.index('=')-1]
                if result_str.isdigit():
                    result=int(result_str)
            if result == -1:
                continue
            #print item
            if part1_str.split()[0].isdigit():
                pid=int(part1_str.split()[0])
            else:
                continue
            pname=part1_str.split()[-1] 
            
            if pname in sys_calls:
                sys_calls_count[sys_calls.index(pname)]+=1
            else:
                print 'ERROR   ',pname,'   not in the list'
            

#print sys_calls_count
sys_calls_statistics=zip(sys_calls,sys_calls_count)
for item in sys_calls_statistics:
    print item[0],float(item[1])/float(n_graphs)

#print sys_calls_statistics
sorted_list=sorted(sys_calls_statistics,key=lambda x: x[1])


#print sorted_list
print n_graphs
for item in sorted_list:
    print item[0],float(item[1])/float(n_graphs)
     
    


