#!/bin/bash

# try make but suppress warning
[ -f "assignshipments" ]                && rm assignshipments
WARNING_AS_ERROR=-w make -B > /dev/null || echo "'make' failed"
[ -f "assignshipments" ]                || echo "'make' does not produce assignshipments"

# try make clean
make clean > /dev/null     || echo "'make clean' failed"
[ -f "assignshipments"  ]  && echo "'make clean' does not clean assignshipments"
