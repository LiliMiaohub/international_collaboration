"""this script cleans the raw article file with replace column with new names, define data type and output the mapping between ost_bk and uid
"""
import pickle
import sys
import pandas as pd

if __name__ == "__main__":
    pub_path = sys.argv[1]
    clean_pub_path = sys.argv[2]
    id_map = sys.argv[3]
    
    pub_df = pd.read_csv(pub_path,sep="|",on_bad_lines='skip')
    
    pub_df.columns=['uid','ost_bk','year','dis','title']
    pub_df = pub_df.dropna(subset=['uid','ost_bk','year','dis'])
    
    pub_df.loc[:,'ost_bk'] = pub_df['ost_bk'].astype('int64')
    pub_df.loc[:,'year'] = pub_df['year'].astype('int64')
    pub_df.loc[:,'dis'] = pub_df['dis'].astype('int64')
    pub_df[['ost_bk','year','dis','title']].to_pickle(clean_pub_path)
    
    ostbk2uid = dict(zip(pub_df.ost_bk,pub_df.uid))
    with open(id_map,'wb') as pickle_file:
        pickle.dump(ostbk2uid, pickle_file)
