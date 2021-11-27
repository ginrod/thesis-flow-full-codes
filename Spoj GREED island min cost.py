import sys
from heapq import heappop, heappush
    
oo = 2 ** 63
    
class Edge:
    def __init__(self, u, v, cap, cost, rev):
        self.u = u
        self.v = v
        self.flow = 0
        self.cap = cap
        self.cost = cost
        self.rev = rev
    
def add_edge(adj, u, v, capv, costv):
    adj[u].append(Edge(u, v, capv, costv, len(adj[v])))
    adj[v].append(Edge(v, u, 0, -costv, len(adj[u])-1))
    
    
def bellman_ford(adj, s):
    dist = [oo] * len(adj)
    dist[s] = 0
    
    for _ in range(len(adj)):
        for u in range(len(adj)):
            for e in adj[u]:
                if e.cap - e.flow > 0 and dist[e.v] > dist[e.u] + e.cost:
                    dist[e.v] = dist[e.u] + e.cost
    
    return dist
    
def dijkstra(adj, potential, s, t):
    dist, pi = [+oo] * len(adj), [None] * len(adj)
    
    dist[s] = 0
    heap = [(0, s)]
    
    while heap:
        du, u = heappop(heap)
    
        if dist[u] < du: continue
        if u == t: break
    
        for e in adj[u]:
            reduced_cost = potential[e.u] + e.cost - potential[e.v]
            if e.cap - e.flow > 0 and dist[e.v] > dist[e.u] + reduced_cost:
                dist[e.v] = dist[e.u] + reduced_cost
                heappush(heap, (dist[e.v], e.v))
                pi[e.v] = e
    
    return dist, pi
    
def min_cost_max_flow(adj, s, t, flow_limit = oo):
    min_cost, max_flow = 0, 0
    
    potential = bellman_ford(adj, s)
    
    while True:
        dist, pi = dijkstra(adj, potential, s, t)
        
        if dist[t] == +oo:
            break
    
        for v in range(len(adj)):
            potential[v] += dist[v]
                    
        limit, v = +oo, t
        while v:
            e = pi[v]
            limit = min(limit, e.cap - e.flow)
            v = e.u
        
        v, cost = t, 0
        while v:
            e = pi[v]
            e.flow += limit
            adj[v][e.rev].flow -= limit
            cost += e.cost
            v = e.u
        
        if max_flow + limit >= flow_limit:
            min_cost += limit * cost
            max_flow += flow_limit - max_flow
    
            return min_cost, max_flow
    
        min_cost += limit * cost
        max_flow += limit
    
    return min_cost, max_flow
    
def read_input():
    N = int(sys.stdin.readline())
    adj = [[] for _ in range(1 + N + 1)]
    s, t = 0, len(adj) - 1
    
    cap = [0] * (N + 1)
    for _ in range(N):
        card = int(sys.stdin.readline())
        cap[card] += 1
    
    for v in range(1, N + 1):
        if cap[v] > 0:
            add_edge(adj, s, v, cap[v], 0)
    
    e = int(sys.stdin.readline())
    for _ in range(e):
        xi, yi = map(int, sys.stdin.readline().split())
        add_edge(adj, xi, yi, oo, 1)
        add_edge(adj, yi, xi, oo, 1)
    
    for v in range(1, N + 1):
        add_edge(adj, v, t, 1, 0)
    
    return adj, s, t
    
    
ntest = int(sys.stdin.readline())
    
for _ in range(ntest):
    adj, s, t = read_input()
    
    min_cost, _ = min_cost_max_flow(adj, s, t)
    print(min_cost) 