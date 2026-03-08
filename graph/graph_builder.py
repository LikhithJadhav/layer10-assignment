import networkx as nx
from schema import Entity, Claim

def build_graph(entities: List[Entity], claims: List[Claim]) -> nx.Graph:
    G = nx.Graph()

    for e in entities:
        G.add_node(e.id, label=e.name, type=e.type)

    for c in claims:
        if G.has_node(c.subject) and G.has_node(c.object):
            G.add_edge(c.subject, c.object, relation=c.relation, confidence=c.confidence, evidence=[ev.dict() for ev in c.evidence])

    return G

def save_graph(G, filename="graph.pkl"):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(G, f)

def load_graph(filename="graph.pkl"):
    import pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)