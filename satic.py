# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 17:46:08 2024

@author: 18272022928
"""

import random
import numpy as np
from scipy.optimize import linprog
import copy
import time 
import math
# distance_matrix=[[0,1,1.4,1],[1,0,1,1.4],[1.4,1,0,1],[1,1.4,1,0]]
start=time.process_time()
from pytsp.christofides_tsp import christofides_tsp

# def golden_section_search(a, b, tol=1e-1):
#     golden_ratio = (math.sqrt(5) - 1) / 2
#     length = b - a

#     x1 = a + (1 - golden_ratio) * length
#     x2 = a + golden_ratio * length
    
#     while x2-x1>tol:
       
#         x11=[x[i]+x1*d[i] for i in range(goods)]
#         x22=[x[i]+x2*d[i] for i in range(goods)]
#         if fmin (order,x11) < fmin (order,x22):
#             b = x2
#             x2 = x1
#             x1 = a + (1 - golden_ratio) * (b - a)
#         else:
#             a = x1
#             x1 = x2
#             x2 = a + golden_ratio * (b - a)

#     return a

# def tour (chararray):
#     length=0
#     primgraph = [[0 for col in range(len(chararray))] for row in range(len(chararray))]
#     for p in range(len(chararray)-1):
#         for q in range(p+1,len(chararray)):
#             primgraph[p][q]=distance[chararray[p]][chararray[q]]
#             primgraph[q][p]=distance[chararray[p]][chararray[q]]
#     graph=np.array(primgraph)
#     a=christofides_tsp(graph) 
#     a.append(0)
#     for k in range(len(a)-1) :
#         length=length+graph[a[k]][a[k+1]]             
         
#     return length


    
# def IPA (x):
#     good=[]
#     order1=copy.deepcopy(order)
#     for j in range(goods) :
#         if x[j]!=0:
#             good.append(j+1)
#     #消耗掉x的库存，计算此时的f   
#     for j in good :
#         for d in range(days):
#             inventory=0
#             for i in range(order_n):
#                 if j in order1[d][i]:
#                     inventory=inventory+order1[d][i][j]
#                     if inventory<=x[j-1]:
#                         del order1[d][i][j]
#                     if inventory>=x[j-1]:
#                         break
            
#     #计算每种商品的增量（每天增量求均值）
#     f = [[0 for d in range(days)]  for j in range(goods)]
#     for j in range(1,goods+1) :
#     # for j in range(2,3) :
#         for d in range(days):
#             inventory=0
#             for i in range(order_n):
#                 if j in order1[d][i]:
#                     inventory=inventory+order1[d][i][j]
#                     if inventory<=1:
#                         #计算原路径长度
#                         site={}
#                         temp1=[location[k] for k in order1[d][i] ]
#                         for item in temp1:
#                             site[item] = temp1.count(item)    
#                         chararray=[0]
#                         for k in site:
#                             chararray.append(k)   
#                         # print(chararray)
#                         origin=tour (chararray)
#                         # print(origin)
#                         #删除操作后的路径长度
#                         temp1=[k for k in order1[d][i] ]
                        
#                         temp1.remove(j)
                       
#                         site={}
#                         temp2=[location[k] for k in temp1 ]
#                         for item in temp2:
#                             site[item] = temp2.count(item)    
#                         chararray=[0]
#                         for k in site:
#                             chararray.append(k)  
#                         # print(chararray)
#                         new=tour (chararray)
#                         # print(new)
#                         f[j-1][d]=new-origin
#                         # print(f[0][0])
#                         break
#                     else:
#                         break
#     gradient=[]
#     for j in range(goods):
#         gradient.append(sum(f[j])/days)                
#     return gradient

# def fmin (order,x):
#     good=[]
#     order1=copy.deepcopy(order)
#     for j in range(goods) :
#         if x[j]!=0:
#             good.append(j+1)
#     #消耗掉x的库存，计算此时的f   
#     for j in good :
#         for d in range(days):
#             inventory=0
#             for i in range(order_n):
#                 if j in order1[d][i]:
#                     inventory=inventory+order1[d][i][j]
#                     if inventory<=x[j-1]:
#                         del order1[d][i][j]
#                     if inventory>=x[j-1]:
#                         break
#     # 计算现在的距离
#     #计算距离
#     order2=[[{} for i in range(order_n)] for j in range(days)]  #以储位记录的订单,计算距离时只需记录访问节点，无需明确商品数量
#     route=[[0 for i in range(order_n)] for d in range(days) ]
#     for d in range(days):  
#         for i in range(order_n):
#             temp1=[location[k] for k in order1[d][i]]
#             for item in temp1:
#                 order2[d][i][item] = temp1.count(item)
#     for d in range(days):  
#         for i in range(order_n):
#             chararray=[0]
#             for j in order2[d][i].keys():
#                 chararray.append(j)
#             primgraph = [[0 for col in range(len(chararray))] for row in range(len(chararray))]
#             for p in range(len(chararray)-1):
#                 for q in range(p+1,len(chararray)):
#                     primgraph[p][q]=distance[chararray[p]][chararray[q]]
#                     primgraph[q][p]=distance[chararray[p]][chararray[q]]
#             graph=np.array(primgraph)
#             a=christofides_tsp(graph) 
#             a.append(0)
#             for j in range(len(a)-1) :
#                 route[d][i]=route[d][i]+graph[a[j]][a[j+1]]  
#     return(sum(sum(route[d]) for d in range(days))/days)


# S_list=[250,500,1000,1500,2000]
# S_lst=[2000]
# # S_list=[1,2,3,4,5]
# # S_lst=[5]
# x_list=[]
# days=10
# distance=np.load('distance.npy',allow_pickle=True).tolist()  #距离矩阵
# for S in S_lst:
#     iteration=0
#     random.seed(11)

#     # 储位的生成  
#     location=[] #large
#     # location=[i+1 for i in range(goods)]   
#     row=25
#     column=20
#     for i in range(column):
#         for j in range(row):
#             location.append(i*row+j+1)
#             location.append(i*row+j+1)
#     random.shuffle(location)
#     location.insert(0, 0)
   
    
#     # 订单的生成
#     order_n=1000
#     goods=1000
#     w = [1 for _ in range(goods)]
#     order=[[{} for i in range(order_n)] for j in range(days)]
#     for d in range(days):
#         order_num=[[] for i in range(order_n)]
#         for i in range(order_n):
#             order_num[i]=random.randint(1,10)
#         choices=[i for i in range(1,goods+1)]
#         weight=[]
#         for i in range(1,goods+1):
#             weight.append(pow(i/goods,0.222))
#         for i in range(goods-1,0,-1):
#             weight[i]=weight[i]-weight[i-1]
        
#         for i in range(order_n):
#             temp = random.choices(choices, weight, k=order_num[i])  
#             # temp1=[location[k] for k in temp]
#             for item in temp:
#                 order[d][i][item] = temp.count(item)
# #test       
# # x=[1 for i in range(goods)]            
# # G=IPA(x)         
   
#     #DFW算法
#     K=10
#     delta=0.1
#     x=[0 for i in range(goods)]   
#     x=np.load('x_list.npy',allow_pickle=True).tolist()
#     x=x[iteration]
#     for kk in range(K):
#         G=IPA(x)    
#         c=[G[i] for i in range(goods)] 
#         A_ub=[w]
#         b_ub=[S]
#         x_bounds=[(0,None) for i in range(goods)]
#         result = linprog(c, A_ub, b_ub, bounds=x_bounds, method='simplex')
#         s=list(result.x)
#         # for i in range(goods):
#         #     if s[i]!=0:
#         #         print(i)
        
        
#         d=[s[i]-x[i] for i in range(goods)]
#         g=-sum(G[i]*d[i] for i in range(goods))
#         print(g)
#         if g<0.1:
#             break
#         else:
#             # alpha=2/(S+k)
#             alpha = golden_section_search(0, 1)
#             x=[x[i]+alpha*d[i] for i in range(goods)]
    
    
#         # #贪心算法构造初始值
#         # j=G.index(min(G))
#         # x[j]+=1
#         # S1=kk+1
#         # if S1 in S_list:
#         #     print(S1)
#         #     temp=[i for i in x]
#         #     x_list.append(temp)
        
#     x_list.append(x)
        
# end=time.process_time()
# print(end-start) 
# np.save("x.npy", x_list) 

# test
x_list=np.load('x_list.npy',allow_pickle=True).tolist()
x_list=np.load('x_list_location.npy',allow_pickle=True).tolist() 
# x_list=[[0 for i in range(1000)]for j in range(5)]
# x_list=np.load('x.npy',allow_pickle=True).tolist() 
distance=np.load('distance.npy',allow_pickle=True).tolist()  #距离矩阵
seeds=[i for i in range(1,11)]  #种子
S_lst=[250,500,1000,1500,2000]  #前置仓容量
# seeds=[1]  
# S_lst=[0] 
l0=[[] for i in range(10)]
pdr_list=[[] for i in range(10)]
ratio=[[] for i in range(10)]
origin=[175708.0,167967.0,177882.0,179976.0,176488.0,169998.0,175937.0,170252.0,179782.0,182491.0]
origin=[119265.0,114841.0,116357.0,117590.0,115891.0,115268.0,113391.0,115902.0,112953.0,115643.0]
# origin=[173591.0,164995.0,175006.0,177772.0,174395.0,168531.0,173832.0,168873.0,178909.0,179702.0]
# origin=[117874.0,113424.0,114811.0,116349.0,114604.0,113830.0,112160.0,114367.0,111400.0,114272.0]
iteration=0
for S in S_lst:
    
    for s in seeds:
        random.seed(s)
    
        # 储位的生成  
        location=[] #large
        # location=[i+1 for i in range(goods)]   
        row=25
        column=20
        for i in range(column):
            for j in range(row):
                location.append(i*row+j+1)
                location.append(i*row+j+1)
        random.shuffle(location)
        location.insert(0, 0) 
      
        # 将location按照距离排序
        location=[]
        f=[i for i in distance[0]]

        sku_p=sorted(range(len(f)),key=lambda k: f[k])
        sku_p.remove(0)
        for i in sku_p:
            location.append(i)
            location.append(i)
        location.insert(0, 0)
 
        # 订单的生成
        order_n=1000
        goods=1000
        
        orders=[{} for i in range(order_n)]  #以商品记录的订单
        order_num=[[] for i in range(order_n)]
        for i in range(order_n):
            order_num[i]=random.randint(1,10)
            
        choices=[i for i in range(1,goods+1)]
        weight=[]
        for i in range(1,goods+1):
            weight.append(pow(i/goods,0.222))
        for i in range(goods-1,0,-1):
            weight[i]=weight[i]-weight[i-1]
        
        for i in range(order_n):
            temp = random.choices(choices, weight, k=order_num[i])  
            for item in temp:
                orders[i][item] = temp.count(item) 


        # 计算距离
        d_0=0
        for i in range(order_n):
            for j in orders[i]:
                d_0+=distance[0][location[j]]*orders[i][j]
                
        d_f=0    
        for j in range(goods) :
            d_f+=x_list[iteration][j]*distance[0][location[j]]
                
        ratio[s-1].append((d_f/S)/(d_0/5500.0))
        #消耗掉x的库存，计算此时的f 
        good=[]
        for j in range(goods) :
            if x_list[iteration][j]!=0:
                good.append(j+1)
        
        for j in good :
            inventory=0
            for i in range(order_n):
                if j in orders[i]:
                    inventory=inventory+orders[i][j]
                    if inventory<=x_list[iteration][j-1]:
                        del orders[i][j]
                    if inventory>=x_list[iteration][j-1]:
                        break
                        
        #计算距离
        order=[{} for i in range(order_n)]  #以储位记录的订单,计算距离时只需记录访问节点，无需明确商品数量
        route=[0 for i in range(order_n)]    
        for i in range(order_n):
            temp1=[location[k] for k in orders[i]]
            for item in temp1:
                order[i][item] = temp1.count(item)
                
        for i in range(order_n):
            chararray=[0]
            for j in order[i].keys():
                chararray.append(j)
            primgraph = [[0 for col in range(len(chararray))] for row in range(len(chararray))]
            for p in range(len(chararray)-1):
                for q in range(p+1,len(chararray)):
                    primgraph[p][q]=distance[chararray[p]][chararray[q]]
                    primgraph[q][p]=distance[chararray[p]][chararray[q]]
            graph=np.array(primgraph)
            # route[i]=solve_tsp(graph) 
            # if order[i]=={}:
            #     route[i]=0
            a=christofides_tsp(graph) 
            a.append(0)
            for j in range(len(a)-1) :
                route[i]=route[i]+graph[a[j]][a[j+1]]    
                
        # print(sum(route))        
        
        pdr=1-sum(route)/origin[s-1] 
        print(pdr)
        pdr_list[s-1].append(pdr)  
                         
                        
    iteration+=1                        
pdr_list=np.array(pdr_list)  
column_sum = np.mean(pdr_list,axis=0)  
np.save("b",pdr_list)  
ratio= np.array(ratio)
ratio_mean = np.mean(ratio,axis=0)