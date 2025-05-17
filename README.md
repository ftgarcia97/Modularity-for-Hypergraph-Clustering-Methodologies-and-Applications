# Hypergraph Modularity Clustering algorithms

Implementation of exact models, heuristic algorithms and instance generator that constitute the experimental section of the preprint that can be found in  https://ssrn.com/abstract=5188404 [1]. 
Thereby researchers and practitioners can replicate the experiments or use the algorithms.

## Description

File "Hyp_Cluster_Methods.py" contains the all Hypergraph clustering methods from the paper, exact models and heuristics.
File "Hyp_benchmark_generator.py" contains the random hypergraph generator based on h–ABCD [2] and configuration model [3].

## Dependencies

Algorithms are implemented in Python, and exact models are programmed and solved by Gurobi solver. It would be necessary to install Gurobi and download a Gurobi license to run the exact models 
(https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python).

## Executing program

"Example.py" shows how to run easily these algorithms. In addition, in both scripts, "Hyp_Cluster_Methods.py" and "Hyp_benchmark_generator.py", comment lines for each step can be found to understand better the procedures.

## Authors

Codes from this repository have been developed by researchers Stefano Benati from University of Trento, Justo Puerto from University of Seville and Francisco Temprano from University of Seville, 
and are part of the experimental section of the document [1].

## Citation information

Please cite paper [1] in case the implementation is used.

## References

[1] Benati, Stefano and Puerto, Justo and Temprano, Francisco, 
    Modularity for Hypergraph Clustering: Methodologies and Applications. 
    Available at SSRN: https://ssrn.com/abstract=5188404 or http://dx.doi.org/10.2139/ssrn.5188404

[2] Bogumił Kamiński, Paweł Prałat, François Théberge, 
    Hypergraph Artificial Benchmark for Community Detection (h–ABCD), Journal of Complex Networks, Volume 11, Issue 4, August 2023, cnad028, https://doi.org/10.1093/comnet/cnad028

[3] Newman, Mark,
    Networks: An Introduction – Oxford Scholarship. Oxford University Press. 2021. doi:10.1093/acprof:oso/9780199206650.001.0001. ISBN 9780191594175.
    
