# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 15:21:10 2022

@author: Jasmine.Yang
"""

import pandas as pd
import numpy as np
import os

path = 'O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Test\\ric_conseq\\Tunnel_Invert\\WHTS_inverts'
os.chdir(path)
pwd = os. getcwd()

M5B0_invert = pd.read_csv('M5B0_Unexca.csv')
M5C0_invert = pd.read_csv('M5C0_Unexca.csv')
M5G0_invert = pd.read_csv('M5G0_Unexca.csv')

M5Q0_invert = pd.read_csv('M5Q0.csv')
M5U0_invert = pd.read_csv('M5U0.csv')
M5X0_invert = pd.read_csv('M5X0.csv')
M5Y0_invert = pd.read_csv('M5Y0.csv')

M130_Unexca_invert = pd.read_csv('M130_Unexca.csv')
M140_Unexca_invert = pd.read_csv('M140_Unexca.csv')

# Add RouteID columns

M5B0_invert['RouteID'] = ['M5B0_Unexca']*len(M5B0_invert)
M5C0_invert['RouteID'] = ['M5C0_Unexca']*len(M5C0_invert)
M5G0_invert['RouteID'] = ['M5G0_Unexca']*len(M5G0_invert)
M5Q0_invert['RouteID'] = ['M5Q0']*len(M5Q0_invert)
M5U0_invert['RouteID'] = ['M5U0']*len(M5U0_invert)
M5X0_invert['RouteID'] = ['M5X0']*len(M5X0_invert)
M5Y0_invert['RouteID'] = ['M5Y0']*len(M5Y0_invert)
M130_Unexca_invert['RouteID'] = ['M130_Unexca']*len(M130_Unexca_invert)
M140_Unexca_invert['RouteID'] = ['M140_Unexca']*len(M140_Unexca_invert)

WHTS_inverts = pd.concat([M5B0_invert,M5C0_invert,M5G0_invert,\
                          M5Q0_invert,M5U0_invert,M5X0_invert,M5Y0_invert,\
                             M130_Unexca_invert,M140_Unexca_invert],ignore_index=True)
WHTS_inverts.to_csv('WHTS_inverts_20220331.csv')
