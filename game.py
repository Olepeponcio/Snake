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


class Game:
    def __init__(self, config: dict):
        pygame.init()

        # load JSAON parameters
        screen_conf = config["screen"]
        self.width =screen_conf["width"]
        self.height = screen_conf['height']
        self.fps = screen_conf['fps']
        