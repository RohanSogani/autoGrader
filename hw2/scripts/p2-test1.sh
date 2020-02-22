#!/bin/bash
./assignshipments < test1.in > tmp.out
diff tmp.out test1.out
rm -f tmp.out
