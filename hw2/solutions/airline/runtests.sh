#!/bin/bash

make > /dev/null
make -B testing > /dev/null

for i in {1..6}
do
  ./assignshipments < test$i.in > tmp.out
  diff tmp.out test$i.out
done

rm -f tmp.out

for i in {1..6}
do
  ./testing $i
done
