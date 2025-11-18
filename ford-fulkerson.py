import collections
import matplotlib.pyplot as plt
import networkx as nx

def edmonds_karp_visualized(graph: list[list[int]], source: int, sink: int, node_labels: dict):
    N = len(graph)
    residual_graph = [row[:] for row in graph]
    total_max_flow = 0
    
    G_visual = nx.DiGraph()
    for i, label in node_labels.items():
        G_visual.add_node(i, label=label)
    
    initial_edge_capacities = {}
    for u in range(N):
        for v in range(N):
            if graph[u][v] > 0:
                G_visual.add_edge(u, v, capacity=graph[u][v], flow=0, label=f"0/{graph[u][v]}")
                initial_edge_capacities[(u,v)] = graph[u][v]

    pos = {0: (0, 0), 1: (1, 1), 2: (2, 0), 3: (1, -1), 4: (3, 0)} 

    plt.figure(figsize=(12, 7))
    nx.draw_networkx_nodes(G_visual, pos, node_size=2500, node_color='lightblue')
    nx.draw_networkx_labels(G_visual, pos, labels=node_labels, font_size=10, font_weight='bold')
    
    edge_labels_cap = {(u, v): f"C={initial_edge_capacities[(u,v)]}" for u, v in initial_edge_capacities}
    nx.draw_networkx_edges(G_visual, pos, node_size=2500, arrowstyle='->', arrowsize=20, edge_color='gray')
    nx.draw_networkx_edge_labels(G_visual, pos, edge_labels=edge_labels_cap, font_size=9, font_color='black')
    
    plt.title("Graf Awal: Kapasitas Rute 'Nusantara Cepat'", fontsize=16)
    plt.axis('off')
    plt.show()

    path_count = 0
    flow_on_edges = collections.defaultdict(int)

    while True:
        path_count += 1
        parent = [-1] * N
        queue = collections.deque([source])
        parent[source] = source

        path_found = False
        
        while queue:
            u = queue.popleft()
            
            if u == sink:
                path_found = True
                break
                
            for v in range(N):
                if parent[v] == -1 and residual_graph[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        
        if not path_found:
            break

        path_flow = float('inf')
        path_edges = []
        
        s_node = sink
        while s_node != source:
            u_node = parent[s_node]
            path_flow = min(path_flow, residual_graph[u_node][s_node])
            path_edges.append((u_node, s_node))
            s_node = u_node
        path_edges.reverse()

        plt.figure(figsize=(12, 7))
        plt.title(f"Augmenting Path #{path_count}: Flow = {path_flow} (Total Max Flow: {total_max_flow + path_flow})", fontsize=16)
        
        nx.draw_networkx_nodes(G_visual, pos, node_size=2500, node_color='lightblue')
        nx.draw_networkx_labels(G_visual, pos, labels=node_labels, font_size=10, font_weight='bold')
        
        edge_colors = []
        edge_widths = []
        edge_labels_current_flow = {}

        for u, v in G_visual.edges():
            if (u, v) in path_edges:
                edge_colors.append('red')
                edge_widths.append(3.0)
            else:
                edge_colors.append('gray')
                edge_widths.append(0.5)

            current_flow = flow_on_edges[(u, v)] if (u,v) in initial_edge_capacities else 0
            cap = initial_edge_capacities.get((u,v), 0)
            edge_labels_current_flow[(u,v)] = f"{current_flow}/{cap}"
        
        nx.draw_networkx_edges(G_visual, pos, node_size=2500, arrowstyle='->', arrowsize=20, edge_color=edge_colors, width=edge_widths)
        nx.draw_networkx_edge_labels(G_visual, pos, edge_labels=edge_labels_current_flow, font_size=9, font_color='black')
        
        plt.axis('off')
        plt.show()

        total_max_flow += path_flow
        
        s_node = sink
        while s_node != source:
            u_node = parent[s_node]
            
            if (u_node, s_node) in initial_edge_capacities:
                flow_on_edges[(u_node, s_node)] += path_flow
                G_visual[u_node][s_node]['flow'] = flow_on_edges[(u_node, s_node)]
                G_visual[u_node][s_node]['label'] = f"{flow_on_edges[(u_node, s_node)]}/{initial_edge_capacities[(u_node,s_node)]}"


            residual_graph[u_node][s_node] -= path_flow
            residual_graph[s_node][u_node] += path_flow 

            s_node = u_node

    plt.figure(figsize=(12, 7))
    
    edge_colors_final = []
    edge_widths_final = []
    edge_labels_final_flow = {}

    for u, v in G_visual.edges():
        flow = flow_on_edges.get((u, v), 0)
        cap = initial_edge_capacities.get((u, v), 0)
        
        edge_labels_final_flow[(u, v)] = f"{flow}/{cap}"
        
        if flow == cap and cap > 0:
            edge_colors_final.append('red')
            edge_widths_final.append(3.0)
        elif flow > 0:
            edge_colors_final.append('green')
            edge_widths_final.append(2.0)
        else:
            edge_colors_final.append('gray')
            edge_widths_final.append(0.5)

    nx.draw_networkx_nodes(G_visual, pos, node_size=2500, node_color='lightblue')
    nx.draw_networkx_labels(G_visual, pos, labels=node_labels, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G_visual, pos, node_size=2500, arrowstyle='->', arrowsize=20, 
                           edge_color=edge_colors_final, width=edge_widths_final)
    nx.draw_networkx_edge_labels(G_visual, pos, edge_labels=edge_labels_final_flow, font_size=9, font_color='black')
    
    plt.title(f"Graf Akhir: Aliran Maksimum = {total_max_flow} Ton", fontsize=16)
    plt.axis('off')
    plt.show()

    return total_max_flow

N_NODES = 5
J, B, Sm, Y, S = 0, 1, 2, 3, 4

node_labels_map = {
    J: 'J (Jakarta)', 
    B: 'B (Bandung)', 
    Sm: 'Sm (Semarang)', 
    Y: 'Y (Yogyakarta)', 
    S: 'S (Surabaya)'
}


capacity_matrix = [
    [0, 20, 15, 0, 0],
    [0, 0, 5, 10, 0],  
    [0, 0, 0, 0, 18],  
    [0, 0, 4, 0, 12],  
    [0, 0, 0, 0, 0]   
]

max_flow_result = edmonds_karp_visualized(capacity_matrix, J, S, node_labels_map)

print("\n==========================================================")
print("🚚 Studi Kasus: Ford-Fulkerson (Edmonds-Karp) dengan Visualisasi 🚚")
print(f"Node Source (Jakarta): {node_labels_map[J]}")
print(f"Node Sink (Surabaya): {node_labels_map[S]}")
print("----------------------------------------------------------")
print(f"Total Aliran Maksimum (Maximum Flow): {max_flow_result} ton per hari")
print("==========================================================")