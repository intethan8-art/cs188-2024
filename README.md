Project 1 : Search
    
    q1 q2 q3 q4
    DFS BFS UCS A*
    DFS & BFS are really similar  显式栈（recursion）
    UCS & A* & Dijkstra

    Dijkstra : Relaxation always fails on edges to visited vertices(visited vertices到source的距离本来就更短，而weight非负，加上当前node到source距离必然更远，故relaxation失效)
    对应PQ pop出的就是当前visit的节点，它对前面pop出的visited node毫无影响，只用考虑对还在PQ中的进行relaxation
    
    q5 
    为什么可以“随便定义 state”  接口！ search.py算法都是泛型，具体问题由searchAgents.py实现
    它从来不会做：
    state[0] 是什么？
    state.x 是什么？

    q6
    heuristic selection
    Manhattan function ---> MST （最小生成树 Prim算法）

    最小生成树 任一cutting中weight最小crossing edge必在MST中（反证法 树和环 最小）
    Generic algorithm：（1）找到一个cut，其crossing edges不在 MST中
                       （2）把weight最小的crossing edge加到MST中
                       （3）重复直到v-1条边
    关键：（1）
    Prim：从任意一个node出发，找最近的node连起来（weight最小的edge），以这样连起来的（在MST中的）为一个set，继续找最近的node
          优化：类似Dijkstra，避免遍历所有crossing edges   

    kruskal: 关注edge ，将边按weight从小到大排序，总是连weight最小的边除非形成了环。   
             假设连的是v-->w,所有与v相连的构成一个set，由于不构成环，故v与w本来在不同set，v-->w就是weight最小的cutting edge
             用一个PQ, 用一个WQU (weighted quick union) disjoint

    q7
    延续q6 选离得最近的k个有food的node做MST，同时为了避免MST紧密但实际上到最近的node可能很远的情况，补上nearest correction

    q8
    greedy 吃离自己最近的 利用继承使代码简洁
