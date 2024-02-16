# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:11:21 2022

@author: hugo.thang
"""

import pandas as pd
import sys
sys.path.append('C:\\Program Files\\DHI\\2022\\FEFLOW 7.5\\python')
sys.path.append('C:\\Program Files\\DHI\\2022\\FEFLOW 7.5\\bin64')
import ifm_contrib as ifm
import os
os.chdir('O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Material assignment\\python')
from MaterialAssignFunctions import filter_table, filter_node
from MaterialAssignFunctions import create_selection_eles, create_selection_nodes, create_elemental_user_data
from MaterialAssignFunctions import create_material, assign_material, assign_material_sel
os.chdir('O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Material assignment')



#%%

excel_file = r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Test\ric_conseq\RIC_Geom-rev2_Concept-rev2_NodeProperties-Rev7-quaters-site.csv"
fem_file = "O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\PostAudit\\femdata\\ROZELLE_PR29_Untreated_Cal_v4b.fem"


df = pd.read_csv(excel_file)
doc = ifm.loadDocument(fem_file)


df_copy = df[['NODE','Site']].copy()
df_copy.loc[:, "NODE"] = df_copy["NODE"].apply(lambda x: x - 1)
df_copy_grouped = df_copy.groupby('Site')['NODE'].apply(list)
df_copy_grouped = df_copy_grouped.reset_index(name = 'NODE') 


for ind in df_copy_grouped.index:
    create_selection_nodes(doc,df_copy_grouped['Site'][ind],df_copy_grouped['NODE'][ind])

doc.saveDocument("C:\\Users\\hugo.thang\\Modelling\\Feflow\\RIC\\ROZELLE_PR29_Untreated_Cal_v4b\\ROZELLE_PR29_Untreated_Cal_v4b(siteincluded).fem")

