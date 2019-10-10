import pygame
from bird import Bird
from pipe import Pipe
from base import Base
from background import Background

class Game:
    WIN_WIDTH = 500
    WIN_HEIGHT = 800

    def __init__(self):
        self.isRunning = True
        self.score = 0
        self.bird = Bird(230, 350)
        self.base = Base(730)
        self.pipes = [Pipe(700)]
        self.background = Background()

        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", 1, (255, 255, 255))
        self.win.blit(text, (self.WIN_WIDTH - 10 - text.get_width(), 10))

    def draw_game(self):
        self.background.draw(self.win)
        self.bird.draw(self.win)
        for pipe in self.pipes:
            pipe.draw(self.win)
        self.base.draw(self.win)
        self.draw_score()
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False

    def move_pipes(self):
        pipes_to_remove = []
        add_pipe = False
        for pipe in self.pipes:
            is_pipe_off_screen = pipe.x + pipe.PIPE_BOTTOM.get_width() < 0
            is_bird_pass_pipe = pipe.x < self.bird.x

            if pipe.collide(self.bird):
                pass
            if is_pipe_off_screen:
                pipes_to_remove.append(pipe)
            if not pipe.passed and is_bird_pass_pipe:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        self.pipes = [
            pipe for pipe in self.pipes if pipe not in pipes_to_remove]
        if add_pipe:
            self.score += 1
            self.pipes.append(Pipe(600))

    def check_bird_hit_ground(self):
        is_bird_touching_ground = self.bird.y + self.bird.img.get_height() >= 730
        if is_bird_touching_ground:
            pass

    def gameloop(self):
        clock = pygame.time.Clock()
        while self.isRunning:
            clock.tick(30)
            self.handle_events()
            self.background.move()
            # bird.move()
            self.base.move()
            self.move_pipes()

            self.draw_game()
        pygame.quit()
        quit()


if __name__ == "__main__":
    Game().gameloop()
