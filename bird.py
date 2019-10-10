import os
import random
import pygame
from config import SPRITES_FOLDER

BIRDS_SPRITES = [
    [
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "bluebird-downflap.png"))),
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "bluebird-midflap.png"))),
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "bluebird-upflap.png"))),
    ],
    [
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "redbird-downflap.png"))),
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "redbird-midflap.png"))),
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "redbird-upflap.png"))),
    ],
    [
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "yellowbird-downflap.png"))),
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "yellowbird-midflap.png"))),
        pygame.transform.scale2x(pygame.image.load(
            os.path.join(SPRITES_FOLDER, "yellowbird-upflap.png"))),
    ],
]


class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        bird_color_index = random.randint(0, len(BIRDS_SPRITES)-1)
        self.IMGS = BIRDS_SPRITES[bird_color_index]
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def _calculate_vertical_deslocament(self):
        # second degree formula to calculate the bird parabole
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        max_fall_deslocament = 16
        is_faling_at_max_speed = d >= max_fall_deslocament
        if is_faling_at_max_speed:
            return 16
        is_jumping = d < 0
        if is_jumping:
            return d-2
        return d

    def _move_vertical(self, deslocament):
        self.y = self.y + deslocament

    def _rotate_bird(self, deslocament):
        is_jumping = deslocament < 0
        is_above_initial_pos = self.y < self.height + 50
        is_complete_tilt_down = self.tilt <= -90
        if is_jumping or is_above_initial_pos:
            self.tilt = self.MAX_ROTATION
        elif not is_complete_tilt_down:
            self.tilt -= self.ROT_VEL
        else:
            self.tilt = -90

    def move(self):
        self.tick_count += 1
        deslocament = self._calculate_vertical_deslocament()
        self._move_vertical(deslocament)
        self._rotate_bird(deslocament)

    def _animate_wings(self):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        is_going_down = self.tilt <= -80
        if is_going_down:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

    def _draw_tilted_bird(self, win):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def draw(self, win):
        self._animate_wings()
        self._draw_tilted_bird(win)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
