#北京54坐标高斯投影
#将经纬度换算为XY直角坐标系
#将xy直角坐标系换算为经纬度

import math
import pyproj


#经纬度转直角坐标
#l0是中央子午线，b是纬度的度小数形式，c是经度的度小数形式
def jw2xy(l0,b,c):
    l0 = math.floor(l0)+(math.floor(l0*100)-math.floor(l0)*100)/60+(l0*10000-math.floor(l0*100)*100)/3600
    b = math.floor(b)+(math.floor(b*100)-math.floor(b)*100)/60+(b*10000-math.floor(b*100)*100)/3600
    c = math.floor(c)+(math.floor(c*100)-math.floor(c)*100)/60+(c*10000-math.floor(c*100)*100)/3600
    g = c - l0
    g = g/57.2957795130823
    i2 = math.tan(math.radians(b))
    j2 = math.cos(math.radians(b))
    k2 = 0.006738525415*j2*j2
    l2 = i2*i2
    m2 = 1+k2
    n2 = 6399698.9018/math.sqrt(m2)
    o2 = g*g*j2*j2
    p2 = i2*j2
    q2 = p2*p2
    r2 = (32005.78006+q2*(133.92133+q2*0.7031))
    x = 6367558.49686*b/57.29577951308 - p2*j2*r2 + ((((l2 - 58)*l2+61)*o2/30 + (4*k2+5)*m2 - l2)*o2/12 + 1)*n2*i2*o2/2
    y = ((((l2-18)*l2-(58*l2-14)*k2+5)*o2/20+m2-l2)*o2/6+1)*n2*g*j2
    return x,y

    


#距离计算
def ca_ls(a,b,c,d):
    l_s = math.sqrt(abs(a**2 - c**2)+abs(b**2 - d**2))
    return l_s

#场强功率转换
#dBm=10log(功率值W/1mW)-->30dBm=1W
def e2p(e,s):
    p1 = (e**2)*(10**(-9))/(120*math.pi)
    #自用空间的特性阻抗120pi
    #电场强度单位uV/m,功率密度单位mW/m2
    #转换为dBm
    p2 = 10*math.log10(p1*s)
    return p2

#链路损耗计算,单位dBm
def lose_ls():
    pass
    


#改良版的经纬度转换直角坐标公式
#函数的形参是经纬度，返回一个二元的列表
def t_jw2xy(lon,lat):
    p1 = pyproj.Proj(init='epsg:4214')       # 定义数据地理坐标系，4214表示北京54坐标系
    p2 = pyproj.Proj(init='epsg:3857')       #定义投影坐标系，3854对应WGS_1984_Web_Mercator_Auxiliary_Sphere
    x1,y1 = p1(lon,lat)
    x2,y2 = pyproj.transform(p1,p2,x1,y1,radians = True)
    return [x2,y2]

#改良版的直角坐标转经纬度公式 
#函数的形参是x，y坐标值，返回一个列表
def t_xy2jw(x,y):
    p1 = pyproj.Proj(init = 'epsg:4214')
    p2 = pyproj.Proj(init = 'epsg:3857')
    lon,lat = p2(x,y,inverse = True)     #进行投影反转
    lon,lat = p1(lon,lat)
    lon = (lon*180)/math.pi
    lat = (lat*180)/math.pi
    return [lon,lat]

#构建由四个点求两直线中位线交点的函数
#函数的形参是四个一对x，y值组成的二元列表
def get_point(s1,s2,s3,s4):
    k1 = (s1[1]-s2[1])/(s1[0]-s2[0])
    k2 = (s3[1]-s4[1])/(s3[0]-s4[0])
    k1 = (-1/k1) 
    k2 = (-1/k2) 
    x1 = (s1[0]+s2[0])/2
    y1 = (s1[1]+s2[1])/2
    x2 = (s3[0]+s4[0])/2
    y2 = (s3[1]+s4[1])/2
    if k1 == k2:
        return False
    else:
        x = (k1*x1-k2*x2+y2-y1)/(k1-k2)
        y = k1*(x-x1)+y1
        return [x+3830,y-7820]  #根据已知坐标修改修正参数
#返回一个二元列表，列表元素为交点的坐标

#构建函数，对交点坐标进行优化
#目的是除掉其中的异常值
#函数的形参是一个二维列表，返回一个二维列表
#思路是给定一个阈值，若某个点到其他点的距离大于这个阈值，则舍弃掉这个点
def throw_u(s):
    rest = []
    count = len(s)
    xal = 0
    yal = 0
    lal = 0
    for i in s:
        xal = xal + i[0]
        yal = yal + i[1]
    xav = xal/count
    yav = yal/count
    for j in s:
        lal = lal + math.sqrt((j[0]-xav)**2 + (j[1]-yav)**2)
    lav = lal/count
    upedge = lav + 8000
    dwedge = lav - 8000
    for m in s:
        a = math.sqrt((m[0]-xav)**2 + (m[1]-yav)**2)
        if (a > dwedge) and (a < upedge):
            rest.append(m)
    return rest
#返回一个去除异常值的二维列表    
    
#throw_u的改进
def throw_2u(s):
    clean_over = []
    for i in s:
        [a1,a2] = t_xy2jw(i[0],i[1])
        if (a1 >= 120.0) and (a1 <= 122.0) and (a2 >= 30.0) and (a2 <= 32.0):
            clean_over.append(i)
    return clean_over
            

#构建函数，完成中心迭代算法主体部分
#函数的形参设定为一个二维列表
def mid_point(s):
    num = len(s)
    cmark = 0
    dmark = 1
    pall = []              #使用迭代时候起到更新pall存储的作用
    while cmark < num:
        while dmark < num:
            mid = [(s[cmark][0]+s[dmark][0])/2,(s[cmark][1]+s[dmark][1])/2]
            pall.append(mid)
            dmark = dmark + 1
        cmark = cmark + 1
        dmark = cmark + 1
    return pall            #pall存储所有中点的（x，y）坐标值，是一个二维列表


#上面取出中点的算法不是非常理想，所以再想办法构建一个函数尝试优化结果
#函数的形参同样也是一个二维列表
def progr_ass(s):
    num = len(s)
    cmark = 0
    sall = []
    while cmark < num:
        mid = [(s[cmark-1][0]+s[cmark][0])/2,(s[cmark-1][1]+s[cmark][1])/2]
        sall.append(mid)
        cmark = cmark + 1
    return sall
        

#构建一个函数。用来处理文本型数据二维列表并分类汇总特征值相等的数据
#形参是一个文本型数据的二维列表，第二维有三个参数，分别是经度纬度场强值
def get_sm(s):
    num = len(s)
    cmark = 0
    dmark = 0
    p1 = []   #用于存储场强值相等的经纬度坐标
    p3 = []   #用于存储每一类的p2
    p4 = []   #用于存储已比较过且相等的场强的索引值，避免重复 
    sall = [] #储存汇总坐标，理论上是一个三维的列表
    while cmark < num:
        while (dmark < num):
            a = int(s[cmark][2].strip(']'))
            b = int(s[dmark][2].strip(']'))
            c = abs(a - b)
            if (c == 0) and (dmark not in p4) and (cmark != dmark) and (a>=300) and (b>=300):
                p1.append([float(s[cmark][0].strip('[')),float(s[cmark][1])])
                p1.append([float(s[dmark][0].strip('[')),float(s[dmark][1])])
                p4.append(dmark)                
            dmark = dmark + 1
            p4 = list(set(p4))
        if p1:                         #列表非空，返回一个True
            for j in p1:
                if j not in p3:
                    p3.append(j)
            sall.append(p3)
            p3 = []
            p1 = []
        cmark = cmark + 1
        dmark = cmark + 1
    return sall
                
#构建一个函数获得一堆点集的中心点
#函数的形参是一个二维的列表，储存有x，y坐标
def getmid_pt(s):
    x = 0
    y = 0
    n = len(s)
    for i in s:
        x = x + i[0]
        y = y + i[1]
    new_x = x/n
    new_y = y/n
    return [new_x,new_y]
        
        
#将一定范围区域内的圆心计算为同一点
def del_abn(s):
    pass
                   
        
                
                
                
                
                
        
          
            
            
            
            
            
            
    
    
    

    
    
    
    
    
