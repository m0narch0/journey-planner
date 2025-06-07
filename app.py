import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Build city graph
G = nx.Graph()
G.add_edge("Bangalore", "Chennai", weight=350)
G.add_edge("Chennai", "Hyderabad", weight=500)
G.add_edge("Bangalore", "Hyderabad", weight=600)
G.add_edge("Hyderabad", "Mumbai", weight=700)
G.add_edge("Mumbai", "Delhi", weight=1400)
G.add_edge("Chennai", "Kolkata", weight=1600)
G.add_edge("Kolkata", "Delhi", weight=1500)

# Streamlit UI
st.title("🗺️ Smart Journey Planner")
st.markdown("Select source and destination to find the shortest route!")

cities = list(G.nodes)
source = st.selectbox("Select Source City", cities)
destination = st.selectbox("Select Destination City", cities)

if st.button("Find Best Route"):
    if source == destination:
        st.warning("Source and destination are the same.")
    else:
        try:
            path = nx.dijkstra_path(G, source, destination, weight='weight')
            distance = nx.dijkstra_path_length(G, source, destination, weight='weight')
            st.success(f"Best Route: {' ➝ '.join(path)}")
            st.info(f"Total Distance: {distance} km")

            # Visualize graph
            fig, ax = plt.subplots()
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, ax=ax)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

            # Highlight the path
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)

            st.pyplot(fig)

        except nx.NetworkXNoPath:
            st.error("No path exists between selected cities.")
