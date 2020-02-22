#!/bin/bash
copyfile() {
    [ -f "" ] && cp ../../../solutions/airline/ .
}
copyfile testing.cpp

make testing -B > /dev/null
./testing 3
