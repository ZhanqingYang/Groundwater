# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 16:32:28 2022

@author: Jasmine.Yang
"""
import os
import pandas as pd
import datetime as dt
from datetime import datetime

#%% Functions : Date to Datenum (i.e.'2019-11-25' --> 43794)
def excel_date(date1):
    temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)
#%% Files to adapt: Select Run Directory
rundir = r'\\anf.psm.local\anf-files02\3000\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT' #this is where the POW file would be written and saved to
os.chdir(rundir) # change the current working directory to rundir

#%% Inputs [A date in 120 years into future]
end_date = '2139-11-25'                     
end_date = pd.to_datetime(end_date)     
end_date = excel_date(end_date)     # >> 87623 

#%% Write modulation function .dat file from csvfile
shpfile = pd.read_csv(r"\\anf.psm.local\anf-files02\3000\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\WHT_ElemDatePOWID.csv")

# Sort list of Weekly DateNum and POWID
csvfile = shpfile
csvfile = csvfile.drop_duplicates(subset=['POWID'], keep='last').sort_values('POWID').reset_index(drop=True)
csvfile.index +=100
csvfile['PowDateNumON'] = csvfile['Pow-Date-Num']
csvfile['PowDateNumOFF'] = [end_date]*len(csvfile)

powfilename1 = 'WHT_ExcavationSequence_modulation'

file = open(powfilename1+".txt","a+")

for index, row in csvfile.iterrows():
   file.write("# "+str(row['POWID'])+"\n! "
               +str(row['PowDateNumON'])
               +"\n! [type=Polylined;option=linear;timeunit=d;unitclass=CARDINAL;userunit=]\n GAP\n"
               +str(' ')+str(row['PowDateNumON']) +"\t1" +"\n"
               +str(' ')+str(row['PowDateNumOFF']) +"\t1"+"\n")
    # if row['PowDateNumOFF'] < csvfile['PowDateNumOFF'].max():
    #     file.write("	GAP\nEND\n")
    # else:
   file.write("END\n") 

file.write("END")     
file.close()
os.rename(powfilename1+'.txt', powfilename1+'.dat')

