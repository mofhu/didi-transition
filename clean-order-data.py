# -*- coding: utf-8 -*-

"""Clean order data and group by datetime and district.

"""

# Author: Mo Frank Hu (mofrankhu@gmail.com)
# Dependency: Python 3, pandas

import pandas as pd

def process(file_name, output_file_name):
    order_data = pd.read_table(file_name, header=None,
                               names=[
                                        'order_id', 'driver_id', 'passenger_id',
                                        'start_district_hash', 'dest_district_hash',
                                        'price', 'time'
                                    ])
    # use pd.read_table() to read from tab-separated files.
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_table.html

    # use pd.isnull() to judge if value is NaN
    # (" = np.NaN" just not work, don't know why)

    order_data[['date', 'time']] = order_data.time.str.extract('([^ ]+) ([0-9:]+)', expand=False)
    order_data.loc[:, 'time_slice'] = order_data.loc[:, 'time'].apply(
        lambda x: int(x[:2])*6 + int(x[3]) + 1
    )
    # calculate time slices (1-144, 10-min a slice)

    output = order_data.groupby(['date','start_district_hash','time_slice']).count().iloc[:,:2]
    # print(output) # test output
    # NaN will not be count, so we got succeed orders from groupby driver_id.
    output.columns = ["order_count", "succeed_count"]
    output["gap"] = output["order_count"] - output["succeed_count"]

    output.to_csv(output_file_name)

    # order_data_nan = order_data.loc[lambda order_data: pd.isnull(order_data.driver_id) == True, :]
    # output = order_data_nan.groupby(['date','start_district_hash','time_slice']).count()
    # print(output) # test output
    # output.to_csv(output_file_name)

def main():
    order_data_folder = 'data/season_1/training_data/order_data/'
    import os
    for day in os.listdir(order_data_folder):
        if '2016' in day:
            print(day)
            file_name = order_data_folder + day
            output_file_name = order_data_folder + 'groupby/' + day
            process(file_name, output_file_name)

if __name__ == "__main__":
    main()
