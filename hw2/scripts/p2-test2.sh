#!/bin/bash
./assignshipments < test2.in > tmp.out
diff tmp.out test2.out
rm -f tmp.out
