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

def edmonds_karp(adj, res, s, t):
    max_flow, oo = 0, float('inf')
    while True:
        pi, visit = [None] * len(adj), [+oo] * len(adj)
        visit[s] = 0
        q = deque()
        q.append(s)
        while q:
            u = q.popleft()
            if u == t: break
            for v in adj[u]:
                if res[u][v] > 0 and visit[v] == +oo:
                    visit[v] = visit[u] + 1
                    pi[v] = u
                    q.append(v)
        
        flow = augment(res, pi, s, t, +oo)

        if not flow:
            break

        max_flow += flow
    
    return max_flow

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

max_flow = edmonds_karp(adj, res, s, t)
print(max_flow)