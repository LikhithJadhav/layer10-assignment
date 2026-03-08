# Layer10 Memory System

This project implements a memory graph system for organizational knowledge from the Enron Email Dataset.

## Corpus
- **Dataset**: Enron Email Dataset
- **Source**: https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz
- **Description**: Email threads from Enron, containing communications, entities, and relationships.

## Setup
1. Clone repo
2. `pip install -r requirements.txt`
3. Run `python data/download.py` to download the dataset
4. Run `python data/loader.py` to parse emails
5. Run `python pipeline/pipeline.py` to process and build the graph
6. Run `streamlit run visualization/graph_ui.py` to visualize

## Ontology
- **Entities**: person, organization, project, etc.
- **Claims**: relationships like works_for, sent_email_to, discusses

## Extraction
Uses GPT-4o-mini for structured extraction with validation and retries.

## Deduplication
- Artifact: Hash-based and similarity-based
- Entity: Embedding-based clustering
- Claim: Merge by subject-relation-object

## Graph
NetworkX graph with entities as nodes, claims as edges.

## Retrieval
Semantic search on node labels, returns context packs.

## Visualization
Streamlit + PyVis interactive graph.

## Adaptation to Layer10
- For email/Slack: Similar extraction, add threading.
- For Jira: Structured fields as entities/claims.
- Long-term: Add timestamps, versioning, permissions.