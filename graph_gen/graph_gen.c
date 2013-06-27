#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
int num_graph;
int n_node;


int main(int argc, char *argv[])
{
    int num_graph=atoi(argv[1]);
    int n_node=atoi(argv[2]);
    int n_feat=atoi(argv[3]);
    srand((unsigned)time(NULL));
    for(int graph=1;graph<= num_graph;graph++){
        char file_name[1024];
        char temp[1024];
	    sprintf(temp,"%d",graph);
        strcpy(file_name,"./output/test_");
        strcat(file_name,temp);
        strcat(file_name,".graph");
        FILE *fp = fopen(file_name,"w");
        if(fp ==0)
        {
            printf("error in opening file %s\n",file_name);
            exit(EXIT_FAILURE);
        }
        //fprintf(fp,"%d\n",graph);
        fprintf(fp,"%d %d\n",n_node,n_feat);
        for(int i=0;i<n_node;i++){
            for(int j=0;j<n_feat;j++){
                double rand_num=((double) rand() / (RAND_MAX));
                fprintf(fp,"%lf ",rand_num);
            }
            fprintf(fp,"\n");
        }
        
        for(int i=0;i<n_node;i++){
            for(int j=0;j<n_node;j++){
                if(i==j){ fprintf(fp,"%d ",0); continue;}
                double rand_num=((double) rand() / (RAND_MAX)) ;
                //printf("%lf\n",rand_num);
                //if(rand_num>=0.8)  fprintf(fp,"%d ",1);
                //else fprintf(fp,"%d ",0);
                fprintf(fp,"%d ",1);
            }
            fprintf(fp,"\n");
        }
        fclose(fp);
    }
    return 0;
}
            
         
                    
