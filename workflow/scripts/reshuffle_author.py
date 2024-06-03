"""This script gets the expected authorship number by reshuffling author order within each paper

Author: Lili Miao
"""

import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from random import shuffle
import sys

def reshuffle_author(df, n):
    
    result_df = []
    
    def shuffle_author(df):
        result=[]
        for row in df.values:
            ost_bk, year, dis, cntrylist = row
            cntrylist = np.random.permutation(cntrylist)
            result.extend([
                [ost_bk,year,dis,cntrylist[0],'F'],
                [ost_bk,year,dis,cntrylist[1],'L']
            ])
            result.extend([[ost_bk, year, dis, item,'M'] for item in cntrylist[2:]])
        return result
        
    
    
    for i in tqdm(range(n)):
        shuffled_data = shuffle_author(df)
        result_df.extend(shuffled_data)
        
    result_df = pd.DataFrame(result_df, columns=['id','year','dis','cntry','role'])
    
    return result_df

if __name__ == "__main__":
    pub_author_path = sys.argv[1]
    #pub_author_shuffled_path = sys.argv[2]
    pub_author_expected_path = sys.argv[2]
    
    n = 20 #number of times for reshuffling
    pub_author = pd.read_csv(pub_author_path)
    
    cntrys_df=pub_author.groupby(['ost_bk','year','dis'])['cntry'].apply(list).reset_index()
    
    reshuffled_df = reshuffle_author(cntrys_df, n)
    #reshuffled_df.to_pickle(pub_author_shuffled_path) #commented out due to the endless running time
    
    expected_df = reshuffled_df.groupby(['cntry','year','dis','role']).size().reset_index(name='expected')
    expected_df['expected'] = expected_df['expected']/n
    expected_df.to_csv(pub_author_expected_path, index=False)