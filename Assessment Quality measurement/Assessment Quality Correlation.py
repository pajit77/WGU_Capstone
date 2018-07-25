# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 12:37:29 2018

@author: Pankaj
"""

#SIMULATING THE DATA  (results from BKT and competency scores from objective assessment)

import pandas as pd

studIds = ['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10']
topics = ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10']
learnObj = ['L1','L2','L3','L4','L5']
competency = ['C1','C2','C3']


studIds = pd.DataFrame(studIds)
studIds.columns = ['SID']
topics = pd.DataFrame(topics)
topics.columns = ['Topic']


studIds['key'] = 0
topics['key'] = 0

data = pd.merge(studIds, topics, on='key')
data.drop('key',1,inplace =True)



def topicObjMap(row):
    if row == 'T1':
        return 'L1'
    elif row == 'T2':
        return 'L2'
    elif row == 'T3':
        return 'L2'
    elif row == 'T4':
        return 'L3'
    elif row == 'T5':
        return 'L4'
    elif row == 'T6':
        return 'L4'
    else:
        return  'L5'


data['learnObj'] = data['Topic'].apply(topicObjMap)

def objCompMap(row):
    if row == 'L1':
        return 'C1'
    elif row == 'L2':
        return 'C2'
    else:
        return  'C3'

data['Competency'] = data['learnObj'].apply(objCompMap)


import decimal
import random
randList = list()
randList2 = list()

for i in range (0,data.shape[0],1):
    randList.append(float(decimal.Decimal(random.randrange(0, 100))/100))
    randList2.append(float(decimal.Decimal(random.randrange(0, 100))/100))




randList = pd.DataFrame(randList)
randList.rename(columns={0:'Mastery'},inplace=True)

randList2 = pd.DataFrame(randList2)
randList2.rename(columns={0:'competencyScore'},inplace=True)

randList3 =  randList2.join(randList)

data =  data.join(randList3)
compScore=data.groupby(['SID', 'learnObj'])['competencyScore'].mean()
compScore = pd.DataFrame(compScore)
compScore.reset_index(inplace=True)
data.drop('competencyScore',1,inplace=True)
data = pd.merge(data,compScore,left_on=['SID', 'learnObj'],right_on=['SID', 'learnObj'],how='left')


del randList
del randList2

import numpy as np


mask = ((data['SID'] == 'S1') | (data['SID'] == 'S1') | (data['SID'] == 'S2') |  (data['SID'] == 'S3'))
subset = data[mask]


def compNulls(row):
    if row['SID'] == 'S1':
        return np.nan
    elif row['SID'] == 'S2':
        return np.nan
    elif row['SID'] == 'S3':
        return np.nan
    elif row['SID'] == 'S4':
        return np.nan
    else:
        return  row['Mastery']


data['masteryScore1'] = data.apply(compNulls, axis=1)
meanMastery=data.groupby(['SID', 'learnObj'])['masteryScore1'].agg(np.mean)
meanMastery = pd.DataFrame(meanMastery)
meanMastery.reset_index(inplace=True)
meanMastery.rename(columns={'masteryScore1':'masteryMean'},inplace=True)


devMastery=data.groupby(['SID', 'learnObj'])['masteryScore1'].agg(np.std, ddof=0)
devMastery = pd.DataFrame(devMastery)
devMastery.reset_index(inplace=True)
devMastery.rename(columns={'masteryScore1':'masteryStd'},inplace=True)


dataMastery = pd.merge(meanMastery,devMastery,left_on=['SID', 'learnObj'],right_on=['SID', 'learnObj'],how='inner')
data = pd.merge(data,dataMastery,left_on=['SID', 'learnObj'],right_on=['SID', 'learnObj'],how='left')

data2 = data.groupby(['SID', 'learnObj']).first()

data2.dropna(inplace=True)
import matplotlib.pyplot as plt

plt.matshow(data2.corr())

print (data2.corr())

data2 = data.groupby(['SID', 'learnObj']).first()
data2.reset_index(inplace=True)



mask = (data2['masteryScore1'].isnull()) 
nonTakers = data2[mask]
takers = data2.dropna()

#takers.columns
nonTakers = nonTakers.groupby(['learnObj'])['competencyScore'].agg(np.mean)
takers = takers.groupby(['learnObj'])['competencyScore'].agg(np.mean)


# Testing for statistical difference between students who took the formative assessment vs those who didn't 


from scipy import stats

t2, p2 = stats.ttest_ind(nonTakers,takers)
print("t = " + str(t2))
print("p = " + str(2*p2))









