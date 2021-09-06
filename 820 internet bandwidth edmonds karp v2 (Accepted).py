import sys
from collections import defaultdict, deque

def augment(res, pi, s, v, min_edge):
    if v == s:
        return min_edge
    elif pi[v] != None:
        u = pi[v]
        flow = augment(res, pi, s, u, min(min_edge, res[u, v]))
        res[u,v] -= flow
        res[v,u] += flow

        return flow
    

def edmonds_karp(adj, res, s, t):
    max_flow, oo = 0, float('inf')
    while True:
        pi, visit = { u: None for u in adj }, { u: +oo for u in adj }
        visit[s] = 0
        q = deque()
        q.append(s)
        while q:
            u = q.popleft()
            if u == t: break
            for v in adj[u]:
                if res[u,v] > 0 and visit[v] == +oo:
                    visit[v] = visit[u] + 1
                    pi[v] = u
                    q.append(v)
        
        flow = augment(res, pi, s, t, +oo)

        if not flow:
            break
        
        max_flow += flow
    
    return max_flow

def read_input():
    n = int(sys.stdin.readline())

    if n == 0:
        return None

    s, t, c = map(int, sys.stdin.readline().split())

    adj, res = defaultdict(list), defaultdict(int)

    for _ in range(c):
        u, v, cap = map(int, sys.stdin.readline().split())

        adj[u].append(v)
        adj[v].append(u)

        res[u,v] += cap
        res[v,u] += cap
    
    return adj, res, s, t

# debug_test_case = {
#     1: {
#         'network': (
#             # adj
#             {1: [2, 3], 2: [1, 3, 4], 3: [1, 2, 4], 4: [2, 3]},
#             # res
#             {(1, 2): 20, (3, 2): 5, (1, 3): 10, (2, 3): 5, (4, 3): 20, (4, 2): 10, (3, 1): 10, (3, 4): 20, (2, 4): 10, (2, 1): 20},
#             # s 
#             1,
#             # t 
#             4,
#         )
#     }
# }

i = 1
while True:
    network = read_input()
    # network = i in debug_test_case and debug_test_case[i]['network'] or None

    if not network:
        break

    bandwidth = edmonds_karp(*network)

    print('Network {0}'.format(i))
    print('The bandwidth is {0}.\n'.format(bandwidth))
    
    i += 1