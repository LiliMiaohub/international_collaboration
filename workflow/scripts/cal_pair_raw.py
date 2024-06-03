import pandas as pd
import numpy as np
import itertools
from tqdm import tqdm
import random
import sys

def derive_raw_count(pub_author):
    
    first_last_df = pub_author[pub_author['role']!='M']
    first_last_df = first_last_df.pivot(index=['ost_bk','year'], columns=['role'], values='cntry').reset_index()
    raw_df = first_last_df.groupby(['year','F','L']).size().reset_index(name='raw')
    raw_df = raw_df.rename(columns={'F':'first','L':'last'})
    return raw_df

if __name__ == "__main__":
    
    pub_author_path = sys.argv[1]
    pub_pair_raw_path = sys.argv[2]
    
    pub_author = pd.read_csv(pub_author_path)
    
    raw_df = derive_raw_count(pub_author)
    raw_df.to_csv(pub_pair_raw_path, index=False)
    
    
    
    
     
        