"""This script calculates the expected and raw number of occurrence between first-last country pair
"""
import pandas as pd
import numpy as np
import itertools
from tqdm import tqdm
import random
import sys

def generate_expectation(df, n):
    
    expect_res = pd.DataFrame()
    
    def random_shuffling(df):
        reshuffle_res = []
        for row in df.values:
            pub_id = row[0]
            year = row[1]
            cntrys = row[3]
            first, last = random.sample(cntrys, 2)
            reshuffle_res.append([pub_id, year, first, last])
            
        reshuffle_res = pd.DataFrame(reshuffle_res, columns=['ost_bk','year','first','last'])
        reshuffle_res = reshuffle_res.groupby(['year','first','last']).size().reset_index(name='exp')
        return reshuffle_res
    
    for _ in tqdm(range(n)):
        reshuffle_res = random_shuffling(df)
        expect_res = pd.concat([expect_res, reshuffle_res])
    
    expect_res = expect_res.groupby(['year','first','last'])['exp'].sum().reset_index()
    expect_res['exp'] = expect_res['exp']/n
    return expect_res

    
if __name__ == "__main__":
    
    pub_author_path = sys.argv[1]
    pair_expect_path = sys.argv[2]
    
    pub_author = pd.read_csv(pub_author_path)
    
    pub_cntrys = pub_author.groupby(['ost_bk','year','dis'])['cntry'].apply(list).reset_index()
    
    exp_df = generate_expectation(pub_cntrys, 100)
    
    exp_df.to_csv(pair_expect_path, index=False)
