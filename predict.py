# -*- coding: utf-8 -*-

"""Predict output script.

"""

# Author: Mo Frank Hu (mofrankhu@gmail.com)
# Dependency: Python 3, pandas
import pandas as pd

def main():
    pred_time_slices = open('data/season_1/test_set_2/read_me_2.txt')
    all_time_slices = []
    for line in pred_time_slices:
        if '2016' in line:
            all_time_slices.append(line[:-1])
    #print(all_time_slices)
    #print(len(all_time_slices))

    df = pd.DataFrame({'start_dist_num':[], 'time_slice':[], 'y_pred': []})
    for i in range(0, 66):
        dist_num = i + 1
        dist_df = pd.DataFrame({'start_dist_num':[dist_num] * len(all_time_slices),
                                'time_slice': all_time_slices,
                                'y_pred': [1] * len(all_time_slices)
                                })
        #print(dist_df)
        df = df.append(dist_df, ignore_index=True)
        #print(df)
        #break
    #print(df)
    df.start_dist_num = df.start_dist_num.astype(int)
    #print(df)
    df.to_csv('20160612.csv',index=False, header=False)
main()

