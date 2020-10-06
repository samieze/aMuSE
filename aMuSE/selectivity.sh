#!/bin/sh
cd code
for j in 0.01 0.001 0.0001 0.00001 0.000001
do      
        a=0
	while [ $a -lt 20 ]
	do	  
	  python3.7 selectivity.py $j
	  python3.7 aMuse.py $j  selectivity
	  python3.7 aMuse_star.py $j  selectivity
	  a=`expr $a + 1`
	done
done
