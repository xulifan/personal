INCLUDE=-I/usr/local/include -I/usr/include/opencv
LIBPATH=-L/usr/lib -L/usr/local/lib
LIB=  -lcv -lhighgui
all:
	g++ -O3 main.cc  -o OpticalFlow.exe   ${INCLUDE} ${LIBPATH} ${LIB}  -g
clean:
	rm -f *~ *.exe

