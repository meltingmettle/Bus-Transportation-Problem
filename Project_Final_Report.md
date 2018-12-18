# Main Idea

Due to the diversity of inputs, (parameter bus size, bus quantity, "troublemaker groups", and relative connectivity) we decided to use a combination of several different algorithms for our approximation.  We created several different algorithms which specialized in different cases, then created a handle to run each algorithm a constant factor of times and greedily select outputs which produced a higher score.

# Algorithms 
Algorithm 1: A “greedy” bus approach, which filled each bus by marking nodes in a O(bus_size)-runtime BFS style algorithm.  
The algorithm ran a BFS-style traversal, marking nodes which we "saw" during the traversal, then adding the most “seen” nodes to each bus, taking care to never add a node who will complete a list.  The algorithm chose a randomized starting node which added a touch of randomness without detracting from effectiveness, as the start node was considered equally with respect to the other nodes encountered during the BFS. 

Algorithm 2: For each bus, start with a randomly chosen node, then expand the bus in method similar to Dijkstra’s algorithm, maintaining a fringe of neighbors which are prioritized by the number of edges to the root vertex.  While the fringe is not empty and the bus is not full, the algorithm adds vertices and their neighbors to the fringe.  This algorithm require an additional sweep over remaining nodes to ensure each node was placed in a bus.  

Algorithm 3: is a replica of algorithm 2, but with less randomization. In the beginning, we separate rowdy groups, by placing the loneliest student (student with least friends in the rowdy group) in one bus and the student who is “furthest” (maximum shortest path) from loneliest student in another bus. Then, proceed with Alg 2: fill empty buses with 1 random student, then perform the rest of Alg 2.

Algorithm 4: This algorithm breaks rowdy groups in the same way as Algorithm 3. Then, fills empty buses with 1 random student. After that, the algorithm puts connected components (as much of it as can fit) into buses together. Finally, place students using the “find_best_bus” function which is described in Algorithm 2.

# Appendix and Notes
We used several different approaches to break up lists, with one algorithm storing bus statistics and preventing any addition from completing a list, and another algorithm adding the optimal riders, then doubling back to remove the least “friendly” person in order to break up a list.  


Ideally, we would want to make changes reversible at both points of the adding to buses (Dijkstra’s and node collection), either by tracking changes or randomly checking that any adjustment will improve the score. The non-deterministic algorithms had several possible worst case scenarios and edge cases which were difficult to catch.  Some inputs require very specific starting nodes to “grow” from. Additionally, maximizing the score for one bus might make it impossible to get higher scores for other cars.  

