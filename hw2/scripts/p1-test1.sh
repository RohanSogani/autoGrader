#!/bin/bash


./maintenance < test1.in > tmp.out
diff tmp.out test1.out
rm -f tmp.out
