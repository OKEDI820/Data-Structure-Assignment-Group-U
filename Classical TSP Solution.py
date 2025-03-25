#BARIGYE ROMEO 	2400704269 	24/U/04269/PS 
#OKEDI ISMAIL MUSA 	2400710601 	24/U/10601/EVE 
#AINEBYOONA DATIVAH 	2400702898 	24/U/02898/EVE 
#NANTALE CECILIA 	2400724555 	24/U/24555/PS
#KIGOZI ALLAN 	2400725792 	24/U/25792/PS 
#WALERA EMMANUEL	2400701410	24/U/1410





#chosen method is dynamic programimg algorithm.
import itertools

def held_karp(graph):
    """
    Solves the Traveling Salesman Problem using the Held-Karp algorithm (Dynamic Programming).
    
    Parameters:
    graph (list of list of int): Adjacency matrix representing the distances between cities.
    
    Returns:
    tuple: A tuple containing the optimal cost and the optimal path.
    """
    n = len(graph)
    C = {}

    # Base case: Start at city 0, then visit another city k
    for k in range(1, n):
        C[(1 << k, k)] = (graph[0][k], 0)

    # Iterate over subsets of increasing size
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = sum(1 << bit for bit in subset)  # Correct bitmask calculation
            for k in subset:
                prev_bits = bits & ~(1 << k)
                res = []

                for m in subset:
                    if m == k:
                        continue
                    if (prev_bits, m) in C:
                        res.append((C[(prev_bits, m)][0] + graph[m][k], m))

                C[(bits, k)] = min(res) if res else (float('inf'), -1)  # Avoid KeyError

    # Find the minimum cost to visit all cities and return to the start
    bits = (1 << n) - 2  # All cities visited except city 0
    res = []
    for k in range(1, n):
        if (bits, k) in C:
            res.append((C[(bits, k)][0] + graph[k][0], k))

    opt, parent = min(res)

    # Path reconstruction
    path = [0]
    while parent != 0:
        path.append(parent)
        next_bits = bits & ~(1 << parent)  # Remove current city
        parent = C.get((bits, parent), (None, 0))[1]  # Ensure key exists
        bits = next_bits

    path.append(0)
    
    return opt, path

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

# Solve the TSP using the Held-Karp algorithm
opt_cost, opt_path = held_karp(graph)

# Output the final route and total distance
print(f"Optimal Cost: {opt_cost}")
print(f"Optimal Path: {opt_path}")


#Optimal Cost: 49
#Optimal Path: [0, 5, 1, 4, 3, 2, 6, 0]
