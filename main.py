from sat import *
import math
import plotly.graph_objects as go
# We let n be the number of satellies along a single orbital plane.
# We also let the radius of the orbital plane be 1 for simplicity. 
satellites = []


def inter_plane_connections():
    return



def connect_satellites(l , n , m):

    connections = [[0 for _ in range(len(satellites))] for _ in range(len(satellites))] # Create an adjacency matrix of the appropriate size. 
    pivot = 0

    for i in range(len(satellites)):
        for j in range(len(satellites)):

            if (i % n == 0):
                pivot = i
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

    return connections



def generate_topology(n, m):
    if (n <= 0):
        print("Error: n must be larger than 0.")
        return
    
    deg_inc = 360/n # Calculate the angle increment based on n.


    # Asigning each satellite coordinates along a circle using polar to rectangular conversion. 
    for i in range(n):
        temp_sat = Sat(i+(n*m),math.cos(math.radians(i*deg_inc)),math.sin(math.radians(i*deg_inc)),m)
        satellites.append(temp_sat)


def main():
    n, m, l = init_sim()
    planes = []
    for i in range(m):
        plane = generate_topology(n, i)
    
    for sat in satellites:
        sat.print_sat()

    connections = connect_satellites(l , n, m)
    plot_graph_3d(satellites, connections)
    
    

if __name__ == '__main__':
    main()