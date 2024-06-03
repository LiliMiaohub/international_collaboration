"""This script accomplish following tasks:
1. decide whether a paper is alphabetically order or not based on the last name of authors
2. decide whether a paper is internationally coauthored or not
3. assign "first","last","middle" to authors

The output of the scripts consists three sets of files:
1. all papers (including both internationally/non-internationally, alphabetically/nonalpha): publication information, publication information at author level
2. publication information at author level for **internationally coauthored** papers
3. publication information at author level for **internationally nonalphabetically coauthored** papers

Author: Lili Miao
"""

import pandas as pd
import sys

def return_alpha(df):
    """return the alphabetically type for each paper, namely: single author, alphabetically ordered, non-alphabetically ordered
    """
    
    df = df.sort_values(by=['ost_bk','seqno'])
    df = df.groupby(['ost_bk']).agg({'lastname':list}).reset_index()
    
    def detect_alpha(namelist):
        if len(namelist)==1:
            return "single"
        elif all(namelist[i]<=namelist[i+1] for i in range(len(namelist)-1)):
            return "alpha"
        else:
            return "noalp"
    
    df['alpha'] = df['lastname'].apply(lambda x:detect_alpha(x))
    
    return df[['ost_bk','alpha']]


def return_intl(df):
    """return whether the publication is internationally coauthored
    """
    df = df.groupby(['ost_bk']).agg({'cntry':list}).reset_index()
    df['intl'] = df['cntry'].apply(lambda x: 1 if len(set(x))>1 else 0)
    
    return df[['ost_bk','intl']]


def return_role(df):
    """return the role of authors, namely: first, last and middle
    """
    df['num_author'] = df.groupby(['ost_bk'])['seqno'].transform('max')
    
    def assign_role(seqno, num_author):
        if seqno==1:
            return "F"
        elif seqno==num_author:
            return "L"
        else:
            return "M"
        
    df['role'] = df.apply(lambda x:assign_role(x.seqno, x.num_author),axis=1)
    return df


def select_df(intl, alpha, df):
    selected_df = df[(df.intl==intl)&(df.alpha.isin(alpha))]
    return selected_df[['ost_bk','cluster_id','cntry','role','year','dis']]


if __name__ == "__main__":
    pub_author_path = sys.argv[1]
    pub_info_path = sys.argv[2]
    
    pub_author_all_path = sys.argv[3]
    pub_author_intl_path = sys.argv[4]
    pub_author_intl_noalp_path = sys.argv[5]
    
    pub_author = pd.read_pickle(pub_author_path)
    pub_info = pd.read_pickle(pub_info_path)
    
    alpha_df = return_alpha(pub_author)
    intl_df = return_intl(pub_author)
    pub_author = return_role(pub_author)
    
    pub_info.loc[:,'ost_bk']=pub_info['ost_bk'].astype('int64')
    pub_info_meta = pub_info.merge(alpha_df,on='ost_bk')
    pub_info_meta = pub_info_meta.merge(intl_df,on='ost_bk')
    
    pub_author_all = pub_author.merge(pub_info_meta, on='ost_bk')
    pub_author_all.to_csv(pub_author_all_path, index=False)
    
    pub_author_intl = select_df(1,['single','alpha','noalp'], pub_author_all)
    pub_author_intl.to_csv(pub_author_intl_path, index=False)
    
    pub_author_intl_noalp = select_df(1,['noalp'], pub_author_all)
    pub_author_intl_noalp.to_csv(pub_author_intl_noalp_path, index=False)
    
    