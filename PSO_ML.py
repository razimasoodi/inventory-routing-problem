#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import random
import math
from time import time


# In[2]:


def readFile(address):
    with open(address, 'r') as f:
        data = f.readlines()
        Lines = []
        for line in data:
            Line = line.strip('|').split()
            Lines.append(Line)  
    return Lines 


# In[3]:


def s0_ML(Ui,Ii0):
    s_inv=[]
    flag=True
    for i in range(len(Ui)):
        while(flag):
            x=np.random.randint(ri[i],Ui[i])
            if Ii0[i]+x-ri[i]<=Ui[i]:
                flag=False
                s_inv.append(x)
        flag=True        

    return s_inv 


# In[4]:


def find_cij(i,j,third):
    #print(i,j)
    cij=np.round(np.sqrt(((int(third[i][1])-int(third[j][1]))**2)+((int(third[i][2])-int(third[j][2]))**2)))
    return int(cij)  


# In[5]:


#arraye(H,n)
def fitness(s_inv,s_trans,B1,r1,h1,hi,Ii,ri,third):
    Ii0=Ii.copy()
    supp_cost=0
    costumer_cost=0
    trans_cost=0
    total_cost=0
    a=s_inv[ : ,1: ]
    b=s_trans.copy()
    for i in range(a.shape[0]):
        if B1<0:
            supp_cost+=10000000000
        supp_cost+=(B1)*h1
        #print(B1)
        #print('Ii0 before=',Ii0) 
        for j in range(a.shape[1]):
            if Ii0[j]<0:
                costumer_cost+=10000000000
            z=hi[j]*Ii0[j]
            costumer_cost+=z
            Ii0[j]=Ii0[j]+a[i][j]-ri[j]
        #print('Ii0 after=',Ii0)   
        B1=B1+r1-(np.sum(a[i, : ]))
        for x,y in zip(b[i, :-1].astype(int),b[i,1: ].astype(int)):
            trans_cost+=find_cij(x,y,third)
        trans_cost+=find_cij(b[i,0].astype(int),b[i,-1].astype(int),third)
    total_cost=supp_cost+ costumer_cost+trans_cost
    return total_cost 


# In[6]:


def check_valid(s_inv,s_trans,Ii,B1,r1,ri,Ui):
    Ii0=Ii.copy()
    a=s_inv.copy()
    b=s_trans.copy()
    flag=True
    if a[ : ,0].any()<0:
        flag=False
        print(0)
    for i in range(a.shape[0]):
        if B1<0:
            flag=False
            print(1)
        #print('B1=',B1)
        B1=(B1+r1)-sum(a[i,1: ])  
        for j in range(a.shape[1]):
            if j==len(Ii0):
                break
            else:  
                if Ii0[j]<0:
                    flag=False
                    print(2)
                #print('Ii0=',Ii0) 
                #print('j=',j)
                Ii0[j]=Ii0[j]+a[i][j+1]-ri[j]
                if Ii0[j]<0:
                    flag=False
                    print(2)
                if  a[i][j+1]>Ui[j]:    
                    flag=False
                    print(3)
        if np.sum(a[i,1: ])>C:
            flag=False
            print(4)          

    return flag


# In[7]:


def initial_sol(Ii,B,n,Ui,ri,H,v):
    B1=B
   # v=0.5
    Ii0=Ii.copy()
    inv=np.zeros((H,n+1))
    trans=np.zeros((H,int(np.round(n*v))))
    s_trans=[]
    s_trans.append(0)
    p=0
    for k in range(H):
        #print('B1=',B1)
        must_visit=[]
        while len(s_trans)!=(np.round(n*v)):
            r=np.random.randint(1,n+1)
            if r not in s_trans:
                s_trans.append(r)    
        #print("s_trans=",s_trans)
        s_inv=s0_ML(Ui,Ii0) 
        for i in range(len(s_inv)+1):
            if i ==len(s_inv):
                break
            else:    
                if i+1 not in s_trans:
                    s_inv[i]=0 
                Ii0[i]=Ii0[i]+s_inv[i]-ri[i]  
                if Ii0[i]==0:
                    must_visit.append(i+1)
                if s_inv[i]>Ui[i]:
                    p=s_inv[i]-Ui[i]
                    s_inv[i]-=p
                    
        #print('Ii0=',Ii0)    
        s_inv.insert(0,p)
        s_inv=np.array(s_inv)
        s_trans=np.array(s_trans)
        if sum(s_inv[1: ])>C:
            o=np.argmax(s_inv[1: ])
            delta=sum(s_inv[1: ])-C
            s_inv[o+1]=s_inv[o+1]-delta
            s_inv[0]+=delta
                
        s_inv[0]+=(B1+r1)-sum(s_inv[1: ])
        B1=(B1+r1)-sum(s_inv[1: ])
        #print('s_inv=',s_inv)
        inv[k]=s_inv[ : ]
        trans[k]=s_trans[ : ]
        #print('must_visit',must_visit)
        s_trans=[]
        s_trans.append(0)
        s_trans.extend(must_visit)
        
    return inv,trans.astype(int)


# In[8]:


def construct_sol(s_inv,s_trans,pbest_s_inv,pbest_s_trans,gbest,prob,v):
    #prob=[0.6,0.3,0.1]        
    intervals_list=[]    #list bazeha
    pi=0
    #v=0.5
    inv=np.zeros((H,n+1))
    trans=np.zeros((H,int(np.round(n*v))))    
   # for i in range(H):
    #    p=1/H
     #   prob.append(p)

    for i in range(len(prob)):
        #t.append(pi)
        h=pi+prob[i]
        intervals_list.append ([pi,h])
        pi=pi+prob[i]

    nums=np.random.uniform(0,1,H)
    between_three=[]
    for i in nums:
        for j in intervals_list:
            if i>j[0] and i<j[1]:
                between_three.append(intervals_list.index(j))
                
    #print('between_three',between_three)
    for i in range(len(between_three)):
        if between_three[i] ==0:
            inv[i]=s_inv[i]
            trans[i]=s_trans[i]
        if between_three[i] ==1:
            inv[i]=pbest_s_inv[i]
            trans[i]=pbest_s_trans[i]
        if between_three[i] ==2:
            inv[i]=gbest[0][i]
            trans[i]=gbest[1][i]
                
    return inv,trans


# In[9]:


#Instances_lowcost_H3
#test_instance
path="C:/Users/razeeee/test_instance"
adresses=[]
Instance=[]
for file in os.listdir(path):
    z=[]
    Instance.append(file)
    full_path = os.path.join(path, file)
    if os.path.isfile(full_path):
        #print (full_path)
        o=readFile(full_path)
        for k in o:
            s=[]
            for j in k:
                s.append(float(j))
            z.append(s)
        adresses.append(z)  


# In[10]:


best_list=[]
worst_list=[]
mean_list=[]
avg_time=[]
for i in range(len(adresses)):
    print(i)
    start = time()
    #print('instance=',i)
    third=adresses[i][1: ] #0=i
    nHC=adresses[i][0]     #0=i
    #print('nHC=',nHC)
    n=int(nHC[0])-1
    H=int(nHC[1])
    C=int(nHC[2])
    supp=adresses[i][1]   #0=i
    x1=supp[1]
    y1=supp[2]
    B1=supp[3]
    r1=supp[4]
    h1=supp[5]
    costumer=np.array(adresses[i][2: ])  #0=i
    Ii=costumer[ : ,3]
    Ui=costumer[ : ,4]
    Li=costumer[ : ,5]
    ri=costumer[ : ,6]
    hi=costumer[ : ,7]
    if n<=30:
        v=0.75
    else:
        v=0.5
    population_inv=[]
    population_trans=[]
    pbest_inv=[]
    pbest_trans=[]
    for particle in range(30):
        s,t=initial_sol(Ii,B1,n,Ui,ri,H,v)
        population_inv.append(s)
        population_trans.append(t)
        pbest_inv.append(s)
        pbest_trans.append(t)
    #print('population_trans[2]',population_trans[2])
    best_list1=[]
    worst_list1=[]
    mean_list1=[]
    #endd=time() +60
    #while time()<endd:
    for k in range(5):
        for t in range(20):
            fitness_list=[] 
            prob=[0.75,0.16,0.09]
            #print('1',population_trans[0])
            for p in range(len(population_inv)):
                fitness_list.append(fitness(population_inv[p],population_trans[p],B1,r1,h1,hi,Ii,ri,third))
                s_value=fitness(population_inv[p],population_trans[p],B1,r1,h1,hi,Ii,ri,third)
                pbest_value=fitness(pbest_inv[p],pbest_trans[p],B1,r1,h1,hi,Ii,ri,third)
                if s_value<pbest_value:
                    pbest_inv[p]=population_inv[p]
                    pbest_trans[p]=population_trans[p]


            min_indx=np.argmin(np.array(fitness_list))    
            gbest=[population_inv[min_indx],population_trans[min_indx]]    
            #print('gbest fitness=',fitness(gbest[0],gbest[1],B1,r1,h1,hi,Ii,ri,third))
            for p in range(len(population_inv)): 
                new_inv,new_trans=construct_sol(population_inv[p],population_trans[p],pbest_inv[p],pbest_trans[p],gbest,prob,v)
                population_inv[p]=new_inv
                population_trans[p]=new_trans
            #print(min(fitness_list))    
            best_list1.append(min(fitness_list))
            worst_list1.append(max(fitness_list))
            mean_list1.append(np.mean(np.array(fitness_list)))
            prob[0]=prob[0]-0.03
            prob[1]=prob[1]+0.03
    best=min(best_list1)  
    worst=max(worst_list1)
    mean=np.mean(np.array(mean_list1))
    end=time() 
    D=(end-start)/5
    avg_time.append(D)
    #andis_min=valid_andis[valid_list.index(min(valid_list))]
    #check_valid(best_solutions_list[andis_min][0],best_solutions_list[andis_min][1],Ii,B1,r1,ri,Ui)   
    best_list.append(best)
    worst_list.append(worst)
    mean_list.append(mean)


# In[11]:


best_array=np.array(best_list)
worst_array=np.array(worst_list)
mean_array=np.array(mean_list)
avgtime_array=np.array(avg_time)
Instance_arr=np.array(Instance)
df_marks = pd.DataFrame({'Instance':Instance_arr,'best': best_array,'worst':worst_array,'avg':mean_array,'avg_time':avgtime_array})


# In[12]:


#writer = pd.ExcelWriter('PSO_ML_IRP_highcost.xlsx')
#df_marks.to_excel(writer)
#writer.save()


# In[ ]:


df_marks

