# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:17:26 2018

@author: BC
"""

import os
import csv

#将关键频率段所含有的重要信息都从总文件中提取出来打包进一个csv文件中，并返回csv文件的列表形式
def plot_data(data_csv,n_step):
    reads = csv.reader(data_csv) 
    s = list(reads)
    #得到数据条数
    num = int(len(s))
    strf = float(s[0][14])
    step = float(s[0][15])
    #需要的频率need_f
    need_f = strf + n_step*step
    s1 = []
    cmark = 0
    if os.path.isfile('C:/Users/BC/Desktop/washing_data/part_f_data/'+str(need_f)+'.csv'):
        j_csv = open('C:/Users/BC/Desktop/washing_data/part_f_data/'+str(need_f)+'.csv','r')
        return j_csv
    else:
        while cmark < num:
            dmark = 11
            emark = 17 + n_step
            s1.append(float(s[cmark][dmark]))
            while dmark == 11:
                dmark = 12
                s1.append(float(s[cmark][dmark]))
                s1.append(int(s[cmark][emark].strip(']'+'[')))
                fout = open('C:/Users/BC/Desktop/washing_data/part_f_data/'+str(need_f)+'.csv','a')
                print(s1,file=fout)
                fout.close()
                s1.clear()
            cmark = cmark + 1
        j_csv = open('C:/Users/BC/Desktop/washing_data/part_f_data/'+str(need_f)+'.csv','r')
        return j_csv
        

if __name__ == '__main__':
    data_csv = open('C:/Users/BC/Desktop/washing_data/wash_csv/32050000_0031_20170717_101949_48MHz_72MHz_25kHz_V_M.csv','r')
    plot_data(data_csv,int(input('输入步进')))
    data_csv.close()
    