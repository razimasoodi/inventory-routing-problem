#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os


# In[2]:


# for instance 'abs1n5.dat'
file='abs1n5.dat'
data= np.loadtxt(r'abs1n5.dat',delimiter='\t',dtype=str)
#DATADIR="C:/Users/razeeee/instances_irp_large"
#DATADIR1="C:/Users/razeeee/Instances_lowcost_H3"
#path=os.path.abspath(DATADIR)
#path=os.path.abspath(DATADIR)
#data=[]
#for file in os.listdir(path):
    #data.append( np.loadtxt(r 'file',delimiter='\t',dtype=str))


# In[3]:


data


# In[4]:


first=[float(i) for i in data[0].split()]
second=[float(i) for i in data[1].split()]
third=[]
t=[]
for i in range(2,data.shape[0]):
    t=[float(j) for j in data[i].split()]
    third.append(t)
costumer=np.array(third)  
third.insert(0,second) #costumers+ supplier


# In[5]:


n=int(first[0])-1
H=first[1]
C=int(first[2])
x1=second[1]
y1=second[2]
B1=second[3]
r1=second[4]
h1=second[5]
X=costumer[ : ,1]    # array
Y=costumer[ : ,2]
Ii0=costumer[ : ,3]
Ui=costumer[ : ,4]
Li=costumer[ : ,5]
ri=costumer[ : ,6]
hi=costumer[ : ,7]
s0_inv=[]
s0_trans=[]
sn_inv=[]
sn_trans=[]


# In[6]:


def find_cij(i,j,third):
    #print(i,j)
    cij=np.round(np.sqrt(((int(third[i][1])-int(third[j][1]))**2)+((int(third[i][2])-int(third[j][2]))**2)))
    return cij


# In[7]:


def find_xij(a,b,s_trans):
    xij=[]
    for i in range(len(s_trans)-1):
        if (s_trans[i]==a and s_trans[i+1]==b) or (s_trans[i]==b and s_trans[i+1]==a):
            return 1
            break
    return 0   


# In[8]:


#initioial solution(OU)
def s0_OU(n,Ui,Ii0,costumer):
    s_trans=[]
    s_inv=[]
    s_trans.append(0)
    #w=list(np.random.randint(1,n,n))
    for i in range(n):
        r=np.random.randint(1,n)
        if r not in s_trans:
            s_trans.append(r)
    #print(s_trans)      
    x=costumer[ : ,4]-costumer[ : ,3]
    s_inv=list(x)
    return (s_trans,s_inv)    


# In[9]:


#initioial solution(ML)
def s0_ML(n,Ui,Ii0,costumer):
    s_trans=[]
    s_inv=[]
    s_trans.append(0)
    #w=list(np.random.randint(1,n,n))
    for i in range(n):
        r=np.random.randint(1,n)
        if r not in s_trans:
            s_trans.append(r)
    #print(s_trans)      
    flag=True
    for i in range(len(costumer)):
        while(flag):
            x=np.random.randint(0,costumer[i,4])
            if Ii0[i]+x-ri[i]<=Ui[i]:
                flag=False
                s_inv.append(x)
        flag=True        
    #for i in range(len(Ui)):
     #   s_inv.append(np.random.randint(0,Ui[i]-Ii0[i]))
    return (s_trans,s_inv)  


# In[10]:


#cost function
def cost_func(s0_inv,s0_trans):
    #h0=0.03
    #hi=np.random.uniform(0.01,0.05)
    #H=3
    supp_cost=0
    costumer_cost=0
    trans_cost=0
    Bt=[]
    Bt.append(B1)
    Iit=[]
    Iit.extend(list(Ii0))
    h=list(hi)
    r=list(ri)
    Ii=[]
    for i in range(int(H)+1):
        supp_cost+=Bt[i]*h1
        B=Bt[i]+r1-sum(s0_inv)
        Bt.insert(i+1,B)
    #for i in range(len(s0_inv)):
    for t in range(int(H)+1):
        costumer_cost+=h[t]*Iit[t]
        #print(costumer_cost)
        I=Iit[t]+s0_inv[t]-r[t]
        #print(I)
        if I<0:
            I=0
            #print(Iit)
            #print(Iit[t][i]+s0_inv[i]-r[i])
        Iit.insert(i+1,I)
        #print(Iit)    

    for i in s0_trans:
        for j in s0_trans:
            #print(find_cij(i,j,third))
            trans_cost+=find_xij(i,j,s0_trans)*find_cij(i,j,third)

    value=supp_cost+costumer_cost+trans_cost
    return value


# In[11]:


#neighbour of inventory
def noi(s_inv,s_trans,Ii0,Ui,h1):
    s=s_inv.copy()
    t=s_trans.copy()
    
    for j in range(len(s)):
        if h1>hi[j]:
       # k=s0_inv.index(s0_inv[j])
            s.remove(s[j])
            s.insert(j,int(Ui[j]-Ii0[j]))
        else:
            s.remove(s[j])
            s.insert(j,0)
            
    a=np.random.randint(1,len(t))
    #print("x=",a)
    b=np.random.randint(1,len(t))
    #print("y=",b)
    m=0
    if a==b:
        pass
    else:
        m=t[a]
        t[a]=t[b]
        t[b]=m    
    if t[0]!=0 and 0 not in t:
        t.insert(0,0)
    for i in t:
        if i>=6 or i<0:
            z=t.index(i)
            t.remove(i)
            t.insert(z,np.random.randint(1,n))
    for i in s_trans:
        if i>=6 or i<0:
            z=s_trans.index(i)
            s_trans.remove(i)
            s_trans.insert(z,np.random.randint(1,n))        
    #print(s_trans)
    return s_trans,s_inv,t,s


# In[12]:


solutions=[]
for t in range(5):
    T=500
    s0_trans,s0_inv=s0_ML(n,Ui,Ii0,costumer)
    #s0_trans,s0_inv=s0_OU(n,Ui,Ii0,costumer)
    value_s0=cost_func(s0_inv,s0_trans)
    for i in range(100):
        #print('i=',i)
        #for i in range(20*H):
        t,s,sn_trans,sn_inv=noi(s0_inv,s0_trans,Ii0,Ui,h1)
        #print('t=',t)
        #print('s=',s)
        #print('sn_inv,sn_trans=',sn_inv,sn_trans)
        value_sn=cost_func(sn_inv,sn_trans)
        deltaE=value_s0-value_sn
        #print(deltaE)
        #print(sn_inv)
        if deltaE<=0:
            s.clear()
            s.extend(sn_inv)
            #print(s0_inv)
            t.clear()
            t.extend(sn_trans)
        else:
            z=np.random.uniform(0,1)
            #print('z',z)
            prob=np.exp(-deltaE/T)
            #print('prob',prob)
            if z<=prob:
                s.clear()
                s.extend(sn_inv)
                #print(s0_inv)
                t.clear()
                t.extend(sn_trans)
        #print('s,t=',s,t)        
        #s0_inv.clear()
        s0_inv=s
        #s0_trans.clear()
        s0_trans=t 
        #print('s0_inv,s0_trans=',s0_inv,s0_trans)
        T=0.2*T    
    #print(s0_inv,s0_trans)  
    solutions.append(cost_func(s0_inv,s0_trans))

#print('cost of solution',s0_inv,s0_trans,'is:',cost_func(s0_inv,s0_trans))
print(file)
print('min of solution=', min(solutions))
print('max of solution=', max(solutions))
print('avg of solution=', np.mean(solutions))

