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


#def initial_trans():
def initial_sol(B1,Ii0):
    s_trans=[]
    s_trans.append(0)
    while(len(s_trans)!=n+1):
        r=np.random.randint(1,n+1)
        if r not in s_trans:
            s_trans.append(r)
        #return s_trans 
    t=[]    
    t.append(0)
    for i in range(1,len(s_trans)):
        z=np.random.uniform(0,1)
        if z>=0.5:
            t.append(s_trans[i])
    s_inv=s0_OU(Ui,Ii0)   
    s_inv.insert(0,0) 
    for i in range(len(s_inv)):
        if i not in t:
            s_inv[i]=0 
    s_inv.remove(0)
    s_inv.insert(0,B1-sum(s_inv))  
    return (s_inv,t)


# In[4]:


def check_valid(s_inv,s_trans,Ii0):
    s=s_inv.copy()
    flag=True
    if s[0]<0:
        flag=False
    s.remove(s[0])   
    for i in range(len(s)):
        if  Ii0[i]+s[i]-ri[i]>Ui[i]:    #Ii0[i]+s[i]<ri[i] or
            flag=False
    return flag   


# In[5]:


def find_cij(i,j,third):
    #print(i,j)
    cij=np.round(np.sqrt(((int(third[i][1])-int(third[j][1]))**2)+((int(third[i][2])-int(third[j][2]))**2)))
    return cij   


# In[6]:


def swap(s_inv,s_trans):
    s=s_inv.copy()
    t=s_trans.copy()
    a,b=np.random.randint(1,len(t),2)
    #print('a1=',a,'b1=',b)
    m=0
    if a!=b:
        m=t[a]
        t[a]=t[b]
        t[b]=m   
    else:
        while(a==b):
            a,b=np.random.randint(1,len(t),2)
        #print('a=',a,'b=',b) 
        m=t[a]
        t[a]=t[b]
        t[b]=m
    return s,t,(a,b)


# In[7]:


def add(s_inv,s_trans,Ui,Ii0):
    q=np.arange(n+1)
    feasible_rout=[]
    for i in q:
        if i not in s_trans:
            feasible_rout.append(i)
    z=random.choice(feasible_rout)      
    s_trans.append(z)
    s=s0_OU(Ui,Ii0)
    s_inv[z]=s[z-1]
    s_inv[0]-=s[z-1]
    return s_inv,s_trans,z


# In[8]:


def delete(s_inv,s_trans):
    z=random.choice(s_trans[1: ])
    s_trans.remove(z)
    s_inv[0]+=s_inv[z]
    s_inv[z]=0
    return s_inv,s_trans,z


# In[9]:


def neighbour(s_inv,s_trans,Ui,Ii0):
    z=np.random.randint(-2,0)
    #print('z=',z)
    if z==-1 and len(s_trans)>2:    
        s,t,andis=delete(s_inv,s_trans)
        return s,t,(-1,andis)
    elif z==-2 and len(s_trans)<n-1:
        s,t,andis=add(s_inv,s_trans,Ui,Ii0)  
        return s,t,(-2,andis)
    elif z==-2 and len(s_trans)>2:
        s,t,andis=swap(s_inv,s_trans)
        return s,t,andis
    return s_inv,s_trans,(0,0)


# In[10]:


def cost(s_inv,s_trans,B1,r1,h1,hi,Ii0,ri,third,n):
    supp_cost=0
    costumer_cost=0
    trans_cost=0
    total_cost=0
    a=s_inv.copy()
    b=s_trans.copy()
    a.remove(a[0])
    supp_cost+=(B1+r1-(sum(a)))*h1
    if B1<0:
        supp_cost+=350
    #print('supp_cost=',supp_cost)
    for i in range(n):
        if Ii0[i]<0:
            if n>=20:
                costumer_cost+=30
            else:    
                costumer_cost+=300
        z=hi[i]*(Ii0[i]+a[i]-ri[i])
        costumer_cost+=z
    #print(costumer_cost)
    for i,j in zip(b[ :-1],b[1: ]):
        trans_cost+=find_cij(i,j,third)
    trans_cost+=find_cij(b[0],b[-1],third)
    total_cost=supp_cost+costumer_cost+trans_cost
    return total_cost


# In[11]:


def s0_OU(Ui,Ii0):
    s_inv=[]  
    x=Ui-Ii0
    s_inv=list(x)
    return (s_inv)  
#Instances_lowcost_H3


# In[12]:


path="C:/Users/razeeee/Instances_lowcost_H3"
adresses=[]
Instance=[]
for file in os.listdir(path):
    z=[]
    Instance.append(file)
    full_path = os.path.join(path, file)
    if os.path.isfile(full_path):
        #print (full_path)
        o=readFile(full_path)
        for i in o:
            s=[]
            for j in i:
                s.append(float(j))
            z.append(s)
        adresses.append(z)   


# In[14]:


min_list=[]
max_list=[]
mean_list=[]
for i in range(len(adresses)):
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
    Ii0=costumer[ : ,3]
    Ui=costumer[ : ,4]
    Li=costumer[ : ,5]
    ri=costumer[ : ,6]
    hi=costumer[ : ,7]
    result=[]
    s_inv,s_trans=initial_sol(B1,Ii0)
    while(len(s_trans)<=3 and check_valid(s_inv,s_trans,Ii0)==True):
        s_inv,s_trans=initial_sol(B1,Ii0) 
    #end = time() + 120
    #while time() < end:
    for i in range(5):
        tabu_list=[]
        l=int(n/2)+1    
        tabu_list.append((0,0))
        #print('s_inv,s_trans=',s_inv,s_trans)
        for i in range(H):
            #print('h=',i)
            sbest=[s_inv,s_trans]
            value_s=cost(s_inv,s_trans,B1,r1,h1,hi,Ii0,ri,third,n) 
            sbest_value=value_s
            #print(s_inv,s_trans)
            n0_inv,n0_trans,n0_andis=neighbour(s_inv,s_trans,Ui,Ii0)
            #print('n0_inv=',n0_inv)
            value_n0=cost(n0_inv,n0_trans,B1,r1,h1,hi,Ii0,ri,third,n)
            bestcandid=[n0_inv,n0_trans]
            best_value=value_n0
            #print('tabu_list=',len(tabu_list))
            for i in range(2*n):
                n_inv,n_trans,andis=neighbour(s_inv,s_trans,Ui,Ii0)
                #while(check_valid(n_inv,n_trans,Ii0)==True):
                #   n_inv,n_trans,andis=neighbour(s_inv,s_trans,Ui,Ii0)
                # print('n_inv=',n_inv)
                value_n=cost(n_inv,n_trans,B1,r1,h1,hi,Ii0,ri,third,n)
                #print('value=',value_n)
                #print('andis=',andis)
                t=n0_andis
                if value_n < value_n0 and andis not in tabu_list:
                    bestcandid[0]=n_inv
                    bestcandid[1]=n_trans
                    best_value=value_n
                    t=andis
                    #print('y')       
            if best_value<value_s:
                sbest[0]=bestcandid[0]
                sbest[1]=bestcandid[1]
                sbest_value=best_value
            tabu_list.append(t)
            if len(tabu_list)>l:
                tabu_list.remove(tabu_list[0]) 
            #print('tabu_list1=',len(tabu_list))    
            s=sbest[0]
            s_trans=sbest[1]
            B1=B1+r1-sum(s[1: ])
            #print('B1=',B1)
            #sup=s[0]
            s.remove(s[0])
            for i in range(n):
                k=Ii0[i]+s[i]-ri[i]
                    #print('k=',k)
                    #if k<0:
                     #   Ii0[i]=0
                    #else:
                Ii0[i]=k
               # print('Ii0=',Ii0)    
            s.insert(0,B1)
                #print('s=',s)
            s_inv=s


            #print('sbest=',sbest)
            #print('sbest_value=',sbest_value)
            result.append(sbest_value)
            #print('result=',result)
                                
    
    re=np.array(result)
    min_list.append(np.min(re))
    max_list.append(np.max(re))
    mean_list.append(np.mean(re))
        


# In[15]:


df_marks = pd.DataFrame({'Instance':Instance,'best': max_list,'avg': mean_list})

writer = pd.ExcelWriter('OU_run.xlsx')
df_marks.to_excel(writer)
writer.save()

