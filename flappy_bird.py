import os
import neat
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
        self.birds = []
        self.nets = []
        self.ge = []
        self.base = Base(730)
        self.pipes = []
        self.background = Background()

        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", 1, (255, 255, 255))
        self.win.blit(text, (self.WIN_WIDTH - 10 - text.get_width(), 10))

    def draw_game(self):
        self.background.draw(self.win)
        for bird in self.birds:
            bird.draw(self.win)
        for pipe in self.pipes:
            pipe.draw(self.win)
        self.base.draw(self.win)
        self.draw_score()
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False

    def kill_bird(self, bird_idx):
        self.ge[bird_idx].fitness -= 1
        self.birds.pop(bird_idx)
        self.nets.pop(bird_idx)

    def update_score(self):
        self.score += 1
        for bird_idx, bird in enumerate(self.birds):
            self.ge[bird_idx].fitness += 5

    def move_pipes(self):
        pipes_to_remove = []
        add_pipe = False
        for pipe in self.pipes:
            is_pipe_off_screen = pipe.x + pipe.PIPE_BOTTOM.get_width() < 0
            for bird_idx, bird in enumerate(self.birds):
                is_bird_pass_pipe = pipe.x + pipe.PIPE_BOTTOM.get_width() < bird.x

                if pipe.collide(bird):
                    self.kill_bird(bird_idx)
                if not pipe.passed and is_bird_pass_pipe:
                    pipe.passed = True
                    add_pipe = True
            if is_pipe_off_screen:
                pipes_to_remove.append(pipe)
            pipe.move()
        self.pipes = [
            pipe for pipe in self.pipes if pipe not in pipes_to_remove]
        if add_pipe:
            self.update_score()
            self.add_pipe()

    def check_bird_hit_limits(self, bird_idx, bird):
        is_bird_touching_ground = bird.y + bird.img.get_height() >= 730
        is_bird_above_screen = bird.y + bird.img.get_height() < 0

        if is_bird_touching_ground:
            self.kill_bird(bird_idx)

        if is_bird_above_screen:
            self.kill_bird(bird_idx)

    def move_birds(self):
        for bird_idx, bird in enumerate(self.birds):
            bird.move()
            self.check_bird_hit_limits(bird_idx, bird)

    def add_pipe(self):
        self.pipes.append(Pipe(550))

    def get_next_pipe(self):
        for pipe in self.pipes:
            if not pipe.passed:
                return pipe

    def command_birds(self):
        pipe = self.get_next_pipe()
        if not pipe:
            return
        for bird_idx, bird in enumerate(self.birds):
            self.ge[bird_idx].fitness += 0.1
            neat = self.nets[bird_idx]
            dist_bird_pipe = {
                "top_pipe": abs(bird.y - pipe.height),
                "bottom_pipe": abs(bird.y - pipe.bottom)
            }
            output = neat.activate((bird.y, dist_bird_pipe["top_pipe"],
                                    dist_bird_pipe["bottom_pipe"]))
            if (output[0] > 0.5):
                bird.jump()

    def is_birds_alive(self):
        return len(self.birds) > 0
    
    def reset(self):
        self.pipes = []
        self.score = 0
        self.add_pipe()

    def gameloop(self, genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.birds.append(Bird(230, 350))
            genome.fitness = 0
            self.ge.append(genome)

        clock = pygame.time.Clock()
        while self.isRunning and self.is_birds_alive():
            clock.tick(30)
            self.handle_events()
            self.background.move()
            self.move_birds()
            self.command_birds()
            self.base.move()
            self.move_pipes()

            self.draw_game()
        self.reset()
        # pygame.quit()
        # quit()


def run(fitness, config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(fitness, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat.config')
    run(Game().gameloop, config_path)
