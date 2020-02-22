#!/bin/bash


./maintenance < test3.in > tmp.out
diff tmp.out test3.out
rm -f tmp.out
