import networkx as nx
import os
from random import choice
import math
import random

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
path_to_outputs = "./alg_3_outputs"

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

def solve(graph, num_buses, size_bus, constraints):
    print('start')
    #TODO: Write this method as you like. We'd recommend changing the arguments here as well
    #helpers
    def find_best_bus(node):
        comp = {}
        bad_friend = {}
        for i in range(num_buses):
            bad_friend[i] = set()
            comp[i] = 0
        full = set()
        for i in range(num_buses):
            if is_full(buses[i]):
                full.add(i)
        for neighbor in graph.adj[node]:
            bus = getbus[neighbor]
            if bus and not buses.index(bus) in full:
                comp[buses.index(bus)] += 1
        for i in list_containing[node]:
            lst = constraints[i]
            if len(lst) > 1 and in_one_bus(lst, node):
                if getbus[lst[0]]:
                    bus = getbus[lst[0]]
                else :
                    bus = getbus[lst[1]]
                for i in lst:
                    bad_friend[buses.index(bus)].add(i)
        for busindex in bad_friend.keys():
            if not busindex in full:
                lst = bad_friend[busindex]
                bus = buses[busindex]
                counter = 0
                for i in lst:
                    for neighbor in graph.adj[i]:
                        if bus == getbus[neighbor]:
                            if neighbor not in lst or i < neighbor:
                                counter += 1
                comp[busindex] -= counter
        index = max(comp, key = lambda x : -math.inf if x in full else comp.get(x))
        return buses[index]

    def is_full(bus):
        return len(bus) >= size_bus

    def add_to_bus(bus, node):
        bus.append(node)
        getbus[node] = bus
    def in_one_bus(lst, aspresent = None) :
        if not getbus[lst[0]]:
            if lst[0] != aspresent or not getbus[lst[1]]:
                return False
        for i in lst:
            if getbus[i] != getbus[lst[0]] and i != aspresent:
                return False
        return True
    def remove_from_bus(bus, node):
        bus.remove(node)
        getbus[node] = None

    def value(node, bus):
        counter = 0
        completes_list = False
        for i in list_containing[node]:
            lst = constraints[i]
            if in_one_bus(lst) :
                completes_list = True
                counter -= total_value(bus, lst)

        if not completes_list :
            if len(bus) < graph.degree[node] :
                for y in bus:
                    if graph.has_edge(node,y):
                        counter += 1
            else :
                for y in graph.neighbors(node):
                    if y in bus:
                        counter += 1
        return counter

    def total_value(bus, lst) :
        counter1 = 0
        counter2 = 0
        for node in lst:
            if len(bus) < graph.degree[node] :
                for y in bus:
                    if graph.has_edge(node,y):
                        counter1 += 1
            else :
                for y in graph.neighbors(node):
                    if y in bus:
                        counter2 += 1
        return counter1 + counter2/2
    def break_list(bus, lst):
        rtn = set()
        for i in lst:
            if not in_one_bus(constraints[i]):
                print("wrong")
            rtn.add(min(constraints[i], key = value_helper))
        return rtn
    def value_helper (node):
        counter = 0
        for neighbor in graph.adj[node]:
            if getbus[neighbor] == getbus[node]:
                counter += 1
        return counter

    # scored by: +1 for each mutual friend
    def mutual_friend_scorer(graph, node1, node2):
        score = 0
        for n in list(graph.nodes):
            if n == node1 or n == node2:
                pass
            elif graph.has_edge(node1, n) and graph.has_edge(node2, n):
                score += 1
        return score

    def degree_in_constraint(graph, node, constraint_list):
        score = 0
        for neighbor in constraint_list:
            if graph.has_edge(node, neighbor):
                score += 1
        return score


    #start

    start = []
    buses = [[] for x in range(num_buses)]
    nodes = list(graph.nodes)
    num = graph.number_of_nodes()
    getbus = {node:None for node in nodes}
    # makes dictionary of node mapped to a list of all the nodes which appear in rowdy groups with the node
    list_containing = {node:[] for node in nodes}
    for i in range(len(constraints)):
        for node in constraints[i]:
            list_containing[node].append(i)

    # BREAK CONSTRAINTS:
    bus_number = 0
    cons = 0
    for rowdy in constraints:
        rowdy_degree_dict = {}
        for node in rowdy:
            if node not in start:
                rowdy_degree_dict[node] = degree_in_constraint(graph, node, rowdy)
        if not bool(rowdy_degree_dict):
            loneliest = min(rowdy_degree_dict.keys(), key = rowdy_degree_dict.get)
            connection_to_loneliest_dict = {}
            for node in rowdy:
                if nx.has_path(graph, source=node, target=loneliest):
                    connection_to_loneliest_dict[node] = nx.shortest_path_length(graph, source=node, target=loneliest)
                else:
                    connection_to_loneliest_dict[node] = 0
            second_node = min(connection_to_loneliest_dict.keys(), key = connection_to_loneliest_dict.get)
            start.append(loneliest)
            add_to_bus(buses[bus_number], loneliest)
            if bus_number + 1 >= num_buses:
                start.append(second_node)
                add_to_bus(buses[0], second_node)
            else:
                start.append(second_node)
                add_to_bus(buses[bus_number + 1], second_node)
                bus_number += 2
                if bus_number >= num_buses:
                    bus_number = 0
            cons += 1
    if num_buses > cons:
        # add a random person to remaining buses
        for i in range(cons, num_buses):
            node = nodes[random.randint(0,num - 1)]
            while node in start :
                node = nodes[random.randint(0,num - 1)]
            start.append(node)
            add_to_bus(buses[i], node)

    # add connected components:
    conn_comps = [c for c in sorted(nx.connected_components(graph), key=len, reverse=True)]
    bus_idx = 0
    for comp in conn_comps:
        num_of_friends = 0
        for kid in comp:
            if kid not in start and num_of_friends + len(buses[bus_idx]) < size_bus:
                start.append(kid)
                add_to_bus(buses[bus_idx], kid)
                num_of_friends += 1
        bus_idx += 1
        if bus_idx >= num_buses:
            bus_idx = 0

    # for each bus
    for i in range(num_buses) :
        fringe = {}
        kicked = set()
        list_counter = {}
        for j in range(len(constraints)):
            list_counter[j] = len(constraints[j])
        bus = buses[i]
        for neighbor in graph.adj[bus[0]]:
            fringe[neighbor] = 1
        counter = 1
        while (fringe and counter < size_bus):
            lists_to_break = []
            node = max(fringe.keys(), key = fringe.get)
            fringe.pop(node)
            if getbus[node] == None:
                add_to_bus(bus, node)
                for i in list_containing[node]:
                    list_counter[i] -= 1
                    if list_counter[i] == 0:
                        lists_to_break.append(i)
                if (lists_to_break):
                    removed = break_list(bus, lists_to_break)
                    for item in removed:
                        remove_from_bus(bus, item)
                        for i in list_containing[item]:
                            list_counter[i] += 1
                        for neighbor in graph.adj[node]:
                            if neighbor in fringe:
                                fringe[neighbor] -= 1
                        kicked.add(item)
                    counter -= 1
                counter += 1
                if not node in kicked:
                    for neighbor in graph.adj[node]:
                        if not neighbor in bus and not neighbor in kicked :
                            if neighbor in fringe:
                                fringe[neighbor] += 1
                            else :
                                fringe[neighbor] = 1

    for node in list(graph.nodes) :
        if getbus[node] == None:
            bus = find_best_bus(node)
            add_to_bus(bus, node)
    for bus in buses:
        if len(bus) > size_bus:
            print(len(bus))
    return buses


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
