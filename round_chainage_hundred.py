# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:42:45 2022

@author: Jasmine.Yang
"""
import pandas as pd
import numpy as np
import os

def round_to_hundred(chainage):
    roundednum = np.floor(int(chainage)/100)*100
    return roundednum

#%% Round chainage to hundred
path = r'O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Construction sequence'
os.chdir(path) # change directl=ory to new location

folder_path = 'O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Construction sequence\\WHT\\'
filename_elem = 'WHT_ElemDatePOWID_Site_Mar03.csv'
filename_node = 'WHT_NodeDatePOWID_Site_Mar03.csv'

Elem_csvfile = pd.read_csv(folder_path + filename_elem, index_col=None )
Elem_csvfile['CH_group'] = Elem_csvfile['chainage_group'].apply(lambda x:round_to_hundred(x))
Elem_csvfile.to_csv('WHT_ElemDatePOWID_CH_group.csv')

Node_csvfile = pd.read_csv(folder_path + filename_node, index_col=None)
Node_csvfile['CH_group'] = Node_csvfile['chainage_group'].apply(lambda x:round_to_hundred(x))
Node_csvfile.to_csv('WHT_NodeDatePOWID_CH_group.csv')

