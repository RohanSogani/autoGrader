#!/bin/bash

# test if the program compiles with no error
testfile () {
    file=${1}
    [ -f "${file}" ] || echo "${file} is missing"
}

[ -f "Makefile" ] && mv Makefile Makefile.1.bak

[ -f "maintenance.cpp" ]  || cp ../../../solutions/aircraft/maintenance.cpp .
[ -f "Aircraft.h" ]       || cp ../../../solutions/aircraft/Aircraft.h .
[ -f "testAircraft.cpp" ] || cp ../../../solutions/aircraft/testAircraft.cpp .

cat >> Makefile <<EOF
CXXFLAGS = -w

all: maintenance testAircraft

maintenance: maintenance.o Aircraft.o
	@\$(CXX) -o \$@ \$^

testAircraft: testAircraft.o Aircraft.o
	@\$(CXX) -o \$@ \$^

clean:
	@find . -type f | xargs touch
	@rm -f unittest maintenance testAircraft *.o
EOF

make clean

make -B > /dev/null || echo "'make' failed"
testfile maintenance
testfile maintenance.o
testfile Aircraft.o
testfile testAircraft
testfile testAircraft.o

make clean
