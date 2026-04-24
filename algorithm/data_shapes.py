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

    def midpoint(self):
        return ((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2)

class PathTile:
    def __init__(self):
        self.connections = []
        self.walls = []
        self.reset_search_params()

    def reset_search_params(self):
        self.visited = False
        self.parent = None
        self.f = float("inf")
        self.g = float("inf")
        self.h = 0

    def center(self):
        points = [conn.p1 for conn in self.connections]
        if not points:
            return None
        cx = (min(p.x for p in points) + max(p.x for p in points)) / 2
        cy = (min(p.y for p in points) + max(p.y for p in points)) / 2
        return (cx, cy)
    
    def polygon(self):
        # Returner en liste af sorterede punkter som danner
        # omkredsen af arealet PathTile

        # Da arealets omkreds er splittet i connections og walls er det gavnligt
        # at samle alle segmenter som udgør omkredsen i et array
        segments = [] # (x, y)[]
        for conn in self.connections:
            segments.append((conn.p1, conn.p2))
        for wall in self.walls:
            segments.append((wall[0], wall[1]))

        # Der bude altid være segmenter, men for at undgå fejl i den
        # senere kode griber vi det her, skulle det være sket aligevel.
        if not segments:
            print("ERROR: PathTile should have segments, but didn't. Returned empty polygon []")
            return []

        # Tag første segment ud, og tilføj de to punkter til den
        # sorterede liste: ordered
        ordered = [segments[0][0], segments[0][1]]

        # Lav en liste med de resterende segmenter
        remaining = list(segments[1:])

        # Så længde der stadig er resterende segmenter
        while remaining:

            # Tag det sidste segment i den sorterede liste
            last = ordered[-1]

            # For hvert resterende segment
            for i, (a, b) in enumerate(remaining):
                # Undersøg om et af punkterne a og b er lig det sidste i
                # den sorterede række
                if a is last:
                    # a er sidst, og den næste i rækken må derfor være b
                    ordered.append(b)
                    remaining.pop(i)
                    break
                elif b is last:
                    # b er sidst, og den næste i rækken må derfor være a
                    ordered.append(a)
                    remaining.pop(i)
                    break
            else: # Fanger hvis for loop ikke ramte et break
                # Segmenter af ikke sammenhængende, burde ikke ske på valid PathTile
                print("ERROR: PathTile invalid while making polygon.")
                break  

        # Fjern nu det sidste punkt, hvis det sidste og første punkt
        # er ens, for ikke at duplikere punkter
        if ordered[-1] is ordered[0]:
            ordered.pop()

        # Returner nu en liste (x, y)[] istedet for Point[]
        return [p.get_xy() for p in ordered]