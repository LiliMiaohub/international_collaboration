"""This script plots the representation in First and Last authorship for countries over years 
Author: Lili Miao
"""

import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gp
import matplotlib.colors as colors
import pandas as pd
import numpy as np
import sys
from matplotlib.lines import Line2D
import os

def get_normed_authorship(raw_df, exp_df):
    cntry_raw = raw_df.groupby(['cntry','year','role']).size().reset_index(name='raw')
    cntry_exp = exp_df.groupby(['cntry','year','role'])['expected'].sum().reset_index(name='exp')
    cntry_all = cntry_raw.merge(cntry_exp, on=['cntry','year','role'])
    cntry_all['norm'] = np.log(cntry_all['raw']/cntry_all['exp'])
    #cntry_norm = cntry_all.pivot(index='cntry', columns='role', values='norm').reset_index()
    
    return cntry_all

def plot_line(data,authorship,ax,title, color_dict):
    df=data[data.role==authorship]
    sns.lineplot(x='year',y='norm',hue='class',data=df,ax=ax,legend=False,
             palette=color_dict)
    ax.axhline(y=0, color='#C8C8C8', linestyle='--')
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title(title,fontsize=12)
    return ax

def plot(df, color_dict):
    
    fig, ax=plt.subplots(nrows=1,ncols=3,figsize=(16,5))
    ax0=plot_line(df,'F',ax[0],'First Author', color_dict)
    ax1=plot_line(df,'M',ax[1],'Middle Author', color_dict)
    ax2=plot_line(df,'L',ax[2],'Last Author', color_dict)

   
    lines = [Line2D([0], [0], color=v, linewidth=3, linestyle='-', label=k) for k,v in color_dict.items()]
    plt.legend(handles=lines, frameon=False)
    
    fig.text(x=0.45,y=0.01,s="Year of publication",fontsize=15)
    ax0.set_ylabel("Log normalized occurance of authorship",fontsize=15)
    return fig, ax

if __name__ == "__main__":
    
    pub_author_raw_path = sys.argv[1]
    pub_author_exp_path = sys.argv[2]
    stgroup_path = sys.argv[3]
    color_scheme_path = sys.argv[4]
    plot_path = sys.argv[5]
    
    pub_author_raw = pd.read_csv(pub_author_raw_path)
    pub_author_exp = pd.read_csv(pub_author_exp_path)
    
    stgroup = pd.read_csv(stgroup_path)
    color_scheme = pd.read_csv(color_scheme_path)
    
    #distinguish the classification system (st, income) and then retrieve the corrosponding color scheme
    classify_type = os.path.splitext(os.path.basename(stgroup_path))[0].split("_")[1]
    color_filter = color_scheme[color_scheme.type==classify_type]
    color_dict = dict(zip(color_filter['class'], color_filter['color']))
    
    
    cntry_norm = get_normed_authorship(pub_author_raw, pub_author_exp)
    cntry_norm = cntry_norm.merge(stgroup, left_on='cntry', right_on='Code')
    
    fig, ax = plot(cntry_norm, color_dict)
    plt.savefig(plot_path,bbox_inches='tight')