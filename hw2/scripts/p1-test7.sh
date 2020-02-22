#!/bin/bash


./maintenance < test7.in > tmp.out
diff tmp.out test7.out
rm -f tmp.out
