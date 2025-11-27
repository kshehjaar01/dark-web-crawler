import csv
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from pathlib import Path

EDGES_CSV = "data/edges.csv"  # matches settings EDGES_CSV
GRAPH_PNG = "data/link_graph.png"
GRAPH_HTML = "data/link_graph.html"

def read_edges(path):
    edges = []
    if not Path(path).exists():
        print("No edges file found at", path)
        return edges
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            from_url = row.get("from")
            to_url = row.get("to")
            if from_url and to_url:
                edges.append((from_url, to_url))
    return edges

def build_and_save_graph(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Simplify node labels for readability: use domain or path summary
    labels = {}
    for n in G.nodes():
        labels[n] = (n if len(n) <= 40 else n[:37] + "...")

    plt.figure(figsize=(12, 9))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    nx.draw_networkx_nodes(G, pos, node_size=300, alpha=0.9)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=10)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.title("Link Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(GRAPH_PNG, dpi=200)
    print("Saved PNG graph to", GRAPH_PNG)

    # Interactive HTML via pyvis
    net = Network(height="800px", width="100%", directed=True)
    for n in G.nodes():
        net.add_node(n, label=labels[n], title=n)
    for u, v in G.edges():
        net.add_edge(u, v)
    net.show(GRAPH_HTML)
    print("Saved interactive HTML graph to", GRAPH_HTML)

if __name__ == "__main__":
    edges = read_edges(EDGES_CSV)
    if not edges:
        print("No edges to build graph.")
    else:
        build_and_save_graph(edges)
