
# coding: utf-8

# In[45]:

import pandas as pd

from sklearn.metrics.scorer import make_scorer
import math


def MAPE_scorer(y, y_pred):
    error = 0
    num = len(y)
    for i in range(0, num):
        if y[i] > 0:
            error += math.fabs(y_pred[i] - y[i]) / y[i]
    #print('error, num:', error, num)
    if num > 0:
        return error / num
    else:
        return 0

my_scorer = make_scorer(MAPE_scorer)
# y = df['gap'][:21*66*144]
# MAPE_scorer(y, [1 for i in range(0, 21*66*144)])


def cal_dist(dist):
    global cv_pred_all, cv_real_all
    # split training, CV, test set
    df = pd.read_csv("data/season_1/features/"+ str(dist)+".csv")

    df["date"] = df["date"].apply(lambda x: pd.to_datetime(x, errors='coerce'))

    training = df.loc[(df.date < '2016-01-17') | (df.date == '2016-01-18')]

    training_time = training.loc[df.time_slice.isin([46, 58, 70, 82, 94, 106, 118, 130, 142])]

    cv = df.loc[df['date'].isin(['2016-01-17','2016-01-19','2016-01-20',
                                '2016-01-21'])]

    cv_time = cv.loc[df.time_slice.isin([46, 58, 70, 82, 94, 106, 118, 130, 142])]
    # only catch time slice in test set

    test = df.loc[(df['date'].isin(['2016-01-23','2016-01-27','2016-01-31']) &         df['time_slice'].isin([46, 58, 70, 82, 94, 106, 118, 130, 142]))
        |\
        (df['date'].isin(['2016-01-25','2016-01-29']) &\
            df['time_slice'].isin([58, 70, 82, 94, 106, 118, 130, 142]))]


    # In[126]:
    def modifier(y_pred):
        # print(y_pred)
        for i in range(len(y_pred)):
            if y_pred[i] < 1:
                y_pred[i] = 1
        #print(y_pred)
        return y_pred
    #modifier(list(y_training))

    from sklearn import linear_model
    y_test_all = []
    for time in [46, 58, 70, 82, 94, 106, 118, 130, 142]:
        training_ts = training_time.loc[training_time.time_slice == time]
        cv_ts = cv_time.loc[cv.time_slice == time]
        test_ts = test.loc[test.time_slice == time]
        X_training = training_ts.as_matrix(columns=[
                                    # 'is_workday',
                                    'gap_30min',
                                    'gap_20min',
                                    'gap_10min'])
        y_training = training_ts.as_matrix(columns=['gap']).ravel()
        X_cv = cv_ts.as_matrix(columns=[
                                    # 'is_workday',
                                    'gap_30min',
                                    'gap_20min',
                                    'gap_10min'])
        y_cv = cv_ts.as_matrix(columns=['gap']).ravel()
        X_test = test_ts.as_matrix(columns=[
                                    # 'is_workday',
                                    'gap_30min',
                                    'gap_20min',
                                    'gap_10min'])
        clf = linear_model.LinearRegression()
        clf.fit(X_training, y_training)
        #print(time, clf.score(X_training, y_training), clf.score(X_cv, y_cv),
        #     (MAPE_scorer(y_cv, clf.predict(X_cv))))
        #print(clf.coef_ ,clf.predict(X_test))
        MAPE_train = MAPE_scorer(y_training, modifier(clf.predict(X_training)))
        MAPE_cv = MAPE_scorer(y_cv, modifier(clf.predict(X_cv)))
        MAPE_1_train = MAPE_scorer(y_training, [1 for x in range(len(y_training))])
        MAPE_1_cv = MAPE_scorer(y_cv, [1 for x in range(len(y_cv))])
        """if MAPE_train > MAPE_1_train or MAPE_cv > MAPE_1_cv:
            print('dist {}, time_slice {}: train {:.2}, cv {:.2}'.format(dist, time,
                MAPE_train, MAPE_cv))
            print('dist {}, time_slice {}: baseline {:.2}, {:.2}'.format(dist, time,
                MAPE_1_train ,
                MAPE_1_cv ))
                """
        print(MAPE_cv, MAPE_1_cv)
        if MAPE_train >= MAPE_1_train:
            y_cv_pred = [1 for x in range(len(y_cv))]
            y_test = [1 for x in range(X_test.shape[0])]
        else:
            y_test = modifier(clf.predict(X_test))
            y_cv_pred = modifier(clf.predict(X_cv))

        #print(y_test)
        #print(modifier(y_test))
        cv_real_all += list(y_cv)
        cv_pred_all += list(y_cv_pred)
        y_test_all += list(y_test)

    test = test.sort_values(by=['time_slice','date'])
    test['y'] = y_test_all

    # test[['start_district_num','date','time_slice','y']].to_csv('pred' + str(dist) + '.csv')

cv_real_all = []
cv_pred_all = []
for dist in range(1, 67):
    cal_dist(dist)
    #print(cv_real_all, cv_pred_all)
    print(len(cv_real_all))
print(MAPE_scorer(cv_real_all, cv_pred_all))
print(MAPE_scorer(cv_real_all, [1 for i in range(len(cv_real_all))]))
