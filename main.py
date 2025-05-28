from sat import *
import math
import matplotlib.pyplot as plt
import random as rnd

''' This program generates the topology model based on user input. 
'''
satellites = []

def gen_bond_prob():
    ''' This function returns a 0 or a 1 under a certain probability. 
    Currently, the probability that two neighbouring satellites are connected is 1/2.
    '''
    return rnd.choice([0,1])

def connect_satellites(l , n , m):
    ''' This function creates the adjacency matrix that defines the connection between satellites.
    The function uses:
    l - the number of satellites from the left of the source satellite to the destination satellite, 
    n - the number of satellites along a single orbital plane,
    m - the number of orbital planes.
    The function returns the adjacency matrix called connections.
    '''
    connections = [[0 for _ in range(len(satellites))] for _ in range(len(satellites))] # Create an adjacency matrix of the appropriate size. 
    pivot = 0

    for i in range(len(satellites)):
        for j in range(len(satellites)):

            if (gen_bond_prob() == 1): # This if condition is used to ensure connections happen under a certain probability.

                if (i % n == 0):
                    pivot = i # The pivot is used to keep track of the destenation or parallel neighbour of the destination to ensue connections follow the correct direction.

                    if (i != n*m -1 and j == i + n):
                        # If thi current satellite is not the destination, we need to have an inter-plane connection with the parallel neighbour. 
                        connections[i][j] = 1 


                elif (i-pivot <= l): # If the current satellite is within the specified distance from the destination satellite
                    if ( j == i -1 or j == i + n):
                        # Connect to the neighbour along the plane that is closer to the destination, and connect to the parallel neighbour.
                        connections[i][j] = 1

                elif (i-pivot == l+1):
                    # If the current satellite corresponds to the source or a parallel satellite to the source.
                    connections[i][i+1] = 1
                    connections[i][i-1] = 1
                    if (j == i+n):
                        connections[i][j] = 1
                
                elif (i == pivot + n - 1) :
                    # If the current satellite corresponds to the last satellite along the current plane
                    connections[i][pivot] = 1
                    if (j == i+n):
                        connections[i][j] = 1

                elif( j == i + 1 or j == i + n):
                        # Connect to the neighbour along the plane that is closer to the destination, and connect to the parallel neighbour.
                        connections[i][j] = 1
            else:
                continue # This is when the gen_bond_prob returns 0, indicating the current two satellites are disconnected.

    return connections

def generate_topology(n, m):
    ''' This function generates satellites appropriately in a circular arrangement.
    The function uses:
    n - the number of satellites along a single orbital plane,
    m - the number of orbital planes.
    '''

    if (n <= 0):
        print("Error: n must be larger than 0.")
        return
    
    deg_inc = 360/n # Calculate the angle increment based on n.


    # Asigning each satellite coordinates along a circle using polar to rectangular conversion. 
    for i in range(n):
        temp_sat = Sat(i+(n*m),math.cos(math.radians(i*deg_inc)),math.sin(math.radians(i*deg_inc)),m)
        satellites.append(temp_sat)

def init_sim():
    ''' This function kicks off the program by prompting the user to enter desired variables that define the network's topology.
    The collected information is:
    l - the number of satellites from the left of the source satellite to the destination satellite, 
    n - the number of satellites along a single orbital plane,
    m - the number of orbital planes.
    These are all returned.
    '''
    n = int( input("Enter number of satellites along a single orbital plane: "))
    m = int( input("Enter number of orbital planes: "))
    r = int( input("Enter number of satellites on the left from the source to the destination: ") )
    return n, m, r

def plot_topology(connections, m,l,n):
    ''' This function is responsible for the visualization of the network topology. 
    The function uses:
    connections - the adjecancy matrix containing the directed edges between satellites,
    m - the number of orbital planes to define axis limits,
    satellites -  a global list containing Sat instances that describe the satellites in the network. 
    The function outputs a plot.
    '''
    # Set up:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(0, m+1)
    ax.set_axis_off()
    ax.dist = 6

    # Plotting satellites: (as a scatter plot)
    x_vals = [sat.x for sat in satellites]
    y_vals = [sat.y for sat in satellites]
    z_vals = [sat.z for sat in satellites]

    labels = [f'sat {i}' for i in range(len(satellites)) ]
    labels[l+1] = "SRC"
    if (m == 1):
        labels[0] = "DST"
    else:
        labels[(m-1)*n] = "DST"

    ax.scatter(x_vals, y_vals, z_vals)
    for x, y, z, label in zip(x_vals, y_vals, z_vals, labels):
        ax.text(x, y, z, label, fontsize=10, color='black')

    # Plotting connections: (as vectors)
    for i in range(len(satellites)):
        for j in range(len(satellites)):

            if (connections[i][j] == 1):
                ax.quiver(satellites[i].x, satellites[i].y, satellites[i].z, satellites[j].x -satellites[i].x, satellites[j].y -satellites[i].y, satellites[j].z -satellites[i].z)
    
    plt.show()

def main():
    # n, m, l = init_sim() # Collect network variables that defines the topology from the

    n = 7
    m = 2
    l = 2

    # Generate n satellites along each of the m planes:
    for i in range(m):
        generate_topology(n, i)
    
    connections = connect_satellites(l , n, m) # Establish appropriate connections between the satellites in the network.
    # print((m-1)*n + l + 1)
    connections[l+1][(m-1)*n + l + 1] = 0 # Entry corresponding to edge S
    connections[0][(m-1)*n] = 0 # Entry corresponding to edge D

    print(m, n )
    plot_topology(connections, m, l, n) # Visualize the topology of the network. 




if __name__ == '__main__':
    main()