from constants import SNAP_RADIUS
import vector

def near_first_point(pos, points):
    if not points:
        return False
    dx, dy = pos[0] - points[0][0], pos[1] - points[0][1]
    return (dx * dx + dy * dy) ** 0.5 <= SNAP_RADIUS

def cross_2d(a, b):
    return a.x * b.y - a.y * b.x

def ray_seg_intersect(p, d, a, b):
    # p: Punkt hvor ray starter (vector)
    # d: Vektor som viser ray retning (vector)
    # a: seg punkt 1 (vector)
    # b: seg punkt 2 (vector)

    # Vector from ray origin P to segment start A
    e = a - p

    # Segment direction vector (B - A)
    sd = b - a

    # zero if ray and segment are parallel
    denom = cross_2d(d, sd)
    if abs(denom) < 1e-9:
        return None  
    
    # t: how far along the ray the intersection is (P + t*D)
    t = cross_2d(e, sd) / denom
    # s: where on the segment the intersection is (0 = A, 1 = B)
    s = cross_2d(e, d) / denom
    if -1e-9 <= s <= 1 + 1e-9:  # Hit is within the segment (with floating-point tolerance)
        return t, s  # Caller checks t >= 0 to confirm hit is in front of the ray
    return None  # Intersection point lies outside the segment

def mouse_intersects_tile(path_tile, mouse_pos):
    if not path_tile.connections:
        return False
    p = vector.obj(x=mouse_pos[0], y=mouse_pos[1])
    d = vector.obj(x=1, y=0)
    hits = 0
    for conn in path_tile.connections:
        result = ray_seg_intersect(p, d, conn.p1.get_vector(), conn.p2.get_vector())
        if result is not None:
            t, _ = result
            if t >= 0:
                hits += 1
    return hits % 2 == 1