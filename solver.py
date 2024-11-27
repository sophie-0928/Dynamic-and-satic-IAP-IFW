# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:45:14 2024

@author: 18272022928
"""
import sys
import gurobipy as gp
from gurobipy import GRB
import time 
import random
import numpy as np

#from scipy import io
#import numpy as np 

seeds=[i for i in range(1,11)]  #种子
S_lst=[250,500,1000,1500,2000]  #前置仓容量
S_lst=[250] 
seeds=[1]
# time=[]
obj=[]
run_time=[]
for S in S_lst:
    start=time.process_time()
    for s in seeds:
        random.seed(s)
    # 储位的生成  


        graph=np.load('graph.npy',allow_pickle=True).tolist()  #距离矩阵
        location=[] #large
        # location=[i+1 for i in range(goods)]   
        # row=5
        # column=4
        row=25
        column=20       
        R=row* column
        V=len(graph)
        I=[i for i in range(R+1,len(graph))]
        for i in range(column):
            for j in range(row):
                location.append(i*row+j)
                location.append(i*row+j)
        random.shuffle(location)
        # location.insert(0, 0)
        
        gamma=[[] for i in range(V)]
        for i in range(V):
            for j in range(V):
                if graph[i][j]!=0 and graph[i][j]<=1000:
                    gamma[i].append(j)
        
        # 订单的生成
        # order_n=100
        # goods=40
        order_n=1000
        goods=1000        
        order=[{} for i in range(order_n)]
        order_num=[[] for i in range(order_n)]
        w = [1 for _ in range(goods)]
        for i in range(order_n):
            order_num[i]=random.randint(1,10)
            
        choices=[i for i in range(goods)]
        weight=[]
        for i in range(1,goods+1):
            weight.append(pow(i/goods,0.222))
        for i in range(goods-1,0,-1):
            weight[i]=weight[i]-weight[i-1]
        
        for i in range(order_n):
            temp = random.choices(choices, weight, k=order_num[i])  
            # temp1=[location[k] for k in temp]
            for item in temp:
                order[i][item] = temp.count(item)


        m=gp.Model("wo")
        m.setParam('MIPGap', 0.0)
        y=m.addVars(order_n,goods,vtype=GRB.BINARY, name="y")
        x=m.addVars(order_n,goods,vtype=GRB.INTEGER, name="x")
        
        z=m.addVars(order_n,R,vtype=GRB.BINARY, name="y")
        lamda=m.addVars(order_n,V,V,vtype=GRB.BINARY, name="u")
        c=m.addVars(order_n,V,V,vtype=GRB.CONTINUOUS, name="v")
        
        m.addConstr((sum(w[j]*x[i,j] for i in range(order_n) for j in order[i])<=S),"con2")
        m.addConstrs((x[i,j]<=order[i][j] for i in range(order_n) for j in order[i]),"con3")
        m.addConstrs((order[i][j]-x[i,j]<=order[i][j]*y[i,j] for i in range(order_n) for j in order[i]),"con4")
        m.addConstrs((order[i][j]-x[i,j]>=y[i,j] for i in range(order_n) for j in order[i]),"con5")
        m.addConstrs((z[i,location[j]]>=y[i,j] for i in range(order_n) for j in order[i]),"con6")
        m.addConstrs((sum(lamda[i,p,q] for q in gamma[p])>=z[i,p] for i in range(order_n) for p in range(R)),"con7")    
        m.addConstrs((sum(lamda[i,R,q] for q in gamma[R])*len(order[i])>=sum(y[i,j] for j in order[i]) for i in range(order_n)),"con8")
        m.addConstrs((sum(lamda[i,p,q] for q in gamma[p])==sum(lamda[i,q,p] for q in gamma[p]) for p in range(V) for i in range(order_n)),"con9")
        m.addConstrs((sum(c[i,q,p] for q in gamma[p])-sum(c[i,p,q] for q in gamma[p])==z[i,p] for p in range(R) for i in range(order_n)),"con10")
        m.addConstrs((sum(c[i,q,p] for q in gamma[p])-sum(c[i,p,q] for q in gamma[p])==0 for p in I for i in range(order_n)),"con11")
        m.addConstrs(c[i,p,q] <=len(order[i])*lamda[i,p,q] for p in range(V) for q in gamma[p] for i in range(order_n))
        m.setObjective(sum(graph[p][q]*lamda[i,p,q] for i in range(order_n) for p in range(V) for q in gamma[p]),GRB.MINIMIZE)
        m.optimize()
        obj.append(m.objVal)
        
        lamda1= {ind:lamda[ind].x for ind in lamda}
        
        # for i in range(order_n):
        #     for p in range(V) :
        #         for q in range(V) :
        #             if lamda1[(i,p,q)]>0:
        #                 print(p)
        #                 print(q)
        #                 print(lamda1[(i,p,q)])
        
    end=time.process_time()
    print('Running time:%s Seconds'%(end-start))
    run_time.append(end-start)