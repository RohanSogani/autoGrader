#!/bin/bash

# test if the program compiles with any warning
testfile () {
    file=${1}
    [ -f "${file}" ] || echo "${file} is missing"
}

[ -f "Makefile" ] && mv Makefile Makefile.2.bak

[ -f "maintenance.cpp" ]  && chmod 600 maintenance.cpp  && mv maintenance.cpp  maintenance.cpp.2.back
[ -f "Aircraft.h" ]       && chmod 600 Aircraft.h       && mv Aircraft.h       Aircraft.h.2.back
[ -f "testAircraft.cpp" ] && chmod 600 testAircraft.cpp && mv testAircraft.cpp testAircraft.cpp.2.back

cp ../../../solutions/aircraft/unittest.cpp .
cp ../../../solutions/aircraft/maintenance.cpp .
cp ../../../solutions/aircraft/Aircraft.h .
cp ../../../solutions/aircraft/testAircraft.cpp .

cat >> Makefile <<EOF
CXXFLAGS = -Wall

all: maintenance testAircraft unittest

maintenance: maintenance.o Aircraft.o
	@\$(CXX) -o \$@ \$^

testAircraft: testAircraft.o Aircraft.o
	@\$(CXX) -o \$@ \$^

unittest: unittest.o Aircraft.o
	@\$(CXX) -o \$@ \$^

clean:
	@find . -type f | xargs touch
	@rm -f unittest maintenance testAircraft *.o
EOF

make clean > /dev/null

make -B > /dev/null  || echo "'make' failed"
testfile maintenance
testfile maintenance.o
testfile Aircraft.o
testfile testAircraft
testfile testAircraft.o

for i in {1..4}
do
    cp ../../../solutions/aircraft/test$i.in  .
    cp ../../../solutions/aircraft/test$i.out .
done
cp ../../../solutions/aircraft/unit*.out .
