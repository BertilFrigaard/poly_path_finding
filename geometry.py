from constants import SNAP_RADIUS


def near_first_point(pos, points):
    if not points:
        return False
    dx, dy = pos[0] - points[0][0], pos[1] - points[0][1]
    return (dx * dx + dy * dy) ** 0.5 <= SNAP_RADIUS