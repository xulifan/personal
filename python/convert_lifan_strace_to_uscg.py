import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python ./python_scripts/convert_strace_to_graph_onesyscallpernode_androot.py ./original_data_from_jose/malware ./SCG_malware bad
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
        self.n_fork=0
        self.n_feat=0
        self.sys_calls=systemcalls
        self.n_feat=len(self.sys_calls)
        self.fork_height=[0]
        self.fork_list=[self.pid]
        self.fork_parent=[-1]
        self.last_fork=[]
        self.node_list=[]
        self.feat_mat=[]
        self.node_label=[]
        self.node_pid=[]
        self.parent_node_number=[]
        self.adj_mat=[]
        self.edge_list=[]
        self.filter_contents=[]
        self.uni_pid=[]
        self.uni_pname=[]
    
    def read_strace(self):
        f=open(self.filename,'r')
        contents=f.readlines()
        f.close()
        self.filter_contents=[]
        #print len(contents)

        
        for item in contents:
            if item[0] != '[':
                continue
            if 'unfinished' in item:
                continue
            
            pid=''
            pname=''
            result='1'
            
            if 'resumed>' in item:
                item=item.split()
                pid=item[1][:-1]
                pname=item[4]
                result=item[-1]
            else:
                item=item.split()
                pid=item[1][:-1]
                pname=item[3]
                pname=pname[0:pname.find('(')]
                result=item[-1]
            
            if pname not in self.uni_pname:
                self.uni_pname.append(pname)
            
            self.filter_contents.append(str(pid)+' '+pname+' '+str(result))
        #print uni_pname
        #return filter_contents
        
    def create_fork_list(self):
        n_node=0
        n_item=len(self.filter_contents)
        index=0
        for item in self.filter_contents:
            #print index,n_item,item
            index+=1
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            
            if pid_temp in self.fork_list:
                n_node+=1
            if pname_temp == 'clone' or pname_temp == 'fork':
                result_temp=int(item.split()[2])
                if pid_temp in self.fork_list:
                    if result_temp not in self.fork_list:
                        height=self.fork_height[self.fork_list.index(pid_temp)]
                        self.fork_height.append(height+1)
                        self.fork_list.append(result_temp)
                        self.fork_parent.append(pid_temp)
        self.n_fork=len(self.fork_list)
        self.last_fork=[ -1 for i in range(self.n_fork)]
        self.n_node=n_node+1
        
        #print self.n_node,max(self.fork_height),self.class_label+'_'+self.input_direc+'.linegraph'
        #self.adj_mat=[[0 for i in range(self.n_node)] for j in range(self.n_node)]
        #print self.n_node,self.fork_list
        
    def create_label_and_edgelist(self):
        cur_node=0
        self.node_label.append("root")
        self.parent_node_number.append(cur_node)
        cur_node+=1
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            
            if pid_temp in self.fork_list:
                #print item,cur_node
                self.node_label.append(pname_temp)
                parent_node_number=self.parent_node_number[self.fork_list.index(pid_temp)]
                #print parent_node_number,cur_node,self.n_node,self.n_fork
                #self.adj_mat[parent_node_number][cur_node]=1
                self.edge_list.append([parent_node_number,cur_node])
                if pname_temp == 'clone' or pname_temp == 'fork':
                    result_temp=int(item.split()[2])
                    if pid_temp in self.fork_list and result_temp in self.fork_list:
                        #self.node_label.append("Process_"+str(self.fork_list.index(result_temp)))
                        self.parent_node_number.append(cur_node) 
                        if self.parent_node_number.index(cur_node) != self.fork_list.index(result_temp):
                            print 'Parent node number index error!'
                            sys.exit()
                cur_node+=1
                        
                
        
    
            
    def output_graph_adjmat(self):
        if self.n_node < 2:
            return
        input_direc=self.input_direc
        #print input_direc
        self.output_filename=self.output_direc+self.class_label+'_'+input_direc+'.txt'
        #print 'output file name is ',self.output_filename
        f=open(self.output_filename,'w')
        f.write(str(self.n_node)+' '+'1'+'\n')
        for item in self.node_label:
            f.write(item)
            f.write('\n')
        for item in self.adj_mat:
            f.write(' '.join(str(i) for i in item))
            f.write('\n')
        f.close()
    
    def output_graph_edge(self):
        if self.n_node < 2:
            return
        input_direc=self.input_direc
        #print input_direc
        self.output_filename=self.output_direc+self.class_label+'_'+input_direc+'.linegraph'
        #print 'output file name is ',self.output_filename
        f=open(self.output_filename,'w')
        f.write('t # 1\n')
        for i in range(len(self.node_label)):
            if i==0:
                f.write('v 0 0\n')
            else:
                node_label=self.node_label[i]
                if node_label in self.sys_calls:
                    f.write('v '+str(i)+' '+str(self.sys_calls.index(node_label)+1)+'\n')
                else:
                    f.write('v '+str(i)+' '+str(self.n_feat+1)+'\n')
        for item in self.edge_list:
            start=item[0]
            end=item[1]
            f.write('e '+str(start)+' '+str(end)+ ' 1\n')
        
        f.close()
        
    def output_dot_graph(self):
        input_direc=self.input_direc
        
        dot_graph_name='./test_dot_graph/'+input_direc+'.dot'
        f=open(dot_graph_name,'w')
        f.write('digraph strace {\n')
        f.write('node [style=rounded]\n')
        
        for i in range(self.n_node):
            f.write(str(i)+' [shape=record, label="{'+self.node_label[i])
            f.write('}"]\n')
            
        f.write('\n\n')
        
        for item in self.edge_list:
            start=item[0]
            end=item[1]
            f.write(str(start)+' ->'+str(end)+'\n')
                
        
        f.write('}')
        f.close()   
            




'''
sys_calls=['recvmsg', 'open', 'fork', 'clone', 'access', 'socket', 'connect', 'getsockopt', 'sendto', 'sendmsg', 'stat64', 'pread', 'fstat64', 'statfs64', 'rename', 'chmod', 'lstat64', 'unlink', 'mkdir', 'setsockopt', 'recvfrom', 'socketpair', 'bind', 'pwrite', 'getsockname', 'wait4', 'listen', 'execve', 'shutdown', 'rmdir', 'getcwd', 'ftruncate64', 'utimes', 'readlink', 'chdir', 'accept', 'getpeername', 'symlink', 'syscall_11', 'truncate', 'vfork']
'''
sys_calls=['select', 'ioctl', 'recvmsg', 'recv', 'munmap', 'open', 'pivot_root', 'close', 'sigaction', 'fork', 'mprotect', 'clone', 'syscall_983045', 'prctl', 'SYS_224', 'write', 'setgroups32', 'setgid32', 'fstat64', 'setuid32', 'personality', 'capset', 'setrlimit', 'msgget', 'setpriority', 'getpriority', 'socket', 'pipe', 'getpid', 'connect', 'getsockopt', 'getpgid', 'setpgid', 'sendmsg', 'fcntl64', 'access', 'getuid32', 'ipc_subcall', 'semop', 'semget', 'dup', 'read', 'writev', 'stat64', '_llseek', 'pread', 'gettimeofday', 'mkdir', 'chmod', 'lseek', 'sched_getparam', 'sched_getscheduler', 'syscall_983042', 'sigprocmask', 'getdents64', 'flock', 'nanosleep', 'pwrite', 'fsync', 'unlink', 'ftruncate', 'geteuid32', 'getgid32', 'getegid32', 'socketpair', 'bind', 'rename', 'lstat64', 'setsockopt', 'getsockname', 'rt_sigtimedwait', 'recvfrom', 'poll', 'dup2', 'getrlimit', 'execve', 'wait4', 'uname', 'fchmod', 'msync', 'sched_yield', 'shutdown', 'listen', 'rmdir', 'sigaltstack', 'rt_sigreturn', 'setitimer', 'getpeername', 'msgctl', 'getcwd', 'getgroups32', 'chdir', 'getrusage', 'symlink', 'vfork', 'ftruncate64', 'kill', 'sched_get_priority_min', 'sched_get_priority_max', 'mlock', 'umask', 'fchown32', 'munlock', 'chown32', 'readlink', 'setup', 'setsid', 'getdents', 'fdatasync', 'sendto']


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
            
            for line in lines:
                line=line.split()
                if line[0]=='Package:':
                    app_name=line[1]
                if line[0]=='ZygotePID:':
                    root_num=int(line[1])
                if line[0]=='AppPID:':
                    app_id=int(line[1])
        else:
            print 'Cannot find information.out !'
            continue
        
            
        if 'strace.out' in files:
            strace_filename=apk_dir+'/strace.out'
        else:
            print 'Cannot find strace.out !'
            continue
        

       
   
        #print 'converting ', dirs
        g=graph(strace_filename,app_id,app_name,root_num,output,sys.argv[3],sys_calls)
        g.read_strace()
        #for item in g.uni_pname:
        #    if item not in sys_calls_all:
        #        sys_calls_all.append(item)
        g.create_fork_list()
        g.create_label_and_edgelist()
        g.output_graph_edge()  
        g.output_dot_graph()
#print sys_calls_all,len(sys_calls_all) 
    
    


