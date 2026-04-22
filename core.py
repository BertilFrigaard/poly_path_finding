from algorithm.preperation import make_division_with_rays, make_edges, make_screen_corners, make_shape_segments, make_shapes, make_tiles, sort_point_neighbors
from constants import WIDTH, HEIGHT


GAME_STATE_MENU = 0
GAME_STATE_SETUP = 1
GAME_STATE_PATHFINDING = 2
GAME_STATE_LOADING = 3

class Core():
    def __init__(self):
        self._active = []
        self._primitive_shapes = []
        self._game_state = GAME_STATE_MENU
        self._ready_for_pathfinding = False
        self._tiles = []
        self._start = None
        self._dest = None
    
    def add_to_active(self, point):
        self._active.append(point)
    
    def pop_from_active(self):
        if self._active:
            self._active.pop()

    def get_active(self):
        return self._active
    
    def get_active_length(self):
        return len(self._active)
    
    def clear_active(self):
        self._active = []
    
    def make_shape_from_active(self):
        self._ready_for_pathfinding = False
        self._start = None
        self._dest = None
        self._primitive_shapes.append(self._active)
        self._active = []

    def clear_shapes(self):
        self._ready_for_pathfinding = False
        self._start = None
        self._dest = None
        self._primitive_shapes = []
        self._active = []

    def get_shapes(self):
        return self._primitive_shapes
    
    def get_game_state(self):
        return self._game_state
    
    def set_game_state(self, game_state):
        self._game_state = game_state

    def is_ready_for_pathfinding(self):
        return self._ready_for_pathfinding

    def prepare_for_pathfinding(self):
        shapes = make_shapes(self._primitive_shapes)
        shape_segments = make_shape_segments(shapes)
        (screen_points, screen_segments) = make_screen_corners() 

        (collision_points, dead_pairs) = make_division_with_rays(shape_segments, screen_segments, shapes)
        all_points = collision_points + screen_points + [point for shape in shapes for point in shape.points]
        sort_point_neighbors(all_points)
        edges = make_edges(all_points[0])

        for edge in edges[:]:
            if (edge.p1, edge.p2) in dead_pairs or (edge.p2, edge.p1) in dead_pairs:
                edges.remove(edge)

        self._tiles = make_tiles(edges) 
        if self._tiles:
            self._ready_for_pathfinding = True
    
    def get_path_tiles(self):
        return self._tiles
    
    def ready_to_start_pathfinding(self):
        return (self._dest and self._start)

    def set_pathfinding_dest(self, dest):
        self._dest = dest
    
    def get_pathfinding_dest(self):
        return self._dest

    def set_pathfinding_start(self, start):
        self._start = start

    def get_pathfinding_start(self):
        return self._start