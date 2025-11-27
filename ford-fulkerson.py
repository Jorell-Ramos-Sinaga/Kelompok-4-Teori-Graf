import collections
import matplotlib.pyplot as plt
import networkx as nx

class FlowNetwork:
    def __init__(self, capacity_matrix: list[list[int]], node_labels: dict):
        self.N = len(capacity_matrix)
        self.capacity_matrix = capacity_matrix
        self.residual_graph = [row[:] for row in capacity_matrix] 
        self.flow_on_edges = collections.defaultdict(int)         
        self.node_labels = node_labels
        self.initial_edge_capacities = {}

        for u in range(self.N):
            for v in range(self.N):
                if capacity_matrix[u][v] > 0:
                    self.initial_edge_capacities[(u,v)] = capacity_matrix[u][v]

def edmonds_karp_solver(network: FlowNetwork, source: int, sink: int) -> tuple[int, list]:
    N = network.N
    total_max_flow = 0
    path_trace = []

    path_trace.append({
        'total_flow_before': 0,
        'path_flow': 0,
        'path_edges': [],
        'flow_state': network.flow_on_edges.copy()
    })

    while True:
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
                if parent[v] == -1 and network.residual_graph[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        
        if not path_found:
            break

        path_flow = float('inf')
        path_edges = []
        
        s_node = sink
        while s_node != source:
            u_node = parent[s_node]
            path_flow = min(path_flow, network.residual_graph[u_node][s_node])
            path_edges.append((u_node, s_node))
            s_node = u_node
        path_edges.reverse()

        path_trace.append({
            'total_flow_before': total_max_flow,
            'path_flow': path_flow,
            'path_edges': path_edges.copy(),
            'flow_state': network.flow_on_edges.copy()
        })
        
        total_max_flow += path_flow
        
        s_node = sink
        while s_node != source:
            u_node = parent[s_node]
            
            if (u_node, s_node) in network.initial_edge_capacities:
                network.flow_on_edges[(u_node, s_node)] += path_flow

            network.residual_graph[u_node][s_node] -= path_flow 
            network.residual_graph[s_node][u_node] += path_flow 

            s_node = u_node

    path_trace.append({
        'total_flow_before': total_max_flow,
        'path_flow': 0, 
        'path_edges': [],
        'flow_state': network.flow_on_edges.copy()
    })

    return total_max_flow, path_trace

def visualize_flow(network: FlowNetwork, path_trace: list, max_flow: int, source: int, sink: int):
    N = network.N
    node_labels = network.node_labels
    initial_edge_capacities = network.initial_edge_capacities
    
    pos = {0: (0, 0), 1: (1, 1), 2: (2, 0), 3: (1, -1), 4: (3, 0)}

    for i, step in enumerate(path_trace):
        G_visual = nx.DiGraph()
        
        for u in range(N):
            G_visual.add_node(u, label=node_labels[u])
            for v, cap in initial_edge_capacities.items():
                if u == v[0]:
                    G_visual.add_edge(u, v[1], capacity=cap)

        is_final_step = (i == len(path_trace) - 1)
        
        plt.figure(figsize=(12, 7))

        if i == 0:
            title = "Graf Awal: Kapasitas Rute 'Nusantara Cepat'"
            flow_state = {}
            highlight_color = 'gray'
        elif is_final_step:
            title = f"Graf Akhir: Aliran Maksimum = {max_flow} Ton"
            flow_state = step['flow_state']
            highlight_color = 'blue'
        else:
            flow_state = step['flow_state']
            path_flow = step['path_flow']
            path_edges = step['path_edges']
            total_flow_after = step['total_flow_before'] + path_flow
            title = f"Augmenting Path #{i}: Flow = {path_flow} (Total: {total_flow_after} Ton)"
            highlight_color = 'blue'

        edge_colors = []
        edge_widths = []
        edge_labels_flow = {}

        for u, v in G_visual.edges():
            cap = initial_edge_capacities.get((u, v), 0)
            flow = flow_state.get((u, v), 0)
            
            if not is_final_step and (u, v) in step['path_edges']:
                edge_colors.append(highlight_color)
                edge_widths.append(3.0)
            elif flow == cap and cap > 0:
                edge_colors.append('red') 
                edge_widths.append(2.5)
            elif flow > 0:
                edge_colors.append('green') 
                edge_widths.append(1.5)
            else:
                edge_colors.append('gray')
                edge_widths.append(0.5)

            if i == 0:
                 edge_labels_flow[(u,v)] = f"C={cap}"
            else:
                edge_labels_flow[(u,v)] = f"{flow}/{cap}"

        nx.draw_networkx_nodes(G_visual, pos, node_size=2500, node_color='lightblue')
        nx.draw_networkx_labels(G_visual, pos, labels=node_labels, font_size=10, font_weight='bold')
        nx.draw_networkx_edges(G_visual, pos, node_size=2500, arrowstyle='->', arrowsize=20, edge_color=edge_colors, width=edge_widths)
        nx.draw_networkx_edge_labels(G_visual, pos, edge_labels=edge_labels_flow, font_size=9, font_color='black')
        
        plt.title(title, fontsize=16)
        plt.axis('off')
        plt.show()

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

network = FlowNetwork(capacity_matrix, node_labels_map)

max_flow_result, path_trace_data = edmonds_karp_solver(network, J, S)

visualize_flow(network, path_trace_data, max_flow_result, J, S)

print("\n==========================================================")
print("✅ Pemisahan Algoritma dan Visualisasi Selesai ✅")
print(f"Total Jumlah Langkah Augmenting Path: {len(path_trace_data) - 1}")
print("----------------------------------------------------------")
print(f"Total Aliran Maksimum (Maximum Flow): {max_flow_result} ton per hari")
print("==========================================================")
