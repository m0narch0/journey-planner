import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq  # we use this for priority queue

# Making the graph
graph = nx.Graph()

# adding cities and distances
graph.add_edge("Bangalore", "Chennai", weight=350)
graph.add_edge("Chennai", "Hyderabad", weight=500)
graph.add_edge("Bangalore", "Hyderabad", weight=600)
graph.add_edge("Hyderabad", "Mumbai", weight=700)
graph.add_edge("Mumbai", "Delhi", weight=1400)
graph.add_edge("Chennai", "Kolkata", weight=1600)
graph.add_edge("Kolkata", "Delhi", weight=1500)

# dijkstra implementation manually
def dijkstra_algo(graph, start, end):
    q = []
    heapq.heappush(q, (0, start, []))  # distance, node, path
    done = set()

    while q:
        dist, node, path = heapq.heappop(q)

        if node in done:
            continue

        done.add(node)
        path = path + [node]

        if node == end:
            return path, dist

        for neigh in graph.neighbors(node):
            if neigh not in done:
                cost = graph[node][neigh]['weight']
                heapq.heappush(q, (dist + cost, neigh, path))

    return None, float('inf')  # if no path found

# streamlit app part
st.title("Simple Journey Planner 🚗")
st.write("This app helps you find the best route between two cities using Dijkstra algorithm")

all_cities = list(graph.nodes)
src = st.selectbox("Choose starting city", all_cities)
dest = st.selectbox("Choose destination city", all_cities)

if st.button("Find route"):
    if src == dest:
        st.warning("Start and end cannot be same!")
    else:
        result = dijkstra_algo(graph, src, dest)
        if result[0] is None:
            st.error("Sorry, no route found")
        else:
            path, total = result
            st.success("Route found!")
            st.write(" ➝ ".join(path))
            st.write(f"Distance: {total} km")

            # draw map
            fig, ax = plt.subplots()
            pos = nx.spring_layout(graph, seed=1)
            nx.draw(graph, pos, with_labels=True, node_size=1200, node_color="lightblue", ax=ax)
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'), ax=ax)

            red_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(graph, pos, edgelist=red_edges, edge_color='red', width=3, ax=ax)

            st.pyplot(fig)
