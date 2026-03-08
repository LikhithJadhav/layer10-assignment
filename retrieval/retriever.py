from sentence_transformers import SentenceTransformer
import numpy as np
from graph_builder import load_graph
import networkx as nx

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(text):
    return model.encode(text)

def retrieve_context(question, graph_path="graph.pkl", top_k=5):
    G = load_graph(graph_path)
    q_emb = embed(question)

    # find nodes with similar names
    node_scores = {}
    for node, data in G.nodes(data=True):
        if 'label' in data:
            n_emb = embed(data['label'])
            sim = np.dot(q_emb, n_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(n_emb))
            node_scores[node] = sim

    top_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    # Get edges connected to top nodes
    context = []
    for node, score in top_nodes:
        neighbors = list(G.neighbors(node))
        for neigh in neighbors:
            edge_data = G.get_edge_data(node, neigh)
            context.append({
                "node1": G.nodes[node]['label'],
                "node2": G.nodes[neigh]['label'],
                "relation": edge_data.get('relation', ''),
                "confidence": edge_data.get('confidence', 0),
                "evidence": edge_data.get('evidence', [])
            })

    return context