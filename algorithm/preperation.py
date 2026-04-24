from algorithm.data_shapes import Edge, PathConnection, PathTile, Point, Shape
from constants import HEIGHT, WIDTH
from geometry import ray_seg_intersect
import math

### STEP 1
def make_shapes(primitive_shapes):
    shapes = []
    for p_shape in primitive_shapes:
        new_shape = Shape([Point(a[0], a[1]) for a in p_shape])
        shapes.append(new_shape)
        for i, p in enumerate(new_shape.points):
            # n1 is left neighbor, n2 is right neighbor
            # This is predictable because shapes must be defined in counterclockwise order
            n1 = new_shape.points[i - 1 if i >= 1 else len(new_shape.points) - 1]
            n2 = new_shape.points[i + 1 if i < len(new_shape.points) - 1 else 0]
            p.neighbors.append(n1)
            p.neighbors.append(n2)
    return shapes

### STEP 2
def make_shape_segments(shapes):
    shape_segments = []
    for shape in shapes:
        n = len(shape.points)
        for i in range(n):
            a = shape.points[i]
            b = shape.points[(i + 1) % n]
            shape_segments.append((a, b))
    return shape_segments

### STEP 3
def make_screen_corners():
    screen_top_left = Point(0, 0)
    screen_top_right = Point(WIDTH, 0)
    screen_bottom_left = Point(0, HEIGHT)
    screen_bottom_right = Point(WIDTH, HEIGHT)

    # Add the corner neighbors
    screen_top_left.neighbors = [screen_top_right, screen_bottom_left]
    screen_top_right.neighbors = [screen_top_left, screen_bottom_right]
    screen_bottom_left.neighbors = [screen_bottom_right, screen_top_left]
    screen_bottom_right.neighbors = [screen_bottom_left, screen_top_right]

    screen_segments = [
        (screen_top_left, screen_top_right),
        (screen_bottom_left, screen_bottom_right),
        (screen_top_left, screen_bottom_left),
        (screen_top_right, screen_bottom_right),
    ]

    return ([screen_top_left, screen_top_right, screen_bottom_left, screen_bottom_right], screen_segments)

### STEP 4
def make_division_with_rays(shape_segments, screen_segments, shapes):
    dead_pairs = shape_segments.copy() + screen_segments.copy()
    new_points = []
    for shape in shapes:
        for i, p in enumerate(shape.points):
            # p is point, n1 is left neighbor, n2 is right neighbor
            n1 = shape.points[i - 1 if i >= 1 else len(shape.points) - 1]
            n2 = shape.points[i + 1 if i < len(shape.points) - 1 else 0]

            # Vektor fra p til n1
            v1 = n1.get_vector() - p.get_vector()
            # Vektor fra p til n2
            v2 = n2.get_vector() - p.get_vector()

            # Enheds vektorer
            u1 = v1.unit()
            u2 = v2.unit()

            # Gennemsnitlig vektor der peger væk fra shape
            # Bemærk d ikke længere er en enheds vektor men retningen er nu gennemsnittet af u1 og u2's retning
            cross = u1.x * u2.y - u1.y * u2.x

            if cross > 0:
                # Convex corner: average points inward, flip it
                d = (u1 + u2) * -1
            else:
                # Reflex corner: average already points outward, don't flip
                d = (u1 + u2)

            # Bestem alle collisions for ray (ray fra punkt p)
            collisions = []

            for (a, b) in shape_segments:
                result = ray_seg_intersect(p.get_vector(), d, a.get_vector(), b.get_vector())
                if result:
                    t, s = result
                    if abs(t) < 1e-6 or t < 0:
                        continue
                    c = p.get_vector() + t * d
                    collisions.append((a, b, c, t))

            for (a, b) in screen_segments:
                result = ray_seg_intersect(p.get_vector(), d, a.get_vector(), b.get_vector())
                if result:
                    t, s = result
                    if abs(t) < 1e-6 or t < 0:
                        continue
                    c = p.get_vector() + t * d
                    collisions.append((a, b, c, t))

            # Vælg kun den tætteste collision point
            closest = None
            for collision in collisions:
                if closest == None or closest[3] > collision[3]:
                    closest = collision

            # Lav et nyt punkt i den tætteste collision
            collision_p = Point(closest[2].x, closest[2].y)
            new_points.append(collision_p)

            # Fjern nu connection mellem punkter der dannede segment som ray skar i punkt closest.
            try:
                
                closest[0].neighbors.remove(closest[1])
            except:
                collision_p.debug.append("Failed to remove neighbor 1 from 0")
                print("Failed to remove neighbor 1 from 0")

            try:
                closest[1].neighbors.remove(closest[0])
            except:
                collision_p.debug.append("Failed to remove neighbor 0 from 1")
                print("Failed to remove neighbor 0 from 1")

            # Lav nye connections til collision point som erstater den netop fjernede connection
            closest[0].neighbors.append(collision_p)
            closest[1].neighbors.append(collision_p)

            p.neighbors.append(collision_p)

            collision_p.neighbors.append(p)
            collision_p.neighbors.append(closest[0])
            collision_p.neighbors.append(closest[1])

            # Slet evt. fjernet dead_pair
            if (closest[0], closest[1]) in dead_pairs:
                dead_pairs.remove((closest[0], closest[1]))
                # Og tilføj nye dead pairs (Forestil dig at et deadpair er blevet splittet op, derfor kommer to nye)
                dead_pairs.append((closest[1], collision_p))
                dead_pairs.append((closest[0], collision_p))

            elif (closest[1], closest[0]) in dead_pairs:
                dead_pairs.remove((closest[1], closest[0]))
                # Tilføj igen nye dead pairs
                dead_pairs.append((closest[1], collision_p))
                dead_pairs.append((closest[0], collision_p))

            # Update the segment lists by removing the one hit segment as we have removed that
            # And adding the 3 newly created segments
            if (closest[0], closest[1]) in shape_segments:
                shape_segments.remove((closest[0], closest[1]))

                shape_segments.append((closest[0], collision_p))
                shape_segments.append((closest[1], collision_p))
                shape_segments.append((p, collision_p))
            elif (closest[1], closest[0]) in shape_segments:
                shape_segments.remove((closest[1], closest[0]))
                
                shape_segments.append((closest[0], collision_p))
                shape_segments.append((closest[1], collision_p))
                shape_segments.append((p, collision_p))
            elif (closest[1], closest[0]) in screen_segments:
                screen_segments.remove((closest[1], closest[0]))
                
                screen_segments.append((closest[0], collision_p))
                screen_segments.append((closest[1], collision_p))
                screen_segments.append((p, collision_p))
            elif (closest[0], closest[1]) in screen_segments:
                screen_segments.remove((closest[0], closest[1]))
                
                screen_segments.append((closest[0], collision_p))
                screen_segments.append((closest[1], collision_p))
                screen_segments.append((p, collision_p))
    return (new_points, dead_pairs)

### STEP 5
def sort_point_neighbors(points):
    for point in points:
        cx, cy = point.x, point.y
        point.neighbors.sort(key=lambda n: math.atan2(n.y - cy, n.x - cx))

### STEP 6
def make_edges(any_point):
    edges = []
    consumed = []
    groups = 0

    def get_new_group():
        nonlocal groups
        groups += 1
        return groups

    def migrate_edge_group(old, new):
        for e in edges:
            if e.left == old:
                e.left = new
            if e.right == old:
                e.right = new 

    def get_edge(neighbor, anchor):
        # Returns the directed edge that goes FROM neighbor TO anchor, if it exists
        res = [e for e in edges if (e.p1 == neighbor and e.p2 == anchor)]
        if res:
            return (res[0], False)
        
        res = [e for e in edges if (e.p1 == anchor and e.p2 == neighbor)]
        if res: 
            return (res[0], True)
        return (None, False)


    def make_edge_recursively(point):
        # Skip points we have already processed to avoid infinite recursion and duplicate edges
        if point in consumed:
            return
        consumed.append(point)

        # Walk every neighbor n of this point and create the directed edge: point -> n 
        for i, n in enumerate(point.neighbors):
            # Don't create it, if it already exists
            already_exists = any(e.p1 == n and e.p2 == point for e in edges)
            if not already_exists:

                # Get the parent right edge and the dest right edge
                # Remember the dest right edge is found by going the opposite way around the neighbors
                (parent_right_edge, parent_reverse) = get_edge(point.neighbors[(i + 1) % len(point.neighbors)], point)
                dest_index = n.neighbors.index(point)
                (dest_right_edge, dest_reverse) = get_edge(n.neighbors[(dest_index - 1) % len(n.neighbors)], n)

                if parent_right_edge and dest_right_edge:
                    parent_left = parent_right_edge.right if parent_reverse else parent_right_edge.left
                    dest_left = dest_right_edge.right if not dest_reverse else dest_right_edge.left
                    if parent_left == dest_left:
                        final_left = dest_left
                    else:
                        # The dest and source (parent) point want to give the point different groups
                        # To solve this all groups of group parent_left is migrated to group dest_left
                        migrate_edge_group(parent_left, dest_left)
                        final_left = dest_left

                elif parent_right_edge:
                    final_left = parent_right_edge.right if parent_reverse else parent_right_edge.left

                elif dest_right_edge:
                    final_left = dest_right_edge.right if not dest_reverse else dest_right_edge.left

                else:
                    final_left = get_new_group()

                (parent_left_edge, parent_reverse) = get_edge(point.neighbors[(i - 1) % len(point.neighbors)], point)
                (dest_left_edge, dest_reverse) = get_edge(n.neighbors[(dest_index + 1) % len(n.neighbors)], n)

                if parent_left_edge and dest_left_edge:
                    parent_right = parent_left_edge.left if parent_reverse else parent_left_edge.right
                    dest_right = dest_left_edge.left if not dest_reverse else dest_left_edge.right
                    if parent_right == dest_right:
                        final_right = dest_right
                    else:
                        migrate_edge_group(parent_right, dest_right)
                        final_right = dest_right

                elif parent_left_edge:
                    final_right = parent_left_edge.left if parent_reverse else parent_left_edge.right

                elif dest_left_edge:
                    final_right = dest_left_edge.left if not dest_reverse else dest_left_edge.right

                else:
                    final_right = get_new_group()

                edges.append(Edge(point, n, final_left, final_right))

            # Recurse into n so that its outgoing edges are created next (depth-first traversal)
            if n not in consumed:
                make_edge_recursively(n)

    make_edge_recursively(any_point)
    return edges

### STEP 8
def make_tiles(edges, dead_edges):
    tiles = {}
    for edge in edges:
        left_tile = tiles.get(edge.left)
        right_tile = tiles.get(edge.right)

        if not left_tile:
            left_tile = PathTile()
            tiles[edge.left] = left_tile

        if not right_tile:
            right_tile = PathTile()
            tiles[edge.right] = right_tile

        left_tile.connections.append(PathConnection(edge.p1, edge.p2, right_tile))
        right_tile.connections.append(PathConnection(edge.p1, edge.p2, left_tile))

    for edge in dead_edges:
        left_tile = tiles.get(edge.left)
        right_tile = tiles.get(edge.right)

        if left_tile:
            left_tile.walls.append((edge.p1, edge.p2))
        
        if right_tile:
            right_tile.walls.append((edge.p1, edge.p2))
            
    return tiles.values()