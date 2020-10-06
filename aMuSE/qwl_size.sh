#!/bin/bash
cd code
j=1
while [ $j -lt 40 ]
do      
        a=0
	while [ $a -lt 20 ]
	do
	  python3.7 generate_qwls.py $j 
	  python3.7 aMuse_star.py $j qwl_size
          a=`expr $a + 1`
	done
        j=`expr $j + 1`
done    
