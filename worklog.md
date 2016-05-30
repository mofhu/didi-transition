# Worklog

## 20160527

First submission: all zero

## 20160529

Second submission: plan to use averages.

### Informations

    训练集中给出M市2016年连续三周的数据信息，需预测M市第四周和第五周中某五天的某些时间段的供需。测试集中给出了每个需预测的时间片的前半小时的数据信息，具体需预测的时间片见说明文件（说明文件含在数据集下载包内）。 具体数据如下，其中订单信息表、天气信息表和POI信息表为数据库中直接的表信息，而区域定义表、拥堵信息表是由数据库中其他表衍生的信息。

Training set: 20160101-20160121

Test set: 20160122, 24, 26, 28, 30; (time 46, 58, 70, 82, 94, 106, 118, 130, 142)

最终由于时间不够(deadline 11am), 只提交了 all 1 version.

继续用 pandas 洗数据:

- 先把 Order data 整理为 count data (sort by districts and time slices) `clean-data.ipynb` and `clean-order-data.py`
- 用 `cat *.tsv > NaN.csv` 整理为单个 csv 文件
- 再进一步整理为 average 时, 到了限时. 不确定提交的最终版本是 all 2 还是 all 10(10 is all average).

