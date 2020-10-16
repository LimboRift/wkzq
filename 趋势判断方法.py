# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:30:31 2019

@author: Lenovo
"""

import pandas as pd 
import numpy as np
from copy import deepcopy
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import math
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as ts
from sklearn import preprocessing
from sklearn import linear_model
from scipy.stats import pearsonr
from scipy import stats
from statsmodels.tsa.arima_model import ARIMA
from sklearn.decomposition import PCA
  #%%
print ('----- 取数据 -----')
read_path = "data\\"
data=pd.read_excel(read_path+'黄金分割.xlsx')
#data=pd.read_excel(read_path+'利率走廊1.xlsx')
#data.fillna(method='ffill', axis = 0 ,inplace = True)
#series=deepcopy(data.ix[:,0])
#trend=deepcopy(data.ix[:,0])
#trend[:]=np.nan
#sig=deepcopy(data.ix[:,0])
#sig[:]=np.nan
#newtrend=deepcopy(data.ix[:,0])
#newtrend[:]=np.nan
#for i in np.arange(60,len(series)):
#    max1=series[i-60:i].max()
#    min1=series[i-60:i].min()
#    ##下跌趋势中
#    if(series[series==max1].index[0]<series[series==min1].index[0]):
#        trend[i]=-1
#        if((series[i]-min1)/(max1-min1)>0.628):
#            sig[i]=1
#            newtrend[i]=1
#        else:
#           
#            newtrend[i]=-1            
#
#    ##上涨趋势中
#    if(series[series==max1].index[0]>series[series==min1].index[0]):
#        trend[i]=1
#        if((max1-series[i])/(max1-min1)>0.628):
#            sig[i]=1
#            newtrend[i]=-1 
#        else:
#           
#            newtrend[i]=1             
#            
#data.ix[:,'原趋势']=trend
#data.ix[:,'是否反转']=sig
#data.ix[:,'现趋势']=newtrend
#data.to_excel('黄金分割结果-2个月.xlsx')
   
#%%周度
n=0
m=0.1
def trend(n,m):
    read_path = "data\\"
    data=pd.read_excel(read_path+'黄金分割周度.xlsx')
    data.fillna(method='ffill', axis = 0 ,inplace = True)
    series=deepcopy(data.ix[:,n])
    trend=deepcopy(data.ix[:,n])
    trend[:]=np.nan
    sig=deepcopy(data.ix[:,n])
    sig[:]=np.nan
    upsig=deepcopy(data.ix[:,n])
    upsig[:]=np.nan
    dsig=deepcopy(data.ix[:,n])
    dsig[:]=np.nan
    newtrend=deepcopy(data.ix[:,n])
    newtrend[:]=np.nan
    N=8
    for i in np.arange(N,len(series)):
        max1=series[i-N:i+1].max()
        min1=series[i-N:i+1].min()
        ##下跌趋势中
        if(series[series==max1].index[0]<series[series==min1].index[0]):
            trend[i]=-1
            if(trend[i-1]==1):
                sig[i]=1
                dsig[i]=1
            if((series[i]-min1)/(max1-min1)>0.628):
                sig[i]=1
                upsig[i]=1
                newtrend[i]=1
            else:
               
                newtrend[i]=-1            
    
        ##上涨趋势中
        if(series[series==max1].index[0]>series[series==min1].index[0]):
            trend[i]=1
            if(trend[i-1]==-1):
                sig[i]=1 
                upsig[i]=1
            if((max1-series[i])/(max1-min1)>0.628):
                sig[i]=1
                dsig[i]=1
                newtrend[i]=-1 
            else:
               
                newtrend[i]=1             
                
    data.ix[:,'原趋势']=trend
    data.ix[:,'是否反转']=sig
    data.ix[:,'向上反转']=upsig
    data.ix[:,'向下反转']=dsig
    data.ix[:,'现趋势']=newtrend
    
    data.ix[:,'现趋势涨幅修正']=deepcopy(data.ix[:,'现趋势'])
    
    N1=4
    for i in np.arange(100,len(data)):
        if(data.ix[i,'现趋势涨幅修正']==1):
            now=data.ix[i,n]/(data.ix[i-N1+1:i+1,n]).min()-1
          
            maxl=list()
            for j in np.arange(N1,i):
                x=data.ix[j-N1:j,'现趋势涨幅修正']
                if(len(x[x==1])==N1):
                    maxl.append(data.ix[j-N1:j,n].max()/data.ix[j-N1:j,n].min()-1)
            if(now<np.quantile(maxl,m)):
                data.ix[i,'现趋势涨幅修正']=data.ix[i-1,'现趋势涨幅修正']
        if(data.ix[i,'现趋势涨幅修正']==- 1):
            now=data.ix[i,n]/(data.ix[i-N1+1:i+1,n]).max()-1
            minl=list()
            for j in np.arange(N1,i):
                x=data.ix[j-N1:j,'现趋势涨幅修正']
                if(len(x[x==-1])==N1):
                    minl.append(data.ix[j-N1:j,n].min()/data.ix[j-N1:j,n].max()-1)
            if(now>np.quantile(minl,1-m)):
                data.ix[i,'现趋势涨幅修正']=data.ix[i-1,'现趋势涨幅修正']                
            
    
    data.ix[:,'现趋势修正']=deepcopy(data.ix[:,'现趋势涨幅修正'])
    for i in np.arange(1,len(data)-3):
        
        if(data.ix[i-1,'现趋势修正']+data.ix[i,'现趋势修正']==0 and data.ix[i,'现趋势修正']+data.ix[i+1,'现趋势修正']==0):
            data.ix[i,'现趋势修正']=data.ix[i-1,'现趋势修正']
        if(data.ix[i-1,'现趋势修正']+data.ix[i,'现趋势修正']==0 and data.ix[i,'现趋势修正']-data.ix[i+1,'现趋势修正']==0 and data.ix[i+2,'现趋势修正']+data.ix[i+1,'现趋势修正']==0):
            data.ix[i,'现趋势修正']=data.ix[i-1,'现趋势修正']
            data.ix[i+1,'现趋势修正']=data.ix[i-1,'现趋势修正']
        if(data.ix[i-1,'现趋势修正']+data.ix[i,'现趋势修正']==0 and data.ix[i,'现趋势修正']-data.ix[i+1,'现趋势修正']==0 and data.ix[i,'现趋势修正']-data.ix[i+2,'现趋势修正']==0 and data.ix[i+3,'现趋势修正']+data.ix[i+2,'现趋势修正']==0):
            data.ix[i,'现趋势修正']=data.ix[i-1,'现趋势修正']
            data.ix[i+1,'现趋势修正']=data.ix[i-1,'现趋势修正']        
            data.ix[i+2,'现趋势修正']=data.ix[i-1,'现趋势修正']          
    #data.to_excel('黄金分割周度修正-8周-股票.xlsx')
    
    #%%转月度
    data1=pd.read_excel(read_path+'黄金分割月度.xlsx')
    data1.ix[:,'黄金分割趋势判断']=np.nan
    for i in range(len(data1)):
        year=data1.index[i].year
        month=data1.index[i].month 
        result=data.ix[data.index.year==year,]
        data1.ix[i,'黄金分割趋势判断']=result.ix[result.index.month==month,'现趋势修正'][-1]
    
    data1.ix[:,'趋势修正']=deepcopy(data1.ix[:,'黄金分割趋势判断'])
    for i in np.arange(1,len(data1)-2):
        
        if(data1.ix[i-1,'趋势修正']+data1.ix[i,'趋势修正']==0 and data1.ix[i,'趋势修正']+data1.ix[i+1,'趋势修正']==0):
            data1.ix[i,'趋势修正']=data1.ix[i-1,'趋势修正']
        if(data1.ix[i-1,'趋势修正']+data1.ix[i,'趋势修正']==0 and data1.ix[i,'趋势修正']-data1.ix[i+1,'趋势修正']==0 and data1.ix[i+2,'趋势修正']+data1.ix[i+1,'趋势修正']==0):
            data1.ix[i,'趋势修正']=data1.ix[i-1,'趋势修正']
            data1.ix[i+1,'趋势修正']=data1.ix[i-1,'趋势修正']
    return data1.ix[:,'趋势修正']
#data1.to_excel('黄金分割周度转月度-8周-股票.xlsx')
data1=pd.read_excel(read_path+'黄金分割月度.xlsx')     
data1.ix[:,'股票趋势判断']=trend(0,0.5)
data1.ix[:,'商品趋势判断']=trend(1,0.5)
data1.ix[:,'债券趋势判断']=trend(2,0.1)
data1.ix[:,'短端债券趋势判断']=trend(3,0)
data=deepcopy(data1)
#data.ix[:,'债券趋势判断']=-data.ix[:,'债券趋势判断']
data.ix[:,'普林格划分']=np.nan
for i in range(len(data)):
    if data.ix[i,'股票趋势判断']==-1 and data.ix[i,'债券趋势判断']==-1 :
        data.ix[i,'普林格划分']=1
    if data.ix[i,'股票趋势判断']==1 and data.ix[i,'商品趋势判断']==-1 and data.ix[i,'债券趋势判断']==-1 :
        data.ix[i,'普林格划分']=2
    if data.ix[i,'股票趋势判断']==1 and data.ix[i,'商品趋势判断']==1 and data.ix[i,'债券趋势判断']==-1 :
        data.ix[i,'普林格划分']=3
    if data.ix[i,'股票趋势判断']==1 and data.ix[i,'商品趋势判断']==1 and data.ix[i,'债券趋势判断']==1 :
        data.ix[i,'普林格划分']=4
    if data.ix[i,'股票趋势判断']==-1 and data.ix[i,'商品趋势判断']==1 and data.ix[i,'债券趋势判断']==1 :
        data.ix[i,'普林格划分']=5
    if data.ix[i,'股票趋势判断']==-1 and data.ix[i,'商品趋势判断']==-1 and data.ix[i,'债券趋势判断']==1 :
        data.ix[i,'普林格划分']=6


data.ix[:,'阶段1']=np.nan
data.ix[data.ix[:,'普林格划分']==1,'阶段1']=1

data.ix[:,'阶段2']=np.nan
data.ix[data.ix[:,'普林格划分']==2,'阶段2']=1

data.ix[:,'阶段3']=np.nan
data.ix[data.ix[:,'普林格划分']==3,'阶段3']=1

data.ix[:,'阶段4']=np.nan
data.ix[data.ix[:,'普林格划分']==4,'阶段4']=1

data.ix[:,'阶段5']=np.nan
data.ix[data.ix[:,'普林格划分']==5,'阶段5']=1

data.ix[:,'阶段6']=np.nan
data.ix[data.ix[:,'普林格划分']==6,'阶段6']=1
namelist=['过热','复苏','衰退','滞胀']

data.to_excel('黄金分割-普林格.xlsx')


