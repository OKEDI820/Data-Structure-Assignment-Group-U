#BARIGYE ROMEO 	2400704269 	24/U/04269/PS 
#OKEDI ISMAIL MUSA 	2400710601 	24/U/10601/EVE 
#AINEBYOONA DATIVAH 	2400702898 	24/U/02898/EVE 
#NANTALE CECILIA 	2400724555 	24/U/24555/PS
#KIGOZI ALLAN 	2400725792 	24/U/25792/PS 
#WALERA EMMANUEL	2400701410	24/U/1410


import random
import math

def euclidean_distance(a, b):
    """Computes the Euclidean distance between two points."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def som_tsp(cities, max_epochs=1000, initial_lr=0.8, initial_radius=3):
    """
    Solves the Traveling Salesman Problem using a Self-Organizing Map (SOM) without NumPy.
    
    Parameters:
    cities (list of tuples): List of city coordinates (x, y).
    max_epochs (int): Number of training iterations.
    initial_lr (float): Initial learning rate.
    initial_radius (int): Initial neighborhood radius.
    
    Returns:
    list: The approximate route found by the SOM.
    """
    n = len(cities)

    # Initialize neurons in a circular arrangement
    theta = [2 * math.pi * i / n for i in range(n)]
    mean_x = sum(x for x, y in cities) / n
    mean_y = sum(y for x, y in cities) / n
    scale = max(max(x for x, y in cities) - min(x for x, y in cities),
                max(y for x, y in cities) - min(y for x, y in cities)) / 2
    neurons = [(mean_x + scale * math.cos(t), mean_y + scale * math.sin(t)) for t in theta]

    for epoch in range(max_epochs):
        lr = initial_lr * (1 - epoch / max_epochs)  # Decay learning rate
        radius = max(1, int(initial_radius * (1 - epoch / max_epochs)))  # Decay neighborhood radius

        for city in cities:
            # Find winner neuron (closest to city)
            distances = [euclidean_distance(neuron, city) for neuron in neurons]
            winner = distances.index(min(distances))

            # Update winner and neighbors
            for i in range(-radius, radius + 1):
                neighbor = (winner + i) % n
                influence = math.exp(- (i ** 2) / (2 * (radius ** 2)))  # Gaussian function
                
                # Move neuron toward the city
                neurons[neighbor] = (
                    neurons[neighbor][0] + lr * influence * (city[0] - neurons[neighbor][0]),
                    neurons[neighbor][1] + lr * influence * (city[1] - neurons[neighbor][1])
                )

    # Find nearest-neighbor mapping between neurons and cities
    route = []
    remaining = set(range(n))
    for city in cities:
        distances = {idx: euclidean_distance(neurons[idx], city) for idx in remaining}
        best_match = min(distances, key=distances.get)
        route.append(best_match)
        remaining.remove(best_match)

    return route

# Example input (list of city coordinates)
cities = [(0, 0), (1, 2), (3, 3), (6, 5), (8, 8), (10, 10), (12, 12)]

# Train the SOM on the given TSP graph data
route = som_tsp(cities)

# Function to calculate the total distance of a given route
def calculate_total_distance(route, graph):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += graph[route[i]][route[i + 1]]
    total_distance += graph[route[-1]][route[0]]  # Return to the starting city
    return total_distance

# Adjacency matrix representing the distances between cities
graph = [
    [0, 12, 10, 8, 12, 3, 9],  
    [12, 0, 12, 11, 6, 7, 9],  
    [10, 12, 0, 11, 10, 11, 6], 
    [8, 11, 11, 0, 7, 9, 12],  
    [12, 6, 10, 7, 0, 9, 10],  
    [3, 7, 11, 9, 9, 0, 11],   
    [9, 9, 6, 12, 10, 11, 0]   
]

# Convert route indices to city indices
city_route = [int(i) for i in route]

# Calculate the total distance of the route
total_distance = calculate_total_distance(city_route, graph)

# Output the final route and total distance
print(f"Approximate Route: {city_route}")
print(f"Total Distance: {total_distance} units")

#Approximate Route: [3, 4, 2, 5, 1, 0, 6]
#Total Distance: 68 units
