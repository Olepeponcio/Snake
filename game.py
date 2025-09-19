"""Initialize Pygame (window, clock, colors, fonts).
Create instances of your GameObjects (Snake, Food, etc.).
Handle the main loop:
Capture keyboard events.
Update objects.
Render them on the main Surface.
Control FPS (frames per second).
Manage game over and restart."""

import pygame
from pygame.examples.go_over_there import screen
from sanake import Snake
from food import Food


class Game:
    def __init__(self, config: dict):
        pygame.init()

        # load JSAON parameters
        screen_conf = config["screen"]
        self.width =screen_conf["width"]
        self.height = screen_conf['height']
        self.fps = screen_conf['fps']

        colors_conf = config['colors']
        self.color_background = tuple(colors_conf['background'])
        self.color_snake = tuple(colors_conf['snake'])
        self.color_foof = tuple(colors_conf['food'])

        # --- main window ---
        self.screen = pygame.display.set_mode(self.width, self.height)
        pygame.display.set_caption('Snake Game')

        # --- Time Control ---
        self.running = True
        self.score = 0

        # here build game objects
        self.snake = Snake(config['snake'])   # instantiated after
        self.food = None    # instantiated after

    # --- class methods ---
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # here handle sanke input
                pass

    def update(self):
        if self.snake:
            self.snake.update()




