# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:28:47 2024

@author: 18272022928
"""

import numpy as np
import math
import time
import random
from itertools import combinations
from tsp import solve_tsp

seeds = [i for i in range(1, 11)]  # 种子
S_list = [250, 500, 1000, 1500, 2000]  # 前置仓容量
S_list=[10,20,40,60,80] 
# S_list = [250]
# seeds = [6]
pdr_list = [[] for i in range(10)]
ratio=[[] for i in range(10)]
origin_list=[[] for i in range(10)]
route_list=[[] for i in range(10)]
reduction=[[] for i in range(10)]
run_time=[]
distance = np.load('distance.npy', allow_pickle=True).tolist()  # 距离矩阵
# 储位的生成
for S1 in S_list:
    start=time.process_time()
    for s in seeds:
        random.seed(s)
        location = []  # large
        # location=[i+1 for i in range(goods)]
        row = 5
        column = 4
        # row = 25
        # column = 20
        for i in range(column):
            for j in range(row):
                location.append(i*row+j+1)
                location.append(i*row+j+1)
        random.shuffle(location)
        location.insert(0, 0)

        # # 将location按照距离排序
        # location=[]
        # f=[i for i in distance[0]]

        # sku_p=sorted(range(len(f)),key=lambda k: f[k])
        # sku_p.remove(0)
        # for i in sku_p:
        #     location.append(i)
        #     location.append(i)
        # location.insert(0, 0)

        # 订单的生成
        order_n =100
        goods = 40           
        # order_n =1000
        # goods = 1000
        order = [{} for i in range(order_n)]
        order_num = [[] for i in range(order_n)]
        for i in range(order_n):
            order_num[i] = random.randint(1, 10)
            # order_num[i]=5
        choices = [i for i in range(1, goods+1)]
        weight = []
        for i in range(1, goods+1):
            weight.append(pow(i/goods, 0.222))
        for i in range(goods-1, 0, -1):
            weight[i] = weight[i]-weight[i-1]
        
        for i in range(order_n):
            temp = random.choices(choices, weight, k=order_num[i])
            temp1 = [location[k] for k in temp]
            for item in temp1:
                order[i][item] = temp1.count(item)


        # 组合的计算
        u = [[] for i in range(order_n)]  # 单位价值
        U = []  # 每个组合中最大的单位价值
        I = []  # 每个组合中最大的单位价值组合索引
        save = [[] for i in range(order_n)]  # 节省的距离
        v = [[] for i in range(order_n)]  # 体积
        com = [[] for i in range(order_n)]  # 组合的信息
        tour = [[] for i in range(order_n)]  # 保存路径
        origin = [0 for i in range(order_n)]  # 原始路径长度

        for i in range(order_n):
            chararray = [0]
            for j in order[i].keys():
                chararray.append(j)
            primgraph = [[0 for col in range(len(chararray))]
                         for row in range(len(chararray))]
            for p in range(len(chararray)-1):
                for q in range(p+1, len(chararray)):
                    primgraph[p][q] = distance[chararray[p]][chararray[q]]
                    primgraph[q][p] = distance[chararray[p]][chararray[q]]
            graph = np.array(primgraph)
            # a = christofides_tsp(graph)
            a=solve_tsp(graph)
            for j in range(len(a)-1):
                origin[i] = origin[i]+graph[a[j]][a[j+1]]
            tour[i] = [chararray[k] for k in a]
        # print(sum(origin))
            # 开始选组合
            for j in range(len(chararray)-1, 0, -1):  # 组合个数 n+...+1
                long = len(chararray)-j  # 组合长度
                for k in range(j):
                    temp = 0
                    for r in range(long+1):
                        temp = temp+graph[a[k+r]][a[k+r+1]]
                    temp = temp-graph[a[k]][a[k+r+1]]
                    save[i].append(temp)
                    temp1 = 0
                    for r in range(long):
                        temp1 = temp1+order[i][tour[i][k+r+1]]
                    v[i].append(temp1)
                    com[i].append([k+1, long])
            for j in range(len(v[i])):
                u[i].append(save[i][j]/v[i][j])
            U.append(max(u[i]))
            I.append(u[i].index(max(u[i])))

        # 循环筛选
        P_e = 0
        P_bf = 0
        S=S1
        d_f=0
        while (S > 0):
            m = U.index(max(U))  # 确认哪个订单里的组合
            C = com[m][I[m]]  # 根据组合的索引找到组合的信息
            S = S-v[m][I[m]]
            if S >= 0:
                for i in range(C[1]):
                    
                    del tour[m][C[0]]
                                   
                P_bf = P_bf+save[m][I[m]]
                if tour[m] == [0, 0]:
                    U[m] = 0
                else:
                    save[m] = []
                    u[m] = []
                    v[m] = []
                    com[m] = []
                    for j in range(len(tour[m])-2, 0, -1):  # 组合个数 n+...+1
                        long = len(tour[m])-j-1  # 组合长度
                        for k in range(j):
                            temp = 0
                            for r in range(long+1):
                                temp = temp + \
                                    distance[tour[m][k+r]][tour[m][k+r+1]]
                            temp = temp-distance[tour[m][k]][tour[m][k+r+1]]
                            save[m].append(temp)
                            temp1 = 0
                            for r in range(long):
                                temp1 = temp1+order[m][tour[m][k+r+1]]
                            v[m].append(temp1)
                            com[m].append([k+1, long])
                    for j in range(len(v[m])):
                        u[m].append(save[m][j]/v[m][j])
                    U[m] = max(u[m])
                    I[m] = u[m].index(max(u[m]))
            else:
                P_e = P_e+save[m][I[m]]
                C_e = []
                for i in range(C[1]):
                    C_e.append(tour[m][C[0]+i])

        # 比较
        route = [0 for i in range(order_n)]
        if P_e < P_bf:
            # 最终路径长度
            for i in range(order_n):
                for j in range(len(tour[i])-1):
                    route[i] = route[i]+distance[tour[i][j]][tour[i][j+1]]
            pdr = 1-sum(route)/sum(origin)
            print(pdr)
        else:
            for j in C_e:
                tour[m].remove(j)
            for j in range(len(tour[m])-1):
                route[m] = route[m]+distance[tour[m][j]][tour[m][j+1]]
            pdr = 1-sum(route[m])/sum(origin[m])
            print(pdr)

        pdr_list[s-1].append(pdr)
        # ratio[s-1].append((d_f/S1)/(d_0/5500.0))
        origin_list[s-1].append(sum(origin))
        reduction[s-1].append(sum(origin)-sum(route))
        route_list[s-1].append(sum(route))
        print(sum(route))   
    end=time.process_time()    
    # print('Running time:%s Seconds'%(end-start))    
    run_time.append(end-start)
pdr_list = np.array(pdr_list)
route_list = np.array(route_list)
column_sum = np.mean(pdr_list,axis=0)

# np.save("a",pdr_list)
# ratio= np.array(ratio)
# ratio_mean = np.mean(ratio,axis=0)
# origin_list= np.array(origin_list)
# origin_mean = np.mean(origin_list,axis=0)
# reduction= np.array(reduction)
# reduction_mean = np.mean(reduction,axis=0)