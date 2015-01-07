import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python collect_system_call_list.py 6 ~/Software/genymotion-2.3.0/genymotion/tools/output_benign_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2014_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2013_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2012_10s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2014_120s/ ~/Software/genymotion-2.3.0/genymotion/tools/output_2013_120s/
#
'''
['select', 'ioctl', 'recvmsg', 'futex', 'munmap', 'sigprocmask', '_exit', 'open', 'getdents64', 'mmap2', 'madvise', 'mprotect', 'clone', 'set_thread_area', 'prctl', 'gettid', 'getuid32', 'mkdir', 'unshare', 'lstat64', 'chmod', 'chown32', 'mount', 'setgroups32', 'setgid32', 'setuid32', 'personality', 'capset', 'access', 'sched_setscheduler', 'setrlimit', 'sigaction', 'clock_gettime', 'getpgid', 'setpgid', 'sendmsg', 'socket', 'pipe', 'getpid', 'connect', 'getsockopt', 'sendto', 'close', 'fcntl64', 'epoll_create', 'epoll_ctl', 'gettimeofday', 'epoll_wait', 'setpriority', 'getpriority', 'read', 'write', 'stat64', '_llseek', 'pread64', 'lseek', 'flock', 'fstat64', 'nanosleep', 'writev', 'brk', 'sched_yield', 'statfs64', 'unlink', 'umask', 'fchown32', 'pwrite64', 'fdatasync', 'geteuid32', 'getgid32', 'getegid32', 'socketpair', 'bind', 'recvfrom', 'fsync', 'rename', 'setsockopt', 'getsockname', 'poll', 'dup', 'ftruncate', 'rt_sigaction', 'rt_sigprocmask', 'get_thread_area', 'sigaltstack', 'getuid', 'fork', 'dup2', 'getrlimit', 'execve', 'exit_group', 'wait4', 'restart_syscall', 'ftruncate64', 'utimes', 'getpeername', 'sigreturn', 'fchmod', 'msync', 'rmdir', 'uname', 'clock_getres', 'readlink', 'tkill', 'sigsuspend', 'rt_sigreturn', 'sched_getparam', 'sched_getscheduler', 'sched_get_priority_min', 'sched_get_priority_max', 'shutdown', 'kill', 'listen', 'setitimer', 'accept', 'symlink', 'getcwd', 'getgroups32', 'getppid', 'setresgid32', 'setresuid32', 'inotify_init', 'inotify_add_watch', 'rt_sigtimedwait', 'tgkill', 'inotify_rm_watch', 'getrusage', 'sched_getaffinity', 'sched_setaffinity', 'chdir', 'mlock', 'munlock', 'setsid', 'vfork', 'fstatfs64', 'sync', 'old_mmap', 'ptrace', 'times', 'mknod', 'pipe2', 'timer_create', 'truncate'] 143
'''
class graph:
    def __init__(self,inputfile,pid,app_name,root_num,outputdirec,label,systemcalls):
        self.filename=inputfile
        self.app_name=app_name
        self.input_direc=self.filename
        self.input_direc=self.input_direc[0:self.input_direc.rfind('/')]
        self.input_direc=self.input_direc[self.input_direc.rfind('/')+1:]
        self.pid=pid
        self.root_num=root_num
        self.output_filename=''
        self.class_label=label
        self.output_direc=outputdirec.rstrip('/')+'/'
        self.n_node=0
        self.height=0
        self.n_feat=0
        self.sys_calls=systemcalls
        self.n_feat=len(self.sys_calls)
        self.node_list=[self.pid]
        self.node_height=[0]
        self.feat_mat=[]
        self.adj_mat=[]
        self.filter_contents=[]
        self.uni_pid=[]
        self.uni_pname=[]
    
    def read_strace(self,systemcalls):
        f=open(self.filename,'r')
        contents=f.readlines()
        f.close()
        self.filter_contents=[]
        #print len(contents)

        
        for item in contents:
            original_item=item
            if item[0] != '[':
                continue
            if 'unfinished' in item:
                continue
            
            pid=''
            pname=''
            result='1'
            try:
                if 'resumed>' in item:
                    item=item.split()
                    pid=item[1][:-1]
                    pname=item[4]
                    result=item[-1]
                else:
                    item=item.split()
                    if len(item) > 4:
                        pid=item[1][:-1]
                        pname=item[3]
                        pname=pname[0:pname.find('(')]
                        result=item[-1]
                    else:
                        continue
                
                if '++' in pname:
                    #[pid  1117] 05:43:30 +++ killed by SIGTERM +++
                    continue
                if '--' in pname:
                    #[pid  1114] 03:51:33 --- {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=1115, si_status=0, si_utime=0, si_stime=1} (Child exited) ---
                    continue
                if pname not in systemcalls:
                    systemcalls.append(pname)
                    print 'add into the system call list: ',pname,self.filename
            except:
                print self.filename
                print original_item
                print contents.index(original_item)
                sys.exit()
            
            
        


sys_calls_all=[]

n_folder=int(sys.argv[1])
input_folder=[]
for i in range(n_folder):
    tmp=sys.argv[2+i].rstrip('/')
    input_folder.append(tmp)

for folder in input_folder:
    for dirs in listdir(folder):
        #print dirs
        apk_dir=folder+'/'+dirs
        if os.path.isdir(apk_dir):
            files=listdir(apk_dir)
            strace_filename=''
            app_name=''
            app_id=-1
            root_num=-1
            
            if 'information.out' in files:
                f=open(apk_dir+'/information.out','r')
                lines=f.readlines()
                f.close()
                try:
                    for line in lines:
                        line=line.split()
                        if line[0]=='Package:':
                            app_name=line[1]
                        if line[0]=='ZygotePID:':
                            root_num=int(line[1])
                        if line[0]=='AppPID:':
                            app_id=int(line[1])
                except:
                    print 'Error in ',apk_dir
                    continue                    
            else:
                print 'Cannot find information.out ! ',dirs
                continue
            
                
            if 'strace.out' in files:
                strace_filename=apk_dir+'/strace.out'
            else:
                print 'Cannot find strace.out !', dirs
                continue
            
       
            #print 'converting ', dirs
            g=graph(strace_filename,app_id,app_name,root_num,folder,'nothing',sys_calls_all)
            g.read_strace(sys_calls_all)
            

print sys_calls_all,len(sys_calls_all) 
    
    


