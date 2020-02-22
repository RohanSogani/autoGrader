#!/bin/bash

./unittest 7 > tmp.out
diff tmp.out unit7.out

rm -f tmp.out
