import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Build city graph
G = nx.Graph()
G.add_edge("Bangalore", "Chennai", weight=350)
G.add_edge("Chennai", "Hyderabad", weight=500)
G.add_edge("Bangalore", "Hyderabad", weight=600)
G.add_edge("Hyderabad", "Mumbai", weight=700)
G.add_edge("Mumbai", "Delhi", weight=1400)
G.add_edge("Chennai", "Kolkata", weight=1600)
G.add_edge("Kolkata", "Delhi", weight=1500)

def manual_dijkstra(graph, start, end):
    # graph: networkx graph
    # start, end: nodes

    # Min-heap for priority queue
    queue = [(0, start, [])]  # (distance, current_node, path_taken)
    visited = set()

    while queue:
        (dist, current_node, path) = heapq.heappop(queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path = path + [current_node]

        if current_node == end:
            return path, dist

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                weight = graph[current_node][neighbor]['weight']
                heapq.heappush(queue, (dist + weight, neighbor, path))

    return None, float('inf')  # no path found

# Streamlit UI
st.title("🗺️ Smart Journey Planner (Manual Dijkstra)")

st.markdown("Select source and destination to find the shortest route!")

cities = list(G.nodes)
source = st.selectbox("Select Source City", cities)
destination = st.selectbox("Select Destination City", cities)

if st.button("Find Best Route"):
    if source == destination:
        st.warning("Source and destination are the same.")
    else:
        result = manual_dijkstra(G, source, destination)
        if result[0] is None:
            st.error("No path exists between selected cities.")
        else:
            path, distance = result
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
