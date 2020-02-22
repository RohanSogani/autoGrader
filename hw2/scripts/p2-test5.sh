#!/bin/bash
./assignshipments < test5.in > tmp.out
diff tmp.out test5.out
rm -f tmp.out
