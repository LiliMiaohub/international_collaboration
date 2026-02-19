"""this script selects publications that are collaborated between different scientific capacity groups
"""

import pandas as pd
import sys

if __name__ =="__main__":
    
    pub_author_path = sys.argv[1]
    stgroup_path = sys.argv[2]
    filtered_pub_path = sys.argv[3]
    
    pub_author_df=pd.read_csv(pub_author_path)
    
    stgroup_df = pd.read_csv(stgroup_path)
    stgroup_df = stgroup_df.drop_duplicates()
    
    pub_author_df = pub_author_df.merge(stgroup_df, left_on='cntry', right_on='Code', how='left')
    pub_author_df['unique_group'] = pub_author_df.groupby(['ost_bk'])['class'].transform('nunique')
    filtered_df = pub_author_df[pub_author_df.unique_group!=1]
    
    filtered_df.to_csv(filtered_pub_path, index=False)