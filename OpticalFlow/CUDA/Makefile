OpenCL_SDK=/opt/AMDAPP
INCLUDE= -I/usr/include/opencv -I/usr/local/include
LIBPATH=-L/usr/lib -L/usr/local/stow/cuda-4.0.17/lib64/
LIB=-lcudart  -lcv -lhighgui
all:
	nvcc -c cudaLK.cu -o cudaLK.o
	g++ ${INCLUDE} ${LIBPATH} ${LIB} -O3 cudaLK.o main.cc -o cudaLK.exe
clean:
	rm -f *~ *.exe

