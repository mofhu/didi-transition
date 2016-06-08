# -*- coding: utf-8 -*-

"""Clean order data and group by datetime and district.

"""

# Author: Mo Frank Hu (mofrankhu@gmail.com)
# Dependency: Python 3, pandas

import pandas as pd
import re

def process(file_name, output_file_name):

    df = pd.read_csv(file_name)
    cluster_map = pd.read_table("data/season_1/training_data/cluster_map/cluster_map.tsv",
                                header=None,
                                names=["start_district_hash", "start_district_num"])

    df = pd.merge(cluster_map, df, on='start_district_hash')

    i = 1
    dist_nums = []
    for i in range(1, 67):
        dist_nums += [i] * 144

    all_time_slices = pd.DataFrame({'start_district_num': dist_nums,
                                    'time_slice': list(range(1,145)) * 66})

    combined = pd.merge(all_time_slices, df, how='left', on=["start_district_num", "time_slice"])
    # SQL-like join (left join)

    combined = combined.fillna(value=0)
    combined["date"] = "-".join(re.findall("\d+", file_name)[1:])

    print(output_file_name)
    combined.to_csv(output_file_name, index=False, columns=['start_district_num','time_slice',
                                        'date','order_count',
                                        'succeed_count','gap'])
    # ignore index and dist_hash

def main():
    order_data_folder = 'data/season_1/training_data/order_data/groupby/'
    import os
    for day in os.listdir(order_data_folder):
        if '2016' in day and 'all' not in day:
            print(day)
            file_name = order_data_folder + day
            output_file_name = order_data_folder + day + '_all.csv'
            process(file_name, output_file_name)

if __name__ == "__main__":
    main()
