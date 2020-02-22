#!/bin/bash

./unittest 8 > tmp.out
diff tmp.out unit8.out

rm -f tmp.out
