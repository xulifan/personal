import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python convert_strace_to_graph_oneapp.py ./original_data_from_DrJose/delaware-benign/all-android-benign-samples-set-14-results/2014.02.11.15.52.10/ ./benign/ good
#

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
        self.dfs_visit=[]
    
    def read_strace(self):
        f=open(self.filename,'r')
        contents=f.readlines()
        f.close()
        self.filter_contents=[]
        #print len(contents)

        
        for item in contents:
            #print item
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
                    #print item
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
                
            except:
                print 'Error in parsing strace log file ',pid,pname,result, sys.exc_info()[0]
                print self.filename
                print original_item
                print contents.index(original_item)
                print 'Quit!'
                sys.exit()
                    
            if pname not in self.uni_pname:
                self.uni_pname.append(pname)
            
            self.filter_contents.append(str(pid)+' '+pname+' '+str(result))
        #print uni_pname
        #return filter_contents
        
    def create_node_list(self):
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            #result_temp=int(item.split()[2])
            
            
            if pname_temp == 'clone' or pname_temp == 'fork':
                if pid_temp in self.node_list:
                    try:
                        result_temp=int(item.split()[2])
                        if result_temp not in self.node_list:
                            height=self.node_height[self.node_list.index(pid_temp)]
                            self.node_height.append(height+1)
                            self.node_list.append(result_temp)
                    except:
                        print 'result error ',pid_temp,pname_temp,result_temp
        self.n_node=len(self.node_list)
        self.height=max(self.node_height)
        #if(self.n_node>1):
        #    print self.n_node,self.height,self.output_direc+self.class_label+'_'+self.input_direc+'.txt'
        
    def create_feat_mat(self):
        self.feat_mat=[[0 for i in range(self.n_feat)] for i in range(self.n_node)]
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            #result_temp=int(item.split()[2])
            
            if pid_temp in self.node_list:
                pid_index=self.node_list.index(pid_temp)
                if pname_temp in self.sys_calls:
                    self.feat_mat[pid_index][self.sys_calls.index(pname_temp)]+=1
                else:
                    #print 'ERROR:   '+pname_temp+'      not in the feature vector'
                    #sys.exit(0)
                    continue
                #print pid_temp,pid_index,len(uni_pid)     
            #print pid_temp,pid_index,len(uni_pid) 
            
    def create_adj_mat(self):
        self.adj_mat=[ [0 for j in range(self.n_node)] for i in range(self.n_node)]
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            #result_temp=int(item.split()[2])
            
            if pid_temp in self.node_list:
                if pname_temp == 'clone' or pname_temp == 'fork':
                    try:
                        result_temp=int(item.split()[2])
                        pid_index=self.node_list.index(pid_temp)
                        result_index=self.node_list.index(result_temp)
                        self.adj_mat[pid_index][result_index]=1
                    except:
                        print 'result error ',pid_temp,pname_temp,result_temp
    
    def normalize_feat_mat(self):
        for i in range(self.n_node):
            row_sum=sum(self.feat_mat[i])
            if row_sum>0:
                for j in range(self.n_feat):
                    self.feat_mat[i][j]=round(float(self.feat_mat[i][j])/row_sum,6)
    
                
    def print_feat_mat(self):
        for item in self.feat_mat:
            print item
     
    def print_adj_mat(self):
        for item in self.adj_mat:
            print item,sum(item)
            
    def output_graph(self):
        if self.n_node < 2:
            return
        input_direc=self.input_direc
        #print input_direc
        self.output_filename=self.output_direc+self.class_label+'_'+input_direc+'.txt'
        #print 'output file name is ',self.output_filename
        f=open(self.output_filename,'w')
        f.write(str(self.n_node)+' '+str(self.n_feat)+'\n')
        for item in self.feat_mat:
            f.write(' '.join(str(i) for i in item))
            f.write('\n')
        for item in self.adj_mat:
            f.write(' '.join(str(i) for i in item))
            f.write('\n')
        f.close()
        
    def output_dot_graph(self):
        input_direc=self.input_direc
        dot_graph_name='./test_dot_graph/'+input_direc+'.dot'
        f=open(dot_graph_name,'w')
        f.write('digraph strace {\n')
        f.write('node [style=rounded]\n')
        
        for i in range(self.n_node):
            node_id=self.node_list[i]
            f.write(str(node_id)+' [shape=record, label="{PID: '+str(node_id)+'|name: '+self.app_name)
            for j in range(self.n_feat):
                if self.feat_mat[i][j] != 0:
                    f.write('|'+self.sys_calls[j]+'('+str(self.feat_mat[i][j])+')')
            f.write('}"]\n')
            
        f.write('\n\n')
            
        for i in range(self.n_node):
            for j in range(self.n_node):
                if self.adj_mat[i][j]!=0:
                    f.write(str(self.node_list[i])+' -> '+str(self.node_list[j])+'\n')
        f.write('}')
        f.close() 

    def output_json(self):
        self.dfs_visit=[0 for i in range(self.n_node)]
        
        input_direc=self.input_direc
        
        json_name='./test_json/'+input_direc+'.json'
        f=open(json_name,'w')
        indent=0
        #self.dfs_fv(0,indent,f)
        self.dfs_extra_hist(0,indent,f)
        f.close()
        
    def dfs_extra_hist(self,node_id,indent,f):
        self.dfs_visit[node_id]=1
        for i in range(indent):
            f.write(' ')
        f.write('{\n')
        
        for i in range(indent+2):
            f.write(' ')
        f.write("\"name\": \"")
        f.write(str(node_id))
        f.write("\",\n")
        
        for i in range(indent+2):
            f.write(' ')
        f.write("\"size\": \"")
        #f.write(str(sum(self.feat_mat[node_id])))
        f.write("1")
        f.write("\"")
        
        if sum(self.adj_mat[node_id]) !=0 or sum(self.feat_mat[node_id])!= 0:
            f.write(",\n")
            for i in range(indent+2):
                f.write(' ')
            f.write("\"children\": [\n")
        else:
            f.write("\n")
            
        
        first_child=1
        
        for i in range(self.n_node):
            if self.adj_mat[node_id][i]!= 0 and self.dfs_visit[i] == 0:
                if first_child==0:
                    for j in range(indent+2):
                        f.write(' ')
                    f.write(",\n")
                self.dfs_extra_hist(i,indent+2,f)
                first_child=0
        if first_child==0:
            for j in range(indent+2):
                f.write(' ')
            f.write(",\n")
        
        first_child=1
        if sum(self.feat_mat[node_id])!= 0:        
            #write the histogram node
            for i in range(indent+2):
                f.write(' ')
            f.write('{\n')
            
            for i in range(indent+4):
                f.write(' ')
            f.write("\"name\": \"")
            f.write("histogram")
            f.write("\",\n")
            
            for i in range(indent+4):
                f.write(' ')
            f.write("\"size\": \"")
            #f.write(str(sum(self.feat_mat[node_id])))
            f.write("1")
            f.write("\"")
            
            f.write(",\n")
            for i in range(indent+4):
                f.write(' ')
            f.write("\"children\": [\n")
            
            for i in range(self.n_feat):
                if self.feat_mat[node_id][i]!= 0:
                    if first_child==0:
                        f.write(",\n")
                    for j in range(indent+4):
                            f.write(' ')
                    f.write("{\"name\" : \""+self.sys_calls[i]+" "+str(self.feat_mat[node_id][i])+"\", \"size\" : "+str(self.feat_mat[node_id][i])+" }")
                    first_child=0
            f.write("\n")
            for i in range(indent+4):
                f.write(' ')
            f.write("]\n")
            
            for i in range(indent+2):
                f.write(' ')
            f.write('}\n')
            
            
        
                
        self.dfs_visit[node_id]=2   
        
        if sum(self.adj_mat[node_id]) !=0 or sum(self.feat_mat[node_id])!= 0:
            for i in range(indent+2):
                f.write(' ')
            f.write("]\n")
            
        for i in range(indent):
            f.write(' ')
        f.write('}\n') 
        

    def dfs_fv(self,node_id,indent,f):
        self.dfs_visit[node_id]=1
        for i in range(indent):
            f.write(' ')
        f.write('{\n')
        
        for i in range(indent+2):
            f.write(' ')
        f.write("\"name\": \"")
        f.write(str(node_id))
        f.write("\",\n")
        
        for i in range(indent+2):
            f.write(' ')
        f.write("\"size\": \"")
        #f.write(str(sum(self.feat_mat[node_id])))
        f.write("10")
        f.write("\",\n")
        
        for j in range(self.n_feat):
            for i in range(indent+2):
                f.write(' ')
            f.write("\""+self.sys_calls[j]+"\": \"")
            f.write(str(self.feat_mat[node_id][j]))
            if j==self.n_feat-1:
                f.write("\"\n")
            else:
                f.write("\",\n")
                    
        if sum(self.adj_mat[node_id]) !=0:
            f.write(",\n")
            for i in range(indent+2):
                f.write(' ')
            f.write("\"children\": [\n")
        else:
            f.write("\n")
        
        first_child=1
        
        for i in range(self.n_node):
            if self.adj_mat[node_id][i]!= 0 and self.dfs_visit[i] == 0:
                if first_child==0:
                    for j in range(indent+2):
                        f.write(' ')
                    f.write(",\n")
                self.dfs_fv(i,indent+2,f)
                first_child=0
                
        self.dfs_visit[node_id]=2   
        
        if sum(self.adj_mat[node_id]) !=0:
            for i in range(indent+2):
                f.write(' ')
            f.write("]\n")
            
        for i in range(indent):
            f.write(' ')
        f.write('}\n')
        
        
        

    def dfs(self,node_id,indent,f):
        self.dfs_visit[node_id]=1
        for i in range(indent):
            f.write(' ')
        f.write('{\n')
        
        for i in range(indent+2):
            f.write(' ')
        f.write("\"name\": \"")
        f.write(str(node_id))
        f.write("\",\n")
        
        for i in range(indent+2):
            f.write(' ')
        f.write("\"size\": \"")
        f.write(str(sum(self.feat_mat[node_id])))
        f.write("\"")
        
        if sum(self.adj_mat[node_id]) !=0:
            f.write(",\n")
            for i in range(indent+2):
                f.write(' ')
            f.write("\"children\": [\n")
        else:
            f.write("\n")
            
        
        first_child=1
        
        for i in range(self.n_node):
            if self.adj_mat[node_id][i]!= 0 and self.dfs_visit[i] == 0:
                if first_child==0:
                    for j in range(indent+2):
                        f.write(' ')
                    f.write(",\n")
                self.dfs(i,indent+2,f)
                first_child=0
                
        self.dfs_visit[node_id]=2   
        
        if sum(self.adj_mat[node_id]) !=0:
            for i in range(indent+2):
                f.write(' ')
            f.write("]\n")
            
        for i in range(indent):
            f.write(' ')
        f.write('}\n')       
        
        
        



'''
#110f
sys_calls=['select', 'ioctl', 'recvmsg', 'recv', 'munmap', 'open', 'pivot_root', 'close', 'sigaction', 'fork', 'mprotect', 'clone', 'syscall_983045', 'prctl', 'SYS_224', 'write', 'setgroups32', 'setgid32', 'fstat64', 'setuid32', 'personality', 'capset', 'setrlimit', 'msgget', 'setpriority', 'getpriority', 'socket', 'pipe', 'getpid', 'connect', 'getsockopt', 'getpgid', 'setpgid', 'sendmsg', 'fcntl64', 'access', 'getuid32', 'ipc_subcall', 'semop', 'semget', 'dup', 'read', 'writev', 'stat64', '_llseek', 'pread', 'gettimeofday', 'mkdir', 'chmod', 'lseek', 'sched_getparam', 'sched_getscheduler', 'syscall_983042', 'sigprocmask', 'getdents64', 'flock', 'nanosleep', 'pwrite', 'fsync', 'unlink', 'ftruncate', 'geteuid32', 'getgid32', 'getegid32', 'socketpair', 'bind', 'rename', 'lstat64', 'setsockopt', 'getsockname', 'rt_sigtimedwait', 'recvfrom', 'poll', 'dup2', 'getrlimit', 'execve', 'wait4', 'uname', 'fchmod', 'msync', 'sched_yield', 'shutdown', 'listen', 'rmdir', 'sigaltstack', 'rt_sigreturn', 'setitimer', 'getpeername', 'msgctl', 'getcwd', 'getgroups32', 'chdir', 'getrusage', 'symlink', 'vfork', 'ftruncate64', 'kill', 'sched_get_priority_min', 'sched_get_priority_max', 'mlock', 'umask', 'fchown32', 'munlock', 'chown32', 'readlink', 'setup', 'setsid', 'getdents', 'fdatasync', 'sendto','getppid','mknod','rt_sigaction','fcntl','syscall_359','fchdir','sync','sched_setscheduler']
'''

'''
#143f
sys_calls=['select', 'ioctl', 'recvmsg', 'futex', 'munmap', 'sigprocmask', '_exit', 'open', 'getdents64', 'mmap2', 'madvise', 'mprotect', 'clone', 'set_thread_area', 'prctl', 'gettid', 'getuid32', 'mkdir', 'unshare', 'lstat64', 'chmod', 'chown32', 'mount', 'setgroups32', 'setgid32', 'setuid32', 'personality', 'capset', 'access', 'sched_setscheduler', 'setrlimit', 'sigaction', 'clock_gettime', 'getpgid', 'setpgid', 'sendmsg', 'socket', 'pipe', 'getpid', 'connect', 'getsockopt', 'sendto', 'close', 'fcntl64', 'epoll_create', 'epoll_ctl', 'gettimeofday', 'epoll_wait', 'setpriority', 'getpriority', 'read', 'write', 'stat64', '_llseek', 'pread64', 'lseek', 'flock', 'fstat64', 'nanosleep', 'writev', 'brk', 'sched_yield', 'statfs64', 'unlink', 'umask', 'fchown32', 'pwrite64', 'fdatasync', 'geteuid32', 'getgid32', 'getegid32', 'socketpair', 'bind', 'recvfrom', 'fsync', 'rename', 'setsockopt', 'getsockname', 'poll', 'dup', 'ftruncate', 'rt_sigaction', 'rt_sigprocmask', 'get_thread_area', 'sigaltstack', 'getuid', 'fork', 'dup2', 'getrlimit', 'execve', 'exit_group', 'wait4', 'restart_syscall', 'ftruncate64', 'utimes', 'getpeername', 'sigreturn', 'fchmod', 'msync', 'rmdir', 'uname', 'clock_getres', 'readlink', 'tkill', 'sigsuspend', 'rt_sigreturn', 'sched_getparam', 'sched_getscheduler', 'sched_get_priority_min', 'sched_get_priority_max', 'shutdown', 'kill', 'listen', 'setitimer', 'accept', 'symlink', 'getcwd', 'getgroups32', 'getppid', 'setresgid32', 'setresuid32', 'inotify_init', 'inotify_add_watch', 'rt_sigtimedwait', 'tgkill', 'inotify_rm_watch', 'getrusage', 'sched_getaffinity', 'sched_setaffinity', 'chdir', 'mlock', 'munlock', 'setsid', 'vfork', 'fstatfs64', 'sync', 'old_mmap', 'ptrace', 'times', 'mknod', 'pipe2', 'timer_create', 'truncate']
'''

#23f
sys_calls=['munmap', 'madvise', 'fcntl64', 'getuid32', 'mprotect', 'mmap2', 'epoll_wait', 'sendto', 'getpid', 'recvfrom', 'gettid', 'write', 'ioctl', 'close', 'wait4', 'sched_yield', 'read', 'clock_gettime', 'futex', 'gettimeofday', 'lseek', 'sigprocmask', 'access']


sys_calls_all=[]

input=sys.argv[1]
output=sys.argv[2]
input=input.rstrip('/')
output=output.rstrip('/')
if(os.path.isdir(output)!=True):
    os.mkdir(output,0755)

for dirs in listdir(input):
    #print dirs
    apk_dir=input+'/'+dirs
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
            print 'Cannot find strace.out !'
            continue
        
   
        print 'converting ', dirs
        g=graph(strace_filename,app_id,app_name,root_num,output,sys.argv[3],sys_calls)
        g.read_strace()
        #for item in g.uni_pname:
        #    if item not in sys_calls_all:
        #        sys_calls_all.append(item)
        g.create_node_list()
        #
        #   need to run this function agian just in case the fork return get delayed by 'resumed'
        #
        g.create_node_list()
        g.create_feat_mat()
        #g.normalize_feat_mat()
        g.create_adj_mat()
        #g.print_feat_mat()
        #g.print_adj_mat()
        #g.output_graph()  
        #g.output_dot_graph()
        g.output_json()

    
    


