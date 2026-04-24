import heapq

class Incrementer:
    def __init__(self):
        self.i = 0

    def get(self):
        self.i += 1
        return self.i - 1

def calculate_h(tile, destTile):
    min_dist = float("inf")
    for conn in tile.connections:
        mx, my = conn.midpoint()
        for dest_conn in destTile.connections:
            dmx, dmy = dest_conn.midpoint()
            dist = ((mx - dmx) ** 2 + (my - dmy) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
    return min_dist if min_dist != float("inf") else 0

def calculate_g(tile, connection):
    # Determine the path cost (Length of travel)
    # To travel to the connection from tile
    if tile.parent:
        # start is the edge between tile and parent
        previous_conn_midpoint = [conn.midpoint() for conn in tile.parent.connections if conn.toTile == tile]
        if not previous_conn_midpoint:
            # The first tile will land here
            start = tile.center()
        else:
            start = previous_conn_midpoint[0]
    else:
        # This is the start tile, approximate the start
        # to the center of the tile
        start = tile.center()

    end = connection.midpoint()
    return ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5

def trace_path(dest):
    path = []
    i = dest
    while not i == i.parent:
        path.append(i)
        i = i.parent
    
    path.append(i)
    path.reverse()
    return path


def search_path(start, dest):
    if start == dest:
        print("Start and destination are equal")
        return
    
    start.f = 0
    start.g = 0
    start.h = 0
    start.parent = start

    open_list = []
    heap_incrementer = Incrementer()
    heapq.heappush(open_list, (0.0, heap_incrementer.get(), start))

    while len(open_list) > 0:

        popped = heapq.heappop(open_list)
        current = popped[2]
        current.visited = True

        for conn in current.connections:
            neighbor = conn.toTile
            if not neighbor.visited:
                if neighbor == dest:
                    print("FOUND DESTINATION")
                    neighbor.parent = current
                    return trace_path(dest)
                else:
                    g_new = current.g + calculate_g(current, conn)
                    h_new = calculate_h(neighbor, dest)
                    f_new = g_new + h_new

                    if neighbor.f == float("inf") or neighbor.f > f_new:
                        heapq.heappush(open_list, (f_new, heap_incrementer.get(), neighbor))
                        neighbor.f = f_new
                        neighbor.g = g_new
                        neighbor.h = h_new
                        neighbor.parent = current
    print("NEVER FOUND DESTINATION")
    return None