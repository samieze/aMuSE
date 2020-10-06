#!/bin/sh

cd code
for j in  1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0
do          
	a=0 
	while [ $a -lt 20 ]  
	do
	  python3.7 generate_network.py 20 0.5 $j
	  python3.7 aMuse.py $j event_skew
	  python3.7 aMuse_star.py $j event_skew
          a=`expr $a + 1`
	done
done
