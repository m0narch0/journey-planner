import streamlit as st
import folium
from streamlit_folium import st_folium
from collections import defaultdict
import heapq

# Set page
st.set_page_config(page_title="India Journey Planner", layout="centered")

# Cities and coordinates
city_coords = {
    "Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777), "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639), "Bangalore": (12.9716, 77.5946), "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567), "Ahmedabad": (23.0225, 72.5714), "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462), "Kanpur": (26.4499, 80.3319), "Nagpur": (21.1458, 79.0882),
    "Indore": (22.7196, 75.8577), "Bhopal": (23.2599, 77.4126), "Visakhapatnam": (17.6868, 83.2185),
    "Patna": (25.5941, 85.1376), "Ranchi": (23.3441, 85.3096), "Coimbatore": (11.0168, 76.9558),
    "Thiruvananthapuram": (8.5241, 76.9366), "Guwahati": (26.1445, 91.7362)
}

# Graph edges with weights (distance)
edges = [
    ("Delhi", "Jaipur", 280), ("Delhi", "Lucknow", 500), ("Delhi", "Kanpur", 480),
    ("Delhi", "Mumbai", 1400), ("Delhi", "Bhopal", 780), ("Delhi", "Kolkata", 1500),
    ("Mumbai", "Pune", 150), ("Mumbai", "Hyderabad", 700), ("Mumbai", "Ahmedabad", 530),
    ("Mumbai", "Bangalore", 980), ("Chennai", "Bangalore", 350), ("Chennai", "Coimbatore", 500),
    ("Chennai", "Hyderabad", 630), ("Kolkata", "Patna", 580), ("Kolkata", "Ranchi", 400),
    ("Hyderabad", "Nagpur", 500), ("Nagpur", "Bhopal", 360), ("Bhopal", "Indore", 190),
    ("Indore", "Ahmedabad", 400), ("Ahmedabad", "Jaipur", 670), ("Lucknow", "Kanpur", 90),
    ("Kanpur", "Patna", 600), ("Patna", "Ranchi", 320), ("Visakhapatnam", "Hyderabad", 620),
    ("Visakhapatnam", "Kolkata", 880), ("Coimbatore", "Thiruvananthapuram", 380),
    ("Guwahati", "Kolkata", 1050), ("Bangalore", "Coimbatore", 360)
]

# Build graph
graph = defaultdict(list)
for u, v, w in edges:
    graph[u].append((v, w))
    graph[v].append((u, w))

# Dijkstra function
def dijkstra(graph, start, end):
    heap = [(0, start, [])]
    visited = set()
    while heap:
        dist, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return path, dist
        visited.add(node)
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (dist + weight, neighbor, path))
    return None, float('inf')

# Title
st.title("🗺️ India Journey Planner")
st.markdown("Plan your best route between major Indian cities using Dijkstra's Algorithm!")

# UI
cities = list(city_coords.keys())
source = st.selectbox("Select Source City", cities)
destination = st.selectbox("Select Destination City", cities)

# Store button click in session_state
if 'route_found' not in st.session_state:
    st.session_state.route_found = False

if st.button("Find Best Route"):
    if source == destination:
        st.warning("Source and destination are the same.")
        st.session_state.route_found = False
    else:
        st.session_state.route_found = True
        st.session_state.path, st.session_state.total_dist = dijkstra(graph, source, destination)

# Only display when button clicked
if st.session_state.route_found:
    path = st.session_state.path
    total_dist = st.session_state.total_dist
    st.success(f"Best Route: {' ➝ '.join(path)}")
    st.info(f"Total Distance: {total_dist} km")

    # Map visualization
    m = folium.Map(location=[22.0, 80.0], zoom_start=5)
    for city, coord in city_coords.items():
        folium.Marker(location=coord, popup=city).add_to(m)
    folium.PolyLine(locations=[city_coords[city] for city in path], color='red', weight=4).add_to(m)
    st_folium(m, width=700, height=500)
