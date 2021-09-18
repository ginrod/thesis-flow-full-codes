import sys
from heapq import heappop, heappush

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

def read_input():
    n, m, s, t = map(int, sys.stdin.readline().split())
    adj = [[] for _ in range(n)]

    for _ in range(m):
        u, v, c, w = map(int, sys.stdin.readline().split())
        add_edge(adj, u, v, c, w)

    return adj, s, t

def bellman_ford(adj):
    potential = [0] * len(adj)

    for _ in range(len(adj)):
        for u in range(len(adj)):
            for e in adj[u]:
                reduced_cost = potential[e.u] + e.cost - potential[e.v]
                if e.cap > 0 and reduced_cost < 0:
                    potential[e.v] += reduced_cost
    
    return potential

def dijkstra(adj, potential, s, t):
    oo = float('inf')
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

def min_cost_max_flow(adj, s, t):
    min_cost, max_flow = 0, 0
    oo = float('inf')

    potential = bellman_ford(adj)

    while True:
        dist, pi = dijkstra(adj, potential, s, t)
        
        if dist[t] == +oo:
            break
            
        for u in range(len(adj)):
            if dist[u] < dist[t]:
                potential[u] += dist[u] - dist[t]
        
        limit, v = +oo, t
        while v:
            e = pi[v]
            limit = min(limit, e.cap - e.flow)
            v = e.u
        
        # max_limit_reached = max_flow + limit >= flow_limit
        # limit = max_limit_reached and flow_limit - max_flow or limit

        # if max_limit_reached:
        #     min_cost += limit * (potential[t] - potential[s])
        #     max_flow += limit

        #     return min_cost, max_flow
        
        v = t
        while v:
            e = pi[v]
            e.flow += limit
            adj[v][e.rev].flow -= limit
            v = e.u
        
        min_cost += limit * (potential[t] - potential[s])
        max_flow += limit
    
    return min_cost, max_flow

adj, s, t = read_input()

min_cost, max_flow = min_cost_max_flow(adj, s, t)
print('{0} {1}'.format(max_flow, min_cost))