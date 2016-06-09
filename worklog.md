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


## 20160531

提交三周 weekly average: 

`20160531, a142475, weekday average, 0.491462`

效果比全1预测差很多, 也就比预想差很多, 猜测是因为评判指标对偏高的预测惩罚严重 (如 y=1 而 y_pred = 10 时, 惩罚是 9/1 ).

后续思路是微调, 看看能否通过调整预测明显提高得分.

## 20160601

`20160601, 4a828f8, (if<5, then =1; else = average), 0.385906`

微调后有明显改善, 说明确实可能因大量高估被惩罚得比较严重. 不过仍然不如全1

## 20160602

`20160602, 6612639, half weekday average(0 to 1), 0.420103`

改用 0.5 * average 预测. 比 average 好, 但提升不大

## 20160604

`20160604, d7e4e44,(if<20, then =1; else = average) , 0.385778`

进一步提高预测门槛, 提升也很有限.

## 20160607

`20160607, 3a2e088, filter rule , 0.345423`

改用 filter rule 写预测, 全部比均值调低, 希望可以超过全1. 结果比全1(0.368782)有一定的提升, 但很有限. 要注意到目前的晋级线在 0.26 左右.

- [0, 4]: 1
- [5, 6]: 2
- [7, 20]: 5
- [21, 50]: 10
- [51, 99]: 20
- [100, 200]: 50
- [201, inf]: 100

## 20160608

决定用这周在训练集继续尝试, 如果效果好 (100-200), 则下周更新数据后冲前50; 否则考虑提前撤.

继续洗数据: 先洗成所有区域的时间段信息, order_count, gap

commit: `f6aa188`

## 20160609

### 统计大致情况

total: 

order_count | 9.10m  
gap | 1.62m

outliers:

- district 51 一个区就有 1.42m 订单 (15.6%)
- 不同区域的 succ_ratio 差别不小

### 可视化与初步思路

### CV 集打分脚本

### 预测算法