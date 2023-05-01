import pygame

from const import *


class Map:
    def __init__(self):
        pass

    def show_bg(self, surface):
        bg_img = pygame.image.load('src/img/phuongNguyenDu2.png')
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        surface.blit(bg_img, (0, 0))
