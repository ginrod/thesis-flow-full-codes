import sys
from collections import deque

def augment(res, pi, s, v, limit):
    if v == s:
        return limit
    elif pi[v] != None:
        u = pi[v]
        flow = augment(res, pi, s, u, min(res[u][v], limit))
        res[u][v] -= flow
        res[v][u] += flow

        return flow

s, t, oo = 0, 1, float('inf')
res = [[0] * 102 for _ in range(102)]

while True:
    M, W = map(int, sys.stdin.readline().split())

    if not M and not W:
        break
    
    for i in range(2 * (M - 1)):
        for j in range(2 * (M - 1)):
            res[i][j] = 0

    for _ in range(M - 2):
        i, c = map(int, sys.stdin.readline().split())
        i -= 1
        u, v = 2 * i, 2 * i + 1
        res[u][v] = c
    
    for _ in range(W):
        j, k, d = map(int, sys.stdin.readline().split())
        j, k = j - 1, k - 1
        j, k = min(j, k), max(j, k)
        
        if j == 0 and k == M - 1:
            res[s][t], res[t][s] = d, d
        elif j == 0:
            u, v = 2 * k, 2 * k + 1 
            res[s][u], res[v][s] = d, d
        elif k == M - 1:
            u, v = 2 * j, 2 * j + 1
            res[t][u], res[v][t] = d, d
        else:
            u, v = 2 * j + 1, 2 * k
            res[u][v] = d
            u, v = 2 * k + 1, 2 * j
            res[u][v] = d

    max_flow = 0
    while True:
        visit, pi = [oo] * (2 * (M - 1)), [None] * (2 * (M - 1))
        visit[s] = 0
        q = deque()
        q.appendleft(s)
        while q:
            u = q.popleft()
            if u == t: break
            for v in range(2 * (M - 1)):
                if res[u][v] > 0 and visit[v] == oo:
                    visit[v] = visit[u] + 1
                    pi[v] = u
                    q.append(v)
        
        flow = augment(res, pi, s, t, oo)
        if not flow: break
        max_flow += flow

    
    print(max_flow)