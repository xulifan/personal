import os, sys, shutil
from os import listdir
from os.path import isfile, join


class graph:
    def __init__(self,inputfile,outputdirec,label,systemcalls):
        self.filename=inputfile
        self.output_filename=''
        self.class_label=label
        self.output_direc=outputdirec
        self.output_direc=self.output_direc.rstrip('/')+'/'
        self.n_node=0
        self.n_feat=0
        self.root_num=-1
        self.sys_calls=systemcalls
        self.n_feat=len(self.sys_calls)
        self.feat_mat=[]
        self.adj_mat=[]
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
            if 'finished' in item:
                continue
            if 'resumed' in item:
                continue
            if item.find('(')==-1:
                continue
            part1_str=item[0:item.find('(')]
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
            if pname=='fork' and self.root_num==-1:
                self.root_num=pid   
            #print pid,pname,result
            if pname not in self.uni_pname:
                self.uni_pname.append(pname)
            
            self.filter_contents.append(str(pid)+' '+pname+' '+str(result))
        #print uni_pname
        #return filter_contents
        
    def create_feat_mat(self):
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            result_temp=int(item.split()[2])
            
            if pid_temp not in self.uni_pid:
                self.uni_pid.append(pid_temp)
                self.feat_mat.append([0 for i in range(self.n_feat)])
            
            ##
            ##  TODO:
            ##      should the threads make no system call in the graph?
            ##
            if pname_temp == 'clone' or pname_temp == 'fork':
                if result_temp not in self.uni_pid:
                    self.uni_pid.append(result_temp)
                    self.feat_mat.append([0 for i in range(self.n_feat)])
                
            
            pid_index=self.uni_pid.index(pid_temp)
            
            ##
            ##  TODO:
            ##      how about the system calls not in the feature vector
            ##
            
            if pname_temp in self.sys_calls:
                self.feat_mat[pid_index][self.sys_calls.index(pname_temp)]+=1
            else:
                print 'ERROR:   '+pname_temp+'      not in the feature vector'
                sys.exit(0)
            #print pid_temp,pid_index,len(uni_pid) 
            
    def create_adj_mat(self):
        self.n_node=len(self.uni_pid)
        self.adj_mat=[ [0 for j in range(self.n_node)] for i in range(self.n_node)]

        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            result_temp=int(item.split()[2])
            
            if pname_temp == 'clone' or pname_temp == 'fork':
                pid_index=self.uni_pid.index(pid_temp)
                result_index=self.uni_pid.index(result_temp)
                self.adj_mat[pid_index][result_index]=1
                
    def print_feat_mat(self):
        for item in self.feat_mat:
            print item
     
    def print_adj_mat(self):
        for item in self.adj_mat:
            print item,sum(item)
            
    def output_graph(self):
        self.output_filename=self.output_direc+self.class_label+'_'+self.filename[self.filename.rfind('/')+1:]
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






sys_calls=['select', 'ioctl', 'recvmsg', 'recv', 'munmap', 'open', 'pivot_root', 'close', 'sigaction', 'fork', 'mprotect', 'clone', 'getuid32', 'fstat64', 'syscall_983045', 'prctl', 'SYS_224', 'write', 'setgroups32', 'setgid32', 'setuid32', 'personality', 'capset', 'setrlimit', 'msgget', 'getpriority', 'setpriority', 'socket', 'pipe', 'getpid', 'connect', 'getsockopt', 'getpgid', 'setpgid', 'sendmsg', 'fcntl64', 'writev', 'access', 'ipc_subcall', 'semget', 'dup', 'read', 'gettimeofday', 'lseek', 'sched_getparam', 'sched_getscheduler', 'syscall_983042', 'rt_sigtimedwait', 'stat64', '_llseek', 'pread', 'mkdir', 'chmod', 'sigprocmask', 'flock', 'semop', 'setsockopt', 'getdents64', 'bind', 'getsockname', 'recvfrom']


sys_calls_all=[]

input=sys.argv[1]
output=sys.argv[2]
input=input.rstrip('/')
output=output.rstrip('/')
if(os.path.isdir(output)!=True):
    os.mkdir(output,0755)

for dirs in listdir(input):
    if os.path.isfile(input+'/'+dirs) and dirs[-4:]=='.txt':
        print 'converting ', dirs
        g=graph(input+'/'+dirs,output,sys.argv[3],sys_calls)
        g.read_strace()
        for item in g.uni_pname:
            if item not in sys_calls_all:
                sys_calls_all.append(item)
        g.create_feat_mat()
        g.create_adj_mat()
        #g.print_feat_mat()
        #g.print_adj_mat()
        g.output_graph()  
print sys_calls_all,len(sys_calls_all) 
     
    


