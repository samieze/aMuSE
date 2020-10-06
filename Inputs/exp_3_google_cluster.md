## Google Cluster Data

### Network 

Nodes = 20

E/N-Ratio = 1.0

Eventrates = [0,855, 212, 24, 400, 129, 0, 0.005,0.05]

### Queries 
#### SEQ
- SEQ(D, C, F, H)

#### AND
- AND(E, D, F, H)

#### QWL
- SEQ(B, D, C, AND(H, I))
- AND(B, H, I)
- SEQ(D, E, H, I)

### Selectivity

{'HF':0.05, 'FH':0.05,'IF':0.05,'FI':0.05,'IE':0.05,'EI':0.05,'HC':0.05, 'CH':0.05,'HD':0.05, 'DH':0.05,'IB':0.05,'BI':0.05,'HI':0.05, 'IH':0.05, 'IC':0.05,'CI':0.05,'DI':0.05,'ID':0.05,  'IB':0.05,'BF': 0.05, 'FB': 0.05,'AB': 0.05,'AF': 0.05,'FA': 0.05,'BA':0.05,'AC':0.05,'CA':0.05, 'BC':0.05, 'CB':0.05,'BG':0.05, 'GB':0.05, 'AD': 0.05, 'DA':0.05, 'CD':0.05, 'DC':0.05, 'BD':0.05, 'DB': 0.05,  'AE':0.05, 'EA':0.05, 'CF':0.05, 'FC':0.05, 'CG': 0.05,  'GC':0.05, 'GF':0.05, 'FG':0.05,  'DF':0.05, 'DG':0.05 }

