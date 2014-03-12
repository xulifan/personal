//#include "OpticalFlow.h"
//#include <stdio.h>

const float scaling[] = {1, 0.5f, 0.25f, 0.125f, 0.0625f, 0.03125f, 0.015625f, 0.0078125f};

cudaLK::cudaLK()
{
	// Load the kernel source code into the array source_str
	fp = fopen("cudaLK.cl", "r");
	if (!fp) {
		fprintf(stderr, "Failed to load kernel.\n");
		exit(1);
	}
	source_str = (char*)malloc(MAX_SOURCE_SIZE);
	source_size = fread( source_str, 1, MAX_SOURCE_SIZE, fp);
	fclose( fp );

	// Get platform and device information
	errcode = clGetPlatformIDs(0, NULL, &num_platforms);
	if(errcode == CL_SUCCESS) printf("number of platforms is %d\n",num_platforms);

	
	if (0 < num_platforms) 
	{
		platform_id = new cl_platform_id[num_platforms];
		errcode = clGetPlatformIDs(num_platforms, platform_id, NULL);
		if(errcode != CL_SUCCESS) printf("error in getting platform id\n");

		for (unsigned i = 0; i < num_platforms; ++i) 
		{

			errcode = clGetPlatformInfo(platform_id[i],CL_PLATFORM_VENDOR,sizeof(str_temp), str_temp, NULL);

			if(errcode != CL_SUCCESS) printf("error in getting platform name\n");
			if(errcode == CL_SUCCESS) printf("platform %d vendor is %s\n",i,str_temp);
			


			if (strcmp(str_temp, "NVIDIA Corporation")!=0) 
			  {
			    printf("Platform is not NVIDIA, check next platform\n");
			  }
			else{
			  errcode = clGetPlatformInfo(platform_id[i],CL_PLATFORM_NAME, sizeof(str_temp), str_temp,NULL);
			  if(errcode == CL_SUCCESS) printf("platform %d name is %s\n",i,str_temp);
			  errcode = clGetDeviceIDs( platform_id[i], CL_DEVICE_TYPE_GPU, 1, &device_id, &num_devices);
			  if(errcode == CL_SUCCESS) printf("device id is %d\n",device_id);
			}
		}


        delete[] platform_id;
	}

	errcode = clGetDeviceInfo(device_id,CL_DEVICE_NAME, sizeof(str_temp), str_temp,NULL);
	if(errcode == CL_SUCCESS) printf("device name is %s\n",str_temp);
	
	// Create an OpenCL context
	clGPUContext = clCreateContext( NULL, 1, &device_id, NULL, NULL, &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating context\n");
 
	//Create a command-queue
	clCommandQue = clCreateCommandQueue(clGPUContext, device_id, 0, &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating command queue\n");

	// Create a program from the kernel source
	clProgram = clCreateProgramWithSource(clGPUContext, 1, (const char **)&source_str, (const size_t *)&source_size, &errcode);

	if(errcode != CL_SUCCESS) printf("Error in creating program\n");

	// Build the program
	errcode = clBuildProgram(clProgram, 1, &device_id, NULL, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in building program\n");
		
	// Create the OpenCL kernel
	clKernel_convert = clCreateKernel(clProgram, "convertToGrey", &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating kernel\n");
	// Create the OpenCL kernel
	clKernel_down = clCreateKernel(clProgram, "pyrDownsample", &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating kernel\n");
	// Create the OpenCL kernel
	clKernel_smoothx = clCreateKernel(clProgram, "smoothX", &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating kernel\n");
	// Create the OpenCL kernel
	clKernel_smoothy = clCreateKernel(clProgram, "smoothY", &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating kernel\n");
	// Create the OpenCL kernel
	clKernel_track = clCreateKernel(clProgram, "track", &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating kernel\n");
	
}

cudaLK::~cudaLK()
{

	errcode = clFlush(clCommandQue);
	errcode = clFinish(clCommandQue);
	errcode = clReleaseKernel(clKernel_convert);
	errcode = clReleaseKernel(clKernel_down);
	errcode = clReleaseKernel(clKernel_smoothx);
	errcode = clReleaseKernel(clKernel_smoothy);
	errcode = clReleaseKernel(clKernel_track);
	errcode = clReleaseProgram(clProgram);
	errcode = clReleaseCommandQueue(clCommandQue);
	errcode = clReleaseContext(clGPUContext);
	

    for(int i=0; i < LEVELS; i++) {
	errcode = clReleaseMemObject(gpu_img_pyramid_prev[i]);
	errcode = clReleaseMemObject(gpu_img_pyramid_cur[i]);
    }

	errcode = clReleaseMemObject(gpu_smoothed_prev_x);
	errcode = clReleaseMemObject(gpu_smoothed_cur_x);
	errcode = clReleaseMemObject(gpu_smoothed_prev);
	errcode = clReleaseMemObject(gpu_smoothed_cur);

	errcode = clReleaseMemObject(gpu_dx);
	errcode = clReleaseMemObject(gpu_dy);
	errcode = clReleaseMemObject(gpu_status);
	if(errcode != CL_SUCCESS) printf("Error in cleanup\n");
    delete [] dx;
    delete [] dy;
    delete [] status;
}

cl_mem cudaLK::initTexture2D(float *h_volume, const size_t volumeSize[2])
{
    cl_int ciErrNum;

    // create 3D array and copy data to device
    cl_image_format volume_format;
    volume_format.image_channel_order = CL_RGBA;
    volume_format.image_channel_data_type = CL_FLOAT;
	float* h_tempVolume =(float*)malloc(sizeof(float)*volumeSize[0] * volumeSize[1] * 4);
	for(int i = 0; i<(volumeSize[0] * volumeSize[1]); i++)
    {
	h_tempVolume[4 * i] = h_volume[i];
    }
	
    cl_mem d_volume = clCreateImage2D(clGPUContext, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, &volume_format, volumeSize[0], volumeSize[1],0,h_tempVolume, &ciErrNum);
    if(ciErrNum != CL_SUCCESS) printf("Error in initializing image %d\n",ciErrNum);
    free (h_tempVolume);
    return d_volume;
}

void cudaLK::initMem()
{

	gpu_img_prev_RGB = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(char)*w*h*3, NULL, &errcode);
	gpu_img_cur_RGB = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(char)*w*h*3, NULL, &errcode);
	gpu_img_pyramid_prev[0] = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
	gpu_img_pyramid_cur[0] = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
    //cudaMalloc((void**)&gpu_img_prev_RGB, sizeof(char)*w*h*3);
    //cudaMalloc((void**)&gpu_img_cur_RGB, sizeof(char)*w*h*3);
    //cudaMalloc((void**)&gpu_img_pyramid_prev[0], sizeof(float)*w*h);
    //cudaMalloc((void**)&gpu_img_pyramid_cur[0], sizeof(float)*w*h);

	gpu_smoothed_prev_x = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
	gpu_smoothed_cur_x = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
	gpu_smoothed_prev = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
	gpu_smoothed_cur = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
    //cudaMalloc((void**)&gpu_smoothed_prev_x, sizeof(float)*w*h);
    //cudaMalloc((void**)&gpu_smoothed_cur_x, sizeof(float)*w*h);
    //cudaMalloc((void**)&gpu_smoothed_prev, sizeof(float)*w*h);
    //cudaMalloc((void**)&gpu_smoothed_cur, sizeof(float)*w*h);
	
	volumeSamplerLinear = clCreateSampler(clGPUContext, CL_FALSE, CL_ADDRESS_CLAMP, CL_FILTER_LINEAR, &errcode);

    // Texture
    //cudaMallocArray(&gpu_array_pyramid_prev, &texRef_pyramid_prev.channelDesc, w, h);
    //cudaMallocArray(&gpu_array_pyramid_cur, &texRef_pyramid_cur.channelDesc, w, h);
    //cudaBindTextureToArray(texRef_pyramid_prev, gpu_array_pyramid_prev);
    //cudaBindTextureToArray(texRef_pyramid_cur, gpu_array_pyramid_cur);

    //texRef_pyramid_prev.normalized = 0;
    //texRef_pyramid_prev.filterMode = cudaFilterModeLinear;
    //texRef_pyramid_prev.addressMode[0] = cudaAddressModeClamp;
    //texRef_pyramid_prev.addressMode[1] = cudaAddressModeClamp;

    //texRef_pyramid_cur.normalized = 0;
    //texRef_pyramid_cur.filterMode = cudaFilterModeLinear;
    //texRef_pyramid_cur.addressMode[0] = cudaAddressModeClamp;
    //texRef_pyramid_cur.addressMode[1] = cudaAddressModeClamp;
	
	gpu_dx = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
	gpu_dy = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*w*h, NULL, &errcode);
	gpu_status = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(char)*w*h, NULL, &errcode);

    //cudaMalloc((void**)&gpu_dx, sizeof(float)*w*h);
    //cudaMalloc((void**)&gpu_dy, sizeof(float)*w*h);
    //cudaMalloc((void**)&gpu_status, sizeof(char)*w*h);

    int _w = w;
    int _h = h;

    dx = new float[w*h];
    dy = new float[w*h];
    status = new char[w*h];

    pyr_w[0] = w;
    pyr_h[0] = h;

    for(int i=1; i < LEVELS; i++) {
        _w /= 2;
        _h /= 2;
        pyr_w[i] = _w;
        pyr_h[i] = _h;

	gpu_img_pyramid_prev[i] = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*_w*_h, NULL, &errcode);
	gpu_img_pyramid_cur[i] = clCreateBuffer(clGPUContext, CL_MEM_READ_WRITE, sizeof(float)*_w*_h, NULL, &errcode);
        
	//cudaMalloc((void**)&gpu_img_pyramid_prev[i], sizeof(float)*_w*_h);
        //cudaMalloc((void**)&gpu_img_pyramid_cur[i], sizeof(float)*_w*_h);
    }
}

void cudaLK::cl_load_prog()
{
	// Create a program from the kernel source
	clProgram = clCreateProgramWithSource(clGPUContext, 1, (const char **)&source_str, (const size_t *)&source_size, &errcode);

	if(errcode != CL_SUCCESS) printf("Error in creating program\n");

	// Build the program
	errcode = clBuildProgram(clProgram, 1, &device_id, NULL, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in building program\n");
		
	// Create the OpenCL kernel
	clKernel_convert = clCreateKernel(clProgram, "convertToGrey", &errcode);
	clKernel_down = clCreateKernel(clProgram, "pyrDownsample", &errcode);
	clKernel_smoothx = clCreateKernel(clProgram, "smoothX", &errcode);
	clKernel_smoothy = clCreateKernel(clProgram, "smoothY", &errcode);
	clKernel_track = clCreateKernel(clProgram, "track", &errcode);
	if(errcode != CL_SUCCESS) printf("Error in creating kernel\n");
}

int cudaLK::round_up(int n,int m)
{
	int temp = n;
	if(m == 0)
	{
		printf("Error in rounding up!");
		exit(1);
	}
	if(temp % m !=0) temp++;
	return temp;
}

void cudaLK::run(unsigned char *prev, unsigned char *cur, int _w, int _h)
{;
    w = _w;
    h = _h;
    initMem();

    int nThreadsX = NTHREAD_X;
    int nThreadsY = NTHREAD_Y;

    int blocksW = w/nThreadsX + ((w % nThreadsX)?1:0);
    int blocksH = h/nThreadsY + ((h % nThreadsY )?1:0);
    
	size_t localWorkSize[2], globalWorkSize[2];
	localWorkSize[0] = nThreadsX;
	localWorkSize[1] = nThreadsY;
	globalWorkSize[0] = round_up(w,nThreadsX);
	globalWorkSize[1] = round_up(h,nThreadsY);

    //dim3 blocks(blocksW, blocksH);
    //dim3 threads(nThreadsX, nThreadsY);

	int globalsizetemp=round_up(w*h,256);
	size_t globalItemSize= globalsizetemp;
	size_t localitemSize= 64;
    //int blocks1D = (w*h)/256 + (w*h % 256?1:0); // for greyscale

	  
    int start = getTimeNow();
    int s;

    // Copy image to GPU 
    s = getTimeNow();

	errcode = clEnqueueWriteBuffer(clCommandQue, gpu_img_prev_RGB, CL_TRUE, 0, w*h*3*sizeof(char), prev, 0, NULL, NULL);
	errcode = clEnqueueWriteBuffer(clCommandQue, gpu_img_cur_RGB, CL_TRUE, 0, w*h*3*sizeof(char), cur, 0, NULL, NULL);
	if(errcode != CL_SUCCESS)printf("Error in writing buffers\n");
    //cudaMemcpy(gpu_img_prev_RGB, prev, w*h*3, cudaMemcpyHostToDevice);  
    //cudaMemcpy(gpu_img_cur_RGB, cur, w*h*3, cudaMemcpyHostToDevice);  
    //checkCUDAError("start");

    printf("Copying 2 images from CPU to GPU: %d ms\n", getTimeNow() - s);

    // RGB -> grey
    s = getTimeNow();
	int image_size = w*h;
	// Set the arguments of the kernel
	errcode =  clSetKernelArg(clKernel_convert, 0, sizeof(cl_mem), (void *)&gpu_img_prev_RGB);
	errcode |= clSetKernelArg(clKernel_convert, 1, sizeof(cl_mem), (void *)&gpu_img_pyramid_prev[0]);
	errcode |= clSetKernelArg(clKernel_convert, 2, sizeof(int), (void *)&image_size);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments convert1\n");
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_convert, 1, NULL, &globalItemSize, &localitemSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernelconvert1\n");
	clEnqueueBarrier(clCommandQue);

	errcode =  clSetKernelArg(clKernel_convert, 0, sizeof(cl_mem), (void *)&gpu_img_cur_RGB);
	errcode |= clSetKernelArg(clKernel_convert, 1, sizeof(cl_mem), (void *)&gpu_img_pyramid_cur[0]);
	errcode |= clSetKernelArg(clKernel_convert, 2, sizeof(int), (void *)&image_size);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments convert2\n");
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_convert, 1, NULL, &globalItemSize, &localitemSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel convert2\n");
	clEnqueueBarrier(clCommandQue);

    //convertToGrey<<<blocks1D, 256>>>(gpu_img_prev_RGB, gpu_img_pyramid_prev[0], w*h);
    //convertToGrey<<<blocks1D, 256>>>(gpu_img_cur_RGB, gpu_img_pyramid_cur[0], w*h);
    //cudaThreadSynchronize();
    //checkCUDAError("convertToGrey");
    printf("Converting from RGB to greyscale: %d ms\n", getTimeNow() - s);

  
    s = getTimeNow();

    for(int i=0; i < LEVELS-1; i++) {

	errcode =  clSetKernelArg(clKernel_smoothx, 0, sizeof(cl_mem), (void *)&gpu_img_pyramid_prev[i]);
	errcode |= clSetKernelArg(clKernel_smoothx, 1, sizeof(int), (void *)&pyr_w[i]);
	errcode |= clSetKernelArg(clKernel_smoothx, 2, sizeof(int), (void *)&pyr_h[i]);
	errcode |= clSetKernelArg(clKernel_smoothx, 3, sizeof(cl_mem), (void *)&gpu_smoothed_prev_x);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments smoothx1 %d\n",i);
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_smoothx, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel smoothx1 %d\n",i);
	clEnqueueBarrier(clCommandQue);

	errcode =  clSetKernelArg(clKernel_smoothx, 0, sizeof(cl_mem), (void *)&gpu_img_pyramid_cur[i]);
	errcode |= clSetKernelArg(clKernel_smoothx, 1, sizeof(int), (void *)&pyr_w[i]);
	errcode |= clSetKernelArg(clKernel_smoothx, 2, sizeof(int), (void *)&pyr_h[i]);
	errcode |= clSetKernelArg(clKernel_smoothx, 3, sizeof(cl_mem), (void *)&gpu_smoothed_cur_x);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments smoothx2 %d\n",i);
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_smoothx, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel smoothx2 %d\n",i);
	clEnqueueBarrier(clCommandQue);

	errcode =  clSetKernelArg(clKernel_smoothy, 0, sizeof(cl_mem), (void *)&gpu_smoothed_prev_x);
	errcode |= clSetKernelArg(clKernel_smoothy, 1, sizeof(int), (void *)&pyr_w[i]);
	errcode |= clSetKernelArg(clKernel_smoothy, 2, sizeof(int), (void *)&pyr_h[i]);
	errcode |= clSetKernelArg(clKernel_smoothy, 3, sizeof(cl_mem), (void *)&gpu_smoothed_prev);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments smoothy1 %d\n",i);
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_smoothy, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel smoothy1 %d\n",i);
	clEnqueueBarrier(clCommandQue);

	errcode =  clSetKernelArg(clKernel_smoothy, 0, sizeof(cl_mem), (void *)&gpu_smoothed_cur_x);
	errcode |= clSetKernelArg(clKernel_smoothy, 1, sizeof(int), (void *)&pyr_w[i]);
	errcode |= clSetKernelArg(clKernel_smoothy, 2, sizeof(int), (void *)&pyr_h[i]);
	errcode |= clSetKernelArg(clKernel_smoothy, 3, sizeof(cl_mem), (void *)&gpu_smoothed_cur);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments smoothy2 %d\n",i);
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_smoothy, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel smoothy2 %d\n",i);
	clEnqueueBarrier(clCommandQue);

	

        //smoothX<<<blocks, threads>>>(gpu_img_pyramid_prev[i], pyr_w[i], pyr_h[i], gpu_smoothed_prev_x);
        //smoothX<<<blocks, threads>>>(gpu_img_pyramid_cur[i], pyr_w[i], pyr_h[i], gpu_smoothed_cur_x);
        //cudaThreadSynchronize();
        //smoothY<<<blocks, threads>>>(gpu_smoothed_prev_x, pyr_w[i], pyr_h[i], gpu_smoothed_prev);
        //smoothY<<<blocks, threads>>>(gpu_smoothed_cur_x, pyr_w[i], pyr_h[i], gpu_smoothed_cur);
        //cudaThreadSynchronize();


	errcode =  clSetKernelArg(clKernel_down, 0, sizeof(cl_mem), (void *)&gpu_smoothed_prev);
	errcode |= clSetKernelArg(clKernel_down, 1, sizeof(int), (void *)&pyr_w[i]);
	errcode |= clSetKernelArg(clKernel_down, 2, sizeof(int), (void *)&pyr_h[i]);
	errcode |= clSetKernelArg(clKernel_down, 3, sizeof(cl_mem), (void *)&gpu_img_pyramid_prev[i+1]);
	errcode |= clSetKernelArg(clKernel_down, 4, sizeof(int), (void *)&pyr_w[i+1]);
	errcode |= clSetKernelArg(clKernel_down, 5, sizeof(int), (void *)&pyr_h[i+1]);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments down1 %d\n",i);
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_down, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel down1 %d\n",i);
	clEnqueueBarrier(clCommandQue);

	errcode =  clSetKernelArg(clKernel_down, 0, sizeof(cl_mem), (void *)&gpu_smoothed_cur);
	errcode |= clSetKernelArg(clKernel_down, 1, sizeof(int), (void *)&pyr_w[i]);
	errcode |= clSetKernelArg(clKernel_down, 2, sizeof(int), (void *)&pyr_h[i]);
	errcode |= clSetKernelArg(clKernel_down, 3, sizeof(cl_mem), (void *)&gpu_img_pyramid_cur[i+1]);
	errcode |= clSetKernelArg(clKernel_down, 4, sizeof(int), (void *)&pyr_w[i+1]);
	errcode |= clSetKernelArg(clKernel_down, 5, sizeof(int), (void *)&pyr_h[i+1]);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments down2 %d\n",i);
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_down, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel down2 %d\n",i);
	clEnqueueBarrier(clCommandQue);

        //pyrDownsample<<<blocks, threads>>>(gpu_smoothed_prev, pyr_w[i], pyr_h[i], gpu_img_pyramid_prev[i+1], pyr_w[i+1], pyr_h[i+1]);
        //pyrDownsample<<<blocks, threads>>>(gpu_smoothed_cur,  pyr_w[i], pyr_h[i], gpu_img_pyramid_cur[i+1],  pyr_w[i+1], pyr_h[i+1]);
        //cudaThreadSynchronize();

        //checkCUDAError("pyrDownsample here");  
    }

    printf("Generating the pyramids: %d ms\n", getTimeNow() - s);

    s = getTimeNow();
    //cudaMemset(gpu_status, 1, sizeof(char)*w*h);
	char *gpu_status_cpu=(char *)malloc(sizeof(char)*w*h);
	for(int i = 0 ; i < w*h;i++) gpu_status_cpu[i] = 1;
	errcode = clEnqueueWriteBuffer(clCommandQue, gpu_status, CL_TRUE, 0, w*h*sizeof(char), gpu_status_cpu, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in writing gpu_status\n");
	
    // Do the actual tracking
    for(int l=LEVELS-1; l >= 0; l--) {
	size_t volumeSize[] = {pyr_w[l], pyr_h[l]};
	float *temp = (float *)malloc(sizeof(float)*pyr_w[l]*pyr_h[l]);
	errcode = clEnqueueReadBuffer(clCommandQue, gpu_img_pyramid_prev[l], CL_TRUE, 0, sizeof(float)*pyr_w[l]*pyr_h[l], temp, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in reading gpu_img_pyramid_prev %d\n",l);
	texRef_pyramid_prev = initTexture2D(temp,volumeSize);
	
	errcode = clEnqueueReadBuffer(clCommandQue, gpu_img_pyramid_cur[l], CL_TRUE, 0, sizeof(float)*pyr_w[l]*pyr_h[l], temp, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in reading gpu_img_pyramid_cur %d\n",l);
	
	texRef_pyramid_cur = initTexture2D(temp,volumeSize);
	free(temp);
	//cudaMemcpy2DToArray(gpu_array_pyramid_prev, 0, 0, gpu_img_pyramid_prev[l], 
        //                    sizeof(float)*pyr_w[l], sizeof(float)*pyr_w[l], pyr_h[l], cudaMemcpyDeviceToDevice);

        //cudaMemcpy2DToArray(gpu_array_pyramid_cur, 0, 0, gpu_img_pyramid_cur[l], 
        //                    sizeof(float)*pyr_w[l], sizeof(float)*pyr_w[l], pyr_h[l], cudaMemcpyDeviceToDevice);
	

	char initGuess = (l == LEVELS-1);
	int l_temp = l;
	errcode =  clSetKernelArg(clKernel_track, 0, sizeof(int), (void *)&w);
	errcode |= clSetKernelArg(clKernel_track, 1, sizeof(int), (void *)&h);
	errcode |= clSetKernelArg(clKernel_track, 2, sizeof(int), (void *)&pyr_w[l]);
	errcode |= clSetKernelArg(clKernel_track, 3, sizeof(int), (void *)&pyr_h[l]); // pyr_w or pyr_h??????????????
	errcode |= clSetKernelArg(clKernel_track, 4, sizeof(float), (void *)&scaling[l]);
	errcode |= clSetKernelArg(clKernel_track, 5, sizeof(int), (void *)&l_temp);
	errcode |= clSetKernelArg(clKernel_track, 6, sizeof(char), (void *)&initGuess);
	errcode |= clSetKernelArg(clKernel_track, 7, sizeof(cl_mem), (void *)&gpu_dx);
	errcode |= clSetKernelArg(clKernel_track, 8, sizeof(cl_mem), (void *)&gpu_dy);
	errcode |= clSetKernelArg(clKernel_track, 9, sizeof(cl_mem), (void *)&gpu_status);
	errcode |= clSetKernelArg(clKernel_track, 10, sizeof(cl_mem), (void *)&texRef_pyramid_prev);
	errcode |= clSetKernelArg(clKernel_track, 11, sizeof(cl_mem), (void *)&texRef_pyramid_cur);
	errcode |= clSetKernelArg(clKernel_track, 12, sizeof(cl_sampler), (void *)&volumeSamplerLinear);
	if(errcode != CL_SUCCESS) printf("Error in seting arguments track");
	// Execute the OpenCL kernel
	errcode = clEnqueueNDRangeKernel(clCommandQue, clKernel_track, 2, NULL, globalWorkSize, localWorkSize, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in launching kernel track");
	clEnqueueBarrier(clCommandQue);
	
        //track<<<blocks, threads>>>(w, h, pyr_w[l], pyr_w[l], scaling[l], l, (l == LEVELS-1), gpu_dx, gpu_dy, gpu_status);

        //cudaThreadSynchronize();
    }

    printf("Tracking: %d ms\n", getTimeNow() - s);

    // Copy back results 
    s = getTimeNow();

	errcode = clEnqueueReadBuffer(clCommandQue, gpu_dx, CL_TRUE, 0, w*h*sizeof(float), dx, 0, NULL, NULL);
	errcode |= clEnqueueReadBuffer(clCommandQue, gpu_dy, CL_TRUE, 0, w*h*sizeof(float), dy, 0, NULL, NULL);
	errcode |= clEnqueueReadBuffer(clCommandQue, gpu_status, CL_TRUE, 0, w*h*sizeof(char), status, 0, NULL, NULL);
	if(errcode != CL_SUCCESS) printf("Error in reading GPU mem\n");
	
    //cudaMemcpy(dx, gpu_dx, sizeof(float)*w*h, cudaMemcpyDeviceToHost);  
    //cudaMemcpy(dy, gpu_dy, sizeof(float)*w*h, cudaMemcpyDeviceToHost);  
    //cudaMemcpy(status, gpu_status, sizeof(char)*w*h, cudaMemcpyDeviceToHost);  
    printf("Copying results from GPU to CPU: %d ms\n", getTimeNow() - s);

    printf("Total time for cudaLK: %d ms\n", getTimeNow() - start);
}
