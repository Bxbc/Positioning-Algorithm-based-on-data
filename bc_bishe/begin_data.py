#-*- coding:utf-8 -*-
"""
Created on Tue Apr  3 02:10:31 2018

@author: BC
"""

import os
import binascii
import csv
from struct import *

    #构建函数切割并导入数据
def cut_data(raw_bin):
    s=[]

    #读取前7字节：记录头，设备编号，设备、天线参数和信息
    c1 = raw_bin.read(7)
    if len(c1) != 7:
        return '读取文件头错误'
    else:
        p1 = unpack('4s2s1s',c1)
        
    #解析的字节流倒序放入s列表中
        for i in p1:
            s.append(binascii.b2a_hex(i[::-1]))

    #读取之后7字节：年月日时分秒   
        c2 = raw_bin.read(7)
        p2 = unpack('HBBBBB',c2)
        for i in p2:
            if isinstance(i,int):
                s.append(i)
            else:
                s.append(int(binascii.b2a_hex(i[::-1]),16))

    #读取之后的4字节：毫秒，扫描速度
        c3 = raw_bin.read(4)
        p3 = unpack('2H',c3)
        for i in p3:
            s.append(i)

    #读取之后18字节：经度，纬度，挂高
        c4 = raw_bin.read(18)
        p4 = unpack('2Qh',c4)
        for i in range(len(p4)):
            if i == 2:
                s.append(float(p4[i]/10))
            else:
                s.append(float(p4[i] / (10**8)))

    #读取之后8字节：开始频率，单位Hz
        c5 = raw_bin.read(8)
        p5 = unpack('d',c5)
        for i in p5:
            s.append(i)
            begin = float(i)

    #读取之后4字节：步进频率，单位Hz
        c6 = raw_bin.read(4)
        p6 = unpack('f',c6)
        for i in p6:
            s.append(i)
            step = float(i)

    #读取之后4字节：频率点数量
        c7 = raw_bin.read(4)
        p7 = unpack('i',c7)
        for i in p7:
            s.append(i)
            count = int(i) 
    #读取之后2字节：以0.1dBuV/m为单位，到此总字节数目为54字节
        c8 = raw_bin.read(2)
        p8 = unpack('h',c8)
        for i in p8:
            s.append(i)

    #读取剩下count-1个频率点的测量值
        while count > 1:
           count = count-1
           c = raw_bin.read(2)
           p = unpack('h',c) 
           for i in p:
               s.append(i)

    #引入循环读取bin文件中剩下的所有数据
        fout = open('C:/Users/BC/Desktop/washing_data/wash_csv/'+dv[bmark]+'.csv', 'a')
        print(s, file=fout)
        fout.close()
        return
    
    
    #构建函数对导出来的csv文件中的数据进行进一步清洗和整理
def ajust_data(pr_csv):
    #得到csv每行字符串组成的二维列表
    reads = csv.reader(pr_csv)
    s = list(reads)
    
    #得到列表数据条数,频率点数量,开始频率，步进频率
    num = int(len(s))
    count = int(s[0][16])+17
    #获取开始频率和步进频率
    stf = float(s[0][14])
    step = float(s[0][15])
    s1 = []
    s2 = []
    s3 = []
    cmark = 0
    #最外层遍历数据条目，里层更新数据细节
    while cmark < num:
    #获取经度
        dmark = 11
        emark = 0
        s1.append(float(s[cmark][dmark]))
        while dmark == 11:
    #获取纬度
            dmark = 12
            s1.append(float(s[cmark][dmark]))
    #计算测试时候的频率
            while dmark == 12:
                s1.append(stf+step*emark)
    #获取测试场强，并将前两位的经纬度储存
                dmark = 17
                s1.append(int(s[cmark][dmark]))
                s2 = s1[0:2]
                s3 = s1[0:2]
                while dmark < count-1:
                    if dmark < count-2:
                        fout = open('D:/txt/my_data.txt','a')
                        print(s1,file=fout)
                        fout.close()
                        s1.clear()
                        s1 = s2[:]
                        emark = emark + 1
                        dmark = dmark + 1
                        s1.append(stf+step*emark)
                        s1.append(int(s[cmark][dmark]))
                    else:
                        fout = open('D:/txt/my_data.txt','a')
                        print(s1,file=fout)
                        fout.close()
                        s1.clear()
                        s1 = s3[:]
                        emark = emark + 1
                        dmark = dmark + 1
                        if dmark == count - 1:
                            s1.append(stf+step*emark)
                            s1.append(int(s[cmark][dmark].strip(']')))
                            fout = open('D:/txt/my_data.txt','a')
                            print(s1,file=fout)
                            fout.close()
                            s1.clear()
                            s2.clear()
                            s3.clear()
        cmark = cmark + 1
    return
                  

    
    
    #测试段代码，成功，已经注释掉  
'''
raw_bin = open('C:/Users/BC/Desktop/washing_data/bin/'+dv[bmark]+'.bin', 'rb')
cut_data(raw_bin)
'''
 

if __name__ == '__main__':
    
    #创建一个字典
     d = {1:'32050000_0031_20170717_101949_48MHz_72MHz_25kHz_V_M',
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
          34:'32050000_0031_20170717_101950_2655MHz_2690MHz_25kHz_V_M'}
     
    #将字典中的key值value分别存入一个列表中方便引用,并初始化一个能被全局引用的书签
     global dk
     global dv
     global bmark
     global fmark
     dk = list(d.keys())
     dv = list(d.values())
     
    #为遍历书签初始化
    #如果未导出初始数据，bmark设置为0，否则设置为34
    #如果未导出筛选数据，fmark设置为0，否则设置为34
     bmark = 34
     fmark = 34
    #遍历目录下的所有bin文件并分别读取它们的内容

     while bmark < 34:
         raw_bin = open('C:/Users/BC/Desktop/washing_data/bin/'+dv[bmark]+'.bin', 'rb')
    
    #获取频率点的数量
         d = raw_bin.read(48)
         d = raw_bin.read(4)
         a = unpack('i',d)
         for i in a:
             num = int(i) 
    #指针归零
             raw_bin.seek(0,0)
             cut_data(raw_bin)
             num = num - 1
         while (raw_bin.read(num*2+54)):
             cut_data(raw_bin)
         raw_bin.close()
         bmark = bmark + 1

    
    #调用函数对于数据进行进一步整理
     while fmark < 34:
            pr_csv = open('C:/Users/BC/Desktop/washing_data/wash_csv/'+dv[fmark]+'.csv','r')
            ajust_data(pr_csv)
            fmark = fmark + 1
            pr_csv.close()
         
  
     
