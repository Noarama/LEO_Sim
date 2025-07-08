# from sat import *
from topology import *
from theory import *
import math
import matplotlib.pyplot as plt

import numpy as np


REP = 1500 # This variable indicates how many repetition for each n value. 

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
    topology - An object containing all the information needed to generate this instance of the topology.
    '''
    # The indecies that store the source and desteniation satellites.
    con_list = topology.connections
    visited = [False for _ in range(len(topology.satellites))] # Initialize a visited list where all values are false. 
    dfs_rec(con_list, 0, topology.n *(topology.m-1) + topology.d, visited)

    if visited[topology.n *(topology.m-1) + topology.d]:
        return 1
    
    else:
        return 0

def one_d_sim(n_vals):
    ''' This function is used to generate the plots for the 1D case (message propagation along a single orbital plane).
    This function uses:
    n_vals - a list containing all the different values for the number of satellites along a single orbital plane.
    '''

    p = 8/9 # The value of the probability of each ISL being connected. This value is according to topology.gen_bond_prob()
    d_vals = [2] # A list containing the values of d, the distance between the source and destination satellites.

    # The variables to hold results:
    values = 0
    results = []
    theory_results= []

    plt.figure(figsize=(8, 5))

    for val in d_vals:
        for n in n_vals:
            d = int(n/val)
            values = 0
            for _ in range(REP):
                top = Topology(n,1,d)
                values += traverse_topology(top)

            results.append(values/REP)
            theory_results.append(one_d_prob(n,d,p))

        
        plt.plot(n_vals, results, marker = 'o', label =f'Simulation Results, d = n/{val}')
        plt.plot(n_vals, theory_results, marker = 'x', label = f'Theoretical Results, d = n/{val}')
        results = []
        theory_results= []
        

    
    plt.ylim(0, 1)
    plt.legend()
    plt.xlabel("Number of Satellites Along a Plane")
    plt.ylabel("Message Delivery Probability")
    plt.title("1D Message Delivery Probability vs. Number of Satellites Along a Plane")
    plt.show()

def multi_d_sim(n_vals):
    ''' This function is used to generate the plots for the 2D case (message propagation along a two orbital planes).
    This function uses:
    n_vals - a list containing all the different values for the number of satellites along a single orbital plane.
    '''
    values = 0
    results = []
    theory_results= []
    p = 8/9

    for n in n_vals:
        d = int(n/4)
        values = 0
        for _ in range(REP):
            top = Topology(n,2,d)

            # Set S and D to be disconnected
            # top.connections[0][n] = 0 
            # top.connections[d][n + d] = 0

            values += traverse_topology(top)

        theory_results.append(two_d_prob(n,d,p))
        results.append(values/REP)

    print(theory_results)
    plt.figure(figsize=(8, 5))
    plt.plot(n_vals, results, marker = 'o', label ='Simulation Results')
    plt.plot(n_vals, theory_results, marker = 'o', label ='Theory Results')

    plt.ylim(0, 1)
    plt.legend()
    plt.xlabel("Number of Satellites Along a Plane")
    plt.ylabel("Message Delivery Probability")
    plt.title("2D Message Delivery Probability vs. Number of Satellites Along a Plane")
    plt.show()

def main():

    # These varaibles are for the simulation
    # n_vals = [3,7,9,12,20,30,40,50,60,80,100] 
    n_vals = [3,5,8,10,20, 30]

    # Simulations:
    # one_d_sim(n_vals)
    multi_d_sim(n_vals)

    # top = Topology(5,2,2)
    # top.plot_topology()

    

        
if __name__ == '__main__':
    main()