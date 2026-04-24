import heapq

def calculate_h(conn, destTile):
    min_dist = float("inf")
    for destConn in destTile.connections:
        cx, cy = conn.midpoint()
        dcx, dcy = destConn.midpoint()
        dist = ((cx - dcx) ** 2 + (cy - dcy) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
    return min_dist

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
    while i != i.parent:
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
    heap_increment = 0
    heapq.heappush(open_list, (0.0, heap_increment, start))

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
                    h_new = calculate_h(conn, dest)
                    f_new = g_new + h_new

                    if neighbor.f == float("inf") or neighbor.f > f_new:
                        heap_increment += 1
                        heapq.heappush(open_list, (f_new, heap_increment, neighbor))
                        neighbor.f = f_new
                        neighbor.g = g_new
                        neighbor.h = h_new
                        neighbor.parent = current
    print("NEVER FOUND DESTINATION")
    return None