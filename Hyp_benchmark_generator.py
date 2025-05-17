
import random
import math

##  Hypergraph benchmark generator algorithm based on LFR benchmark and h-ABCD benchmark

# s_min: Minimum community size
# s_max: Maximum community size
# nc_max: Maximum number of communities
# n_hyp: number of hyperedges
# L: maximum size of hyperedges
# 1-mu: fraction of hyperedges that are internal
# 1-noise: fraction of nodes from an internal hyperedge that belong to the same community

def Benati_Hyp_benchmark_generator(N,s_min,s_max,mu,noise,nc_max,L,n_hyp):
    nodes=range(1,N+1)
    nodes_null=nodes
    community_sizes=[]
    sum_sizes=0
    while(sum_sizes<N):
        if(N-sum_sizes<s_min):
            sum_sizes=0
            community_sizes=[]
        size=random.choices(range(s_min,s_max+1))[0]
        if(size>N-sum_sizes):
            size=N-sum_sizes
        community_sizes.append(size)
        sum_sizes=sum_sizes+size
        if(len(community_sizes)>nc_max):
            sum_sizes=0
            community_sizes=[]
    nc=len(community_sizes)
    com_null=set(range(1,nc+1))
    
    S={}
    for s in range(1,nc+1):
        S[s]=set()
    candidate_nodes=set(nodes)
    while(candidate_nodes!=set()):
        node=random.choice(list(candidate_nodes))
        community=random.choice(range(1,nc+1))
        S[community].add(node)
        candidate_nodes=candidate_nodes-{node}
        if(len(S[community])>community_sizes[community-1]):
            out_node=random.choice(list(S[community]))
            S[community]=S[community]-{out_node}
            candidate_nodes.add(out_node)
            
    hyp_edges=[]
    n_hyp_int=math.ceil((1-mu)*n_hyp)
    n_hyp_ext=n_hyp-n_hyp_int
    while(n_hyp_int>0):
        if(len(com_null)>0):
            com=random.choice([s for s in com_null])
        else:
            com=random.choice([s for s in range(1,nc+1)])
        
        max_size=min(L,math.floor(len(S[com])/(1-noise)))
        size_hyp=random.choice(list(range(2,max_size+1)))
        max_int_degree=min(size_hyp,len(S[com]))
        min_int_degree=max(math.ceil(size_hyp*(1-noise)),size_hyp-len([i for i in nodes if(i not in S[com])]))
        int_degree_hyp=random.choice(list(range(min_int_degree,max_int_degree+1)))
        nodes_null_com=[t for t in list(S[com]) if(t in nodes_null)]
        if(len(nodes_null_com)>0):
            n0=min(len(nodes_null_com),int_degree_hyp)
            select_int_nod_0=random.sample([t for t in list(S[com]) if(t in nodes_null_com)],n0)
            if(n0<int_degree_hyp):
                select_int_nod_1=random.sample([t for t in list(S[com]) if(t not in nodes_null_com)],int_degree_hyp-n0)
                select_int_nod=select_int_nod_0+select_int_nod_1
                com_null=com_null-{com}
            else:
                select_int_nod=select_int_nod_0
                if(len(nodes_null_com)==int_degree_hyp):
                    com_null=com_null-{com}
        else:
            select_int_nod=random.sample(list(S[com]),int_degree_hyp)
        
        nodos_ext=[i for i in nodes if(i not in S[com])]
        select_ext_nod=random.sample(nodos_ext,size_hyp-int_degree_hyp)
        
        h_edge=select_int_nod+select_ext_nod
        hyp_edges.append(h_edge)
        nodes_null=[t for t in nodes_null if(t not in select_int_nod)]
        n_hyp_int=n_hyp_int-1
    while(n_hyp_ext>0):
        size_hyp=random.choice(list(range(2,L+1)))
        select_nodes=random.sample(nodes,size_hyp)
        hyp_edges.append(select_nodes)
        n_hyp_ext=n_hyp_ext-1
        
        
    # Returning Hypergraph, number of communities and Ideal Partition
    return hyp_edges,nc,S
