# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:33:29 2022

@author: Jasmine.Yang
"""
import glob
import os
import pandas as pd
import datetime as dt
from datetime import datetime,timedelta

#%% 
def excel_date(date1):                  # Date to Datenum (i.e.'2019-11-25' --> 43794)
    temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

#%% Import DailyRoadHeader data
rundir = r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export' #this is where the script writes the model files
os.chdir(rundir)
pwd = os.getcwd()

seqdf = pd.read_csv('sequence_combine_correction.csv').iloc[:,[1,2,5,-6,-5,-4,-3,-2]]
seqdf['RouteID'] = seqdf['RouteID'].replace(to_replace = ['M450'], value='XP585')
    
# Weekly construction sequence
seqdf['Date'] = pd.to_datetime(seqdf['Date'],dayfirst = True)
seqdf['Week'] = seqdf.Date.dt.to_period(freq='W')

#%% Assign Dates accroding to RouteID and Chainage

## View list of RouteIDs of seqdf for check before merging with control line chainages
# seqIDList = list(seqdf.groupby('RouteID').groups.keys())

directory_path = os.fsencode(r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export\Chainage-Calculate')      

for file in os.scandir(directory_path):
      
      # Sequence-Chainage dataframe for a control line:
      CLineID = os.fsdecode(file).split('\\')[-1].split('-')[0]
      indivseqdf =  seqdf[seqdf['RouteID'] == CLineID]
      indivseqdf.sort_values(by='Chainage',inplace=True,ignore_index=True)
      indivseqdf.loc[:,'Chainage'] = indivseqdf.loc[:,'Chainage'].astype('int32')
      
      # Element-Chainage Dataframe of each Controiline
      filename = os.fsdecode(file).split('\\')[-1]
      ch = pd.read_csv(pwd+'/Chainage-Calculate/'+filename)
      ch.sort_values(by='chainage_group',inplace=True,ignore_index=True)
      ch.loc[:,'chainage_group'] = ch.loc[:,'chainage_group'].astype('int32')
      ch.reset_index(inplace=True,drop=True)
      
      # Merge dataframes: ch & indivseqdf 
      df1 = pd.merge_asof(left=ch, right=indivseqdf,\
                           left_on ='chainage_group',right_on = 'Chainage',\
                               direction='nearest',allow_exact_matches=False)
      
      df1.to_csv(pwd+'/Chainage-Sequence_correction/'+CLineID+'-ascwkly.csv',index=False)         
      print(CLineID+' done') # to track progess
      

#%% Link weekly date to POWID  /edit:2022-01-17/

# Step1- concate all RouteID dataframes
# Step2- extract Date (weekly) 
# Step3- convert to Datenum
# Step4- match Datenum with POWID: func 'element_powID()' applied

#'Step 1 concate all RouteID dataframes
all_files_folder = r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export\Chainage-Sequence_correction'
DFFs = pd.concat(map(pd.read_csv, glob.glob(os.path.join(all_files_folder,"*.csv")))).reset_index(drop=True)

# 'Step 2 Extract Date (weekly) 
DFFs = DFFs.dropna(subset=['Date'])
PowDate = DFFs['Week'].apply(lambda x: str(x).split('/')[0])
DFFs['Pow-Date']=PowDate
DFFs = DFFs[['Element',
              'Excav',
              'CENTER_X',
              'CENTER_Y',
              'CENTER_Z',
              'chainage_group',
              'OBJECTID',
              'RouteID',
              'Site',
              'Chainage',
              'Date',
              'Pow-Date']]

# 'Step 3 convert to Datenum
PowDateNum =  DFFs['Pow-Date'].apply(lambda x:datetime.strptime(x,'%Y-%m-%d')).apply(lambda x:excel_date(x))
DFFs['Pow-Date-Num'] = PowDateNum
DFFs.sort_values(by='Pow-Date-Num',inplace=True,ignore_index=True)

# 'Step 4 Generate POWIDs according to DateNums:
PowIDList = DFFs.drop_duplicates(subset=['Pow-Date-Num'], keep='last').sort_values('Pow-Date-Num').reset_index(drop=True)
PowIDList.index +=100
PowIDList['POW-ID'] = PowIDList.index
PowIDList = PowIDList[['Pow-Date-Num','POW-ID']]

DFFs = DFFs.merge(PowIDList,on='Pow-Date-Num',how='left')
DFFs['Date'] = DFFs['Date'].astype('datetime64[ns]')
DFFs['Pow-Date'] =  pd.to_datetime(DFFs['Pow-Date'], format='%Y-%m-%d')

# Save result file to result folder
result_path = 'O:\\PSM3696\\Eng\\20 HIR\\FEFLOW\\Mesh\\Construction sequence\\WHT\\results'
DFFs.to_csv(result_path+'\WHT_ElemDatePOWID_correction1.csv',index=False)





