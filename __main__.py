from core import GAME_STATE_LOADING, GAME_STATE_MENU, GAME_STATE_PATHFINDING, GAME_STATE_SETUP, Core
from constants import HEIGHT, TILE_END_COLOR, TILE_PATH_COLOR, TILE_START_COLOR, WIDTH
from geometry import mouse_intersects_tile, near_first_point
from render import draw_active_polygon, draw_closed_polygon, draw_path_tiles, draw_text_lines, start_render
import pygame
import sys

core = Core()

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                core.set_game_state(GAME_STATE_MENU)

            if core.get_game_state() == GAME_STATE_MENU:
                if event.key == pygame.K_1:
                    core.set_game_state(GAME_STATE_SETUP)
                    
                if event.key == pygame.K_2:
                    core.set_game_state(GAME_STATE_LOADING)
                    core.prepare_for_pathfinding()
                    core.set_game_state(GAME_STATE_MENU)

                if event.key == pygame.K_3:
                    if core.is_ready_for_pathfinding():
                        core.set_game_state(GAME_STATE_PATHFINDING)

            if core.get_game_state() == GAME_STATE_SETUP:
                if event.key == pygame.K_RETURN:
                    core.clear_active()
                    core.set_game_state(GAME_STATE_MENU)

                if event.key == pygame.K_DELETE:
                    core.clear_shapes()

            if core.get_game_state() == GAME_STATE_PATHFINDING:
                if event.key == pygame.K_1 or event.key == pygame.K_2:
                    hovering_tiles = [tile for tile in core.get_path_tiles() if mouse_intersects_tile(tile, pygame.mouse.get_pos())]
                    if hovering_tiles:
                        if event.key == pygame.K_1:
                            if core.has_path():
                                core.clear_path()
                            core.set_pathfinding_start(hovering_tiles[0])
                            if core.get_pathfinding_dest() == hovering_tiles[0]:
                                core.set_pathfinding_dest(None)
                        
                        elif event.key == pygame.K_2:
                            if core.has_path():
                                core.clear_path()
                            core.set_pathfinding_dest(hovering_tiles[0])
                            if core.get_pathfinding_start() == hovering_tiles[0]:
                                core.set_pathfinding_start(None)

                if event.key == pygame.K_RETURN:
                    if not core.has_path():
                        if core.ready_to_start_pathfinding():
                            core.do_pathfinding()

                if event.key == pygame.K_DELETE:
                    core.clear_path()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if core.get_game_state() == GAME_STATE_SETUP:
                if event.button == 1:  # left click
                    if core.get_active_length() >= 3 and near_first_point(mouse_pos, core.get_active()):
                        core.make_shape_from_active()
                    else:
                        core.add_to_active(mouse_pos)

                if event.button == 3:  # right click
                    core.pop_from_active()


def draw(screen):
    if core.get_game_state() == GAME_STATE_MENU:
        draw_text_lines(screen, ["Path Finding"], (WIDTH // 2, 100), 32, center=True)
        draw_text_lines(screen, [
            "Press a key to do one of the following actions",
            " ",
            "1) Goto setup where you can define the map",
            "2) Prepare setup for path finding",
            ("3) Path finding (Ready)" if core.is_ready_for_pathfinding() else "3) Path finding (Not Ready!)"),
            " ",
            "You can always return to this page by pressing Escape"
            ], (WIDTH // 2, 150), 22, center=True)

    if core.get_game_state() == GAME_STATE_SETUP:
        mouse_pos = pygame.mouse.get_pos()
        draw_active_polygon(screen, core.get_active(), mouse_pos, near_first_point(mouse_pos, core.get_active()) and core.get_active_length() >= 3)

        for shape in core.get_shapes():
            draw_closed_polygon(screen, shape)

        draw_text_lines(screen, [
            "Esc) Return to menu   Left Click) Make point   Right Click) Undo last point",
            "Delete) Erase all shapes   Enter) Save and cloes"
        ], (WIDTH // 2, HEIGHT - 70), 22, center=True)

    if core.get_game_state() == GAME_STATE_LOADING:
        draw_text_lines(screen, ["Loading..."], (WIDTH // 2, 20), 26, center=True)

    if core.get_game_state() == GAME_STATE_PATHFINDING:
        for shape in core.get_shapes():
            draw_closed_polygon(screen, shape, (200, 200, 220))

        if core.has_path():
            for tile in core.get_path():
                draw_closed_polygon(screen, tile.polygon(), TILE_PATH_COLOR)

        draw_path_tiles(screen, core.get_path_tiles())

        if core.get_pathfinding_start():
            draw_closed_polygon(screen, core.get_pathfinding_start().polygon(), TILE_START_COLOR)

        if core.get_pathfinding_dest():
            draw_closed_polygon(screen, core.get_pathfinding_dest().polygon(), TILE_END_COLOR)


        draw_text_lines(screen, [
            f"Esc) Return to menu   1) Set starting point    2) Set destination point",
            f"Enter) Start ({"Ready" if core.ready_to_start_pathfinding() else "Not Ready!"})   Delete) Clear path",
        ], (WIDTH // 2, HEIGHT - 70), 22, center=True)



def main():
    start_render(update, draw)
    pass


if __name__ == "__main__":
    main()