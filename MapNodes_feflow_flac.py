# -*- coding: utf-8 -*-
"""

@author: Qinqian.Yu

"""
import pandas as pd
import numpy as np
import meshio

def map_nodes(T_feflow,T_flac):
    T_feflow = T_feflow.rename(columns={'Node':'nodes_Feflow','X':'x','Y':'y','Z':'z'})
    T_feflow = T_feflow.astype(float)
    
    
    T_flac[T_flac[T_flac<0.0001]>-0.0001]=0
    T_flac['x'] = (T_flac['x']*100000).apply(np.floor)/100000
    T_flac['y'] = (T_flac['y']*100000).apply(np.floor)/100000
    T_flac['z'] = (T_flac['z']*1000000).apply(np.floor)/1000000
    # T_flac['coord'] = T_flac[['x', 'y', 'z']].apply(lambda x:round(x,5)).astype(str).agg(','.join, axis=1)
    
    T_flac['x']=T_flac[['x']].apply(lambda x:round(x,5)).astype(str)
    T_flac['y']=T_flac[['y']].apply(lambda x:round(x,5)).astype(str)
    T_flac['z']=T_flac[['z']].apply(lambda x:round(x,5)).astype(str)
    T_flac['coord'] = T_flac[['x', 'y','z']].agg(','.join, axis=1)
    
    T_feflow[T_feflow[T_feflow<0.0001]>-0.0001]=0
    T_feflow['x'] = (T_feflow['x']*100000).apply(np.floor)/100000
    T_feflow['y'] = (T_feflow['y']*100000).apply(np.floor)/100000
    T_feflow['z'] = (T_feflow['z']*1000000).apply(np.floor)/1000000
    
    T_feflow['x']=T_feflow[['x']].apply(lambda x:round(x,5)).astype(str)
    T_feflow['y']=T_feflow[['y']].apply(lambda x:round(x,5)).astype(str)
    T_feflow['z']=T_feflow[['z']].apply(lambda x:round(x,5)).astype(str)
    T_feflow['coord'] = T_feflow[['x', 'y','z']].agg(','.join, axis=1)
    
    out = T_flac.merge(T_feflow,on='coord',how='outer')
    
    out = out.rename(columns={"id":"nodes_flac","x_x":'x_flac',"y_x":'y_flac',"z_x":"z_flac",
                        'id_y':"nodes_feflow",'x_y':'x_feflow',"y_y":'y_feflow','z_y':'z_feflow'})
    # out = out.drop(columns=['coord','x_feflow','y_feflow','z_feflow'],axis=1)

    return out


def assign_group(mesh,centroids,conn):
    meshcell_sets_dicts= mesh.cell_sets_dict
    mesh_keys = list(meshcell_sets_dicts.keys())
    
    zgroup_2 = []
    zgroup_3 = []
    
    # get the zone group in slot 2 and 3
    for k in mesh_keys:
        if "zone" in k and ':"2"' in k:
            zgroup_2.append(k)
        elif "zone" in k and ':"3"' in k:
            zgroup_3.append(k)
    
    # get the element for slot 2
    slot_2_elem = []
    slot_2_group = []
    for g in zgroup_2:
        elem = meshcell_sets_dicts.pop(g)['tetra'].tolist()
        group = [g] * len(elem)
        slot_2_elem = slot_2_elem + elem
        slot_2_group = slot_2_group + group
    
    # get the element for slot 3
    slot_3_elem = []
    slot_3_group = []
    for g in zgroup_3:
        elem = meshcell_sets_dicts.pop(g)['tetra'].tolist()
        group = [g] * len(elem)
        slot_3_elem = slot_3_elem + elem
        slot_3_group = slot_3_group + group
    
    slot2 = pd.DataFrame(list(zip(slot_2_elem, slot_2_group)),columns=['Element','Material'])
    slot2['Element'] = slot2['Element'] + 1
    slot2.sort_values(by='Element',inplace=True,ignore_index=True)
    
    slot3 = pd.DataFrame(list(zip(slot_3_elem, slot_3_group)),columns=['Element','Excav'])
    slot3['Element'] = slot3['Element'] + 1
    slot3.sort_values(by='Element',inplace=True,ignore_index=True)
    
    zgroup = slot2.merge(slot3,on='Element',how='outer')
    zgroup.fillna('None',inplace=True)
    zgroup_out = zgroup.merge(centroids,on = 'Element',how='left'\
                            ).merge(conn,on='Element',how='left')

    return zgroup_out


#%% Input & output
rundir = r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export' #this is where the script writes the model files
os.chdir(rundir)
pwd = os.getcwd()


# total number of nodes
number_gridpoints = 412270
number_zone = 2266214

# Read the file
FLAC_fname = 'Mesh2.f3grid'
# file export from feflow
node_feflow= pd.read_table('Feflow_Nodes_Coords.dat', sep="\s+").iloc[:,[1,2,3,4]]
elem_centroids =  pd.read_table('Feflow_Element_centroids.dat', sep="\s+", usecols=[5,6,7,8])
# grid file of FLAC
mesh = meshio.read(FLAC_fname)
node_flac= pd.read_table(FLAC_fname,sep="\s+",skiprows=3,\
                      nrows=number_gridpoints, names=['id','x','y','z'],engine='python')
conn_feflow= pd.read_table(FLAC_fname,sep="\s+",skiprows=number_gridpoints+4,nrows=number_zone,\
                           names=['category','category_1','Element','node_1','node_2','node_3','node_4']\
                               ).iloc[:,[2,3,4,5,6]]

# run the map node function
nodes_mapped = map_nodes(node_feflow,node_flac)
nodes_mapped.to_csv('mapped_nodes.csv',index=False)
# nodes_mapped = pd.read_csv('mapped_nodes.csv')
nodes_mapped = nodes_mapped.drop(columns=['coord','x_feflow','y_feflow','z_feflow'],axis=1)
# aassign the group to elements
zgroup = assign_group(mesh,elem_centroids,conn_feflow)

# # map feflow nodes into element file
id_node = nodes_mapped.iloc[:,[0,-1]]
zgroup_f = zgroup.merge(right = id_node, how = 'left',left_on='node_1', right_on='nodes_flac')\
            .rename(columns = {'nodes_Feflow':'node_feflow_1','node_1':'node_flac_1'})\
            .drop(columns='nodes_flac')
zgroup_f = zgroup_f.merge(right = id_node, how = 'left',left_on='node_2',right_on='nodes_flac')\
            .rename(columns = {'nodes_Feflow':'node_feflow_2','node_2':'node_flac_2'})\
            .drop(columns='nodes_flac')
zgroup_f = zgroup_f.merge(right = id_node, how = 'left',left_on='node_3',right_on='nodes_flac')\
            .rename(columns = {'nodes_Feflow':'node_feflow_3','node_3':'node_flac_3'})\
            .drop(columns='nodes_flac')
zgroup_f = zgroup_f.merge(right = id_node, how = 'left',left_on='node_4',right_on='nodes_flac')\
            .rename(columns = {'nodes_Feflow':'node_feflow_4','node_4':'node_flac_4'})\
            .drop(columns='nodes_flac')

zgroup_f.to_csv('all_data_v2.csv',index=False)

#%%
tunnel_excavated = pd.read_csv('all_data_v2.csv')
tunnel_excavated = tunnel_excavated[tunnel_excavated['Excav']!='None'].iloc[:,[0,2,3,4,5]]
# tunnel_excavated = zgroup_f[zgroup_f['Excav']!='None'].iloc[:,[0,2,3,4,5]]
tunnel_excavated.to_csv('tunnel_excavated.csv',index=False)



