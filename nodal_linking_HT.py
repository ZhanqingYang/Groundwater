# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 10:41:58 2022

@author: hugo.thang
"""


import pandas as pd
import os
import numpy as np

path = os.getcwd()
os.chdir('O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Construction sequence\\WHT')

def get_nodes(df_1,df_2,df_3):
    #extract the nodes needed
    df_1_c = df_1.columns
    df_1 = df_1[[df_1.columns[0],df_1.columns[1],df_1.columns[10],df_1.columns[11],
                 df_1.columns[12],df_1.columns[13]]].copy()
    
    df_2_c = df_2.columns
    df_2 = df_2[[df_2.columns[0],df_2.columns[1], df_2.columns[5],
                  df_2.columns[7], df_2.columns[8],df_2.columns[9],
                  df_2.columns[10], df_2.columns[11],df_2.columns[12],df_2.columns[13]]].copy()

    df_3_c = df_3.columns
    df_3 = df_3[[df_3.columns[4],df_3.columns[5],df_3.columns[6],
                df_3.columns[7],df_3.columns[8]]].copy()

    merged = pd.merge(df_1,df_2,on = 'Element')
    merged = merged.sort_values('Pow-Date-Num',ascending = True,ignore_index = True)
    nodes = []
    eles = []
    
    for ind in merged.index:
        nodes.append(merged['node_feflow_1'][ind])
        eles.append(merged['Element'][ind])
        nodes.append(merged['node_feflow_2'][ind])
        eles.append(merged['Element'][ind])
        nodes.append(merged['node_feflow_3'][ind])
        eles.append(merged['Element'][ind])
        nodes.append(merged['node_feflow_4'][ind])
        eles.append(merged['Element'][ind])
        
    dataframe = pd.DataFrame()
    dataframe['node'] = nodes
    dataframe['element'] = eles
    dataframe1 = dataframe.groupby('node')
    dataframe1 = dataframe.groupby('node')['element'].last()
    dataframe1 = dataframe1.reset_index(name = 'element')
    dataframe1 = dataframe1.rename(columns={'node':'nodes_Feflow','element':'Element'})
    merged1 = pd.merge(dataframe1,df_3,on = 'nodes_Feflow')
    merged = pd.merge(merged1,merged,on='Element')
    return merged
 
#%%               
# df_1 = pd.read_csv(path + '/all_data_v2.csv') #elements and respective nodes
# df_2 = pd.read_csv(path + '/Face_ElemDatePOWID_wSite.csv') 
# # df_2 = pd.read_csv(path + '/WHT_RIC_ElemProperties_JY.csv')#grouped elements according to chainage
# df_3 = pd.read_csv(path + '/mapped_nodes.csv') #nodal information


df_1 = pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export\all_data_v2.csv") #elements and respective nodes
df_2 = pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_ElemDatePOWID_correction1.csv") 
df_3 = pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export\mapped_nodes.csv") #nodal information


# column_names = ["node_feflow",
#                 "x_feflow",
#                 "y_feflow",
#                 "z_feflow",
#                 "element",
#                 "center_x",
#                 "center_y",
#                 "center_z",
#                 "chainage_group",
#                 "route_id",
#                 "chainage",
#                 "date",
#                 "pow_date(weekly)",
#                 "pow_date_num",
#                 "pow_id"]

# output = pd.DataFrame(columns = column_names)

output = get_nodes(df_1,df_2,df_3)
output = output.reset_index()
resultpath = 'O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Construction sequence\\WHT\\results'
output.to_csv(resultpath+'WHT_NodeDatePOWID_correction1.csv',index = False)
#use reindex function to create new dataframe

#%% Jas check chainage nodes-elements
# Element_to_check = [1934248,
# 1298441,
# 546211,
# 886802,
# 232051,
# 1277763,
# 1277075,
# 1585730,
# 103357,
# 1718788,
# 1723631,
# 567793,
# 1723635,
# 1298443,
# 1723636,
# 1348125,
# 1110247,
# 1718783,
# 599433,
# 1110246,
# 893230,
# 1934247,
# 637113,
# 1934246,
# 560904,
# 93424]

# WHT_element=pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_ElemDatePOWID_CH_group.csv") 
# WHT_nodes=pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_NodeDatePOWID_CH_group_20220404.csv")
# all_data=pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export\all_data_v2.csv")
# mapped_nodes=pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export\mapped_nodes.csv")

# M130_1095_element=all_data[all_data.Element.isin(Element_to_check)]
# merged_M130_1095 = pd.merge(all_data,WHT_element,on = 'Element')
# merged_M130_1095_only = merged_M130_1095[merged_M130_1095.Element.isin(Element_to_check)]
# # merged.sort_values('Pow-Date-Num',ascending = True,ignore_index = True)

# nodes = []
# eles = []

# for ind in merged_M130_1095_only.index:
#     nodes.append(merged_M130_1095_only['node_feflow_1'][ind])
#     eles.append(merged_M130_1095_only['Element'][ind])
#     nodes.append(merged_M130_1095_only['node_feflow_2'][ind])
#     eles.append(merged_M130_1095_only['Element'][ind])
#     nodes.append(merged_M130_1095_only['node_feflow_3'][ind])
#     eles.append(merged_M130_1095_only['Element'][ind])
#     nodes.append(merged_M130_1095_only['node_feflow_4'][ind])
#     eles.append(merged_M130_1095_only['Element'][ind])
    
# check_dataframe = pd.DataFrame()
# check_dataframe['node'] = nodes
# check_dataframe['element'] = eles

# WHT_nodes_M130_1095_elemet=WHT_nodes[WHT_nodes.nodes_Feflow.isin(nodes)]







