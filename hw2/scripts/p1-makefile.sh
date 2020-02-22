#!/bin/bash

# test if the provided make file is working
testfile () {
    file=${1}
    [ -f "${file}" ] || echo "${file} is missing"
}

for f in Aircraft.cpp Aircraft.h maintenance.cpp testAircraft.cpp; do
    testfile ${f}
done

# clean files if they exists
[ -f "maintenance" ]  && rm maintenance
[ -f "testAircraft" ] && rm testAircraft

# try make
make -B > /dev/null   || echo "'make' failed"
[ -f "maintenance"  ] || echo "'make' does not produce maintenance"
[ -f "testAircraft" ] || echo "'make' does not produce testAircraft"

# try make clean
make clean > /dev/null || echo "'make clean' failed"
[ -f "maintenance"  ]  && echo "'make clean' does not clean maintaince"
[ -f "testAircraft" ]  && echo "'make clean' does not clean testAircraft"
