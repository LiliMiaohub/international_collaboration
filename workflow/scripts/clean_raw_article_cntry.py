"""this script cleans the raw article country file with:
1. remove publications with any of the seq_no is nan
2. remove publications without first author
3. remove publications with incomplete author information
4. keep the first affiliation for multi-affiliation cases
5. replace the country name derived from wos to code
"""
import sys
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def return_pub_with_nan(df):
    ids = df[df.isna().any(axis=1)].OST_BK.unique()
    logger.info('{} of papers have NaN values'.format(len(ids)))
    
    return df[~df.OST_BK.isin(ids)]

def return_pub_with_first(df, total):
    '''return articles with first authors'''
    withfirst = df[df.Seq_No==1].OST_BK.unique()
    logger.info('{} of papers have first author assigned'.format(len(withfirst)/total))
    
    return df[df.OST_BK.isin(withfirst)]

def return_pub_with_author(pub_df, author_df, total):
    merged_df = pub_df.merge(author_df, on=['OST_BK','Seq_No'], how='left')
    invalid_ids = merged_df[merged_df.cluster_id.isna()|merged_df.Last_Name.isna()].OST_BK.unique()
    valid_df = merged_df[~merged_df.OST_BK.isin(invalid_ids)]
    logger.info('{} of papers have incomplete author information'.format(len(invalid_ids)/total))
    
    return valid_df

def remove_multi_affiliation(df):
    new_df = df.sort_values(by=['OST_BK','Seq_No','Addr_No']
                           ).drop_duplicates(subset=['OST_BK','Seq_No'],keep='first')
    
    return new_df

def replace_cntry_name_dropna(df, name2code):
    df['cntry'] = df['Country'].map(name2code)
    invalid_ids = df[df.cntry.isna()].OST_BK.unique()
    logger.info('countries without iso-3 code: {}'.format(df[df.cntry.isna()].Country.unique()))
    
    return df[~df.OST_BK.isin(invalid_ids)]

if __name__ == "__main__":
    cntry_path = sys.argv[1]
    author_path = sys.argv[2]
    name2code_path = sys.argv[3]
    cntry_cleaned_path = sys.argv[4]
    
    
    cntry_raw = pd.read_csv(cntry_path, sep="|", on_bad_lines='skip', dtype={'OST_BK':'int64','Seq_No':'float64'})
    author_info = pd.read_csv(author_path, sep=",", on_bad_lines='skip', dtype={'OST_BK':'int64','Seq_No':'float64'})
    name2code_df = pd.read_csv(name2code_path).dropna()
    name2code_dict = dict(zip(name2code_df.cntry,name2code_df['Code']))
    
    pub_total_raw = len(cntry_raw.OST_BK.unique())
    logger.info('{} number of pubs in raw data'.format(pub_total_raw))
    
    cntry_df= return_pub_with_nan(cntry_raw)
    
    cntry_df = return_pub_with_first(cntry_df, pub_total_raw)
    
    cntry_df = return_pub_with_author(cntry_df, author_info, pub_total_raw)
    
    cntry_df = remove_multi_affiliation(cntry_df)
    
    cntry_df = replace_cntry_name_dropna(cntry_df, name2code_dict)
    
    cntry_df.rename(columns={'OST_BK':'ost_bk','Seq_No':'seqno', 'Last_Name':'lastname'}, inplace=True)
    cntry_df.loc[:,'seqno'] = cntry_df['seqno'].astype('int64')
    cntry_df.loc[:,'cluster_id'] = cntry_df['cluster_id'].astype('int64')
    
    logger.info('{}({}) papers are kept in the analysis'.format(len(cntry_df.ost_bk.unique()),len(cntry_df.ost_bk.unique())/pub_total_raw))
    
    cntry_df[['ost_bk','seqno','cluster_id','lastname','cntry']].to_pickle(cntry_cleaned_path)
    
    