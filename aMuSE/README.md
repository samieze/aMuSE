# aMuSE/aMuSE*

Implementation of aMuSE and aMuSE*:
Computes a Muse graphs for a given network and query workload.


## Output Format
The output is formatted such that it can be used as input for DCEP-Ambrosia.
- `SELECT` is followed by the projection/query which is used in the MuSE graph
- `FROM` specifies the projections used as predecessors in the combination of the projection
- `ON` specifies the placement of the projection having the node IDs in curly brackets followed by the event type which determines the local placement
- `selectionRate` specifies the selectivity of the projection

The following output describes a MuSE graph for the query `SEQ(B, L, C)`.
```
SELECT SEQ(B, L, C) FROM  SEQ(B, C), L ON {0, 1, 3, 4, 6, 8, 9}/n(L)
SELECT SEQ(B, C) FROM  B, C ON {6}/n(C) WITH selectionRate = 0.03645995079679039
```
In the example above, the root of the query is placed with a multi sink placement having `L` as a partitioning event type.

## Run

- event node ratio

- event skew

- network size

- selectivities  

- query workload size


