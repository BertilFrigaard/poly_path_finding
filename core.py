from algorithm.preperation import make_division_with_rays, make_edges, make_screen_corners, make_shape_segments, make_shapes, sort_point_neighbors


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
    
    def add_to_active(self, point):
        self._active.append(point)
    
    def pop_from_active(self):
        self._active.pop()

    def get_active(self):
        return self._active
    
    def get_active_length(self):
        return len(self._active)
    
    def clear_active(self):
        self._active = []
    
    def make_shape_from_active(self):
        self._ready_for_pathfinding = False
        self._primitive_shapes.append(self._active)
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
        collision_points = make_division_with_rays(shape_segments, screen_segments, shapes)
        all_points = collision_points + screen_points + [point for shape in shapes for point in shape.points]
        sort_point_neighbors(all_points)
        self.edges = make_edges(all_points[0])
        if self.edges:
            self._ready_for_pathfinding = True
