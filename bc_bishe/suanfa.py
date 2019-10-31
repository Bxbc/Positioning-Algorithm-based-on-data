# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 21:16:45 2018

@author: BC
"""
import csv
import codecs
import re
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FormatStrFormatter

#一共34个csv文件，编写函数判断要在哪一个csv文件中进行索引
#此处的s代表我们要抽选的频率，单位是MHz
def suoyin(s):
    file_index = {1:'32050000_0031_20170717_101949_48MHz_72MHz_25kHz_V_M',
                  2:'32050000_0031_20170717_101949_76MHz_92MHz_25kHz_V_M',
                  3:'32050000_0031_20170717_101949_84MHz_108MHz_25kHz_V_M',
                  4:'32050000_0031_20170717_101949_167MHz_223MHz_25kHz_V_M',
                  5:'32050000_0031_20170717_101949_450MHz_470MHz_25kHz_V_M',
                  6:'32050000_0031_20170717_101949_470MHz_566MHz_25kHz_V_M',
                  7:'32050000_0031_20170717_101949_566MHz_606MHz_25kHz_V_M',
                  8:'32050000_0031_20170717_101949_606MHz_806MHz_25kHz_V_M',
                  9:'32050000_0031_20170717_101949_806MHz_958MHz_25kHz_V_M',
                  10:'32050000_0031_20170717_101949_870MHz_880MHz_25kHz_V_M',
                  11:'32050000_0031_20170717_101949_930MHz_934MHz_25kHz_V_M',
                  12:'32050000_0031_20170717_101949_934MHz_954MHz_25kHz_V_M',
                  13:'32050000_0031_20170717_101949_954MHz_960MHz_25kHz_V_M',
                  14:'32050000_0031_20170717_101950_1805MHz_1830MHz_25kHz_V_M',
                  15:'32050000_0031_20170717_101950_1830MHz_1845MHz_25kHz_V_M',
                  16:'32050000_0031_20170717_101950_1845MHz_1860MHz_25kHz_V_M',
                  17:'32050000_0031_20170717_101950_1860MHz_1875MHz_25kHz_V_M',
                  18:'32050000_0031_20170717_101950_1875MHz_1880MHz_25kHz_V_M',
                  19:'32050000_0031_20170717_101950_1880MHz_1885MHz_25kHz_V_M',
                  20:'32050000_0031_20170717_101950_1885MHz_1915MHz_25kHz_V_M',
                  21:'32050000_0031_20170717_101950_1915MHz_1920MHz_25kHz_V_M',
                  22:'32050000_0031_20170717_101950_2010MHz_2025MHz_25kHz_V_M',
                  23:'32050000_0031_20170717_101950_2110MHz_2130MHz_25kHz_V_M',
                  24:'32050000_0031_20170717_101950_2130MHz_2145MHz_25kHz_V_M',
                  25:'32050000_0031_20170717_101950_2145MHz_2155MHz_25kHz_V_M',
                  26:'32050000_0031_20170717_101950_2155MHz_2170MHz_25kHz_V_M',
                  27:'32050000_0031_20170717_101950_2300MHz_2320MHz_25kHz_V_M',
                  28:'32050000_0031_20170717_101950_2320MHz_2370MHz_25kHz_V_M',
                  29:'32050000_0031_20170717_101950_2370MHz_2400MHz_25kHz_V_M',
                  30:'32050000_0031_20170717_101950_2500MHz_2555MHz_25kHz_V_M',
                  31:'32050000_0031_20170717_101950_2555MHz_2575MHz_25kHz_V_M',
                  32:'32050000_0031_20170717_101950_2575MHz_2635MHz_25kHz_V_M',
                  33:'32050000_0031_20170717_101950_2635MHz_2655MHz_25kHz_V_M',
                  34:'32050000_0031_20170717_101950_2655MHz_2690MHz_25kHz_V_M'
                  }
    
    
#利用正则表达式匹配出CSV文件的频率范围
#找出范围后将csv文件中的内容转换为一个列表，储存在二维列表r3中
#步进储存在step中
    for i in range(1,35):
#匹配出频率段
        pipei = re.search(r'\d{2,4}MHz_\d{2,4}MHz',file_index[i])
#将匹配结果转成字符串
        pilist = pipei.group()
#将字符串分割成为只含有数字的形式
        fenge = pilist.split('_',1)
        if (s <= float(fenge[1].strip('MHz'))) and (s >= float(fenge[0].strip('MHz'))):
            step = int((s - float(fenge[0].strip('MHz')))/0.025 + 0.5)
            r_csv = open('C:/Users/BC/Desktop/washing_data/wash_csv/'+file_index[i]+'.csv','r')
            return r_csv,step
        else:
            continue
#返回了一个二维的列表，并改变了步进的值

#构建一个函数，方便对基站的数据进行调用       
def bs_plot(s):
#建立建站文件索引
    bs_index = {1:'3205_CDMA',
                2:'3205_EVDO',
                3:'3205_GSM',
                4:'3205_LTE_FDD',
                5:'3205_LTE_TDD',
                6:'3205_TDSCDMA',
                7:'3205_WCDMA'
                }
#建立颜色索引
    color_index = {1:'peru',
                   2:'orange',
                   3:'limegreen',
                   4:'yellow',
                   5:'cyan',
                   6:'red',
                   7:'darkmagenta'
                   }

    for i in range(1,8):
        b_csv = codecs.open('C:/Users/BC/Desktop/washing_data/BsData/苏州市/'+bs_index[i]+'.csv','r','utf-8')
        s2 = csv.reader(b_csv)
        s3 = list(s2)
        s3 = s3[1:][:]
        b_csv.close()
        pout1 = []
        pout2 = []
#pout1储存经度值，pout2储存纬度值
        if i == 1:
            num = len(s3)
            cmark = 0
            while cmark < num:
                e1 = float(s3[cmark][1].strip('MHz'))
                if (abs(e1-s) < 0.00625) and (float(s3[cmark][8]) != 0):
                    pout1.append(float(s3[cmark][8]))
                    pout2.append(float(s3[cmark][7]))
                cmark = cmark + 1
            n1 = len(pout1)
            plt.scatter(pout1, pout2, s=100, c=color_index[i], alpha=0.5)
        elif i == 2:
            num = len(s3)
            cmark = 0
            while cmark < num:
                e1 = float(s3[cmark][1].strip('MHz'))
                if (abs(e1-s) < 0.00625) and (float(s3[cmark][8]) != 0):
                    pout1.append(float(s3[cmark][8]))
                    pout2.append(float(s3[cmark][7]))
                cmark = cmark + 1
            n2 = len(pout1)
            plt.scatter(pout1, pout2, s=100, c=color_index[i], alpha=0.5)
        elif i == 3:
            num = len(s3)
            cmark = 0
            while cmark < num:
                e1 = float(s3[cmark][1].strip('MHz'))
                if (abs(e1-s) < 0.00625) and (float(s3[cmark][9]) != 0):
                    pout1.append(float(s3[cmark][9]))
                    pout2.append(float(s3[cmark][8]))
                cmark = cmark + 1
            n3 = len(pout1)
            plt.scatter(pout1, pout2, s=100, c=color_index[i], alpha=0.5)
        elif i == 4:
            num = len(s3)
            cmark = 0
            while cmark < num:
                e1 = float(s3[cmark][1].strip('MHz'))
                if (abs(e1-s) < 0.00625) and (float(s3[cmark][10]) != 0):
                    pout1.append(float(s3[cmark][10]))
                    pout2.append(float(s3[cmark][9]))
                cmark = cmark + 1
            n4 = len(pout1)
            plt.scatter(pout1, pout2, s=100, c=color_index[i], alpha=0.5)
        elif i == 5:
            num = len(s3)
            cmark = 0
            while cmark < num:
                e1 = float(s3[cmark][1].strip('MHz'))
                if (abs(e1-s) < 0.00625) and (float(s3[cmark][10]) != 0):
                    pout1.append(float(s3[cmark][10]))
                    pout2.append(float(s3[cmark][9]))
                cmark = cmark + 1
            n5 = len(pout1)
            plt.scatter(pout1, pout2, s=100, c=color_index[i], alpha=0.5)
        elif i == 6:
            num = len(s3)
            cmark = 0
            while cmark < num:
                e1 = float(s3[cmark][1].strip('MHz'))
                if (abs(e1-s) < 0.00625) and (float(s3[cmark][8]) != 0):
                    pout1.append(float(s3[cmark][8]))
                    pout2.append(float(s3[cmark][7]))
                cmark = cmark + 1
            n6 = len(pout1)
            plt.scatter(pout1, pout2, s=100, c=color_index[i], alpha=0.5)
        elif i == 7:
            num = len(s3)
            cmark = 0
            while cmark < num:
                e1 = float(s3[cmark][1].strip('MHz'))
                if (abs(e1-s) < 0.00625) and (float(s3[cmark][8]) != 0):
                    pout1.append(float(s3[cmark][8]))
                    pout2.append(float(s3[cmark][7]))
                cmark = cmark + 1
            n7 = len(pout1)
            plt.scatter(pout1, pout2, s=100, c=color_index[i], alpha=0.5)
        
    
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    ax = plt.gca()
    a1majorFormatter = FormatStrFormatter('%.3f') 
    ax.xaxis.set_major_formatter(a1majorFormatter)
    ax.yaxis.set_major_formatter(a1majorFormatter)
    plt.xlabel(u"经度",fontproperties=font)
    plt.ylabel(u"纬度",fontproperties=font)
    plt.title(u"该频率下的基站经纬度集合",fontproperties=font)
#返回参与绘点的基站总数方便监测
    return n1+n2+n3+n4+n5+n6+n7
    
#接下来都是尝试构建K-means算法的函数
#构建函数计算两个向量的欧式距离
def d_eclud(vecA,vecB):
    return np.sqrt(np.sum(np.power(vecA-vecB,2)))

#构建函数为给定数据集构建一个包含k个随机质心的集合
#随机质心在整个数据集的边界内
def rand_cent(data,k):
    n = np.shape(data)[1]
    centroids = np.mat(np.zeros((k,n)))  
    for i in range(n):
        minJ = min(data[:,i])
        rangeJ = float(max(data[:,i])-minJ)
        centroids[:,i] = minJ + rangeJ*np.random.rand(k,1)
    return centroids

#构建k-means算法主程序部分
def kmeans(data,k,distMeans=d_eclud,createCent=rand_cent):
    m = np.shape(data)[0]
    clusterAssment = np.mat(np.zeros((m,2)))
    centroids = createCent(data,k)
    clusterChanged = True
#引入一个计数器计算到达收敛时候迭代的次数
    dn = 0
    while clusterChanged:
        clusterChanged = False
#寻找最近的质心
        for i in range(m):
            minDist = np.inf
            minIndex = -1
            dn = dn + 1
            for j in range(k):
                dn = dn + 1
                distJI = distMeans(centroids[j,:],data[i,:])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if (clusterAssment[i,0] != minIndex):
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
#更新质心的位置
        dn = dn + 1
        for cent in range(k):
            ptsInClust = data[np.nonzero(clusterAssment[:,0].A == cent)[0]]
            centroids[cent,:] = np.mean(ptsInClust,axis=0)
        return centroids,clusterAssment,dn

#二分K-means聚类算法
def b_kmeans(data,k,distmeans=d_eclud):
    m = np.shape(data)[0]
#创建一个初始簇
    clusterAssment = np.mat(np.zeros((m,2)))
    centroid0 = np.mean(data,axis=0).tolist()[0]
    centList = [centroid0]
    for j in range(m):
        clusterAssment[j,1] = distmeans(np.mat(centroid0),data[j,:])**2
    while (len(centList) < k):
        lowestSSE = np.inf
#对簇进行划分
        for i in range(len(centList)):
            ptsInCurrCluster = data[np.nonzero(clusterAssment[:,0].A==i)[0],:]
            centroidmat,splitClustAss,dn_2 = kmeans(ptsInCurrCluster,2,distmeans)
            sseSplit = sum(splitClustAss[:,1])
            sseNotSplit = sum(clusterAssment[np.nonzero(clusterAssment[:,0].A != i)[0],1])
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidmat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
#更新簇的分配结果
        bestClustAss[np.nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) 
        bestClustAss[np.nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0] 
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[np.nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reas
    return np.mat(centList),clusterAssment,lowestSSE
                

if __name__ == '__main__':
    fig_bs = plt.figure('location of BS')
    bs_plot(1895)
    
                    
                    
                
    
    
            
        
        
        
  

