# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:43:22 2022

@author: Jasmine.Yang
"""

import pandas as pd
import numpy as np
import os

excav_hhbc = pd.read_csv(r"C:\Users\Jasmine.Yang\OneDrive - Pells Sullivan Meynink\Desktop\Work-Copies\InSemW5\EXCA_HHBC.csv")
excav_hhbc_check_node = excav_hhbc.drop_duplicates(subset=['Node'])

excav_hhbc['IF_duplicated'] = excav_hhbc.duplicated(subset=['Node'], keep=False)
excav_hhbc_dpcs = excav_hhbc[excav_hhbc['IF_duplicated']==True]


excav_hhbc_check_node.to_csv(r'N:\PSM4660\Eng\20 HIR\FEFLOW\forDoug\EXCA_HHBC1.csv')
excav_type = pd.read_csv('')

#%%

HHBC_shp = pd.read_csv(r"N:\PSM4660\Eng\20 HIR\FEFLOW\forDoug\EXCA_HHBC2.csv")
addin = pd.read_csv(r"N:\PSM4660\Eng\20 HIR\FEFLOW\forJon\addin.csv")
HHBC2_update = pd.concat([HHBC_shp,addin])
HHBC2_update.to_csv(r"N:\PSM4660\Eng\20 HIR\FEFLOW\forDoug\EXCA_HHBC3.csv")
# HHBC2_update['IF_duplicated'] =HHBC2_update.duplicated(subset=['Node'], keep=False)
# HHBC2_dpc =HHBC2_update[HHBC2_update['IF_duplicated']==True]

WHT_NodeDate = pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_NodeDatePOWID_CH_group.csv")


WHT_NodeDate_update_0 = WHT_NodeDate.loc[(WHT_NodeDate['RouteID'] == 'M130')&(WHT_NodeDate['chainage_group']>2890)]['chainage_group'].apply(lambda x: x-1)
WHT_NodeDate_update = WHT_NodeDate.loc[(WHT_NodeDate['RouteID'] != 'M130')|(WHT_NodeDate['chainage_group']<2890)]['chainage_group'].apply(lambda x: x)
WHT_NodeDate_list = pd.concat([WHT_NodeDate_update,WHT_NodeDate_update_0])
WHT_NodeDate['chainage_group_ud'] = WHT_NodeDate_list
# WHT_NodeDate['chainage_group'].apply(lambda x: x-1 if (WHT_NodeDate['RouteID'] == 'M130')&(WHT_NodeDate['chainage_group']>2890) else x)


WHT_NodeDate.to_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_NodeDatePOWID_20220404.csv")
# if WHT_NodeDate['RouteID'] == 'M130' and WHT_NodeDate['chainage_group'] > 2890:
#     WHT_NodeDate['chainage_group'].apply(lambda x: x-1)
    
# for i in range(len(WHT_NodeDate)):
#     if (WHT_NodeDate['RouteID'] == 'M130' and WHT_NodeDate['chainage_group'][i]<2890 ):
#         WHT_NodeDate['chainage_group_upd'][i] = WHT_NodeDate['chainage_group'][i]-1
#     else:
#         WHT_NodeDate['chaiage_group_upd'][i] = WHT_NodeDate['chainage_group']
        