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
                if  a[i][j+1]>Ui[j]:    
                    flag=False
                    print(3)
        if np.sum(a[i,1: ])>C:
            flag=False
            print(4)          

    return flag


# In[4]:


def s0_OU(Ui,Ii0):
    s_inv=[]  
    x=Ui-Ii0
    s_inv=list(x)
    return (s_inv)  


# In[5]:


def find_cij(i,j,third):
    #print(i,j)
    cij=np.round(np.sqrt(((int(third[i][1])-int(third[j][1]))**2)+((int(third[i][2])-int(third[j][2]))**2)))
    return int(cij)  


# In[6]:


def calculate_p(pherom,d,x):
    y=0
    to_eta=[]
    p_list=[]
    pi=0
    intervals_list=[]
    for j in d:
        #print('x=',x)
        #print('j=',j)
        to_eta.append((pherom[x,j]**alpha)*((1/(find_cij(x,j,third)+0.1))**beta))
    for t in range(len(d)):
        p_list.append(to_eta[t]/sum(to_eta))
    for i in range(len(p_list)):
        h=pi+p_list[i]
        intervals_list.append ([pi,h])
        pi=pi+p_list[i]
    n1=np.random.uniform(0,1)     #random num
   # print(intervals_list)
   # print('n1=',n1)
    for i in intervals_list:
        if n1>i[0] and n1<i[1]:
            #print ('i=',i)
            y=intervals_list.index(i)
            #print ('index(i)=',z1)
   # print(z1+1) 
    return d[y]


# In[7]:


def construction(Ii,pherom,B,cv):
    B1=B
    Ii0=Ii.copy()
    count_visited=int(np.round(cv*n))
    inv=np.zeros((H,n+1))
    trans=np.zeros((H,count_visited+1))
    s_trans=[]
    s_trans.append(0)
    p=0
    B1=B
    for k in range(H):
        must_visit=[]
        d=list(np.arange(1,n+1)) 
        #print('d=',d)
        #d1=random.sample(d,count_visited)
        #print('d1',d1)
        q=random.uniform(0,1)
        #print('q=',q)
        if q<=q0:
            for i in range(count_visited):
                if len(s_trans)==count_visited+1:
                    break
                else:    
                    to_eta=[]
                    for j in d:
                        to_eta.append(pherom[s_trans[i],j]*(1/(find_cij(s_trans[i],j,third)+0.1)**beta))
                    #print('to_eta=',to_eta)    
                    max_andis=np.argmax(np.array(to_eta))   
                    #print('max_andis=',max_andis)
                    y=d[max_andis]
                    s_trans.append(y)
                    pherom[s_trans[i],y]=(1-Rho)*pherom[s_trans[i],y]+(Rho*(1/(find_cij(s_trans[i],y,third)+0.1)))     
                    pherom[y,s_trans[i]]=(1-Rho)*pherom[y,s_trans[i]]+(Rho*(1/(find_cij(y,s_trans[i],third)+0.1)))#EEE
                    #print('pherom=',pherom)
                    d.remove(y)
                    #print('d=',d)
        else:
            for i in range(count_visited):
                if len(s_trans)==count_visited+1:
                    break
                else:
                    z=calculate_p(pherom,d,s_trans[i])
                   # print('z=',z)
                    s_trans.append(z)
                    #print('s_trans=',s_trans)
                    pherom[s_trans[i],z]=(1-Rho)*pherom[s_trans[i],z]+(Rho*(1/(find_cij(s_trans[i],z,third)+0.1)))
                    pherom[z,s_trans[i]]=(1-Rho)*pherom[z,s_trans[i]]+(Rho*(1/(find_cij(z,s_trans[i],third)+0.1)))          
                    d.remove(z)            
        #print('s_trans=',s_trans)
        #s_inv=s0_OU(Ui,Ii) 
        s_inv=s0_OU(Ui,Ii)
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
        s_trans=[]
        s_trans.append(0)
        s_trans.extend(must_visit)
   
    return inv,trans.astype(int),pherom


# In[8]:


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


# In[9]:


def delta_to(x,y,trans_pop):
    delta=0
    for i in range(len(trans_pop)):
        for j in range(H):
            for t in range(trans_pop[i].shape[1]):
                if t==trans_pop[i].shape[1]-1:
                    break
                elif trans_pop[i][j][t]==x and trans_pop[i][j][t+1]==y:
                    delta+=1/(find_cij(x,y,third)+0.1)
                    #print(delta)
    return delta        


# In[10]:


def initial_sol_NN(Ii,B,cv):
    B1=B
    Ii0=Ii.copy()
    count_visited=int(np.round(cv*n))
    inv=np.zeros((H,n+1))
    trans=np.zeros((H,count_visited+1))
    s_trans=[]
    s_trans.append(0)
    p=0
    costumers=list(np.arange(1,n+1))
    for k in range(H):
        #print('B1=',B1)
        must_visit=[]
        for i in range(count_visited):
            if len(s_trans)==count_visited+1:
                break
            else:    
                min_list=[]
                for j in costumers:
                    #print('costumers',costumers)
                    min_list.append(find_cij(s_trans[i],j,third))
                #print('min list=',min_list)    
                next_costumer=np.argmin(np.array(min_list))  
                s_trans.append(costumers[next_costumer])
                costumers.remove(costumers[next_costumer])

        s_inv=s0_OU(Ui,Ii0)
        for i in range(len(s_inv)+1):
            if i ==len(s_inv):
                break
            else:    
                if i+1 not in s_trans:
                    s_inv[i]=0 
                Ii0[i]=Ii0[i]+s_inv[i]-ri[i]  
                if Ii0[i]<=0:
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
        # print('s_inv=',s_inv)
        inv[k]=s_inv[ : ]
        trans[k]=s_trans[ : ]
        #print('must_visit',must_visit)
        s_trans=[]
        s_trans.append(0)
        s_trans.extend(must_visit)
        #print('must_visit=',must_visit)
        costumers=list(np.arange(1,n+1)) 
        #costumers.remove(must_visit[0])
        #print('costumers=',costumers)
    return inv,trans.astype(int)


# In[11]:


#Instances_lowcost_H3
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


# In[12]:


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
    alpha=1
    beta=0.5
    Rho=0.1
    q0=0.5
    pherom=np.ones((n+1,n+1))
    #np.random.randint(200,210,(n+1)*(n+1)).reshape((n+1,n+1))
    np.fill_diagonal(pherom, 0, wrap=False)
    cost_matrix=np.zeros((n+1,n+1))
    for i1 in range(n+1):
        for j1 in range(n+1):
            cost_matrix[i1,j1]=find_cij(i1,j1,third)
    best_fitness=[]
    best_ant=[]
    inv_pop=[]
    trans_pop=[]
    if n<=30:
        v=0.75
        v1=20
    else:
        v=1
        v1=1   
    inv_pop.append(initial_sol_NN(Ii,B1,v)[0])
    trans_pop.append(initial_sol_NN(Ii,B1,v)[1])
    for k in range(5):
        for k1 in range(v1):
            for t in range(30):
                a,b,c=construction(Ii,pherom,B1,v)
                inv_pop.append(a)
                trans_pop.append(b)
                pherom=c  
                #print('pherom=',c)

            fitness_list=[]
            for i2 in range(len(inv_pop)):
                fitness_list.append(fitness(inv_pop[i2],trans_pop[i2],B1,r1,h1,hi,Ii,ri,third))
            best_ant_andis=np.argmin(np.array(fitness_list))
            best_fitness.append(fitness_list[best_ant_andis])
            best_ant.append([inv_pop[best_ant_andis],trans_pop[best_ant_andis]])
            #print('best_ant_andis=',best_ant_andis)
            #print('fitness_list=',fitness_list[best_ant_andis])
            for i3 in range(H):
                for x,y in zip(trans_pop[best_ant_andis][i3][ :-1],trans_pop[best_ant_andis][i3][1: ]):
                    #print(x,y)
                    delta=delta_to(x,y,trans_pop)
                    #print(delta)
                    pherom[x,y]=((1-Rho)*pherom[x,y])+(Rho*delta)
            pherom=pherom 
            inv_pop=[]
            trans_pop=[]
    
    best=min(best_fitness)
    worst=max(best_fitness)
    mean=np.mean(np.array(best_fitness))
    end=time() 
    D=(end-start)/5
    avg_time.append(D)
    #andis_min=valid_andis[valid_list.index(min(valid_list))]
    #check_valid(best_solutions_list[andis_min][0],best_solutions_list[andis_min][1],Ii,B1,r1,ri,Ui)   
    best_list.append(best)
    worst_list.append(worst)
    mean_list.append(mean)


# In[13]:


best_array=np.array(best_list)
worst_array=np.array(worst_list)
mean_array=np.array(mean_list)
avgtime_array=np.array(avg_time)
Instance_arr=np.array(Instance)
df_marks = pd.DataFrame({'Instance':Instance_arr,'best': best_array,'worst':worst_array,'avg':mean_array,'avg_time':avgtime_array})


# In[14]:


writer = pd.ExcelWriter('ACS_OU2_IRP.xlsx')
df_marks.to_excel(writer)
writer.save()


# In[ ]:




