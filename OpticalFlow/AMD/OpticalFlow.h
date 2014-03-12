#ifndef CUDALK_H
#define CUDALK_H

#include <CL/cl.h>
#include <sys/time.h>
#include <stdio.h>
#include <string.h>
#define LEVELS 3
#define PATCH_R 6 // patch radius, patch size is (2*PATCH_R+1)*(2*PATCH_R+1)
#define NTHREAD_X 16
#define NTHREAD_Y 16
#define MAX_SOURCE_SIZE (0x100000)

class cudaLK
{
public:
    cudaLK();
    ~cudaLK();
    void run(unsigned char *prev, unsigned char *cur, int w, int h);

    float *dx, *dy;
    char *status;
    int pyr_w[LEVELS], pyr_h[LEVELS];

private:
    void initMem();
	cl_mem initTexture2D(float *h_volume, const size_t volumeSize[2]);
	void cl_load_prog();
	int round_up(int n,int m);

FILE *fp;
char *source_str;
char str_temp[1024];
size_t source_size;

cl_platform_id *platform_id;
cl_device_id device_id;   
cl_uint num_devices;
cl_uint num_platforms;
cl_int errcode;
cl_context clGPUContext;
cl_command_queue clCommandQue;
cl_program clProgram;

cl_kernel clKernel_convert;
cl_kernel clKernel_down;
cl_kernel clKernel_smoothx;
cl_kernel clKernel_smoothy;
cl_kernel clKernel_track;

cl_mem gpu_img_prev_RGB;
cl_mem gpu_img_cur_RGB;
cl_mem gpu_img_pyramid_prev[LEVELS];
cl_mem gpu_img_pyramid_cur[LEVELS];
cl_mem gpu_smoothed_prev_x;
cl_mem gpu_smoothed_cur_x;
cl_mem gpu_smoothed_prev;
cl_mem gpu_smoothed_cur;
cl_mem gpu_dx;
cl_mem gpu_dy;
cl_mem gpu_status;

cl_mem texRef_pyramid_prev;
cl_mem texRef_pyramid_cur;

cl_sampler volumeSamplerLinear;

    int w, h;

    //unsigned char *gpu_img_prev_RGB;
    //unsigned char *gpu_img_cur_RGB;

    //float *gpu_img_pyramid_prev[LEVELS];
    //float *gpu_img_pyramid_cur[LEVELS];
    //float *gpu_smoothed_prev_x;
    //float *gpu_smoothed_cur_x;
    //float *gpu_smoothed_prev;
    //float *gpu_smoothed_cur;

    //cudaArray *gpu_array_pyramid_prev;
    //cudaArray *gpu_array_pyramid_prev_Ix;
    //cudaArray *gpu_array_pyramid_prev_Iy;
    //cudaArray *gpu_array_pyramid_cur;
    //float *gpu_dx, *gpu_dy;
    //char *gpu_status;

    inline int getTimeNow() {
        timeval t;
        gettimeofday(&t, NULL);

        return (t.tv_sec*1000 + t.tv_usec/1000);
    }
};

#endif
