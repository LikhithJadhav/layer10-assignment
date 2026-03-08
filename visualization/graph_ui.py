import streamlit as st
from pyvis.network import Network
import networkx as nx
from graph_builder import load_graph

st.title("Memory Graph Visualization")

graph_file = st.text_input("Graph file path", "graph.pkl")

if st.button("Load and Show Graph"):
    try:
        G = load_graph(graph_file)
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

        for node, data in G.nodes(data=True):
            net.add_node(node, label=data.get('label', node), color="#00ff00" if data.get('type') == 'person' else "#ff0000")

        for edge in G.edges(data=True):
            net.add_edge(edge[0], edge[1], title=f"{edge[2].get('relation', '')} (conf: {edge[2].get('confidence', 0)})")

        net.save_graph("temp_graph.html")
        with open("temp_graph.html", "r") as f:
            html = f.read()
        st.components.v1.html(html, height=800)
    except Exception as e:
        st.error(f"Error loading graph: {e}")