# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:35:22 2018

@author: BC
"""

import os
import csv

#构建函数分别将基站信息整理汇总导入txt
def bs_data(r_csv):
    a = csv.reader(r_csv)
#得到一个二维数组
    s = list(a)
#删除第一行类目信息
    s= s[1:][:]
    h1 = len(s) #得到数据数量
    h2 = len(s[0]) #得到每条数据的信息数目
    dmark = 0
    cmark = h2 - 1
    i = int(input('输入载波频率的索引值'))
    p = []
    while dmark < h1:
        p.append(float(s[dmark][cmark])) #提取经度
        if cmark == h2 - 1:              
            cmark = cmark - 1
            p.append(float(s[dmark][cmark]))  #提取纬度
            if cmark == h2 - 2:
                cmark = i - 1 #i的值取载波频率所在位置的索引值
                p.append(float(s[dmark][cmark].strip('M'+'H'+'z'))*1000000)
                cmark = h2 - 3
                p.append(int(s[dmark][cmark].strip('d'+'B'+'m'))) #获取场强对应值
            else:
                break
        else:
            break
        fout = open('C:/Users/BC/Desktop/washing_data/BsDataTxt/'+str_ming+'.txt','a')
        print(p,file=fout)
        fout.close()
        p.clear()
        cmark = h2 - 1
        dmark = dmark + 1



if __name__ == '__main__':
    global str_ming
    str_ming = input('输入文件名')
    r_csv = open ('C:/USers/BC/Desktop/washing_data/BsData/苏州市/3205_'+str_ming+'.csv','r',encoding='utf-8')
    bs_data(r_csv)
    r_csv.close()
    
    
    
    
            
