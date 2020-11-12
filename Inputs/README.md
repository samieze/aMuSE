# Inputs

## Synthetic Data

- `exp_1.md` contains the network configuration and query workload for the first experiment presented in the paper which compares aMuSE and aMuSE*.
- `exp_2_scal.md`contains the network configuration and query workload for the scalability experiment presentd in the paper.

## Google Cluster Data

The complete datasets and descriptions are available at https://github.com/google/cluster-data.
For the experiment we used traces of the first 12h of the task events data set. 
We derived average event rates and selectivities for our queries for the data set partitioned over the machine IDs to be simulated in a network containing 20 nodes:

- `exp_3_google_cluster.md` contains the average event rates for a timewindow of 30 minutes over the first 12h of the google cluster data set, as well as the queries used in the case study and respective selectivities.

The input traces for each of the 20 nodes used for the case study can be found in `aMuSE/DCEP-Ambrosia/inputexamples/queries_google_cluster/`
`.
