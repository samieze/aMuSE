#!/bin/sh


cd code
for j in 25 50 75 100 124 150 175 200
do      
        a=0
	while [ $a -lt 20 ]
	do
	  python3.7 generate_network.py $j
	  python3.7 aMuse.py $j nwsize
	  python3.7 aMuse_star.py $j nwsize
	  a=`expr $a + 1`
	done
done
