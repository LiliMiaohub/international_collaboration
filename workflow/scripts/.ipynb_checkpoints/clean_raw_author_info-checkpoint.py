"""
This script cleans the demographic information of authors and generate the output file with:
cluster_id, gender, yfp(year of first publication), npub(number of publications in total)

author:Lili Miao
"""
import sys
import pandas as pd

if __name__ == "__main__":
    
    author_info_path = sys.argv[1]
    author_info_cleaned_path = sys.argv[2]
    
    author_info = pd.read_csv(author_info_path, sep=",")
    
    author_info = author_info.rename(columns={'YFP':'yfp','npapa':'npub'})
    
    author_info = author_info[['cluster_id','gender','yfp','npub']].dropna(subset=['cluster_id']).drop_duplicates()
    
    author_info['gender'] = author_info['gender'].fillna('U')
    author_info = author_info.replace(to_replace={'gender':{'m':'M','f':'F'}})
    
    author_info = author_info.drop_duplicates()
    
    author_info.loc[:,'cluster_id'] = author_info['cluster_id'].astype('int64')
    author_info.loc[:,'yfp'] = author_info['yfp'].astype('int64')
    author_info.loc[:,'npub'] = author_info['npub'].astype('int64')
    
    author_info.to_pickle(author_info_cleaned_path)