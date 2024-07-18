"""This script plots the representation in First and Last authorship for countries 
Author: Lili Miao
"""

import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gp
import matplotlib.colors as colors
import pandas as pd
import numpy as np
import sys

def get_normed_authorship(raw_df, exp_df):
    cntry_raw = raw_df.groupby(['cntry','role']).size().reset_index(name='raw')
    cntry_exp = exp_df.groupby(['cntry','role'])['expected'].sum().reset_index(name='exp')
    cntry_all = cntry_raw.merge(cntry_exp, on=['cntry','role'])
    cntry_all['norm'] = cntry_all['raw']/cntry_all['exp']
    cntry_norm = cntry_all.pivot(index='cntry', columns='role', values='norm').reset_index()
    return cntry_norm

def map_group(fratio,lratio):
    if fratio<1 and lratio<1:
        return 0.5
    elif fratio>1 and lratio<1:
        return 1.5
    elif fratio<1 and lratio>1:
        return 2.5
    elif fratio>1 and lratio>1:
        return 3.5
    
def plot_worldmap(shp_path, df):
    world_geo=gp.read_file(shp_path)
    world_geo = world_geo[['ADMIN','NAME','ISO_A3','geometry']]
    world_geo=world_geo[world_geo.NAME!='Antarctica']
    world_geo.loc[world_geo.NAME=='France','ISO_A3']='FRA'
    world_geo.loc[world_geo.NAME=='Norway','ISO_A3']='NOR'
    
    colorsList = ['#D9D9D9', '#F4D05E', '#EA6B5F','#912855']
    cmap = colors.ListedColormap(colorsList)
    bounds = np.array([0, 1, 2, 3, 4])
    norm = colors.BoundaryNorm(boundaries=bounds, ncolors=4)
    
    fig, ax=plt.subplots(figsize=(16,6))
    world_geo.plot(ax = ax, linewidth=0.25, edgecolor="#8C8C8C", facecolor="#ffffff")
    df = df.merge(world_geo,left_on='cntry',right_on='ISO_A3')
    df = gp.GeoDataFrame(df)
    df.plot(column='group', cmap=cmap, norm=norm,ax=ax)
    ax.axis("off")
    return fig, ax

def plot_legend():
    # create a figure and axis object
    fig, ax = plt.subplots()

    # set the limits of the x and y axis
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])

    # draw the x and y axis
    ax.axhline(y=0, color='gray')
    ax.axvline(x=0, color='gray')

    # fill the four quadrants with different colors
    ax.fill_betweenx(y=[0, 5], x1=0, x2=5, color='#912855')
    #ax.text(2.5, 2.5, 'Over_First\nOver_Last', ha='center', va='center',fontsize=25, c='white')

    ax.fill_betweenx(y=[0, 5], x1=-5, x2=0, color='#EA6B5F')
    #ax.text(-2.5, 2.5, 'Under_First\nOver_Last', ha='center', va='center',fontsize=25, c='white')

    ax.fill_betweenx(y=[-5, 0], x1=0, x2=5, color='#F4D05E')
    #ax.text(2.5, -2.5, 'Over_First\nUnder_Last', ha='center', va='center',fontsize=25, c='white')

    ax.fill_betweenx(y=[-5, 0], x1=-5, x2=0, color='#D9D9D9')


    ax.set_xticks([])
    ax.set_yticks([])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xlabel("First Author", fontsize=15)
    ax.set_ylabel("Last Author", fontsize=15)

    return fig, ax


if __name__ == "__main__":
    
    pub_author_raw_path = sys.argv[1]
    pub_author_exp_path = sys.argv[2]
    world_shp_path = sys.argv[3]
    world_map_path = sys.argv[4]
    legend_path = sys.argv[5]
    
    pub_author_raw = pd.read_csv(pub_author_raw_path)
    pub_author_exp = pd.read_csv(pub_author_exp_path)
    
    cntry_norm = get_normed_authorship(pub_author_raw, pub_author_exp)
    cntry_norm['group'] = cntry_norm.apply(lambda x:map_group(x.F, x.L), axis=1)
    
    fig, ax = plot_worldmap(world_shp_path, cntry_norm)
    plt.savefig(world_map_path, bbox_inches='tight')
    
    fig, ax = plot_legend()
    plt.savefig(legend_path, bbox_inches='tight')
    
    
    
    