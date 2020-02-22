#!/bin/bash

tar -xf $1

testfile () {
    file=${1}
    [ -f "${file}" ] || echo "${file} is missing"
}

testfile Makefile
testfile Aircraft.cpp
testfile Aircraft.h
testfile maintenance.cpp
testfile testAircraft.cpp
