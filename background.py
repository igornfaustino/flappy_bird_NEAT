import pygame
import os
import random
from config import SPRITES_FOLDER

BG_IMG = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join(SPRITES_FOLDER, "background-day.png"))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join(SPRITES_FOLDER, "background-night.png"))),
]


class Background:
    VEL = 3

    def __init__(self):
        bg_index = random.randint(0, 1)
        self.IMG = BG_IMG[bg_index]
        self.WIDTH = self.IMG.get_width()
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        is_img1_off_screen = self.x1 + self.WIDTH < 0
        if is_img1_off_screen:
            self.x1 = self.x2 + self.WIDTH
        
        is_img2_off_screen = self.x2 + self.WIDTH < 0
        if is_img2_off_screen:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, 0))
        win.blit(self.IMG, (self.x2, 0))
