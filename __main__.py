from core import GAME_STATE_LOADING, GAME_STATE_MENU, GAME_STATE_SETUP, Core
from constants import HEIGHT, WIDTH
from geometry import near_first_point
from render import draw_active_polygon, draw_closed_polygon, draw_text_lines, start_render
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
                core.set_game_State(GAME_STATE_MENU)

            if core.get_game_state() == 0:
                if event.key == pygame.K_1:
                    core.set_game_State(GAME_STATE_SETUP)

            if core.get_game_state() == 1:
                if event.key == pygame.K_KP_ENTER:
                    print("SAVE AND CLOSE")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
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
            "2) Not implemented yet",
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
            "upso"
        ], (WIDTH // 2, HEIGHT - 70), 22, center=True)

    if core.get_game_state() == GAME_STATE_LOADING:
        draw_text_lines(screen, ["Loading..."], (WIDTH // 2, 20), 26, center=True)



def main():
    start_render(update, draw)
    pass


if __name__ == "__main__":
    main()