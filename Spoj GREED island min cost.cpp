#include <bits/stdc++.h>

using namespace std;

#define endl '\n'
#define edges vector<vector<int>>
#define graph vector<vector<Edge>>
#define pii pair<int,int>

const int oo = 0x3f3f3f3f;;

struct Edge {
    int u, v, cap, flow, cost, rev;

    Edge() : u(), v(), cap(), flow(), cost(), rev() {}
    Edge(int _u, int _v, int _cap, int _cost, int _rev)
        : u(_u), v(_v), cap(_cap), flow(0), cost(_cost), rev(_rev) {}
};

void addEdge(graph &adj, int u, int v, int capv, int costv) {
    adj[u].push_back({ u, v, capv, costv, (int)adj[v].size() });
    adj[v].push_back({ v, u, 0, -costv, (int)(adj[u].size() - 1) });
}

vector<int> bellmanFord(graph &adj) {
    auto potential = vector<int>((int)adj.size());

    for (int k = 0; k < (int)adj.size(); ++k)
        for (int u = 0; u < (int)adj[u].size(); ++u)
            for (auto &e: adj[u]) {
                int reducedCost = potential[e.u] + e.cost - potential[e.v];
                if (e.cap > 0 && reducedCost < 0)
                    potential[e.v] += reducedCost;
            }

    return potential;
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
    int minCost = 0, maxFlow = 0;

    auto potential = bellmanFord(adj);

    int s = 0, t = (int)(adj.size() - 1);

    while (true) {
        auto dijkstraResult = dijkstra(adj, potential, s, t);
        auto dist = dijkstraResult.first;
        auto pi = dijkstraResult.second;

        if (dist[t] == +oo)
            break;

        for (int u = 0; u < (int)adj.size(); ++u)
            if (dist[u] < dist[t])
                potential[u] += dist[u] - dist[t];

        int limit = +oo, v = t;
        while (v != s) {
            auto e = pi[v];
            limit = min(limit, e->cap - e->flow);
            v = e->u;
        }

        bool maxLimitReached = maxFlow + limit >= flowLimit;
        limit = maxLimitReached ? flowLimit - maxFlow : limit;

        if (maxLimitReached) {
            minCost += limit * (potential[t] - potential[s]);
            maxFlow += limit;

            return { minCost, maxFlow };
        }

        v = t;
        while (v != s) {
            auto e = pi[v];
            e->flow += limit;
            adj[v][e->rev].flow -= limit;
            v = e->u;
        }

        minCost += limit * (potential[t] - potential[s]);
        maxFlow += limit;
    }

    return { minCost, maxFlow };
}

graph readInput() {

    int N;
    cin >> N;
    graph adj = graph(1 + N + 1);
    int s = 0, t = (int)(adj.size() - 1);

    vector<int> cap = vector<int>(N + 1);

    for (int i = 1; i <= N; ++i) {
        int card;
        cin >> card;
        cap[card] += 1;
    }

    for (int v = 1; v <= N; ++v)
        if (cap[v] > 0)
            addEdge(adj, s, v, cap[v], 0);

    int e;
    cin >> e;

    for (int i = 0; i < e; ++i) {
        int xi, yi;
        cin >> xi >> yi;
        addEdge(adj, xi, yi, cap[xi], 1);
        addEdge(adj, yi, xi, cap[xi], 1);
        cap[yi] = max(cap[xi], cap[yi]);
    }

    for (int v = 1; v <= N; ++v)
        if (cap[v] > 0)
            addEdge(adj, v, t, 1, 0);

    return adj;
};

int main()
{
	ios_base::sync_with_stdio(0);
	cin.tie(0);

    int t;
    cin >> t;

    for (int i = 0; i < t; ++i) {
        auto adj = readInput();

        auto minCost = minCostMaxFlow(adj, +oo).first;
        cout << minCost << endl;
    }

    return 0;
}
