#include <bits/stdc++.h>

using namespace std;

#define endl '\n'
#define edges vector<vector<int>>
#define graph vector<vector<Edge>>
#define pii pair<int,int>

const int oo = (int)(2e32 / 2);

struct Edge {
    int u, v, cap, flow, cost, rev;

    Edge() : u(), v(), cap(), flow(), cost(), rev() {}
    Edge(int _u, int _v, int _cap, int _flow, int _cost, int _rev)
        : u(_u), v(_v), cap(_cap), flow(_flow), cost(_cost), rev(_rev) {}
};

void addEdge(graph &adj, int u, int v, int capv, int flowv, int costv) {
    adj[u].push_back({ u, v, capv, 0, costv, (int)adj[v].size() });
    adj[v].push_back({ v, u, 0, flowv, -costv, (int)(adj[u].size() - 1) });
}

graph readInput() {

    int m, n;
    cin >> m >> n;
    graph adj = graph(1 + m + n + 1);

    vector<int> a = vector<int>(m), b = vector<int>(n);

    for (int i = 0; i < m; ++i)
        cin >> a[i];

    for (int j = 0; j < n; ++j)
        cin >> b[j];

    for (int i = 0; i < m; ++i) {
        int u = 0, v = i + 1;
        addEdge(adj, u, v, a[i], 0, 0);
    }

    for (int j = 0; j < n; ++j) {
        int u = m + 1 + j, v = (int)adj.size() - 1;
        addEdge(adj, u, v, b[j], 0, 0);
    }

    for (int i = 0; i < m; ++i) {
        int cij;
        for (int j = 0; j < n; ++j) {
            cin >> cij;
            int u = i + 1, v = m + 1 + j;
            addEdge(adj, u, v, a[i], 0, cij);
        }
    }

    return adj;
};

vector<int> bellmanFord(graph &adj, int s) {
    auto dist = vector<int>((int)adj.size(), +oo);
    dist[s] = 0;

    for (int k = 0; k < (int)adj.size(); ++k)
        for (int u = 0; u < (int)adj[u].size(); ++u)
            for (auto &e: adj[u]) {
                if (e.cap - e.flow > 0 and dist[e.v] > dist[e.u] + e.cost)
                    dist[e.v] = dist[e.u] + e.cost;
            }

    return dist;
}

pair<vector<int>, vector<Edge*>> dijkstra(graph &adj, vector<int> &potential, int s, int t) {
    int n = (int)adj.size();
    auto dist = vector<int>(n, +oo);
    auto pi = vector<Edge*>(n);

    dist[s] = 0;
    priority_queue<pii, vector<pii>, greater<pii>> heap;
    heap.push({ 0, s });

    while (!heap.empty()) {
        auto p = heap.top(); heap.pop();
        int du = p.first, u = p.second;

        if (dist[u] < du) continue;
        if (u == t) break;

        for (auto &e: adj[u]) {
            int reducedCost = potential[e.u] + e.cost - potential[e.v];

            if (e.cap - e.flow > 0 && dist[e.v] > dist[e.u] + reducedCost) {
                dist[e.v] = dist[e.u] + reducedCost;
                heap.push({ dist[e.v], e.v });
                pi[e.v] = &e;
            }
        }
    }

    return { dist, pi };
}

pii minCostMaxFlow(graph &adj, int flowLimit) {
    int s = 0, t = (int)(adj.size() - 1);
    int minCost = 0, maxFlow = 0;

    auto potential = bellmanFord(adj, s);

    while (true) {
        auto dijkstraResult = dijkstra(adj, potential, s, t);
        auto dist = dijkstraResult.first;
        auto pi = dijkstraResult.second;

        if (dist[t] == +oo)
            break;

        for (int u = 0; u < (int)adj.size(); ++u)
            if (dist[u] < dist[t])
                potential[u] += dist[u];

        int limit = +oo, v = t, cost = 0;
        while (v != s) {
            auto e = pi[v];
            limit = min(limit, e->cap - e->flow);
            v = e->u;
        }

        v = t;
        while (v != s) {
            auto e = pi[v];
            e->flow += limit;
            adj[v][e->rev].flow -= limit;
            cost += e->cost;
            v = e->u;
        }

        if (maxFlow + limit >= flowLimit) {
            minCost += limit * cost;
            maxFlow += flowLimit - maxFlow;

            return { minCost, maxFlow };
        }

        minCost += limit * cost;
        maxFlow += limit;
    }

    return { minCost, maxFlow };
}

int main()
{
	ios_base::sync_with_stdio(0);
	cin.tie(0);

    int nTest;
    cin >> nTest;

    for (int i = 0; i < nTest; ++i) {
        auto adj = readInput();

        auto minCost = minCostMaxFlow(adj, +oo).first;
        cout << minCost << endl;
    }

    return 0;
}