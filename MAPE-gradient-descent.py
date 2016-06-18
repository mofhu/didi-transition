# coding: utf-8

import pandas as pd
import numpy as np
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
    test = df.loc[(df['date'].isin(['2016-01-23','2016-01-27','2016-01-31']) & df['time_slice'].isin([46, 58, 70, 82, 94, 106, 118, 130, 142]))
        |\
        (df['date'].isin(['2016-01-25','2016-01-29']) &\
            df['time_slice'].isin([58, 70, 82, 94, 106, 118, 130, 142]))]

    def modifier(y_pred):
        # print(y_pred)
        for i in range(len(y_pred)):
            if y_pred[i] < 1:
                y_pred[i] = 1
        #print(y_pred)
        return y_pred

    y_test_all = []
    for time in [46, 58, 70, 82, 94, 106, 118, 130, 142]:
    # for time in [70]:
        training_ts = training_time.loc[training_time.time_slice == time]
        cv_ts = cv_time.loc[cv.time_slice == time]
        test_ts = test.loc[test.time_slice == time]
        X_training = training_ts.as_matrix(columns=[
                                    # 'is_workday',
                                    # 'gap_30min',
                                    # 'gap_20min',
                                    'gap_10min'])
        y_training = training_ts.as_matrix(columns=['gap']).ravel()
        X_cv = cv_ts.as_matrix(columns=[
                                    # 'is_workday',
                                    # 'gap_30min',
                                    # 'gap_20min',
                                    'gap_10min'])
        y_cv = cv_ts.as_matrix(columns=['gap']).ravel()
        X_test = test_ts.as_matrix(columns=[
                                    # 'is_workday',
                                    # 'gap_30min',
                                    # 'gap_20min',
                                    'gap_10min'])
        beta = MAPE_gradient_descent(training_ts, y_training)
        pred_cv = modifier(predict(X_cv, beta))
        # print(y_cv, pred_cv)
        # print('cv MAPE', MAPE_scorer(y_cv, pred_cv))
        # print('cv baseline', MAPE_scorer(y_cv, [1 for i in range(len(y_cv))]))
        # print(X_training)
        # print(y_training)
        # return training_ts, y_training
        # input(time)
        pred_test = predict(X_test, beta)
        cv_real_all += list(y_cv)
        cv_pred_all += list(pred_cv)
        y_test_all += list(modifier(pred_test))

    test = test.sort_values(by=['time_slice','date'])
    test['y'] = y_test_all

    test[['start_district_num','date','time_slice','y']].to_csv('pred' + str(dist) + '.csv')



def MAPE_gradient_descent(training_ts, y_ts):

    iterations = 500
    alpha = 0.005

    ## Add a columns of 1s as intercept to X. This becomes the 2nd column
    X_df = training_ts['gap_10min']
    X = np.ones((2, np.array(X_df).size))
    X[:-1,:] = np.array(X_df)
    # print(X)
    ## Transform to Numpy arrays for easier matrix math
    ## and start beta at 0, 0
    # X = np.array(X_df)
    y = y_ts.ravel()
    beta = np.array([0, 0])
    m, b = beta # m-slope, b-intercept

    def cost_function(X, y, beta):
        """
        cost_function(X, y, beta) computes the cost of using beta as the
        parameter for linear regression to fit the data points in X and y
        """
        ## number of training examples
        J_MAPE = MAPE_scorer(y, X.T.dot(beta))
        return J_MAPE

    # cost_function(X, y_ts,beta)

    def gradient_descent(X, y, theta, alpha, iterations):
        """
        gradient_descent() performs gradient descent to learn theta by
        taking num_iters gradient steps with learning rate alpha
        """
        beta = theta

        for iteration in range(iterations):
            m,b = beta
            beta0 = beta
            cost0 = cost_function(X,y_ts,beta)
            gm = 0
            gb = 0
            for i in range(X.shape[1]):
                # cal gradient
                xi = X[0,i]
                yi = y[i]
                #print(xi, yi)
                if yi > 0:
                    gm += (2 * (xi**2) * m + 2 *xi *(b-yi)) / (yi**2)
                    gb += (2 * b + 2*(m *xi -yi)) / (yi**2)
                #print(gm,gb)
            beta = (m-gm*alpha, b-gb*alpha)
            cost1 = cost_function(X,y_ts,beta)
            if cost1 > cost0:
                # print('iter', iteration, cost0, cost1)
                return beta0
            # print(cost_function(X,y_ts,beta))

        return beta
    # print(cost_function(X, y_ts,beta))
    beta = gradient_descent(X, y, beta, alpha, iterations)
    # print(beta)
    # print(cost_function(X, y_ts,beta))
    return beta


def predict(X, beta):
    """Predict by linear regression."""
    # print(X.size)
    X1 = np.ones((2, X.size))
    X1[:-1,:] = np.array(X.T)
    # print(X1)

    return X1.T.dot(beta)



cv_real_all = []
cv_pred_all = []

for dist in range(1, 67):
    cal_dist(dist)
    #print(cv_real_all, cv_pred_all)
    print(len(cv_real_all))
    # input()
print(MAPE_scorer(cv_real_all, cv_pred_all))
print(MAPE_scorer(cv_real_all, [1 for i in range(len(cv_real_all))]))

