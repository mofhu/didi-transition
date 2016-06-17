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

#### total

order_count | 9.10m  
gap | 1.62m

#### outliers

- 51 一个区就有 1.42m 订单 (15.6%)
- 不同区域的 succ_ratio 差别很大 (即使在总订单排名靠前的区域也4%-20%不等)
- 选择 51(最多订单和gap), 8(第二多gap), 1(订单靠前区域中的 gap 极低) 大致先看

### 可视化与初步思路

#### district first look

##### 51

time_slice: 主要 gap 高峰在晚上 (~18:00 & ~22:00)  
需求是尖峰, 供给则平缓得多, gap 的趋势和需求一致.

date: 01 异常高值; 11, 15, 16, 19, 20需求稍高于其它日子(但未发现规律)

##### 8

time_slice: 主要 gap 高峰在早晚 (~9:00 & ~18:00)  
需求是尖峰, 供给则平缓得多, gap 的趋势和需求一致;  
早高峰能看到一个供给的时间后移.

只在早高峰有明显的 gap peak; 其它时间几乎没有 gap.

date: 01, 11, 21 需求稍高于其它日子; 51 和 8 中的 规律对于 1 似乎没用.

##### 1

time_slice: 主要 gap 高峰在早上 (~9:00)  
需求是尖峰, 供给则平缓得多, gap 的趋势和需求一致.

date: 01 的变化不如 dist_51 明显; 11, 15, 16, 19, 20需求也稍高于其它日子(但未发现规律)

##### insights

plot max gaps: 更多的感觉是 outliers 占比例很大.

demand/supply 可能都相对好处理, 但微小的波动就会引起 gap 的极大变化; 有必要同时预测三者!

如何发现异常天的特征, 处理之; 或通过 -30min 的数据预测异常值, 都是需要考虑的思路.

### CV 集打分脚本

迅速实现了整合到 sklearn 的一个打分函数 (commit `f45fea3`). 

### 预测算法

全1预测(baseline) @ 0612

0613 outline

- split test and training set
- try easy ML algorithms (MAPE score)
- fast submission
- plot predict vs real y

0613 submission: average gap, but no 0->1 modification

### split training set and CV/test set locally

- split training CV set: pandas .loc and isin() work well (`split-sets.ipynb`)
- baseline on cv days: all 1 is 0.347 (online baseline 0.353)

### 添加 feature

用 pandas 添加 

- 30/20/10 min 的 order/gap 数据到特征集. (`96f5180`)
- is_weekday

- RF / SVM 的效果都不好. CV MAPE在0.43左右

- 改用线性模型测试

前面的一大 bug 是误用了 order_count 和 succeed_count 进行训练.

只用 6+2 个特征训练, 得到的 gap 波动较大 (dist 51) 

### 20160617 predict

只有两次提交机会, 目前成绩与 top 50 的预期相差甚远.

整理数据用 MAPE 本地测试, 在0617测试baseline, 0618 发掘新特征最后冲一下.

思路:

- 先人工预测看看感觉, 是否能有效估计 QC
- grid search 等方法分开模型预测 (类似 NB) 重点是要用 MAPE 作为评估指标
- cv result

#### 人工预测 & 研究趋势

dist51:

time slice 94 很有意思: 波动极大; 相对来说 succeed 比较稳定, order 则不那么稳定; 

整体只用 gap_10 最小二乘 基本上在 y = x 附近

初步测试 简单线性拟合 (min R2) 后的结果与 baseline 比较: 感觉很有前景

~~~
time_slice 46: train 1.1, cv 0.77
time_slice 46: baseline 0.88, 0.97
time_slice 58: train 0.51, cv 0.29
time_slice 58: baseline 0.84, 0.82
time_slice 70: train 0.23, cv 0.54
time_slice 70: baseline 0.89, 0.93
time_slice 82: train 0.25, cv 0.42
time_slice 82: baseline 0.94, 0.96
time_slice 94: train 1.4, cv 0.56
time_slice 94: baseline 0.96, 0.99
time_slice 106: train 0.29, cv 0.72
time_slice 106: baseline 0.99, 0.98
time_slice 118: train 0.28, cv 0.47
time_slice 118: baseline 0.95, 0.97
time_slice 130: train 0.29, cv 0.23
time_slice 130: baseline 0.99, 1.0
time_slice 142: train 0.39, cv 1.6
time_slice 142: baseline 0.97, 0.95
~~~

#### custom scorer in linear reg

很重要, 但是实现起来比较困难. 可能 17 日来不及.

先写一个简单的 modifier 把已有的预测稍修改: 如 pred < 0 则改为 1. 

修改后, 略有提升

~~~
time_slice 46: train 0.9, cv 0.77
time_slice 46: baseline 0.88, 0.97
time_slice 58: train 0.51, cv 0.29
time_slice 58: baseline 0.84, 0.82
time_slice 70: train 0.23, cv 0.54
time_slice 70: baseline 0.89, 0.93
time_slice 82: train 0.25, cv 0.42
time_slice 82: baseline 0.94, 0.96
time_slice 94: train 1.4, cv 0.56
time_slice 94: baseline 0.96, 0.99
time_slice 106: train 0.29, cv 0.72
time_slice 106: baseline 0.99, 0.98
time_slice 118: train 0.28, cv 0.47
time_slice 118: baseline 0.95, 0.97
time_slice 130: train 0.29, cv 0.23
time_slice 130: baseline 0.99, 1.0
time_slice 142: train 0.39, cv 0.68
time_slice 142: baseline 0.97, 0.95
~~~

增加一个 outlier detect 功能:

打印出 train/cv > baseline (all 1) 的集合, 便于手工弥补

选择了简单策略:

- 在 cv error > all 1 error时, 用 all 1 替代 拟合
