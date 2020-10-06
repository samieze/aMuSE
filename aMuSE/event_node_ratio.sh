#!/bin/sh

cd code
for j in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do      
        a=0
	while [ $a -lt 20 ]
	do
	  python3.7 generate_network.py 20 $j 
	  python3.7 aMuse.py $j event_node_ratio
	  python3.7 aMuse_star.py $j event_node_ratio
          a=`expr $a + 1`
	done
done
