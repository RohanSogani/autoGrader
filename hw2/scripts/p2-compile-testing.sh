#!/bin/bash

# check if the testing program can
WARNING_AS_ERROR=-w make testing -B > /dev/null \
    || echo "cannot compile testing programs, which means some of the required functions are not implemented"
