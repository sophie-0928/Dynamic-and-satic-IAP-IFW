# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 21:58:22 2024

@author: 18272022928
"""

import random
import numpy as np
# distance_matrix=[[0,1,1.4,1],[1,0,1,1.4],[1.4,1,0,1],[1,1.4,1,0]]
from tsp import solve_tsp
from pytsp.christofides_tsp import christofides_tsp


seeds=[i for i in range(1,11)]  #种子
S_lst=[250,500,1000,1500,2000]  #前置仓容量
# seeds=[1]  
# S_lst=[0] 
l0=[[] for i in range(10)]
pdr_list=[[] for i in range(10)]
# origin=[175708.0,167967.0,177882.0,179976.0,176488.0,169998.0,175937.0,170252.0,179782.0,182491.0]
origin=[119265.0,114841.0,116357.0,117590.0,115891.0,115268.0,113391.0,115902.0,112953.0,115643.0]
# origin=[173591.0,164995.0,175006.0,177772.0,174395.0,168531.0,173832.0,168873.0,178909.0,179702.0]
# origin=[117874.0,113424.0,114811.0,116349.0,114604.0,113830.0,112160.0,114367.0,111400.0,114272.0]
ratio=[[] for i in range(10)]
for S in S_lst:
    for s in seeds:
        random.seed(s)
    # 储位的生成  


        distance=np.load('distance.npy',allow_pickle=True).tolist()  #距离矩阵
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
            # temp1=[location[k] for k in temp]
            # for item in temp1:
            #     order[i][item] = temp1.count(item)            

        # 计算距离
        d_0=0
        for i in range(order_n):
            for j in orders[i]:
                d_0+=distance[0][location[j]]*orders[i][j]    
        
        # #这是一段附加代码，要对流行商品进行删除       
        # popular=0    
        # for j in choices:
        #     for i in range(order_n):    
        #         if j in orders[i]:
        #             popular=popular+orders[i][j]
        #             if popular<=S:
        #                 del orders[i][j]
        #             if popular>=S:
        #                 break
        #     if (popular>=S) :        
        #         break    
        
        
        # 这是一段附加代码，要对远距离商品进行删除 
        d_f=0
        f=[i for i in distance[0]]
        s_count=0
        sku_p=sorted(range(len(location)),key=lambda k: f[location[k]],reverse=True) 
        for j in sku_p:
            for i in range(order_n):    
                if j in orders[i]:
                    s_count=s_count+orders[i][j]
                    if s_count<=S:
                        d_f=d_f+orders[i][j]*distance[0][location[j]]
                        del orders[i][j]
                    if s_count>=S:
                        break
            if (s_count>=S) :        
                break   
        
        ratio[s-1].append((d_f/S)/(d_0/5500.0))
        # #这是一段附加代码，如果要删除一部分订单的话需要添加     
        # s_count=0
        # seq=[i for i in range(order_n)]
        # random.shuffle(seq)
        # for i in seq:
        #     for j in orders[i].keys():           
        #         s_count=s_count+orders[i][j]
        #     if s_count<=S:
        #         orders[i]={}        
        #     if (s_count>=S):
        #         break
        
        
        # #这是一段附加代码，如果要删除一部分SKU    
        # s_count=0
        # while 1:
        #     j=random.randint(1, goods+1)
        #     for i in range(order_n):    
        #         if j in orders[i]:
        #             s_count=s_count+orders[i][j]
        #             if s_count<=S:
        #                 del orders[i][j]
        #             if s_count>=S:
        #                 break
        #     if (s_count>=S) :        
        #         break    
        
        
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
pdr_list=np.array(pdr_list)  
column_sum = np.mean(pdr_list,axis=0)
        
np.save("b",pdr_list)
ratio= np.array(ratio)
ratio_mean = np.mean(ratio,axis=0)