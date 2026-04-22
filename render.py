import pygame
from constants import BACKGROUND_COLOR, POINT_RADIUS, SHAPE_LINE_COLOR, SHAPE_POINT_COLOR, ACTIVE_LINE_COLOR, ACTIVE_POINT_COLOR, WIDTH, HEIGHT, PATH_TILE_AREA_COLOR, PATH_TILE_POINT_COLOR, PATH_TILE_CONNECTION_COLOR
from geometry import mouse_intersects_tile

def draw_closed_polygon(screen, points, fill_color=None):
    if fill_color is not None and len(points) >= 3:
        pygame.draw.polygon(screen, fill_color, points)

    if len(points) >= 2:
        for i in range(len(points) - 1):
            pygame.draw.line(screen, SHAPE_LINE_COLOR, points[i], points[i + 1], 2)
        pygame.draw.line(screen, SHAPE_LINE_COLOR, points[-1], points[0], 2)

    for p in points:
        pygame.draw.circle(screen, SHAPE_POINT_COLOR, p, POINT_RADIUS)

def draw_active_polygon(screen, points, mouse_pos, snap):
    if snap:
        mouse_pos = points[0]

    if len(points) >= 2:
        for i in range(len(points) - 1):
            pygame.draw.line(screen, ACTIVE_LINE_COLOR, points[i], points[i + 1], 2)
    if len(points) >= 1:
        pygame.draw.line(screen, ACTIVE_LINE_COLOR, points[-1], mouse_pos, 1)

    for p in points:
        pygame.draw.circle(screen, ACTIVE_POINT_COLOR, p, POINT_RADIUS)

    if points and mouse_pos:
        pygame.draw.circle(screen, ACTIVE_POINT_COLOR, mouse_pos, POINT_RADIUS * 1.5 if snap else POINT_RADIUS, 1)

def draw_text_lines(screen, lines, pos, font_size=16, color=(0, 0, 0), line_spacing=4, center=False):
    font = pygame.font.SysFont("Arial", font_size)
    x, y = pos
    for line in lines:
        surface = font.render(line, True, color)
        blit_x = x - surface.get_width() // 2 if center else x
        screen.blit(surface, (blit_x, y))
        y += font.get_height() + line_spacing

def draw_path_tiles(screen, path_tiles):
    for tile in path_tiles:
        if mouse_intersects_tile(tile, pygame.mouse.get_pos()):
            pygame.draw.circle(screen, (155, 155, 155), tile.center(), POINT_RADIUS * 2)

        for conn in tile.connections:
            pygame.draw.line(screen, PATH_TILE_CONNECTION_COLOR, conn.p1.get_xy(), conn.p2.get_xy(), 2)
            pygame.draw.circle(screen, PATH_TILE_CONNECTION_COLOR, conn.p1.get_xy(), POINT_RADIUS)
            pygame.draw.circle(screen, PATH_TILE_CONNECTION_COLOR, conn.p2.get_xy(), POINT_RADIUS)


def start_render(update, draw):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Program")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    while True:
        update()

        screen.fill(BACKGROUND_COLOR)

        draw(screen)

        pygame.display.flip()
        clock.tick(60)