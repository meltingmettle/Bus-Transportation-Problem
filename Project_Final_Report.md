Due to the diversity of inputs, our algorithm was a combination of several different approaches. For each input, our algorithm runs each sub-algorithm and chooses the best result.

Algorithm 1: We used a “greedy” bus approach, which filled the bus by marking nodes in a O(bus_size)-runtime BFS style algorithm and adding the most “seen” nodes to each bus, taking care to never add a node who will complete a list.  Due to an unusual bug, the nondeterministic nature of the algorithm results in occasional empty buses, which we were unable to debug in the time frame.  

Algorithm 2: We began by randomly choosing one node for each bus. For each bus, we then expanded the bus in a similar method to Dijkstra’s algorithm, maintaining a fringe of neighbors, prioritized by the number of edges to the root vertex.  While the fringe is not empty and the bus is not full, we pull from the fringe and add its neighbors to the fringe.  After doing this for every bus, we iterate over remaining nodes and find the optimal bus for each node. 

Algorithm 3: is a replica of algorithm 2, but with less randomization. In the beginning, we separate rowdy groups, by placing the loneliest student (student with least friends in the rowdy group) in one bus and the student who is “furthest” (maximum shortest path) from loneliest student in another bus. Then, proceed with Alg 2: fill empty buses with 1 random student, then perform the rest of Alg 2.

Algorithm 4: This algorithm breaks rowdy groups in the same way as Algorithm 3. Then, fills empty buses with 1 random student. After that, the algorithm puts connected components (as much of it as can fit) into buses together. Finally, place students using the “find_best_bus” function which is described in Algorithm 2.

We also used several different approaches to break up lists, with one algorithm storing bus statistics and preventing any addition from completing a list, and another algorithm adding the optimal riders, then doubling back to remove the least “friendly” person in order to break up a list.  

Weaknesses: Some inputs require very specific starting nodes to “grow” from. Maximizing the score for one bus might make it impossible to get higher scores for other cars.  

Room for improvement: At both points of the adding to buses (dijkstra’s and node collection) we want to make changes reversible, either by tracking changes or randomly checking that any adjustment will improve the score. The non-deterministic algorithms had several possible worst case scenarios and edge cases which were difficult to catch.  



The majority of our computing was done on personal computers, as our algorithm did not require too much processing power.  

In addition to using NetworkX, we used the choice function from the Random library to nondeterministically choose a start nodes, and dipped into Math for the infinity.  
