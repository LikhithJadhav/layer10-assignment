import pandas as pd
from data.loader import load_enron_emails
from extraction.extractor import extract_structured
from extraction.validator import validate_entities, validate_claims, repair_claims
from dedup.artifact_dedup import deduplicate_artifacts
from dedup.entity_canonicalization import canonicalize
from dedup.claim_dedup import deduplicate_claims
from graph.graph_builder import build_graph, save_graph
from graph.neo4j_store import store_entities, store_claims
from retrieval.retriever import retrieve_context
from retrieval.context_pack import create_context_pack
import json

def main():
    # 1.Load data
    print("Loading emails...")
    emails_df = load_enron_emails()
    emails = emails_df.to_dict('records')[:100]  # Limit for demo

    # 2.Deduplicate artifacts
    print("Deduplicating artifacts...")
    unique_emails = deduplicate_artifacts(emails)

    # 3. Extract structured data
    print("Extracting entities and claims...")
    all_entities = []
    all_claims = []
    for email in unique_emails:
        ents, clms = extract_structured(email)
        all_entities.extend(ents)
        all_claims.extend(clms)

    # 4.Validate
    print("Validating...")
    valid_entities = validate_entities(all_entities)
    valid_claims = validate_claims(all_claims)
    valid_claims = repair_claims(valid_claims)

    # 5.Canonicalize entities
    print("Canonicalizing entities...")
    canonical_entities = canonicalize(valid_entities)

    # 6.Deduplicate claims
    print("Deduplicating claims...")
    merged_claims = deduplicate_claims(valid_claims)

    # 7.Build graph
    print("Building graph...")
    G = build_graph(valid_entities, valid_claims)
    save_graph(G, "graph.pkl")


    store_entities(valid_entities)
    store_claims(valid_claims)
 
    # 8. Example retrieval
    question = "Who works for Enron?"
    context = retrieve_context(question, "graph.pkl")
    pack = create_context_pack(question, context)
    with open("example_context_pack.json", "w") as f:
        json.dump(pack.to_dict(), f, indent=2)

    print("Pipeline complete. Graph saved to graph.pkl, context pack to example_context_pack.json")

if __name__ == "__main__":
    main()