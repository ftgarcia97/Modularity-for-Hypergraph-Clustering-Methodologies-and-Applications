# -*- coding: utf-8 -*-
"""
Created on Sat May 17 01:34:17 2025

@author: pactg
"""

import math
import scipy
import numpy as np
from Hyp_Cluster_Methods import F_hypmod1,F_hypmod3,LSHM_heuristic
from Hyp_benchmark_generator import Benati_Hyp_benchmark_generator

## Random hypergraph generation
s_min=2 
s_max=4
N=10
mu=0
noise=0
nc=5
L=3
n_hyp=100
nodes=range(1,N+1)
hyp_edges,nc1,partition=Benati_Hyp_benchmark_generator(N,s_min,s_max,mu,noise,nc,L,n_hyp)

## Data
rep={} # repetition of each hyperedge
W={} # weight on the projected graph
hyp_set={frozenset(e) for e in hyp_edges} # Set of hyperedges without repetition
for e in hyp_set:
    rep[e]=0
for e in hyp_edges:
    rep[frozenset(e)]=rep[frozenset(e)]+1
for i in nodes:
    W[i,i]=0
    for j in nodes:
        if(i<j):
            W[i,j]=len([e for e in hyp_edges if(i in e and j in e)])
            W[j,i]=W[i,j]
adj_M=np.zeros((N,N))
for i in nodes:
    for j in nodes:
        if(i<=j and W[i,j]>0):
            adj_M[i-1,j-1]=1
            adj_M[j-1,i-1]=1
adj_M = scipy.sparse.csr_array(adj_M)
dist_M=scipy.sparse.csgraph.shortest_path(adj_M)

exp_val={} # expected internal degree of a community for each possible community degree value
degree={} # Adjacent degree
degree_min=len(hyp_edges)
hyp_adj={}
for i in nodes:
    hyp_adj[i]=[e for e in hyp_set if(i in e)]
    degree[i]=len([e for e in hyp_edges if(i in e)])
    if(degree_min>degree[i]):
        degree_min=degree[i]
degree_sum=sum([degree[i] for i in nodes])

gamma=1-noise
gamma_e={}
for e in hyp_set:
    gamma_e[e]=math.ceil(len(e)*gamma)

exp_val[0]=0
for l in range(degree_min,degree_sum+1):
    exp_val[l]=0
    for e in hyp_edges:
        exp_val[l]=exp_val[l]+sum([(t-gamma_e[frozenset(e)]+1)*math.comb(l, t)*math.comb(degree_sum-l,len(e)-t)/math.comb(degree_sum,len(e)) for t in range(max(gamma_e[frozenset(e)],len(e)+l-degree_sum),min(len(e),l)+1)])

print(F_hypmod1(nodes,W)) # Projected modularity
print(F_hypmod3(hyp_set,nodes,gamma_e,rep,degree,degree_sum,exp_val)) # Hypergraph modularity

# LSHM heuristic
obj_heur=-math.inf
multi_start=5 # number of multi-starts
for start in range(multi_start):
    obj,part=LSHM_heuristic(nodes,degree,hyp_adj,exp_val,nc,hyp_set,rep,gamma_e)
    if(obj>obj_heur):
        obj_heur=obj
        partition_heur=part
print(partition_heur,obj_heur)