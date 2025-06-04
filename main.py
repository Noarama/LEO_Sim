# from sat import *
from topology import *
import math
import matplotlib.pyplot as plt

import numpy as np


REP = 500 # This variable indicates how many repetition for each n value. 

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

def one_d_sim(n_vals,m):

    p = 5/6
    values = 0
    results = []
    theory = []

    for n in n_vals:
        d = int(n/3)
        values = 0
        for _ in range(REP):
            top = Topology(n,m,d)
            values += traverse_topology(top)

        results.append(values/REP)
        theory.append((p**d) + (p**(n-d)) - (p**n))

    plt.figure(figsize=(8, 5))
    plt.plot(n_vals, results, marker = 'o', label ='Simulation Results')
    plt.plot(n_vals, theory, marker = 'x', label = 'Theoretical Results')

    plt.ylim(0, 1)
    plt.legend()
    plt.xlabel("Number of Satellites Along a Plane")
    plt.ylabel("Message Delivery Probability")
    plt.title("1D Message Delivery Probability vs. Number of Satellites Along a Plane")
    plt.show()

def multi_d_sim(n_vals,m):

    values = 0
    results = []

    for n in n_vals:
        d = int(n/2)
        values = 0
        for _ in range(REP):
            top = Topology(n,m,d)
            values += traverse_topology(top)

        results.append(values/REP)

    plt.figure(figsize=(8, 5))
    plt.plot(n_vals, results, marker = 'o', label ='Simulation Results')

    plt.ylim(0, 1)
    plt.legend()
    plt.xlabel("Number of Satellites Along a Plane")
    plt.ylabel("Message Delivery Probability")
    plt.title("2D Message Delivery Probability vs. Number of Satellites Along a Plane")
    plt.show()

def main():

    # These varaibles are for the simulation
    n_vals = [3,6,9,12,16,20,30,40,45,50,55,60]
    m = 1

    # Simulations:
    one_d_sim(n_vals, 1)
    multi_d_sim(n_vals, 2)
    

        
if __name__ == '__main__':
    main()