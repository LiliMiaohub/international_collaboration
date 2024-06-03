import pandas as pd
import numpy as np
import itertools
from tqdm import tqdm
import random
import sys

def generate_expectation(df, n, position):
    
    expect_res = pd.DataFrame()
    
    def random_shuffling(df):
        reshuffle_res = []
        for row in df.values:
            pub_id = row[0]
            year = row[1]
            cntrys = row[3]
            if position=='last':
                #Fixed first author, sample for last author
                first = cntrys[0]
                last = random.sample(cntrys[1:], 1)[0]
            else: 
                #Fixed last author, sample for first author
                last = cntrys[-1]
                first = random.sample(cntrys[:-1], 1)[0]
                
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
    
    pub_path = sys.argv[1]
    fixed_first_path = sys.argv[2]
    fixed_last_path = sys.argv[3]
    
    pub_df = pd.read_csv(pub_path)
    pub_cntrys = pub_df.groupby(['ost_bk','year','dis'])['cntry'].apply(list).reset_index()
    
    fixed_first_exp = generate_expectation(pub_cntrys, 100, 'last')
    fixed_first_exp.to_csv(fixed_first_path, index=False)
    
    fixed_last_exp = generate_expectation(pub_cntrys, 100, 'first')
    fixed_last_exp.to_csv(fixed_last_path, index=False)
    
    