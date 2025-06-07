# Required modules
import streamlit as st
import folium
from streamlit_folium import st_folium
from collections import defaultdict
import heapq

# Setup the Streamlit app page
st.set_page_config(page_title="India Journey Planner", layout="centered")

# Dictionary holding city names with their geographical coordinates
city_locations = {
    "Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777), "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639), "Bangalore": (12.9716, 77.5946), "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567), "Ahmedabad": (23.0225, 72.5714), "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462), "Kanpur": (26.4499, 80.3319), "Nagpur": (21.1458, 79.0882),
    "Indore": (22.7196, 75.8577), "Bhopal": (23.2599, 77.4126), "Visakhapatnam": (17.6868, 83.2185),
    "Patna": (25.5941, 85.1376), "Ranchi": (23.3441, 85.3096), "Coimbatore": (11.0168, 76.9558),
    "Thiruvananthapuram": (8.5241, 76.9366), "Guwahati": (26.1445, 91.7362)
}

# Road connections between cities with distances in kilometers
routes = [
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

# Construct a graph as an adjacency list
road_map = defaultdict(list)
for city1, city2, dist in routes:
    road_map[city1].append((city2, dist))
    road_map[city2].append((city1, dist))

# Function implementing Dijkstra's shortest path algorithm
def find_shortest_path(graph, start_city, end_city):
    priority_q = [(0, start_city, [])]
    seen = set()

    while priority_q:
        current_distance, current_city, current_path = heapq.heappop(priority_q)

        if current_city in seen:
            continue

        updated_path = current_path + [current_city]
        if current_city == end_city:
            return updated_path, current_distance

        seen.add(current_city)

        for neighbor, distance in graph[current_city]:
            if neighbor not in seen:
                heapq.heappush(priority_q, (current_distance + distance, neighbor, updated_path))

    return None, float('inf')

# Streamlit interface
st.title("🗺️ India Journey Planner")
st.markdown("Use this tool to plan your travel between cities using the shortest route.")

# City selection dropdowns
all_cities = list(city_locations.keys())
origin = st.selectbox("Choose your starting city", all_cities)
destination = st.selectbox("Choose your destination city", all_cities)

# Initialize session state
if 'route_ready' not in st.session_state:
    st.session_state.route_ready = False

# Route finder logic
if st.button("Plan Route"):
    if origin == destination:
        st.warning("Starting point and destination are the same.")
        st.session_state.route_ready = False
    else:
        st.session_state.route_ready = True
        st.session_state.result_path, st.session_state.result_distance = find_shortest_path(road_map, origin, destination)

# Result display
if st.session_state.route_ready:
    best_path = st.session_state.result_path
    total_distance = st.session_state.result_distance

    st.success(f"Recommended Route: {' ➝ '.join(best_path)}")
    st.info(f"Estimated Travel Distance: {total_distance} km")

    # Show route on an interactive map
    journey_map = folium.Map(location=[22.0, 80.0], zoom_start=5)
    for city, location in city_locations.items():
        folium.Marker(location=location, popup=city).add_to(journey_map)

    folium.PolyLine([city_locations[city] for city in best_path], color='red', weight=4).add_to(journey_map)
    st_folium(journey_map, width=700, height=500)
