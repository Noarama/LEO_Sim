from sat import *
from topology import *
import math
import matplotlib.pyplot as plt

import numpy as np


REP = 150 # This variable indicates how many repetition for each n value. 

def dfs_rec(connections, src, dst, visited):
    ''' This function is the implementation of the depth first seach graph traversal algorithm
    The function uses:
    connections - the adjacency matrix of the graph,
    src - the current satellite we are in. Initially this is the source satellite, 
    dst - the index of the destination satellite,
    visited - a list that keeps track of which satellites have been visited.
    '''

    visited[src] = True
    if (src == dst):
        return True
    for i in range(len(connections[src])): 
        if ((connections[src][i] == 1) and visited[i] == False):
            return dfs_rec(connections, i, dst, visited)
     
def traverse_topology(topology):
    ''' This function initializes the traversal of the topology from the source to the destination satellite.
    The function uses:
    topology - 
    '''
    # The indecies that store the source and desteniation satellites.
    con_list = topology.connections
    visited = [False for _ in range(len(topology.satellites))] # Initialize a visited list where all values are false. 
    dfs_rec(con_list, 0, topology.n *(topology.m-1) + topology.d, visited)

    if visited[topology.n *(topology.m-1) + topology.d]:
        return 1
    
    else:
        return 0

def one_d_results(ns,l):
    ''' This function is responsible for outputting the graph comparison of the theory and simulation for 
    message propogation along a single orbital plane, i.e., when m=1.
    The function uses:
    ns - a list containing the size of the orbital planes,
    l - the number of satellites from the left of the source satellite to the destination satellite.
    '''

    results = [] # This list holds the resulting probabilities
    theory = []
    global satellites
    satellites = []
    values = 0

    for n in ns:

        values = 0

        for _ in range(REP):
            satellites = []
            generate_topology(n, 1)
            connections = connect_satellites(l , n, 1) # Establish appropriate connections between the satellites in the network.
            values += traverse_topology(connections, n,1,l)
        
        results.append(values/REP)
        theory.append((1/2)**(l) + (1/2)**(n-l) - (1/2)**n)


    plt.figure(figsize=(8, 5))
    plt.plot(ns, results, marker = 'o')
    plt.plot(ns, theory, marker = 'x')
    plt.ylim(0, 1)
    plt.xlabel("Number of Satellites Along a Plane")
    plt.ylabel("Message Delivery Probability")
    plt.title("Message Delivery Probability vs. Distance")
    plt.show()

def multi_d_results(ns, m, l):

    results = [] # This list holds the resulting probabilities
    theory = []
    global satellites
    satellites = []
    values = 0

    for n in ns:
        values = 0
        for _ in range(REP):
            satellites = []

            for i in range(m):
                generate_topology(n, i)

            connections = connect_satellites(l , n, m) # Establish appropriate connections between the satellites in the network.
            values += traverse_topology(connections, n,m,l)
        
        results.append(values/REP)


    plt.figure(figsize=(8, 5))
    plt.plot(ns, results, marker = 'o')
    plt.ylim(0, 1)
    plt.xlabel("Number of Satellites Along a Plane")
    plt.ylabel("Message Delivery Probability")
    plt.show()

def main():

    n_vals = [3,4,5,6,7]
    values = 0
    results = []

    for n in n_vals:
        values = 0
        for _ in range(REP):
            top = Topology(n,1,2)
            values += traverse_topology(top)

        results.append(values/REP)

    plt.figure(figsize=(8, 5))
    plt.plot(n_vals, results, marker = 'o')

    plt.ylim(0, 1)
    plt.xlabel("Number of Satellites Along a Plane")
    plt.ylabel("Message Delivery Probability")
    plt.title("Message Delivery Probability vs. Distance")
    plt.show()

        
if __name__ == '__main__':
    main()