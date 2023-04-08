import pygame


def generate_frames(atlas, tile_width, tile_height):
    w, h = atlas.get_size()
    rows, cols = h // tile_height, w // tile_width
    return [[pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height) for j in range(cols)] for i in range(rows)]
