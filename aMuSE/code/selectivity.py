"""
Initialize selectivities for given tuple of primitive event types (projlist) within interval [x,y].
"""
import random as rd
import numpy as np
import sys
from generate_qwls import *



""" Experiment Selectivities:   
    
Scalability: 

selectivities experiment set 1:
    
selectivities experiment set 2 (scalability):  {'GT': 0.21612568437777865, 'GS': 0.26264468965015, 'GR': 0.18052464042595415, 'GQ': 0.11736118247799497, 'GP': 0.1535356320686965, 'GF': 0.27945819055264653, 'GE': 0.19338525554048458, 'GD': 0.29865577466961357, 'GC': 0.19510887494483137, 'GB': 0.16719523511522608, 'GA': 0.1280808851295218, 'GO': 0.2954165850555537, 'GN': 0.163484604065876, 'GM': 0.2567994901936952, 'GL': 0.1705207844083092, 'GK': 0.19831278190072876, 'GJ': 0.2839910720053407, 'GI': 0.1652799338037201, 'GH': 0.17960309337496205, 'ME': 0.22830304300028478, 'MD': 0.29466434180354006, 'MG': 0.2567994901936952, 'MF': 0.2977459933512414, 'MA': 0.14035075480791864, 'MC': 0.20442378169867426, 'MB': 0.21481555404297137, 'ML': 0.22788093561410813, 'MO': 0.1582623313680508, 'MN': 0.15428245869009666, 'MI': 0.1389655042349144, 'MH': 0.24034818610887368, 'MK': 0.10313641416240696, 'MJ': 0.15312540434931945, 'MT': 0.10877859162728556, 'MQ': 0.2564595721865919, 'MP': 0.256085562011916, 'MS': 0.2903325966667135, 'MR': 0.28265259504539264, 'FP': 0.13832972602679935, 'FQ': 0.2685933680940352, 'FR': 0.22201223537634385, 'FS': 0.12250355744248494, 'FT': 0.2300237208312016, 'FA': 0.11670047059139593, 'FB': 0.25787249580139704, 'FC': 0.10682588127460867, 'FD': 0.18922865819849494, 'FE': 0.1905796385555123, 'FG': 0.27945819055264653, 'FH': 0.1317321171800196, 'FI': 0.15135193184998313, 'FJ': 0.18860183485439114, 'FK': 0.2067449178545372, 'FL': 0.17120673942875841, 'FM': 0.2977459933512414, 'FN': 0.2428269821548464, 'FO': 0.1387290569323437, 'SR': 0.23059904740201387, 'SQ': 0.17446470550290566, 'SP': 0.2216306144420745, 'ST': 0.11021408875933288, 'SK': 0.25203496629902006, 'SJ': 0.22559805865721427, 'SI': 0.2988460217052251, 'SH': 0.25016486254869064, 'SO': 0.13127441230330358, 'SN': 0.19530450745652278, 'SM': 0.2903325966667135, 'SL': 0.12991055912046745, 'SC': 0.2119536358174931, 'SB': 0.231761350543546, 'SA': 0.2980959667426486, 'SG': 0.26264468965015, 'SF': 0.12250355744248494, 'SE': 0.22901942238719697, 'SD': 0.21599320863845156, 'LF': 0.17120673942875841, 'LG': 0.1705207844083092, 'LD': 0.18382587274537582, 'LE': 0.20803015723647697, 'LB': 0.29101516614563205, 'LC': 0.17393922000570178, 'LA': 0.29891704815942033, 'LN': 0.19419151964656506, 'LO': 0.1724992863413786, 'LM': 0.22788093561410813, 'LJ': 0.21025496900606438, 'LK': 0.27261883410153304, 'LH': 0.2682695884210411, 'LI': 0.2593513247663297, 'LT': 0.20711943703645092, 'LR': 0.23621691787821747, 'LS': 0.12991055912046745, 'LP': 0.2754075366667387, 'LQ': 0.26766989902557814, 'RT': 0.10658583285513375, 'RP': 0.10288006893231338, 'RQ': 0.278108031555724, 'RS': 0.23059904740201387, 'RD': 0.203330922651743, 'RE': 0.17197924139133786, 'RF': 0.22201223537634385, 'RG': 0.18052464042595415, 'RA': 0.22975387550277546, 'RB': 0.24861544556505985, 'RC': 0.12095721939871287, 'RL': 0.23621691787821747, 'RM': 0.28265259504539264, 'RN': 0.10845923941094458, 'RO': 0.19876013195590747, 'RH': 0.1642974231554714, 'RI': 0.1007714290396221, 'RJ': 0.20220560193534348, 'RK': 0.2794923209548946, 'EM': 0.22830304300028478, 'EL': 0.20803015723647697, 'EO': 0.2152771927452723, 'EN': 0.24560888737168618, 'EI': 0.2213445951302211, 'EH': 0.27436503099066545, 'EK': 0.14322206835533585, 'EJ': 0.2982354627161309, 'ED': 0.17011496541952165, 'EG': 0.19338525554048458, 'EF': 0.1905796385555123, 'EA': 0.2666903925909585, 'EC': 0.1349591747661923, 'EB': 0.16455988367362917, 'ET': 0.10197162903533091, 'EQ': 0.19434904275316572, 'EP': 0.13453562257164944, 'ES': 0.22901942238719697, 'ER': 0.17197924139133786, 'KC': 0.2950658925144942, 'KB': 0.22457874650667187, 'KA': 0.27633246135506107, 'KG': 0.19831278190072876, 'KF': 0.2067449178545372, 'KE': 0.14322206835533585, 'KD': 0.1430291562400703, 'KJ': 0.21676231531313928, 'KI': 0.2141248798987736, 'KH': 0.2602377849852522, 'KO': 0.2521499386009013, 'KN': 0.1495044985367495, 'KM': 0.10313641416240696, 'KL': 0.27261883410153304, 'KS': 0.25203496629902006, 'KR': 0.2794923209548946, 'KQ': 0.12878755317499788, 'KP': 0.17735195951802513, 'KT': 0.2646229358067128, 'DN': 0.27513205569069676, 'DO': 0.17643634972813454, 'DL': 0.18382587274537582, 'DM': 0.29466434180354006, 'DJ': 0.15584437015547103, 'DK': 0.1430291562400703, 'DH': 0.2629296794178153, 'DI': 0.17700233846820101, 'DF': 0.18922865819849494, 'DG': 0.29865577466961357, 'DE': 0.17011496541952165, 'DB': 0.20807851657308718, 'DC': 0.2051751304875858, 'DA': 0.27836370237015273, 'DT': 0.1263050903304519, 'DR': 0.203330922651743, 'DS': 0.21599320863845156, 'DP': 0.25074088545217366, 'DQ': 0.2832596241656146, 'QP': 0.23021912578721168, 'QS': 0.17446470550290566, 'QR': 0.278108031555724, 'QT': 0.17783905776767112, 'QA': 0.20852277398542846, 'QC': 0.21449405371122682, 'QB': 0.13782916433601736, 'QE': 0.19434904275316572, 'QD': 0.2832596241656146, 'QG': 0.11736118247799497, 'QF': 0.2685933680940352, 'QI': 0.12965396480940078, 'QH': 0.18742767724739762, 'QK': 0.12878755317499788, 'QJ': 0.2097425422036185, 'QM': 0.2564595721865919, 'QL': 0.26766989902557814, 'QO': 0.24266336499316252, 'QN': 0.29172097247982665, 'JT': 0.269389860961739, 'JP': 0.2892152480237916, 'JQ': 0.2097425422036185, 'JR': 0.20220560193534348, 'JS': 0.22559805865721427, 'JL': 0.21025496900606438, 'JM': 0.15312540434931945, 'JN': 0.2715398597011616, 'JO': 0.10920278172640228, 'JH': 0.19052534789886255, 'JI': 0.19921319446927754, 'JK': 0.21676231531313928, 'JD': 0.15584437015547103, 'JE': 0.2982354627161309, 'JF': 0.18860183485439114, 'JG': 0.2839910720053407, 'JA': 0.13156659415429556, 'JB': 0.1726178297431852, 'JC': 0.29039086323139784, 'PR': 0.10288006893231338, 'PS': 0.2216306144420745, 'PQ': 0.23021912578721168, 'PT': 0.22207650351140593, 'PB': 0.2566967783896732, 'PC': 0.24920386845350548, 'PA': 0.20283446835805874, 'PF': 0.13832972602679935, 'PG': 0.1535356320686965, 'PD': 0.25074088545217366, 'PE': 0.13453562257164944, 'PJ': 0.2892152480237916, 'PK': 0.17735195951802513, 'PH': 0.2538885738488812, 'PI': 0.24476272502407007, 'PN': 0.1990804855270639, 'PO': 0.2378145493234316, 'PL': 0.2754075366667387, 'PM': 0.256085562011916, 'CK': 0.2950658925144942, 'CJ': 0.29039086323139784, 'CI': 0.19708055323113138, 'CH': 0.13575658880552524, 'CO': 0.13736239712051498, 'CN': 0.14935903568952774, 'CM': 0.20442378169867426, 'CL': 0.17393922000570178, 'CB': 0.19449827695911343, 'CA': 0.24382334754168003, 'CG': 0.19510887494483137, 'CF': 0.10682588127460867, 'CE': 0.1349591747661923, 'CD': 0.2051751304875858, 'CS': 0.2119536358174931, 'CR': 0.12095721939871287, 'CQ': 0.21449405371122682, 'CP': 0.24920386845350548, 'CT': 0.12086970237073212, 'IQ': 0.12965396480940078, 'IP': 0.24476272502407007, 'IS': 0.2988460217052251, 'IR': 0.1007714290396221, 'IT': 0.140140335527, 'IH': 0.10755461350024098, 'IK': 0.2141248798987736, 'IJ': 0.19921319446927754, 'IM': 0.1389655042349144, 'IL': 0.2593513247663297, 'IO': 0.10375786350142802, 'IN': 0.14487628938183492, 'IA': 0.14980502688251113, 'IC': 0.19708055323113138, 'IB': 0.1748677102464673, 'IE': 0.2213445951302211, 'ID': 0.17700233846820101, 'IG': 0.1652799338037201, 'IF': 0.15135193184998313, 'BD': 0.20807851657308718, 'BE': 0.16455988367362917, 'BF': 0.25787249580139704, 'BG': 0.16719523511522608, 'BA': 0.2141945888652845, 'BC': 0.19449827695911343, 'BL': 0.29101516614563205, 'BM': 0.21481555404297137, 'BN': 0.2527633641987493, 'BO': 0.2180480507271843, 'BH': 0.12750366613078185, 'BI': 0.1748677102464673, 'BJ': 0.1726178297431852, 'BK': 0.22457874650667187, 'BT': 0.20322696147099206, 'BP': 0.2566967783896732, 'BQ': 0.13782916433601736, 'BR': 0.24861544556505985, 'BS': 0.231761350543546, 'ON': 0.14140278487282065, 'OM': 0.1582623313680508, 'OL': 0.1724992863413786, 'OK': 0.2521499386009013, 'OJ': 0.10920278172640228, 'OI': 0.10375786350142802, 'OH': 0.21852093640434517, 'OG': 0.2954165850555537, 'OF': 0.1387290569323437, 'OE': 0.2152771927452723, 'OD': 0.17643634972813454, 'OC': 0.13736239712051498, 'OB': 0.2180480507271843, 'OA': 0.22546280639341876, 'OT': 0.19032085035608134, 'OS': 0.13127441230330358, 'OR': 0.19876013195590747, 'OQ': 0.24266336499316252, 'OP': 0.2378145493234316, 'HR': 0.1642974231554714, 'HS': 0.25016486254869064, 'HP': 0.2538885738488812, 'HQ': 0.18742767724739762, 'HT': 0.189053991353532, 'HJ': 0.19052534789886255, 'HK': 0.2602377849852522, 'HI': 0.10755461350024098, 'HN': 0.1488830465866095, 'HO': 0.21852093640434517, 'HL': 0.2682695884210411, 'HM': 0.24034818610887368, 'HB': 0.12750366613078185, 'HC': 0.13575658880552524, 'HA': 0.14817997731994698, 'HF': 0.1317321171800196, 'HG': 0.17960309337496205, 'HD': 0.2629296794178153, 'HE': 0.27436503099066545, 'NH': 0.1488830465866095, 'NI': 0.14487628938183492, 'NJ': 0.2715398597011616, 'NK': 0.1495044985367495, 'NL': 0.19419151964656506, 'NM': 0.15428245869009666, 'NO': 0.14140278487282065, 'NA': 0.2489429979661225, 'NB': 0.2527633641987493, 'NC': 0.14935903568952774, 'ND': 0.27513205569069676, 'NE': 0.24560888737168618, 'NF': 0.2428269821548464, 'NG': 0.163484604065876, 'NP': 0.1990804855270639, 'NQ': 0.29172097247982665, 'NR': 0.10845923941094458, 'NS': 0.19530450745652278, 'NT': 0.29595790145974, 'TR': 0.10658583285513375, 'TS': 0.11021408875933288, 'TP': 0.22207650351140593, 'TQ': 0.17783905776767112, 'TN': 0.29595790145974, 'TO': 0.19032085035608134, 'TL': 0.20711943703645092, 'TM': 0.10877859162728556, 'TJ': 0.269389860961739, 'TK': 0.2646229358067128, 'TH': 0.189053991353532, 'TI': 0.140140335527, 'TF': 0.2300237208312016, 'TG': 0.21612568437777865, 'TD': 0.1263050903304519, 'TE': 0.10197162903533091, 'TB': 0.20322696147099206, 'TC': 0.12086970237073212, 'TA': 0.21504173051677128, 'AC': 0.24382334754168003, 'AB': 0.2141945888652845, 'AE': 0.2666903925909585, 'AD': 0.27836370237015273, 'AG': 0.1280808851295218, 'AF': 0.11670047059139593, 'AI': 0.14980502688251113, 'AH': 0.14817997731994698, 'AK': 0.27633246135506107, 'AJ': 0.13156659415429556, 'AM': 0.14035075480791864, 'AL': 0.29891704815942033, 'AO': 0.22546280639341876, 'AN': 0.2489429979661225, 'AQ': 0.20852277398542846, 'AP': 0.20283446835805874, 'AS': 0.2980959667426486, 'AR': 0.22975387550277546, 'AT': 0.21504173051677128}
    
selectivities Google Cluster Data: [selectivity for each tuple of primitive event types x,y such that x.job_ID == y.job_ID]
selectivities = {'HF':0.05, 'FH':0.05,'IF':0.05,'FI':0.05,'IE':0.05,'EI':0.05,'HC':0.05, 'CH':0.05,'HD':0.05, 'DH':0.05,'IB':0.05,'BI':0.05,'HI':0.05, 'IH':0.05, 'IC':0.05,'CI':0.05,'DI':0.05,'ID':0.05,  'IB':0.05,'BF': 0.05, 'FB': 0.05,'AB': 0.05,'AF': 0.05,'FA': 0.05,'BA':0.05,'AC':0.05,'CA':0.05, 'BC':0.05, 'CB':0.05,'BG':0.05, 'GB':0.05, 'AD': 0.05, 'DA':0.05, 'CD':0.05, 'DC':0.05, 'BD':0.05, 'DB': 0.05,  'AE':0.05, 'EA':0.05, 'CF':0.05, 'FC':0.05, 'CG': 0.05,  'GC':0.05, 'GF':0.05, 'FG':0.05,  'DF':0.05, 'DG':0.05 }
"""

def initialize_selectivities(wl,x,y): 

   
    projlist = generate_twosets(primEvents)       
    projlist = list(set(projlist))
    selectivities = {}
    selectivity = 0
    for i in projlist: 
        #if len(filter_numbers(i)) >1 :                  
            selectivity = rd.uniform(0,0.3)             
            if selectivity > 0.2:
                selectivity = 1
                selectivities[str(i)] =  selectivity
                selectivities[str(changeorder(i))] =  selectivity
            if selectivity < 0.2: 
                selectivity = rd.uniform(x,y)                
                selectivities[str(i)] =  selectivity
                selectivities[str(changeorder(i))] =  selectivity
    return selectivities


def main():
  """default selectivity interval"""
  x = 0.01
  y = 0.2
  

  primEvents = PrimitiveEvents
  
  if len(sys.argv) > 1: 
      x = float(sys.argv[1])
      
  if len(sys.argv) >2 :
      x = float(sys.argv[1])
      y = float(sys.argv[2])
 
  selectivities = initialize_selectivities(primEvents,x,y)
  print("SELECTIVITIES")
  print("--------------")
  print(selectivities)
  

  with open('selectivities', 'wb') as selectivity_file:
    pickle.dump(selectivities,  selectivity_file)   
    
 
  
if __name__ == "__main__":
    main()



    