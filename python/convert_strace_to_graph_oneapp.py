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
        self.n_feat=0
        self.sys_calls=systemcalls
        self.n_feat=len(self.sys_calls)
        self.node_list=[self.pid]
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
            if 'unfinished' in item:
                continue
            if 'resumed' in item:
                continue
            if item.find('(')==-1:
                continue
            part1_str=item[0:item.find('(')]
            if len(part1_str)== 0:
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
            #if pname=='fork' and self.root_num==-1:
            #    self.root_num=pid   
            #print pid,pname,result
            if pname not in self.uni_pname:
                self.uni_pname.append(pname)
            
            self.filter_contents.append(str(pid)+' '+pname+' '+str(result))
        #print uni_pname
        #return filter_contents
        
    def create_node_list(self):
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            result_temp=int(item.split()[2])
            
            if pname_temp == 'clone' or pname_temp == 'fork':
                if pid_temp in self.node_list:
                    if result_temp not in self.node_list:
                        self.node_list.append(result_temp)
        self.n_node=len(self.node_list)
        #print self.n_node,self.node_list
        
    def create_feat_mat(self):
        self.feat_mat=[[0 for i in range(self.n_feat)] for i in range(self.n_node)]
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            result_temp=int(item.split()[2])
            
            if pid_temp in self.node_list:
                pid_index=self.node_list.index(pid_temp)
                if pname_temp in self.sys_calls:
                    self.feat_mat[pid_index][self.sys_calls.index(pname_temp)]+=1
                else:
                    print 'ERROR:   '+pname_temp+'      not in the feature vector'
                    #sys.exit(0)
                    continue
                #print pid_temp,pid_index,len(uni_pid)     
            #print pid_temp,pid_index,len(uni_pid) 
            
    def create_adj_mat(self):
        self.adj_mat=[ [0 for j in range(self.n_node)] for i in range(self.n_node)]
        for item in self.filter_contents:
            pid_temp=int(item.split()[0])
            pname_temp=item.split()[1]
            result_temp=int(item.split()[2])
            
            if pid_temp in self.node_list:
                if pname_temp == 'clone' or pname_temp == 'fork':
                    pid_index=self.node_list.index(pid_temp)
                    result_index=self.node_list.index(result_temp)
                    self.adj_mat[pid_index][result_index]=1
                
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
        highest_strace=-1
        
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
                            app_name=line[8]
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
        

       
   
        print 'converting ', dirs
        g=graph(strace_filename,app_id,app_name,root_num,output,sys.argv[3],sys_calls)
        g.read_strace()
        for item in g.uni_pname:
            if item not in sys_calls_all:
                sys_calls_all.append(item)
        g.create_node_list()
        g.create_feat_mat()
        g.create_adj_mat()
        #g.print_feat_mat()
        #g.print_adj_mat()
        #g.output_graph()  
        g.output_dot_graph()
print sys_calls_all,len(sys_calls_all) 
    
    


