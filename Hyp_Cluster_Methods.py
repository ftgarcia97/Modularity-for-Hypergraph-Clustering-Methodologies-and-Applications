import gurobipy as gp
from gurobipy import GRB
import random

# Random partition generation
def random_partition(iterable,k):
  results = [[] for i in range(k)]
  for value in iterable:
    x = random.randrange(k)
    results[x].append(value)
  return results

# LSHM heuristic algorithm
def LSHM_heuristic(nodes,degree,hyp_adj,exp_value,nc,hyp,rep,gamma_e):
        
    ## Initial partition: Random partition or use mathematical programming model to obtain a stable partition
    initial_partition=random_partition(nodes,nc)
    
    S={}
    obj_val={}
    degree_com={}
    peso_com={}
    for k in range(1,nc+1):
        S[k]=initial_partition[k-1]
        degree_com[k]=sum([degree[i] for i in S[k]])
        obj_val[k]=-exp_value[grados_com[k]]
        for e in hyp:
            weight_com[k,e]=len([i for i in e if(i in S[k])])-gamma_e[e]+1
            if(weight_com[k,e]>=1):
                obj_val[k]=obj_val[k]+weight_com[k,e]*rep[e]
    
    ## obj_val: Objective function value
    ## Initialize the maximum delta
    delta_max=1
    ## Initialize FeasibleMoves set
    while(delta_max>1.e-10):
        delta_max=0
        ## Add movement
        for k in range(1,nc+1):
            for i_star in S[k]:
                for r in range(1,nc+1):
                    if(k!=r):
                        dif1=exp_value[degree_com[k]]-exp_value[degree_com[k]-degree[i_star]]-sum([rep[e] for e in hyp_adj[i_star] if(weight_com[k,e]>=1)])
                        dif2=exp_value[degree_com[r]]-exp_value[degree_com[r]+degree[i_star]]+sum([rep[e] for e in hyp_adj[i_star] if(weight_com[r,e]>=0)])
                        if(dif1+dif2>delta_max + 1.e-10):
                            delta_max=dif1+dif2
                            max_dif1=dif1
                            max_dif2=dif2
                            max_move=(i_star,k,r)

        if(delta_max>1.e-10):
            i_star,k,r=max_move
            S[k]=list(set(S[k])-{i_star})
            S[r]=S[r]+[i_star]
            degree_com[k]=degree_com[k]-degree[i_star]
            degree_com[r]=degree_com[r]+degree[i_star]
            for e in hyp_adj[i_star]:
                weight_com[k,e]=weight_com[k,e]-1
            for e in hyp_adj[i_star]:
                weight_com[r,e]=weight_com[r,e]+1
            obj_val[k]=obj_val[k]+max_dif1
            obj_val[r]=obj_val[r]+max_dif2
    
    partition=[]
    for s in range(1,nc+1):
        if(len(S[s])>0):
            partition.append(set(S[s]))
    obj_val_total=sum([obj_val[k] for k in range(1,nc+1)])

    return obj_val_total,partition

## Projected modularity MILP formulation
def F_hypmod1(nodes,W):
    m_hypmod1 = gp.Model("model F_hypmod1")
    
    # Variables
    x={}
    k={}
    for i in nodes:
        k[i]=sum([W[i,j] for j in nodes]) # adjacent degree
        for j in nodes:
            if(i<j):
                x[i,j]=m_hypmod1.addVar(vtype=GRB.BINARY,name="x_"+str(i)+"_"+str(j))
    
    k_total=sum([k[i] for i in nodes])
    
    # Objective function
    m_hypmod1.setObjective(sum([sum([x[i,j]*(W[i,j]-k[i]*k[j]/(k_total-1)) for j in nodes if(i<j)]) for i in nodes]), GRB.MAXIMIZE)
    
    # Constraints
    for i in nodes:
        for j in nodes:
            for k in nodes:
                if(i<j<k):
                    m_hypmod1.addConstr(x[i,j]+x[j,k]-x[i,k]<=1)
                    m_hypmod1.addConstr(x[i,j]-x[j,k]+x[i,k]<=1)
                    m_hypmod1.addConstr(-x[i,j]+x[j,k]+x[i,k]<=1)
    
    # Solve the model
    m_hypmod1.setParam("LogToConsole",0)
    m_hypmod1.optimize()
    
    candidate_set=nodes
    partition=[]
    while(len(candidate_set)>0):
        nod=random.choice(candidate_set)
        candidate_set=list(set(candidate_set)-{nod})
        com={nod}
        for i in nodes:
            if(i<nod):
                if(x[i,nod].x>0.5):
                    com.add(i)
                    candidate_set=list(set(candidate_set)-{i})
            if(i>nod):
                if(x[nod,i].x>0.5):
                    com.add(i)
                    candidate_set=list(set(candidate_set)-{i})
        partition.append(com)
        
    # Return objective value and final partition
    return m_hypmod1.objVal,partition,m_hypmod1.Runtime


#Hypergraph modularity
def F_hypmod3(hyp,nodes,gamma_e,rep,degree,degree_total,exp_value):
    m_hypmod3 = gp.Model("model F_hypmod3")
    n=len(nodes)
    
    
    # Variables
    z={}
    h={}
    h_pos={}
    d={}
    
    ub_int={}
            
                
    for s in nodes:
        for i in nodes:
            if(i<=s):
                z[i,s]=m_hypmod3.addVar(vtype=GRB.BINARY,lb=0,ub=1,name="z_"+str(i)+"_"+str(s))
        for e in hyp:
            ub_int[e,s]=len([i for i in e if(i<=s)])
            h[e,s]=m_hypmod3.addVar(vtype=GRB.BINARY,lb=0,ub=1)
            h_pos[e,s]=m_hypmod3.addVar(vtype=GRB.CONTINUOUS,lb=0)
        for l in range(degree[s],degree_total-sum([degree[t] for t in nodes if(t>s)])+1):
            d[l,s]=m_hypmod3.addVar(vtype=GRB.BINARY,lb=0,ub=1,name="d_"+str(l)+"_"+str(s))
    
    
    
    # Objective function
    m_hypmod3.setObjective(sum([sum([(h[e,s]+h_pos[e,s])*rep[e] for e in hyp])-sum([d[l,s]*exp_value[l] for l in range(degree[s],degree_total-sum([degree[i] for i in nodes if(i>s)])+1)]) for s in nodes]), GRB.MAXIMIZE)
    
    # Constraints
    for i in nodes:
        m_hypmod3.addConstr(sum([z[i,s] for s in nodes if(i<=s)])==1)
        for s in nodes:
            if(i<s):
                m_hypmod3.addConstr(z[i,s]<=z[s,s])
    for s in nodes:
        m_hypmod3.addConstr(sum([d[l,s] for l in range(degree[s],degree_total-sum([degree[t] for t in nodes if(t>s)])+1)])==z[s,s])
        m_hypmod3.addConstr(sum([d[l,s]*l for l in range(degree[s],degree_total-sum([degree[t] for t in nodes if(t>s)])+1)])==sum([degree[i]*z[i,s] for i in nodes if(i<=s)]))
        
        for e in hyp:
            if(ub_int[e,s]>=gamma[e]):
                m_hypmod3.addConstr(gamma[e]*h[e,s]+h_pos[e,s]<=sum([z[i,s] for i in e if(i<=s)]))
                m_hypmod3.addConstr((ub_int[e,s]-gamma[e])*h[e,s]>=h_pos[e,s])
    
    ## Preprocessing
    m_hypmod3.addConstr(sum([sum([h[e,s]+h_pos[e,s] for e in hyp if(ub_int[e,s]<gamma[e])]) for s in nodes])==0)
    
    
    for s in nodes:
        for i in nodes:
            if(i<=s):
                if(s<max(nodes)):
                    z[i,s].start=0
                else:
                    z[i,s].start=1
    
    # Solve the model
    m_hypmod3.setParam("LogToConsole",0)
    m_hypmod3.setParam("TimeLimit",3600)
    m_hypmod3.optimize()
    
    partition=[]
    for s in nodes: 
        if(z[s,s].x>0.5):
            community={s}
            for i in nodes:
                if(i<s):
                    if(z[i,s].x>=0.5):
                        community.add(i)
            partition.append(community)

    # Return objective value and final partition
    return m_hypmod3.objVal,partition,m_hypmod3.Runtime
