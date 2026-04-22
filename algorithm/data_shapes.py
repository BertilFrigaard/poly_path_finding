import vector

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

    def get_xy(self):
        return (self.x, self.y)
    
    def get_vector(self):
        return vector.obj(x=self.x, y=self.y)
    
class Shape:
    def __init__(self, points=None):
        if not points:
            self.points = []
        else:
            self.points = points

class Edge:
    def __init__(self, p1, p2, leftGroup, rightGroup):
        # Make sure p1 is the starting point, this ensures
        # it is predictable which side of the edge is left / right
        self.p1 = p1
        self.p2 = p2
        self.left = leftGroup
        self.right = rightGroup

class PathConnection:
    def __init__(self, p1, p2, toTile):
        self.p1 = p1
        self.p2 = p2
        self.toTile = toTile

class PathTile:
    def __init__(self):
        self.area = None
        self.connections = []