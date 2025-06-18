# from sat import *
import math
import matplotlib.pyplot as plt
import random as rnd

class Sat:

    def __init__(self, sat_num, x, y, z):
        self.sat_num = sat_num
        self.x = x
        self.y = y
        self.z = z

    def print_sat(self):
        print("Satellite:" , self.sat_num , ": (" , self.x, ",", self.y, ",", self.z, ")")

class Topology:
    satellites = []
    connections = []
    n = 0
    m = 0 
    d = 0

    def __init__(self, n, m, d):
        ''' This function initializes the topology of the network by generating satellties and establishing connections between them. 
        The function uses:
        n - the number of satellites along a single orbital plane,
        m - the number of orbital planes.
        d - the distance between the source and destination from one side.
        '''
        self.n = n
        self.m = m
        self.d = d
        self.satellites = []
        self.connections = []
        self.add_satellites(self.n, self.m)

        self.connect_sats()

    def print_topology(self): 
        '''This function is a helper function that prints the attributes of the topology.'''
        print(f"n is {self.n}, m is {self.m}, and d is {self.d}")

        for sat in self.satellites:
            sat.print_sat()
        
    def add_satellites(self,n,m):
        ''' This function is used by the initializer to generate the satellites appropriately and store them in the satellites list. 
        The satellites are given x,y, and z coordinates using polar to rectangular formulas.
        The function uses:
        n - the number of satellites along a single orbital plane,
        m - the number of orbital planes.
        '''

        deg_inc = 360/(n) # Calculate the angle increment based on n.

        # Asigning each satellite coordinates along a circle using polar to rectangular conversion. 
        for plane in range(m):
            for i in range(n):
                temp_sat = Sat(i+(n*plane),math.cos(math.radians(i*deg_inc)),math.sin(math.radians(i*deg_inc)),plane+1)
                self.satellites.append(temp_sat)

    def connect_sats(self):
        ''' This function is used by the initializer to establish the connections between satellites and stores them in the connections adjacency matrix.
        The function assigns edges according to a specific probability as dictated by the gen_bond_prob function.
        '''

        self.connections = [[0 for _ in range(len(self.satellites))] for _ in range(len(self.satellites))]
        plane = -1

        for sat in range(len(self.connections)):
            if(self.gen_bond_prob() != 0):
                if (sat % self.n == 0):
                    plane += 1
                    self.connections[sat][sat+1] = 1
                    self.connections[sat][sat + self.n -1] = 1
                
                elif (sat < (plane * self.n + self.d)):
                    self.connections[sat][sat+1] = 1

                elif(sat > (plane * self.n + self.d)):
                    self.connections[sat][sat-1] = 1

                if(sat < (self.m-1) * self.n):
                    self.connections[sat][sat+self.n] = 1


    def gen_bond_prob(self):
        ''' This function returns a 0 or a 1 under a certain probability. 
        Currently, the probability that two neighbouring satellites are connected is 6/7.
        '''
        return rnd.choice([0,1,2,3,4,5,6,7,8])
    
    def plot_topology(self):
        ''' This function plots the topology as a directed graph.'''
        # Set up:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(0, self.m+1)
        ax.set_axis_off()
        ax.dist = 6

        # Plotting satellites: (as a scatter plot)
        x_vals = [sat.x for sat in self.satellites]
        y_vals = [sat.y for sat in self.satellites]
        z_vals = [sat.z for sat in self.satellites]

        labels = [f"sat {i}" for i in range(len(self.satellites)) ]
        labels[0] = "SRC"
        
        labels[self.n *(self.m-1) + self.d] = "DST"

        ax.scatter(x_vals, y_vals, z_vals)
        for x, y, z, label in zip(x_vals, y_vals, z_vals, labels):
            ax.text(x, y, z, label, fontsize=10, color='black')

        # Plotting connections: (as vectors)
        for i in range(len(self.satellites)):
            for j in range(len(self.satellites)):

                if (self.connections[i][j] == 1):
                    ax.quiver(self.satellites[i].x, self.satellites[i].y, self.satellites[i].z,
                     self.satellites[j].x -self.satellites[i].x, 
                     self.satellites[j].y -self.satellites[i].y, 
                     self.satellites[j].z -self.satellites[i].z)

        plt.show()

    