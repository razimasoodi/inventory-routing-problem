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
            x=np.random.randint(0,Ui[i])
            if Ii0[i]+x-ri[i]<=Ui[i]:
                flag=False
                s_inv.append(x)
        flag=True        

    return s_inv 


# In[4]:


def initial_sol(Ii,U,H):
    Ui=U.copy()
    Ii0=Ii.copy()
    inv=np.zeros((H,n+1))
    trans=np.zeros((H,int(np.round(n*0.75))))
    for k in range(H):
        s_trans=[]
        s_trans.append(0)
        while(len(s_trans)!=(np.round(n*0.75))):
            r=np.random.randint(1,n+1)
            if r not in s_trans:
                s_trans.append(r)    

        s_inv=s0_ML(Ui,Ii0)   
        s_inv.insert(0,0) 
        for i in range(len(s_inv)):
            if i not in s_trans:
                s_inv[i]=0 
        s_inv.remove(0)
        s_inv.insert(0,(B1+r1)-sum(s_inv))  
        s_inv=np.array(s_inv)
        s_trans=np.array(s_trans)
        #print(s_inv.shape)
        inv[k]=s_inv[ : ]
        trans[k]=s_trans[ : ]
    return inv,trans.astype(int)


# In[5]:


def find_cij(i,j,third):
    #print(i,j)
    cij=np.round(np.sqrt(((int(third[i][1])-int(third[j][1]))**2)+((int(third[i][2])-int(third[j][2]))**2)))
    return cij   


# In[6]:


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
            supp_cost+=100
        supp_cost+=(B1)*h1
        #print(B1)
        #print('Ii0 before=',Ii0) 
        for j in range(a.shape[1]):
            if Ii0[j]<0:
                costumer_cost+=100
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
    
#print(costumer_cost)


# In[7]:


def tselect(population_inv,population_trans):
    parent_inv=[]
    parent_trans=[]
    parents_fitness=[]
    parent1_inv=[]
    parent1_trans=[]
    parents_fitness1=[]
    
    k=list(np.random.randint(0,len(population_inv),5))
    #print('k',k)
    for i in k:
        parent_inv.append(population_inv[i])
        parent_trans.append(population_trans[i])
    #print('parent=',parent)
    for j in range(len(parent_inv)):
        x=fitness(parent_inv[j],parent_trans[j],B1,r1,h1,hi,Ii,ri,third)
        parents_fitness.append(x)
    #print('parents_fitness=',parents_fitness)
    min_fitness=min(parents_fitness)
    idx_best=parents_fitness.index(min_fitness)
    best_chorom1_inv=parent_inv[idx_best]
    best_chorom1_trans=parent_trans[idx_best]

    k1=list(np.random.randint(0,len(population_inv) ,5))
    for i in k1:
        parent1_inv.append(population_inv[i])
        parent1_trans.append(population_trans[i])
    for j in range(len(parent1_inv)):
        y=fitness(parent1_inv[j],parent1_trans[j],B1,r1,h1,hi,Ii,ri,third)
        parents_fitness1.append(y)
        
    min1_fitness=min(parents_fitness1)
    idx_best1=parents_fitness1.index(min1_fitness)
    best_chorom2_inv=parent1_inv[idx_best1]
    best_chorom2_trans=parent1_trans[idx_best1]
    
    return [best_chorom1_inv,best_chorom1_trans],[best_chorom2_inv,best_chorom2_trans]


# In[8]:


def swap_mutation(s_inv,s_trans,H):
    random_horizen=np.random.randint(H)
    #print('random_horizen=',random_horizen)
    #s=s_inv.copy()
    t=s_trans[random_horizen].copy()
    a,b=np.random.randint(1,len(t),2)
    #print('a1=',a,'b1=',b)
    m=0
    #print("a=",a,"b=",b)
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
    #print(t)    
    s_trans[random_horizen]=t 
    #print(s_trans)
        
    return s_inv,s_trans


# In[9]:


def recombination(par1,par2,Ii0,U):
    Ii=Ii0.copy()
    Ui=U.copy()
    chorom1=par1.copy()
    chorom2=par2.copy()
    random_horizen1=np.random.randint(H)
    #print('random_horizen1=',random_horizen1)
    random_horizen2=np.random.randint(H)
    #print('random_horizen2=',random_horizen2)
    choromosome1=list(chorom1[1][random_horizen1].copy())
    choromosome2=list(chorom2[1][random_horizen2].copy())
    child1=[]
    child2=[]
    crossover=np.random.randint(1,len(choromosome1)-1)
    #print('crossover',crossover)
    child1.extend(choromosome1[0:crossover+1])
    #print('child1=',child1)
    child2.extend(choromosome2[0:crossover+1])
    #print('child2=',child2)
    while len(child1)!=len(choromosome1):
        for i in range(crossover+1,len(choromosome1)):
                if choromosome2[i] not in child1:
                    child1.append(choromosome2[i])
                    #print('child1=',child1)
        #print('child1n=',child1)            
        for i in range(0,crossover+1):
                if choromosome2[i] not in child1 and len(child1)!=len(choromosome1):  
                    child1.append(choromosome2[i])

    while len(child2)!=len(choromosome2):              
        for i in range(crossover+1,len(choromosome2)):
                if choromosome1[i] not in child2:
                    child2.append(choromosome1[i])
        for i in range(0,crossover+1):
                if choromosome1[i] not in child2 and len(child2)!=len(choromosome2):  
                    child2.append(choromosome1[i])
              
    for i in range(len(choromosome1)):
        if choromosome1[i] not in child1:
            chorom1[0][random_horizen1][choromosome1[i]]=0
        if child1[i] not in choromosome1:
            chorom1[0][random_horizen1][child1[i]]=np.random.randint(0,Ui[i]) 
       
    for i in range(len(choromosome2)):
        if choromosome2[i] not in child2:
            chorom2[0][random_horizen2][choromosome2[i]]=0
        if child2[i] not in choromosome2:
            chorom2[0][random_horizen2][child2[i]]=np.random.randint(0,Ui[i])  
            
            
    ch1=np.array(child1)
    ch2=np.array(child2)
    chorom1[1][random_horizen1]=ch1
    chorom2[1][random_horizen2]=ch2
    #print(chorom1)
    return chorom1,chorom2


# In[10]:


def elitism_select(population_inv,population_trans,child1,child2):
    count_pop=len(population_inv)
    fitness_list=[]  #the list of fitness
    new_population_inv=[]
    new_population_trans=[]
    X=[] 
    Y=[]    # listi moratab shode shamel tuple haie b shekle (fitness_value,choromosome)
    population_inv.append(child1[0])
    population_inv.append(child2[0])
    population_trans.append(child1[1])
    population_trans.append(child2[1])
    for i in range(len(population_inv)):
        x=fitness(population_inv[i],population_trans[i],B1,r1,h1,hi,Ii,ri,third)
        fitness_list.append(x)
    #print(len(fitness_list))
    m1=np.argmax(np.array(fitness_list).any()) 
    population_inv.remove(population_inv[m1])
    population_trans.remove(population_trans[m1])
    fitness_list.remove(fitness_list[m1])
    m2=np.argmax(np.array(fitness_list).any()) 
    population_inv.remove(population_inv[m2])
    population_trans.remove(population_trans[m2])
    fitness_list.remove(fitness_list[m2])
    best_sol=[population_inv[np.argmin(np.array(fitness_list))],population_trans[np.argmin(np.array(fitness_list))]]
    best_fitness=min(fitness_list)
    new_population_inv=population_inv
    new_population_trans=population_trans
    return new_population_inv,new_population_trans,best_sol,best_fitness


# In[11]:


def check_valid(s_inv,s_trans,Ii,B1,r1,ri,Ui):
    Ii0=Ii.copy()
    a=s_inv.copy()
    b=s_trans.copy()
    flag=True
    if a[ : ,0].any()<0:
        flag=False
       # print(0)
    for i in range(a.shape[0]):
        a[i,0]=(B1+r1)-sum(a[i,1: ])
        if B1<0:
            flag=False
           # print(2)
        for j in range(a.shape[1]):
            if j==len(Ii0):
                break
            else:    
                #if Ii0[j]<0:
                 #   flag=False
                  #  print(3)
                Ii0[j]=Ii0[j]+a[i][j+1]-ri[j]
                if  a[i][j+1]>Ui[j]:    
                    flag=False
                   # print(4)
        if np.sum(a[i,1: ])>C:
            flag=False
            #print(6)          
        B1=B1+r1-(np.sum(a[i,1: ]))

    return flag


# In[12]:


def elitism_select1(population_inv,population_trans,child1,child2):
    count_pop=len(population_inv)
    fitness_list=[]  #the list of fitness
    new_population_inv=[]
    new_population_trans=[]
    X=[] 
    Y=[]    # listi moratab shode shamel tuple haie b shekle (fitness_value,choromosome)
    population_inv.append(child1[0])
    population_inv.append(child2[0])
    population_trans.append(child1[1])
    population_trans.append(child2[1])
    for i in range(len(population_inv)):
        x=fitness(population_inv[i],population_trans[i],B1,r1,h1,hi,Ii,ri,third)
        fitness_list.append(x)

    X = sorted(zip(fitness_list,population_inv))
        #print(len(fitness_list))
    Y = sorted(zip(fitness_list,population_trans))
    for i in range(count_pop):
            new_population_inv.append(X[i][1])
            new_population_trans.append(Y[i][1])
            #print('count_pop=',count_pop)
    #print(len(new_population_inv))        
    #best_sol=
    best_fitness=X[0][0]
    best_sol=[X[0][1],Y[0][1]]
    return new_population_inv,new_population_trans,best_sol,best_fitness


# In[13]:


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
        for k in o:
            s=[]
            for j in k:
                s.append(float(j))
            z.append(s)
        adresses.append(z)  


# In[13]:


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
    population_inv=[]
    population_trans=[]
    for i1 in range(50):
        s,t=initial_sol(Ii,Ui,H)
        population_inv.append(s)
        population_trans.append(t)
    best_solutions_list=[]
    best_fitness_list=[]
    for i2 in range(5):
        for i3 in range(50):
            parent1,parent2=tselect(population_inv,population_trans)
            child1,child2=recombination(parent1,parent2,Ii,Ui)
            child1_after_mutate=swap_mutation(child1[0],child1[1],H)
            child2_after_mutate=swap_mutation(child2[0],child2[1],H)
            new_inv,new_trans,best_sol,value=elitism_select(population_inv,population_trans,child1_after_mutate,child2_after_mutate)
            best_solutions_list.append(best_sol)
            best_fitness_list.append(value)
            population_inv=new_inv
            population_trans=new_trans    
    valid_list=[]
    valid_andis=[]
    for i4 in range(len(best_fitness_list)):
        if check_valid(best_solutions_list[i4][0],best_solutions_list[i4][1],Ii,B1,r1,ri,Ui)==True:
            valid_list.append(best_fitness_list[i4])
            valid_andis.append(i4)
    if valid_list==[]:
        best=min(best_fitness_list)
        worst=max(best_fitness_list)
        mean=np.mean(np.array(best_fitness_list))
    else:    
        best=min(valid_list)
        worst=max(valid_list)
        mean=np.mean(np.array(valid_list))
    end=time() 
    D=(end-start)/5
    avg_time.append(D)
    #andis_min=valid_andis[valid_list.index(min(valid_list))]
    #check_valid(best_solutions_list[andis_min][0],best_solutions_list[andis_min][1],Ii,B1,r1,ri,Ui)   
    best_list.append(best)
    worst_list.append(worst)
    mean_list.append(mean)


# In[16]:


best_array=np.array(best_list)
worst_array=np.array(worst_list)
mean_array=np.array(mean_list)
avgtime_array=np.array(avg_time)


# In[21]:


Instance_arr=np.array(Instance)


# In[25]:


df_marks = pd.DataFrame({'Instance':Instance_arr[ :58],'best': best_array,'worst':worst_array,'avg':mean_array})
writer = pd.ExcelWriter('GA_ML_IRP_run20.xlsx')
df_marks.to_excel(writer)
writer.save()


# In[ ]:




