import sys
from collections import deque

oo = float('inf')

def augment(flow, cap, u, t, level, limit):
    if limit == 0:
        return 0
    
    if u == t:
        return limit
    
    curr_flow = 0
    for v in range(len(cap)):
        if cap[u][v] - flow[u][v] > 0 and level[v] == level[u] + 1:
            aug = augment(flow, cap, v, t, level, min(limit, cap[u][v] - flow[u][v]))
            flow[u][v] += aug
            flow[v][u] -= aug
            curr_flow += aug
            limit -= aug
    
    if not curr_flow:
        level[u] = None
    
    return curr_flow

def dinic(flow, cap, s, t):
    q = deque()
    max_flow = 0
    while True:
        q.append(s)
        level = [None] * len(cap)
        level[s] = 0
        
        while q:
            u = q.popleft()
            for v in range(len(cap)):
                if cap[u][v] - flow[u][v] > 0 and level[v] == None:
                    level[v] = level[u] + 1
                    q.append(v)
        
        if level[t] == None:
            return max_flow
                
        max_flow += augment(flow, cap, s, t, level, sum(cap[s][v] - flow[s][v] for v in range(len(cap))))

sys.stdin = open('cooling.in', 'r') 
sys.stdout = open('cooling.out', 'w')

n, m = map(int, sys.stdin.readline().split())
s = n + 2
t = s + 1
flow = [[0] * (t + 1) for _ in range(t + 1)]
cap = [[0] * (t + 1) for _ in range(t + 1)]

low = [0] * (m + 1)
up = [0] * (m + 1)

ws = [0] * (n + 1)
wt = [0] * (n + 1)

pipes = [None] * (m + 1)

for i in range(1, m+1):
    u, v, low[i], up[i] = map(int, sys.stdin.readline().split())
    pipes[i] = u, v
    ws[v] += low[i]
    wt[u] += low[i]

    cap[u][v] = up[i] - low[i]

for i in range(1, n+1):
    cap[s][i] = ws[i]
    cap[i][t] = wt[i]

max_flow = dinic(flow, cap, s, t)

if max_flow == sum(low):
    print("YES")
    for i in range(1, m+1):
        u, v = pipes[i]
        print(flow[u][v] + low[i])
else:
    print("NO")