#!/bin/bash
./assignshipments < test6.in > tmp.out
diff tmp.out test6.out
rm -f tmp.out
