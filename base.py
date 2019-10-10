import pygame
import os

SPRITES_FOLDER = "assets/sprites"

BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join(SPRITES_FOLDER, "base.png")))


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
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
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
