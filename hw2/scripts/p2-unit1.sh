#!/bin/bash

copyfile() {
    [ -f "$1" ] && cp ../../../solutions/airline/$1 .
}

copyfile testing.cpp

make testing -B > /dev/null
./testing 1
