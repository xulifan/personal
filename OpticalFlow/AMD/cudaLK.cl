#define PATCH_R 6
__kernel void convertToGrey(__global unsigned char *d_in, __global float *d_out, int N) {
    
    // Get the index of the current element
	int idx = get_global_id(0);

	if(idx < N) 
		d_out[idx] = d_in[idx*3]*0.1144f + d_in[idx*3+1]*0.5867f + d_in[idx*3+2]*0.2989f;
	
	return;
}

__kernel void pyrDownsample(__global float *in, int w1,int h1, __global float *out, int w2, int h2) {
    
    // Get the index of the current element
    int x2 = get_global_id(0);
    int y2 = get_global_id(1);

    if( (x2 < w2) && (y2 < h2) ) {    
        int x = x2*2;
        int y = y2*2;
        int x_1 = x-1;
        int y_1 = y-1;
        int x_2 = x+1;
        int y_2 = y+1;

        if(x_1 < 0) x_1 = 0;
        if(y_1 < 0) y_1 = 0;
        if(x_2 >= w1) x_2 = w1 - 1;
        if(y_2 >= h1) y_2 = h1 - 1;

       out[y2*w2 + x2] = 0.25f*in[y*w1+x] + 0.125f*(in[y*w1+x_1] + in[y*w1+x_2] + in[y_1*w1+x] + in[y_2*w1+x]) +
                          0.0625f*(in[y_1*w1+x_1] + in[y_2*w1+x_1] + in[y_1*w1+x_2] + in[y_2*w1+x_2]);
	}
	return;
}

__kernel void smoothX(__global float *in, int w, int h, __global float *out) {
    
    // Get the index of the current element
    int x = get_global_id(0);
    int y = get_global_id(1);

    if(x >= w || y >= h)
        return;

    int idx = y*w;

    int a = x-2;
    int b = x-1;
    int c = x;
    int d = x+1;
    int e = x+2;

    if(a < 0) a = 0;
    if(b < 0) b = 0;
    if(c >= w) c = w-1;
    if(d >= w) d = w-1;

    out[y*w+x] = 0.0625f*in[idx+a] + 0.25f*in[idx+b] + 0.375f*in[idx+c] + 0.25f*in[idx+d] + 0.0625f*in[idx+e];
	return;
}

__kernel void smoothY(__global float *in, int w, int h, __global float *out) {
    
    // Get the index of the current element
    int x = get_global_id(0);
    int y = get_global_id(1);

    if(x >= w || y >= h)
        return;

    int a = y-2;
    int b = y-1;
    int c = y;
    int d = y+1;
    int e = y+2;

    if(a < 0) a = 0;
    if(b < 0) b = 0;
    if(c >= h) c = h-1;
    if(d >= h) d = h-1;

    out[y*w+x] = 0.0625f*in[a*w+x] + 0.25f*in[b*w+x] + 0.375f*in[c*w+x] + 0.25f*in[d*w+x] + 0.0625f*in[e*w+x];
	return;
}
__kernel void track(const int w, const int h, 
                      const int pyr_w, const int pyr_h, 
                      float scaling, int level, char initGuess, 
                      __global float *dx, __global float *dy, __global char *status,
			__read_only image2d_t texRef_pyramid_prev, __read_only image2d_t texRef_pyramid_cur, sampler_t volumeSampler)
{
	int x = get_global_id(0);
	int y = get_global_id(1);
	int idx = y*w +x;

	if(x > w-1 || y > h-1) 
        return;

    if(status[idx] == 0)
        return;

    float prev_x = x*scaling;
    float prev_y = y*scaling;

    float Vx, Vy;
    float cur_x, cur_y;
    float sum_Ixx = 0;
    float sum_Ixy = 0;
    float sum_Iyy = 0;
    float sum_Ixt;
    float sum_Iyt;
    float Ix, Iy, It;
    int xx, yy;
    float det, D;
    float I, J;
    float vx, vy;
    int j;

    if(initGuess) {
        Vx = 0;
        Vy = 0;
        cur_x = prev_x;
        cur_y = prev_y;
    }
    else {
        Vx = dx[idx];
        Vy = dy[idx];
        cur_x = prev_x + Vx;
        cur_y = prev_y + Vy;
    }
    // Calculate spatial gradient 
    for(yy=-PATCH_R; yy <= PATCH_R; yy++) {
        for(xx=-PATCH_R; xx <= PATCH_R; xx++) {  
		float4 temp1, temp2;
		temp1 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx+1,prev_y + yy));
		temp2 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx-1,prev_y + yy));
		Ix = (temp1.x - temp2.x)*0.5f;
		temp1 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx,prev_y + yy+1));
		temp2 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx,prev_y + yy-1));
		Iy = (temp1.x - temp2.x)*0.5f;

            //Ix = (tex2D(texRef_pyramid_prev, prev_x + xx+1, prev_y + yy) - tex2D(texRef_pyramid_prev, prev_x + xx-1, prev_y + yy))*0.5f;
            //Iy = (tex2D(texRef_pyramid_prev, prev_x + xx, prev_y + yy+1) - tex2D(texRef_pyramid_prev, prev_x + xx, prev_y + yy-1))*0.5f;

            sum_Ixx += Ix*Ix;
            sum_Ixy += Ix*Iy;
            sum_Iyy += Iy*Iy;
        }
    }

    det = sum_Ixx*sum_Iyy - sum_Ixy*sum_Ixy;

    if(det < 0.00001f) {
        status[idx] = 0;
        return;
    }

    D = 1/det;

    // Iteration part
   for(j=0; j < 10; j++) {
        if(cur_x < 0 || cur_x > pyr_w || cur_y < 0 || cur_y > pyr_h) {
            status[idx] = 0;
            return;
        }

        sum_Ixt = 0;
        sum_Iyt = 0;

        // No explicit handling of pixels outside the image ... maybe we don't have to because the hardware interpolation scheme
        // will always give a result for pixels outside the image. How greatly the duplicated pixel values affect the result is unknown at the moment.
        for(yy=-PATCH_R; yy <= PATCH_R; yy++) {
            for(xx=-PATCH_R; xx <= PATCH_R; xx++) {
		float4 temp1, temp2;
		temp1 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx,prev_y + yy));
		temp2 = read_imagef(texRef_pyramid_cur , volumeSampler, (float2)(cur_x  + xx,cur_y  + yy));
            	I = temp1.x;
		J = temp2.x;
                //I = tex2D(texRef_pyramid_prev, prev_x + xx, prev_y + yy);   
                //J = tex2D(texRef_pyramid_cur, cur_x + xx, cur_y + yy);
		temp1 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx+1,prev_y + yy));
		temp2 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx-1,prev_y + yy));
		Ix = (temp1.x - temp2.x)*0.5f;
		temp1 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx,prev_y + yy+1));
		temp2 = read_imagef(texRef_pyramid_prev, volumeSampler, (float2)(prev_x + xx,prev_y + yy-1));
		Iy = (temp1.x - temp2.x)*0.5f;
		
                //Ix = (tex2D(texRef_pyramid_prev, prev_x + xx+1, prev_y + yy) - tex2D(texRef_pyramid_prev, prev_x + xx-1, prev_y + yy))*0.5f;
                //Iy = (tex2D(texRef_pyramid_prev, prev_x + xx, prev_y + yy+1) - tex2D(texRef_pyramid_prev, prev_x + xx, prev_y + yy-1))*0.5f;

                It = J - I;

                sum_Ixt += Ix*It;
                sum_Iyt += Iy*It;
            }            
        }

        // Find the inverse of the 2x2 matrix using a mix of determinant and adjugate matrix
        // http://cnx.org/content/m19446/latest/
        vx = D*(-sum_Iyy*sum_Ixt + sum_Ixy*sum_Iyt);
        vy = D*( sum_Ixy*sum_Ixt - sum_Ixx*sum_Iyt);

        Vx += vx;
        Vy += vy;
        cur_x += vx;
        cur_y += vy;
 
        // Movement very small
        if(fabs(vx) < 0.01f && fabs(vy) < 0.01f)
            break;
    }

    if(level != 0) {
        cur_x += cur_x;
        cur_y += cur_y;

        Vx += Vx;
        Vy += Vy;
    }

    dx[idx] = Vx;
    dy[idx] = Vy;
}
