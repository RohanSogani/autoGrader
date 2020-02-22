#!/bin/bash

input=$1 # the tarball

extractfile () {
    tar=$1
    key=$2
    ret=$(tar tvf ${tar} | grep -ohE "\s(\.?\w*/)*${key}")
    if [ -z "${ret}" ]; then
	echo "missing '${key}'"
    else
	tar -xf ${tar} ${ret}
	[ -f "${key}" ] || mv -f ${ret} .
    fi
}

readfile() {
    [ -f "$1" ] || extractfile ${input} $1
}

copyfile() {
    [ -f "$1" ] || cp ../../../solutions/airline/$1 .
}

# extract files written by students
readfile Airplane.cpp
readfile Airline.cpp

for i in {1..6}; do
    copyfile test$i.out
    copyfile test$i.in
done

copyfile Makefile
copyfile Airplane.h
copyfile Airline.h
copyfile assignshipments.cpp

copyfile testing.cpp
