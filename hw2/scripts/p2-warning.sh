#!/bin/bash

# check if the program can even compile. if no, just skip this step
WARNING_AS_ERROR=-w make -B &> /dev/null
if [ $? -eq 0 ]; then

    # now test if it produces warnings
    WARNING_AS_ERROR=-Werror make -B > /dev/null || echo "'make' produces warning failed"

fi
