import networkx as nx
import os
from random import choice

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "./alg_1_outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

# def constraints_breaker(graph, num_buses, size_bus, constraints):
#     nodes = list(graph.nodes)
#     rem = nodes[0]
#     graph.remove(rem)
#     # graph.remove_node('1')
#     # for constraint in constraints:
#     #     # pick node with minimal degree
#     #     degrees_list = [graph.degree[node] for node in rowdy_group]
#     #     min_degree = min(degrees_list)
#     #     min_nodes = [constraints[i] for i in range(0, len(rowdy_group)) if degrees_list[i] == min_degree]
#     #     graph.remove_node(min_nodes[0])
#
# def remove_node_from_constraints(graph, num_buses, size_bus, constraints):
#     nodes =

#solve(graph, num_buses, size_bus, constraints)

#Add one more person

def solve(G, number_of_buses, bus_size, groups):
    S = G.copy()
    def BFS(vex, size): #do size = 2 * bus_size
        vcount = 0
        vcount_nodes = []
        # Mark all the vertices as not visited
        # Create a queue for BFS
        queue = []
        # Mark the source node as
        # visited and enqueue it
        queue.append(vex)
        seen[vex] = 1

        while size > vcount and queue:
            # Dequeue a vertex from
            # queue and print it
            vex = queue.pop(0)
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in nx.all_neighbors(G, vex):
                for n in nx.all_neighbors(G, i):  #Mark all of the bfs pop's neighbors as having been encountered
                    if n in seen:
                        seen[n] = seen[n] + 1
                    else:
                        seen[n] = 1
                if i in seen:
                    seen[i] = seen[i] + 1
                else:
                    seen[i] = 1
                    queue.append(i)
                    vcount = vcount + 1
                    vcount_nodes.append(i)
            for consider_nodes in vcount_nodes:
                seen_total[consider_nodes] = seen[consider_nodes]
                for neighbor in nx.all_neighbors(G, consider_nodes):
                    if neighbor in seen:
                        #Add neighbor's score to current vertex.
                        seen_total[consider_nodes] = seen_total[consider_nodes] + seen[neighbor]
    bus_list = {}
    #temp: remove a person from the list and add it back
    has_space = {}
    for b in range(number_of_buses):
        #Create bus
        bus_list[b] = []
        #Choose a random node?
        if not list(nx.nodes(G)):
            return bus_list.values()
        random_node = choice(list(nx.nodes(G)))
        #Start counting the number of neighbors we've seen
        #Seen: Vertex name -> number of times seen
        seen = {}
        seen_total = {}
        warning_list = {} #list number and number of people in it

        BFS(random_node, bus_size * 2)
        #check that the second exists
        bus_count = 0
        while bus_count < bus_size and seen:
            #Add highest node person and pop.
            #Get the max_seen person
            most_seen =  list(seen.keys())[list(seen.values()).index(max(seen.values()))]
            avoid_complete = False

            for rowdy_group in groups:
                identity = groups.index(rowdy_group)
                if most_seen in rowdy_group:
                    if most_seen in warning_list:
                        warning_list[identity] = warning_list[identity] + 1
                        if warning_list[identity] == len(rowdy_group):
                            #Skip this guy: pop, break, and start over.
                            #start the loop over
                            avoid_complete = True
                            break
                    else:
                        warning_list[identity] = 1

            if not avoid_complete:
                bus_list[b].append(most_seen)
                G.remove_node(most_seen)
                del seen[most_seen]
                bus_count = bus_count + 1
                avoid_complete = False
            else:
                del seen[most_seen]
                avoid_complete = False

        if not seen and bus_count != bus_size:
            has_space[b] = bus_size - bus_count

    #Create a dictionary of buses with space.

    list_of_bois = list(nx.nodes(G))

    #IF there are buses with space and list_of_bois is not empty
    if has_space and list_of_bois != []:
        for lonely_boi in list_of_bois:
            favorite_bus = None
            bus_temp = [0, 0]
            friends_list = [n for n in S.neighbors(lonely_boi)]
            for bus in has_space.keys():
                bus_temp[0] = bus
                bus_temp[1] = [fren for fren in bus_list[bus] if fren in friends_list]
                if favorite_bus == None:
                    favorite_bus = [bus_temp[0], bus_temp[1]]
                elif len(bus_temp[1]) > len(favorite_bus[1]):
                    favorite_bus = bus_temp

            #Add him to a bus
            bus_list[favorite_bus[0]].append(lonely_boi)
            #Subtract the number of available seats
            has_space[favorite_bus[0]] = has_space[favorite_bus[0]] - 1
            #If there are no more seats, remove from has_space
            if has_space[favorite_bus[0]] == 0:
                del has_space[favorite_bus[0]]
            #Remove lonely_boi from list of bois.
            list_of_bois.remove(lonely_boi)
            #Remove lonely_boi from graph for sake of thoroughness
            G.remove_node(lonely_boi)

    while not nx.is_empty(G):
        pests = list(nx.nodes(G))
        for pest in pests:
            av_bus = 0
            while len(bus_list[av_bus]) >= bus_size:
                av_bus = av_bus + 1
            bus_list[av_bus].append(pest)
            pests.remove(pest)
            G.remove_node(pest)


    if not nx.is_empty(G):
        #Make sure everyone is assigned
        return 1/0

    return bus_list.values()

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on eacha.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)

        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            if input_folder == "DS_Store":
                continue
            input_name = os.fsdecode(input_folder)
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            print(graph.nodes)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")

            #TODO: modify this to write your solution to your
            #      file properly as it might not be correct to
            #      just write the variable solution to a file
            if solution != None:
                for i in solution:
                    output_file.write(str(i) + "\n")

            output_file.close()

if __name__ == '__main__':
    main()
