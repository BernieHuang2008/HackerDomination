# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -Wall -std=c++11

# Source files
SRCS = $(shell find files_source -name "*.cpp")

# Object files
OBJS = $(patsubst files_source/%.cpp,files/%,$(SRCS))

all: $(OBJS)

files/%: files_source/%.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(OBJS)