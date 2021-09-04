import sys
from collections import defaultdict

def build_path(pi, t):
    u, path = t, []
    while u != None:
        path.append(u)
        u = pi[u]
    
    path.reverse()

    return path

def bfs(G, s):
    q = [s]
    pi, visit = { u: None for u in G }, { u: 0 for u in G }

    while q:
        u = q.pop()

        for v in G[u]:
            if v != s and not visit[v]:
                visit[v] = visit[u] + 1
                q.insert(0, v)
                pi[v] = u
    
    return pi, visit

def get_residual_network(G, rc):
    edges = [ (u,v) for v in G for u in G if rc(u, v) > 0]

    return { u: [v for w,v in edges if w == u] for u in G }

def read_job():
    job = {
    
    }

    while True:
        line = sys.stdin.readline()
        
        if not line or line == '\r' or line == '\n' or line == '\r\n':
            return job

        application_and_users, computers = line.split(' ')
        application, users = application_and_users[0], int(application_and_users[1:])
        computers = list(map(int, computers.strip()[:-1]))
        job[application] = (users, computers)

def edmonds_karp(G, edges):
    flow_dict = { (u, v): 0 for u,v in edges }
    c = lambda u,v: edges[u,v]
    f = lambda u,v: flow_dict[u,v]
    residual_capacity = lambda u,v : (u, v) in edges and \
                                        c(u,v) - f(u,v) or \
                                    (v, u) in edges and \
                                        f(v,u) or \
                                            0
    Gp = G

    while True:
        Gp = get_residual_network(Gp, residual_capacity)
        
        pi, _ = bfs(Gp, 's')
        path = build_path(pi, 't')
        
        if not path or path[0] != 's': 
            break
        
        path_pairs = [(path[k], path[k+1]) for k in range(len(path) - 1)]
        cp = min([residual_capacity(u, v) for u, v in path_pairs])

        for u, v in path_pairs:
            if (u,v) in edges:
                flow_dict[u, v] += cp
            elif (v, u) in edges:
                flow_dict[v, u] -= cp
    
    return Gp, sum([flow_dict[s,v] for s,v in flow_dict if s == 's'])

def compute_solution(job):
    G, edges = defaultdict(list), { }
    G['t'] = []
    apps, total_apps_to_run = set(job.keys()), 0

    for computer in range(10):
        G[computer] = ['t']

    for app, (users, computers) in job.items():
        G['s'].append(app)
        edges['s', app] = users

        for computer in computers:
            G[app].append(computer)
            edges[app, computer] = 1
            edges[computer, 't'] = 1
        
        total_apps_to_run += users
    
    Gp, maxflow = edmonds_karp(G, edges)

    if maxflow == total_apps_to_run:
        solution = ['_' for _ in range(10)]
        for computer in range(10):
            if computer in Gp and Gp[computer] and Gp[computer][-1] in apps:
                solution[computer] = Gp[computer][-1]

        return ''.join(solution)

    return None

# debug_test_case = {
#     1: {
#         'job': {
#             'A': (4, [0, 1, 2, 3, 4]), 'Q': (1, [5]), 'P': (4, [5, 6, 7, 8, 9])
#             }
#     },
#     2: {
#         'job': {
#             'A': (4, [0, 1, 2, 3, 4]), 'Q': (1, [5]), 'P': (5, [5, 6, 7, 8, 9])
#         }
#     }
# }

# i = 1
while True:
    job = read_job()
    # job = i in debug_test_case and debug_test_case[i]['job'] or None

    if not job:
        break

    solution = compute_solution(job)

    if solution:
        print(solution)
    else:
        print('!')
    
    # i += 1