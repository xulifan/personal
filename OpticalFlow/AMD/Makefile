OpenCL_SDK=/opt/AMDAPP
INCLUDE=-I${OpenCL_SDK}/include -I/usr/include/opencv
LIBPATH=-L${OpenCL_SDK}/lib/x86_64 -L${OpenCL_SDK}/shared/lib -L/usr/lib
#g++  ${INCLUDE} ${LIBPATH} ${LIB} OpticalFlow.cpp -c OpticalFlow.o -O2 -g
LIB=-lOpenCL  -lcv -lhighgui
all:
	g++ -O3 main.cc  -o OpticalFlow.exe   ${INCLUDE} ${LIBPATH} ${LIB}  -g
clean:
	rm -f *~ *.exe

