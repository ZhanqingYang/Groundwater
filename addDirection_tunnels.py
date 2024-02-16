# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 14:50:13 2022

@author: Jasmine.Yang
"""

import pandas as pd
import os

#%% Add direction: North/South/East/Westbound
#  Extract WHT M4M5 nodes only
WHT_nodes=pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_NodeDatePOWID_correction1")
M4M5_nth = pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\direction\m4m5_nth_edt.csv")
M4M5_sth = pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\direction\m4m5_sth_edt.csv")
M4M5_nth_sth = pd.concat([M4M5_nth,M4M5_sth])
M4M5_nth_sth.to_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\direction\M4M5_nth_sth.csv')


# Read WHT_Nodes excluding M4M5
WHT_nodes_noM4M5 = WHT_nodes[WHT_nodes['RouteID']!='M4M5']
WHT_nodes_noM4M5.to_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_NoM4M5.csv')
######## Having Done some VLOOKUP in Excel for 'WHT_Nodes_NoM4M5.csv', adding directions refering to 'direction_index.xlsx' ############
WHT_nodes_noM4M5_updated = pd.read_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_NoM4M5.csv')
WHT_nodes_noM4M5_updated.groupby(by='direction').describe()


#After editing column names in Excel for WHT_NoM4M5.csv and M4M5_nth_sth.csv, merge 2 tables
WHT_nodes_noM4M5_updated = pd.read_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_NoM4M5.csv')
M4M5_nth_sth_updated = pd.read_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\direction\M4M5_nth_sth.csv')
WHTS_merged_direction = pd.concat([WHT_nodes_noM4M5_updated,M4M5_nth_sth_updated])
WHTS_merged_direction = WHTS_merged_direction.reset_index()
WHTS_merged_direction.to_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\direction\WHT_NodesDatePOWID_CH_group_direction.csv')

WHTS_merged_direction['direction_bound']= len(WHTS_merged_direction)*['']
for i in range(len(WHTS_merged_direction)):
    if isinstance(WHTS_merged_direction['direction'][i],str):
        if WHTS_merged_direction['direction'][i].startswith('M'):
            WHTS_merged_direction['direction_bound'][i] = WHTS_merged_direction['direction'][i].split('_')[1]
        else:
            WHTS_merged_direction['direction_bound'][i] = WHTS_merged_direction['direction'][i]
    else:
        WHTS_merged_direction['direction_bound'][i] = WHTS_merged_direction['direction'][i]
        
WHTS_merged_direction.to_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\direction\WHT_NodesDatePOWID_CH_group_direction1.csv')


#%% Add Excavation Type (modify: 'compilingBC25032022.py',adding CutCover and ShaftC couples)

WHTS_merged_direction= pd.read_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_Tunnel_Shaft_CC_forKe.csv')
# WHTS_merged_direction.groupby('RouteID').describe()
# RouteIDList = list(WHTS_merged_direction.groupby('RouteID').groups.keys())
WHTS_merged_direction_type = WHTS_merged_direction
WHTS_merged_direction_type['Excav_ID'] = WHTS_merged_direction_type['Excav'].apply(lambda x: x[5:][:-4])


all_ML = ['M110', 'M120', 'M130_Exca', 'M130_Unexca', 'M140_Exca', 'M140_Unexca', 'M160', 'M170', 
          'M180', 'M190', 'M5B0_Exca', 'M5B0_Unexca', 'M5C0_Exca', 'M5C0_Unexca', 'M5G0_Exca', 'M5G0_Unexca']


all_RampnVent =  ['M150', 'M190_vent', 'M1A0', 'M1D0', 'M1E0', 
                  #'M250', 
                  'M420', 'M430', 'M431', 
                  'M440', 'M460', 'M461', 'M470', 'M4F0', 'M4G0', 'M4H0', 'M4J0', 'M4K0', 'M4L0', 
                  'M4M0', 'M4M1', 'M4N0', 'M4O0', 'M4O1', 'M4O2', 'M4P0', 'M4T0', 'M4Z0', 'M5U0', 
                  'M5Y0', 'MCA0', 'MCC0', 'MCD0', 'MCE0',
                  'M4U0', 'M4V0', 'M4W0', 'M5X0']

all_MLW = ['M420_ML_W', 'M430_ML_W', 'M440_ML_W', 'M460_ML_W', 'M4H0_ML_W', 'M4O0_ML_W', 'M4P0_ML_W','M5Q0']

all_XP = ['XP020', 'XP030', 'XP040', 'XP050', 'XP060', 'XP065', 'XP070', 'XP080', 'XP090', 'XP095', 'XP100', 
          'XP110', 'XP120', 'XP130', 'XP140', 'XP150', 'XP160', 'XP170', 'XP180', 'XP185', 'XP190', 'XP200', 
          'XP230', 'XP240', 'XP250', 'XP260', 'XP270', 'XP280', 'XP290', 'XP300', 'XP310', 'XP315', 'XP320', 
          'XP330', 'XP340', 'XP350', 'XP360', 'XP365', 'XP370', 'XP380', 'XP515', 'XP520', 'XP520A', 'XP525', 
          'XP530', 'XP540', 'XP545', 'XP550', 'XP560', 'XP570', 'XP570A', 'XP580', 'XP585', 'XP590', 'XP600',
          'XP610', 'XP620', 'XP625', 'XP630', 'XP660', 'XP670', 'XP690', 'XP700', 'XP710', 'XP720', 'XP740', 
          'XP750', 'XP760', 'XP775', 'XP780', 'XP800', 'XP820', 'XP830', 'XP840', 'XP850', 'XP870']

all_VTC = ['M4T0_VTC_1', 'M4T0_VTC_2', 'M4U0_VTC',  'M4W0_VTC_1', 'M4W0_VTC_2', 
            'M4Z0_VTC', 'M5U0_VTC_1', 'M5U0_VTC_2',  'M5X0_VTC_1', 'M5X0_VTC_2']

all_CC = ['CutCover1','CutCover2a','CutCover2b','CutCover2c','CutCover3a','CutCover3b','CutCover4']

M4M5L = ['M4M5_link']

shaftC = ['SHAFTC']

etype = {'MainTunnels':all_ML,'RampnVent':all_RampnVent,'Substations':all_MLW,
         'CrossPassage':all_XP,'VentStation':all_VTC, 'M4M5':M4M5L, 'CutCover':all_CC, 'ShaftC':shaftC}

excav_type1 = pd.DataFrame(columns = ['ExcavationType','Excav_ID'])

for i,j in etype.items():
    temp = pd.DataFrame()
    temp['Excav_ID'] = j 
    temp['ExcavationType'] = i
    excav_type1 = excav_type1.append(temp, ignore_index = True)
    
# excav_type = excav_type.rename(columns = {'Excav':'RouteID'})
excav_type = WHTS_merged_direction_type.merge(excav_type1,on = 'Excav_ID')
excav_type = excav_type.rename(columns = {'Excav_ID':'FLAC_ID'})
excav_type.to_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_Tunnel_Shaft_CC_forKe.csv',index=False)
