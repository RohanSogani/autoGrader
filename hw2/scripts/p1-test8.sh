#!/bin/bash

./testAircraft > tmp.out
diff tmp.out output.out
rm -f tmp.out
