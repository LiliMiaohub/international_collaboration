"""this script plots the distribution of individual researchers across countries aggregated at S&T level
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import sys
import os

def plot_line(df, x, y, ylabel, color_dict):
    
    fig, ax = plt.subplots()
    ax = sns.lineplot(x=x, y=y, hue='class', data=df, ax=ax, legend=False, palette=color_dict)
    #lines = [Line2D([0], [0], color=v, linewidth=3, linestyle='-',label=k) for k,v in color_dict.items()]
    #ax.legend(handles=lines,loc=(1.01,0.50),frameon=False)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.set_xlabel("")
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig, ax

def plot_stacked_bar(df, color_dict, ylabel):
    
    fig, ax = plt.subplots(figsize=(4,3))
    df = df[color_dict.keys()]
    df.plot(kind='bar', stacked=True, 
           color=[color_dict[col] for col in df.columns],
           ax=ax, width=0.8, legend=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=-45)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_xlabel('year', fontsize=10)
    return fig, ax
    

if __name__ == "__main__":
    
    pub_author_path = sys.argv[1]
    stgroup_path = sys.argv[2]
    color_scheme_path = sys.argv[3]
    raw_cnt_distribution = sys.argv[4]
    prop_distribution = sys.argv[5]
    
    
    pub_author = pd.read_csv(pub_author_path)
    stgroup = pd.read_csv(stgroup_path)
    color_scheme = pd.read_csv(color_scheme_path)
    
    #distinguish the classification system (st, income) and then retrieve the corrosponding color scheme
    classify_type = os.path.splitext(os.path.basename(stgroup_path))[0].split("_")[1]
    color_filter = color_scheme[color_scheme.type==classify_type]
    color_dict = dict(zip(color_filter['class'], color_filter['color']))

    
    pub_author = pub_author.merge(stgroup, left_on='cntry', right_on='Code')
    
    author_cnt = pub_author[['cluster_id','year','cntry','class']].drop_duplicates()
    author_cnt = author_cnt.groupby(['year','class']).size().reset_index(name='num_author')
    author_cnt.loc[:,'cnt_log'] = np.log10(author_cnt['num_author'])
    
    fig, ax = plot_line(author_cnt, 'year','cnt_log','Log number of authors', color_dict)
    ax.set_yticks([4.5,5,5.5,6],['$10^{4.5}$','$10^{5}$','$10^{5.5}$','$10^{6}$'])
    plt.savefig(raw_cnt_distribution, bbox_inches='tight')
    
    prop_df = author_cnt.pivot(index='year', columns='class', values='num_author')
    prop_df = prop_df.div(prop_df.sum(axis=1), axis=0)
    #prop_df = prop_df.melt(id_vars='year', var_name='class', value_name='prop')
    
    fig, ax = plot_stacked_bar(prop_df, color_dict, '% of international authors')
    plt.savefig(prop_distribution, bbox_inches='tight')
    
    