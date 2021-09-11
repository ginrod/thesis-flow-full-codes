import sys
from collections import deque

def augment(adj, res, u, t, level, limit):
    if limit == 0:
        return 0
    
    if u == t:
        return limit
    
    flow = 0
    for v in adj[u]:
        if res[u][v] > 0 and level[v] == level[u] + 1:
            aug = augment(adj, res, v, t, level, min(limit, res[u][v]))
            res[u][v] -= aug
            res[v][u] += aug
            flow += aug
            limit -= aug
    
    if not flow:
        level[u] = None
    
    return flow

def dinic(adj, res, s, t):
    q = deque()
    max_flow = 0
    while True:
        q.append(s)
        level = [None] * len(adj)
        level[s] = 0
        while q:
            u = q.popleft()
            for v in adj[u]:
                if res[u][v] > 0 and level[v] == None:
                    level[v] = level[u] + 1
                    q.append(v)
        
        if level[t] == None:
            return max_flow
        
        max_flow+=augment(adj,res,s,t,level,sum(res[s][v]for v in adj[s]))

# debug_test_case = {
#     'adj': {1: [2, 3], 2: [1, 3, 2, 2], 3: [2, 1, 4, 4], 4: [3, 3]},
#     'res': {(1, 2): 3, (3, 2): 4, (1, 3): 2, (2, 3): 4, (4, 3): 6, (2, 2): 10, (3, 1): 2, (3, 4): 6, (2, 1): 3},
#     's': 1,
#     't': 4
# }

# debug_test_case = {
#     'adj': {0: [1, 2], 1: [0, 2, 1, 1], 2: [1, 0, 3, 3], 4: [3, 3]},
#     'res': {(1, 2): 3, (3, 2): 4, (1, 3): 2, (2, 3): 4, (4, 3): 6, (2, 2): 10, (3, 1): 2, (3, 4): 6, (2, 1): 3},
#     's': 1,
#     't': 4
# }

def read_input():
    N, M = map(int, sys.stdin.readline().split())
    adj, res, s, t = [[] for _ in range(N)], [[0] * N for _ in range(N)], 0, N - 1
    for _ in range(M):
        A, B, C = map(int, sys.stdin.readline().split())
        A -= 1
        B -= 1
        adj[A].append(B)
        adj[B].append(A)
        res[A][B] += C
        res[B][A] += C
    
    return adj, res, s, t

adj, res, s, t = read_input()
# adj, res, s, t = debug_test_case['adj'], debug_test_case['res'], debug_test_case['s'], debug_test_case['t'],

max_flow = dinic(adj, res, s, t)
print(max_flow)