CC = g++
IDIR = 
LDIR = 
CFLAGS = -c -Wall
LDFLAGS = -lpthread
SOURCES = main.cpp dmatrix.cpp graph.cpp utils.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = create-km

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDIR) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(IDIR) $(CFLAGS) $< -o $@

clean:
	rm *.o
