import sys
from collections import deque

def augment(adj, flow, cap, u, t, level, limit):
    if limit == 0:
        return 0
    
    if u == t:
        return limit
    
    curr_flow = 0
    for v in adj[u]:
        if cap[u][v] - flow[u][v] > 0 and level[v] == level[u] + 1:
            aug = augment(adj, flow, cap, v, t, level, min(limit, cap[u][v] - flow[u][v]))
            flow[u][v] += aug
            flow[v][u] -= aug
            curr_flow += aug
            limit -= aug
    
    if not curr_flow:
        level[u] = None
    
    return curr_flow

def dinic(adj, flow, cap, s, t):
    q = deque()
    max_flow = 0
    while True:
        q.append(s)
        level = [None] * len(adj)
        level[s] = 0
        
        while q:
            u = q.popleft()
            for v in adj[u]:
                if cap[u][v] - flow[u][v] > 0 and level[v] == None:
                    level[v] = level[u] + 1
                    q.append(v)
        
        if level[t] == None:
            return max_flow
                
        max_flow += augment(adj, flow, cap, s, t, level, sum(cap[s][v] - flow[s][v] for v in adj[s]))

def bfs(adj, flow, cap, s):
    q = deque()
    q.append(s)
    visit = [False] * len(adj)
    visit[s] = True

    while q:
        u = q.popleft()
        for v in adj[u]:
            if cap[u][v] - flow[u][v] > 0 and not visit[v]:
                visit[v] = True
                q.append(v)
    
    return visit

def read_input():
    n, m = map(int, sys.stdin.readline().split())

    if not n and not m:
        return None
    
    adj = [[] for _ in range(n + 1)]
    flow = [[0] * len(adj) for _ in range(len(adj))]
    cap = [[0] * len(adj) for _ in range(len(adj))]
    s, t = 1, 2

    for _ in range(m):
        u, v, c = map(int, sys.stdin.readline().split())
        
        adj[u].append(v)
        flow[u][v] = 0
        cap[u][v] += c

        adj[v].append(u)
        flow[v][u] = 0
        cap[v][u] += c
    
    return adj, flow, cap, s, t

while True:
    network = read_input()

    if not network:
        break
    
    adj, flow, cap, s, t = network
    _ = dinic(adj, flow, cap, s, t)

    visit = bfs(adj, flow, cap, s)

    S = [u for u in range(len(adj)) if visit[u]]
    T = [v for v in range(len(adj)) if not visit[v]]

    for u in S:
        for v in T:
            if cap[u][v] > 0 and flow[u][v] > 0:
                print(f'{u} {v}')
    print()
