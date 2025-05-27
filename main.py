from sat import *
import math
# We let n be the number of satellies along a single orbital plane.
# We also let the radius of the orbital plane be 1 for simplicity. 



def generate_topology(n,m):
    if (n <= 0):
        print("Error: n must be larger than 0.")
        return
    
    deg_inc = 360/n # Calculate the angle increment based on n.

    temp_plane = Plane()

    # Asigning each satellite coordinates along a circle using polar to rectangular conversion. 
    for i in range(n):
        temp_sat = Sat(i,math.cos(math.radians(i*deg_inc)),math.sin(math.radians(i*deg_inc)),m)
        temp_plane.add_sat(temp_sat)

    return temp_plane



def init_sim():
    n = int( input("Enter number of satellites along a single orbital plane: "))
    m = int( input("Enter number of orbital planes: "))
    r = int( input("Enter number of satellites on the left from the source to the destination: ") )
    return n, m, r



def main():
    n, m, r = init_sim()
    planes = []
    for i in range(m):
        plane = generate_topology(n,i)
        plane.print_plane()



if __name__ == '__main__':
    main()