# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 11:51:43 2021

@author: Jasmine.Yang
"""
import os
import meshio

def convert_mesh(meshfilename):
    meshtext = meshio.read(meshfilename)
    meshtext_points = meshtext.points
    meshtext_cells = meshtext.cells
    mesh_feflow = meshio.Mesh(meshtext_points,meshtext_cells)
    mesh_feflow_name = meshfilename.split('.')[0]
    mesh_feflow.write( mesh_feflow_name +'.vtu', file_format='vtu')
    return

#%% import then export mesh with different format
#   note: model node numbering system might be altered, elementIDs unchanged 
rundir = r'O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\import+export' #this is where the script writes the model files
os.chdir(rundir)
meshfilename = 'mesh2.f3grid'
convert_mesh(meshfilename)