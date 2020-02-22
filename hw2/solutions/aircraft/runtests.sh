#!/bin/bash
make -B          > /dev/null
make -B unittest > /dev/null

for i in {1..7}
do
  ./maintenance< test$i.in > tmp.out
  diff tmp.out test$i.out
done

for i in {1..4}
do
    ./unittest ${i}a
    ./unittest ${i}b
done

for i in {5..6}
do
    ./unittest ${i}
done

for i in {7..8}
do
    ./unittest ${i} > tmp.out
    diff tmp.out unit$i.out
done
rm -f tmp.out
