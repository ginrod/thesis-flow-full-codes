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
res = [[0] * 202 for _ in range(202)]

while True:
    N = sys.stdin.readline()

    if not N or N == '\r' or N == '\n' or N == '\r\n':
        break
    
    N = int(N)

    for i in range(2 * N + 2):
        for j in range( 2 * N + 2):
            res[i][j] = 0

    capacities = list(map(int, sys.stdin.readline().split()))

    for i in range(1, N+1):
        u, v = 2 * i, 2 * i + 1
        res[u][v] = capacities[i - 1]

    M = int(sys.stdin.readline())
    
    for _ in range(M):
        i, j, C = map(int, sys.stdin.readline().split())
        u, v = 2 * i + 1, 2 * j
        res[u][v] = C

    B, D = map(int, sys.stdin.readline().split())
    line = list(map(int, sys.stdin.readline().split()))
    B_line, D_line = line[:B], line[B:]

    oo = float('inf')
    for k in B_line:
        u = 2 * k
        res[s][u] = oo
    
    for k in D_line:
        v = 2 * k + 1
        res[v][t] = oo
    
    max_flow = 0
    while True:
        visit, pi = [oo] * (2 * N + 2), [None] * (2 * N + 2)
        visit[s] = 0
        q = deque()
        q.appendleft(s)
        while q:
            u = q.popleft()
            if u == t: break
            for v in range(2 * N + 2):
                if res[u][v] > 0 and visit[v] == oo:
                    visit[v] = visit[u] + 1
                    pi[v] = u
                    q.append(v)
        
        flow = augment(res, pi, s, t, oo)
        if not flow: break
        max_flow += flow

    
    print(max_flow)