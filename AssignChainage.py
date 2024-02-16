# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 13:21:02 2021

@author: Qinqian.Yu
"""
import pandas as pd
import numpy as np
import os

def get_chainage_group(pwd,RouteID,CH_start,CH_end,tunnel_excav):
    tunnel_excav = tunnel_excav 
    control_line = pd.read_csv(pwd+'\\ControlLine\\'+RouteID+'.csv',header=None).iloc[:,[0,1,2]].to_numpy()
    control_line = control_line[::-1] 
    pt_center = []
    
    #Chainage calculation starts
    for c, pt in enumerate(control_line):
        if c < len(control_line)-1:
            x1 = pt[0]
            y1 = pt[1]

            x2 = control_line[c+1][0]
            y2 = control_line[c+1][1]
            
            xc = (x1+x2)/2
            yc = (y1+y2)/2
            
            ptc = [xc,yc]
            pt_center.append(ptc)
    
    pt_center = np.array(pt_center)
    
    for pt in pt_center:
        tunnel_excav[len(tunnel_excav.columns)-4] = ((tunnel_excav['CENTER_X']-pt[0])**2 + \
        (tunnel_excav['CENTER_Y']-pt[1])**2)**0.5
    
    dist = tunnel_excav.iloc[:,5:]
    id_min = dist.idxmin(axis=1) #idxmin()  return the index containing minimum distance #id_min return the index of columns with min dist
                                                 
    tunnel_excav = tunnel_excav.iloc[:,:5]
    tunnel_excav['chainage_group'] = id_min   #for each row, there is a the column index where min dist locates
    tunnel_excav['chainage_group'] = CH_start + (id_min-1)*(CH_end-CH_start)/len(pt_center)    #calculate and assign chainage based on the Start and End chainage given by ControlLine.csv
    # tunnel_excav['chainage_group'] = tunnel_excav['chainage_group'].astype('Int64')
    tunnel_excav['Excavated'] = tunnel_excav['Excav'].apply(lambda x: x.split(':')[1]).apply(lambda x: x.split('_')[0])
    tunnel_excav = tunnel_excav[tunnel_excav.Excavated == RouteID]
    tunnel_excav.to_csv(pwd+'/Chainage-Calculate/'+RouteID+'-asc.csv',index=False)
    
    return tunnel_excav

#%% Loop through all the Control Lines to get chainage groups
path = 'O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Construction sequence\\WHT\\import+export'
os.chdir(path)
pwd = os. getcwd()

tunnel_excav = pd.read_csv('tunnel_excavated.csv')
ControlLinedf = pd.read_csv('control line.csv').dropna(how='all')
ControlLinedf = ControlLinedf[['Control line','Start chainage','End chainage']].dropna(how='any').reindex(copy=False)
ControlLineCoordFolder = '\ControlLine'
directory = os.fsencode(path + ControlLineCoordFolder)

for file in os.scandir(directory):
      RouteID = os.fsdecode(file).split('\\')[-1].split('.')[0]
      CH_start = ControlLinedf[ControlLinedf['Control line'] == RouteID]['Start chainage'].values[0]
      CH_end = ControlLinedf[ControlLinedf['Control line'] == RouteID]['End chainage'].values[0]
      Finaltunnel= get_chainage_group(pwd,RouteID,CH_start,CH_end,tunnel_excav)
      print(RouteID,CH_start,CH_end)   # to track progress
      
      
# Edit: Add one more RouteID in Chainage-Calculate /2022-Mar-03/
# RouteID = 'XP585'
# CH_start = 0
# CH_end = 16
# Finaltunnel= get_chainage_group(pwd,RouteID,CH_start,CH_end,tunnel_excav)
# print(RouteID,CH_start,CH_end) 
 