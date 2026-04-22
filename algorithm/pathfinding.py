import heapq

class Incrementer:
    def __init__(self):
        self.i = 0

    def get(self):
        self.i += 1
        return self.i - 1

def calculate_h(tile, destTile):
    # Implement a check that checks for each connection and uses the closest
    return 0
    #return ((node.x - dest.x) ** 2 + (node.y - dest.y) ** 2) ** 0.5

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
                    g_new = current.g + 1.0
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