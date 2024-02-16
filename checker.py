# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:30:20 2022

@author: hugo.thang
"""

import pandas as pd
import plotly.express as px


#%%

df = pd.read_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_NodeDatePOWID_CH_group_latlong20220404.csv")



fig = px.scatter_mapbox(df,
                    lat='lat',
                    lon='long',
                    color="chainage_group",
                    # range_color = [0,1.2],
                    color_continuous_scale = 'Spectral_r',
                    hover_name="RouteID",
                    # hover_data = [],
                    # title = 'Seepage at ' + date_s + ' (1km)',
                    zoom=14.5)
fig.update_layout(mapbox_style="carto-positron")
fig.update_mapboxes(bearing = -65, center_lat = -33.866,center_lon = 151.17)
fig.update_layout(coloraxis_colorbar=dict(thickness = 50),
                 title_x = 0.5,title_font_size = 30)
fig.write_html(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\html_plots\ch_group.html")

fig = px.scatter_mapbox(df,
                    lat='lat',
                    lon='long',
                    color="POW-ID",
                    # range_color = [0,1.2],
                    color_continuous_scale = 'Spectral_r',
                    hover_name="RouteID",
                    # hover_data = [],
                    # title = 'Seepage at ' + date_s + ' (1km)',
                    zoom=14.5)
fig.update_layout(mapbox_style="carto-positron")
fig.update_mapboxes(bearing = -65, center_lat = -33.866,center_lon = 151.17)
fig.update_layout(coloraxis_colorbar=dict(thickness = 50),
                 title_x = 0.5,title_font_size = 30)
fig.write_html(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\html_plots\powid.html")

temp = df
temp1 = temp[(temp['RouteID'] == 'M130') & (temp['POW-ID'] == 336) & (temp["chainage_group"] >= 4461)]
temp2 = temp[(temp['POW-ID'] == 343) & (temp['RouteID'] == 'M140') & (temp["chainage_group"] <= 365)]
temp3 = temp1.append(temp2,ignore_index = True)

fig = px.scatter_mapbox(temp3,
                    lat='lat',
                    lon='long',
                    color="POW-ID",
                    # range_color = [0,1.2],
                    color_continuous_scale = 'Spectral_r',
                    hover_name="RouteID",
                    hover_data = ["chainage_group", 'nodes_Feflow'],
                    # title = 'Seepage at ' + date_s + ' (1km)',
                    zoom=14.5)
fig.update_layout(mapbox_style="carto-positron")
fig.update_mapboxes(bearing = -65, center_lat = -33.866,center_lon = 151.17)
fig.update_layout(coloraxis_colorbar=dict(thickness = 50),
                 title_x = 0.5,title_font_size = 30)
fig.write_html(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\html_plots\toremove.html")

remove_nodes_1 = [61165,13026,21755,116702,368262,206693,198510,94739,408361,120027,94379]
remove_nodes_2 = [144727,286804,239503,6989,100856,258543,239509]

temp1 = temp1[~temp1['nodes_Feflow'].isin(remove_nodes_1)]
temp2 = temp2[~temp2['nodes_Feflow'].isin(remove_nodes_2)]


temp4 = temp1.append(temp2,ignore_index = True)

fig = px.scatter_mapbox(temp4,
                    lat='lat',
                    lon='long',
                    color="POW-ID",
                    # range_color = [0,1.2],
                    color_continuous_scale = 'Spectral_r',
                    hover_name="RouteID",
                    hover_data = ["chainage_group", 'nodes_Feflow'],
                    # title = 'Seepage at ' + date_s + ' (1km)',
                    zoom=14.5)
fig.update_layout(mapbox_style="carto-positron")
fig.update_mapboxes(bearing = -65, center_lat = -33.866,center_lon = 151.17)
fig.update_layout(coloraxis_colorbar=dict(thickness = 50),
                 title_x = 0.5,title_font_size = 30)
fig.write_html(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\html_plots\toremove1.html")


temp4.to_csv(r"O:\PSM3696\Eng\20 HIR\FEFLOW\Mesh\Construction sequence\WHT\results\WHT_notInPackage.csv",index = False)
