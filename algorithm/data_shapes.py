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
        self.walls = []

    def center(self):
        points = [conn.p1 for conn in self.connections]
        if not points:
            return None
        cx = (min(p.x for p in points) + max(p.x for p in points)) / 2
        cy = (min(p.y for p in points) + max(p.y for p in points)) / 2
        return (cx, cy)
    
    def polygon(self):
        segments = []
        for conn in self.connections:
            segments.append((conn.p1, conn.p2))
        for wall in self.walls:
            segments.append((wall[0], wall[1]))

        if not segments:
            return []

        ordered = [segments[0][0], segments[0][1]]
        remaining = list(segments[1:])

        while remaining:
            last = ordered[-1]
            for i, (a, b) in enumerate(remaining):
                if a is last:
                    ordered.append(b)
                    remaining.pop(i)
                    break
                elif b is last:
                    ordered.append(a)
                    remaining.pop(i)
                    break
            else:
                break  # disconnected — shouldn't happen on a valid tile

        # Drop the duplicate closing point if the chain wrapped back to start
        if len(ordered) > 1 and ordered[-1] is ordered[0]:
            ordered.pop()

        return [p.get_xy() for p in ordered]