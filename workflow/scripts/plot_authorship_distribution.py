"""this script plots the distribution of authorship across countries aggregated at S&T level
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import sys
import os

def plot(df, title, ax, color_dict):
    
    sns.lineplot(x='year',y='cnt',hue='class',data=df,ax=ax,legend=False,
                palette=color_dict)
    ax.set_title(title,fontsize=12)
    ax.set_ylim(0,1)
    ax.set_xlabel("")
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_ylabel("")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return ax

if __name__ == "__main__":
    
    pub_author_path = sys.argv[1]
    stgroup_path = sys.argv[2]
    color_scheme_path = sys.argv[3]
    authorship_distribution = sys.argv[4]
    
    
    pub_author = pd.read_csv(pub_author_path)
    stgroup = pd.read_csv(stgroup_path)
    color_scheme = pd.read_csv(color_scheme_path)
    
    
    pub_author = pub_author.merge(stgroup, left_on='cntry', right_on='Code')
    
    authorship_cnt = pub_author.groupby(by=['role','year','class']).size().reset_index(name='cnt')
    authorship_cnt = authorship_cnt.pivot(index=['role','year'], columns=['class'], values='cnt')
    authorship_cnt = authorship_cnt.div(authorship_cnt.sum(axis=1), axis=0).reset_index()
    authorship_cnt = authorship_cnt.melt(id_vars=['role','year'], var_name='class', value_name='cnt')
    
    #distinguish the classification system (st, income) and then retrieve the corrosponding color scheme
    classify_type = os.path.splitext(os.path.basename(stgroup_path))[0].split("_")[1]
    color_filter = color_scheme[color_scheme.type==classify_type]
    color_dict = dict(zip(color_filter['class'], color_filter['color']))

    
    fig, ax=plt.subplots(nrows=1,ncols=3,figsize=(16,5))
    ax[0]=plot(authorship_cnt[authorship_cnt.role=='F'],'First Author', ax[0], color_dict)
    ax[0].set_ylabel("Proportion of authors",fontsize=15)

    ax[1]=plot(authorship_cnt[authorship_cnt.role=='M'],'Middle Author', ax[1], color_dict)
    ax[2]=plot(authorship_cnt[authorship_cnt.role=='L'],'Last Author',ax[2], color_dict)

    lines = [Line2D([0], [0], color=v, linewidth=3, linestyle='-', label=k) for k,v in color_dict.items()]
    ax[2].legend(handles=lines, loc=(0.62,0.77),frameon=False)
    plt.savefig(authorship_distribution, bbox_inches='tight')
    
