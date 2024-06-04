import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import sys
import os

def plot_normalization(df, xlabel, color_dict, xcol, huecol):
    
    fig, ax = plt.subplots()
    sns.barplot(x=xcol, y='norm', hue=huecol, hue_order=color_dict.keys(), order=color_dict.keys(), 
                data=df[df.norm>0],
               palette=color_dict,
               ax=ax)
    sns.barplot(x=xcol, y='norm', hue=huecol, hue_order=color_dict.keys(), order=color_dict.keys(),
                data=df[df.norm<0],
               color='#D9D9D9',
               ax=ax)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("Log(Actual/Expectation)", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.tick_params(axis='both', which='minor', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    legend_patches = [
        mpatches.Patch(color=color, label=label) for label, color in color_dict.items()
    ]
    ax.legend(handles=legend_patches, loc=[1.01,0.4],frameon=False)
    
    return fig, ax

def cntry_to_group(df, group_dict):
    df['first_class'] = df['first'].map(group_dict)
    df['last_class'] = df['last'].map(group_dict)
    return df

def normalization(raw_df, exp_df):
    
    def group_df(df, colname):
        return df.groupby(['first_class','last_class'])[colname].sum().reset_index()
    
    grouped_raw = group_df(raw_df,'raw')
    grouped_exp = group_df(exp_df, 'exp')
    
    grouped_df = pd.merge(grouped_raw, grouped_exp, on=['first_class','last_class'])
    grouped_df['norm'] = np.log(grouped_df['raw']/grouped_df['exp'])
    
    return grouped_df

if __name__ == "__main__":
    
    raw_path = sys.argv[1]
    exp_path = sys.argv[2]
    classify_group_path = sys.argv[3]
    color_scheme_path = sys.argv[4]
    
    plot_path = sys.argv[5]
    
    xlabel = sys.argv[6]
    xcol = sys.argv[7]
    huecol = sys.argv[8]
    
    raw_df = pd.read_csv(raw_path)
    exp_df = pd.read_csv(exp_path)
    
    group_df = pd.read_csv(classify_group_path)
    group_dict = dict(zip(group_df['Code'],group_df['class']))
    
    color_scheme = pd.read_csv(color_scheme_path)
    group_type = os.path.splitext(os.path.basename(classify_group_path))[0].split("_")[1]
    color_scheme = color_scheme[color_scheme.type==group_type]
    color_dict = dict(zip(color_scheme['class'], color_scheme['color']))
    
    raw_df = cntry_to_group(raw_df, group_dict)
    exp_df = cntry_to_group(exp_df, group_dict)
    
    normed_df = normalization(raw_df, exp_df)
    
    fig, ax = plot_normalization(normed_df, xlabel, color_dict, xcol, huecol)
    fig.savefig(plot_path, bbox_inches='tight')