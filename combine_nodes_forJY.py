# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:54:26 2022

@author: hugo.thang
"""

import pandas as pd

#%% Input files
shaft_cc = r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_NODE_SHAFT_CC_latlong.csv"
tunnel = r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_NodeDatePOWID_correction1.csv"
cc = r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\CutnCover\Output\pythonoutputs\CutnCoverNodePOW_JY.csv"
shc = r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\CutnCover\Output\pythonoutputs\SHC_NodePOW_JY.csv"
master = r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\Master.csv"

#%%
scc = pd.read_csv(shaft_cc)
tnl = pd.read_csv(tunnel)
cc = pd.read_csv(cc)
shc = pd.read_csv(shc)

master = pd.read_csv(master)
master = master[['nodes_Feflow','FLAC_ID','RouteID','ExcavationType']].copy()
cc_master = master[master['ExcavationType'] == 'CutnCover']
shc_master = master[master['RouteID']=='SHAFTC']
cc_shc_master = cc_master.append(shc_master,ignore_index = True)


scc = scc.drop(columns = {'Unnamed: 0','Unnamed: 0.1','lat','long'})
cc = cc[['Element','Excav','node_feflow_mapped','x_feflow','y_feflow','z_feflow',\
         'node_feflow_1','node_feflow_2','node_feflow_3','node_feflow_4','chainage_group','RL Group N','Date','PowDate','PowDateNum','POWID']]
    
shc = shc[['Element','Excav','node_feflow_mapped','x_feflow','y_feflow','z_feflow',\
           'node_feflow_1','node_feflow_2','node_feflow_3','node_feflow_4','Date','PowDate','PowDateNum','POWID']]

cc_shc = cc.append(shc,ignore_index = True)
cc_shc = cc_shc.rename(columns = {'PowDate':'Pow-Date','PowDateNum':'Pow-Date-Num','POWID':'POW-ID','node_feflow_mapped':'nodes_Feflow'})
cc_shc_master = cc_shc_master.merge(cc_shc,on = 'nodes_Feflow')
cc_shc_master = cc_shc_master.drop(columns = 'ExcavationType')
tnl = tnl.append(cc_shc_master,ignore_index = True)
tnl = tnl.drop(columns = 'index')
tnl_noextra = tnl.drop_duplicates(subset = ['nodes_Feflow'])

# Output files
tnl_noextra.to_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_Tunnel_Shaft_CC_forKe.csv",index = False)


#%% (Optional) Add Excavation Type (modify: 'compilingBC25032022.py',adding CutCover and ShaftC couples)

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

excav_type1 = pd.DataFrame(columns = ['ExcavationType','FLAC_ID'])

for i,j in etype.items():
    temp = pd.DataFrame()
    temp['FLAC_ID'] = j 
    temp['ExcavationType'] = i
    excav_type1 = excav_type1.append(temp, ignore_index = True)

#
WHTS_merged= pd.read_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_Tunnel_Shaft_CC_forKe.csv')
WHTS_merged['FLAC_ID'] = WHTS_merged['Excav'].apply(lambda x: x[5:][:-4])
excav_type = WHTS_merged.merge(excav_type1,on = 'FLAC_ID')
excav_type.to_csv(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_Nodes_Tunnel_Shaft_CC_forKe.csv',index=False)
