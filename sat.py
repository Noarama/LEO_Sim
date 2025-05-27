class Sat:

    def __init__(self, sat_num, x, y, z):
        self.sat_num = sat_num
        self.x = x
        self.y = y
        self.z = z

    def print_sat(self):
        print("Satellite:" , self.sat_num , ": (" , self.x, ",", self.y, ",", self.z, ")")

class Plane:
    
    satellites = []

    def __init__(self):
        self.satellites = []

    def add_sat(self, satellite):
        self.satellites.append(satellite)

    def print_plane(self):
        for satellite in self.satellites:
            satellite.print_sat()