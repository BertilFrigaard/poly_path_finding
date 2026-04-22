GAME_STATE_MENU = 0
GAME_STATE_SETUP = 1
GAME_STATE_PATHFINDING = 2
GAME_STATE_LOADING = 3

class Core():
    def __init__(self):
        self._active = []
        self._shapes = []
        self._game_state = GAME_STATE_MENU
    
    def add_to_active(self, point):
        self._active.append(point)
    
    def pop_from_active(self):
        self._active.pop()

    def get_active(self):
        return self._active
    
    def get_active_length(self):
        return len(self._active)
    
    def make_shape_from_active(self):
        self._shapes.append(self._active)
        self._active = []

    def get_shapes(self):
        return self._shapes
    
    def get_game_state(self):
        return self._game_state
    
    def set_game_State(self, game_state):
        self._game_state = game_state
