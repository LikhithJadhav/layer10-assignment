from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import DBSCAN
from schema import Entity

model = SentenceTransformer('all-MiniLM-L6-v2')

def canonicalize(entities: List[Entity]) -> List[dict]:
    if not entities:
        return []

    names = [e.name for e in entities]
    embeddings = model.encode(names)

    #DBSCAN for clustering
    clustering = DBSCAN(eps=0.5, min_samples=1, metric='cosine').fit(embeddings)

    clusters = {}
    for i, label in enumerate(clustering.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(entities[i])

    canonical = []
    for cluster in clusters.values():
        # Choose the most common name as canonical
        names = [e.name for e in cluster]
        canonical_name = max(set(names), key=names.count)
        canonical.append({
            "canonical_name": canonical_name,
            "members": cluster
        })

    return canonical