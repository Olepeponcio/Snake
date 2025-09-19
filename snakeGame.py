"""Initialize Pygame (window, clock, colors, fonts).
Create instances of your GameObjects (Snake, Food, etc.).
Handle the main loop:
Capture keyboard events.
Update objects.
Render them on the main Surface.
Control FPS (frames per second).
Manage game over and restart."""

import pygame
from sanake import Snake
from food import Food
from walls import Walls


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
        # self.color_snake = tuple(colors_conf['snake'])
        # self.color_foof = tuple(colors_conf['food'])

        # --- main window ---
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Mi Snake')

        # --- Time Control ---
        self.clock = pygame.time.Clock()
        # ---Game state ---
        self.running = True
        self.score = 0

        # here build game objects
        self.walls = Walls(config['walls'])
        self.snake = Snake(config['snake'])
        self.food = Food(config['food'])
        self.food.randomize_position()

    # --- class methods ---
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # snake input functionality
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.snake.direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.direction = (1, 0)

    def update(self):
        print(self.food)
        if self.snake:
            self.snake.update()
        if self.food:
            self.food.update()

        # Sanake collides with walls or itself
        if self.snake.collides_with_walls(self.walls.blocks):
            self.running = False
            # GAME OVER
            # SHOW FINAL SCORE
            # Pause/restart

        # snake collides with food?
        elif self.snake.collides_with_food(self.food):
            # Generate new food at random position
            self.food.randomize_position()
            # Increase snake length
            self.snake.grow()
            # Increase score
            self.score += 1


    def render(self):
        #background color
        self.screen.fill(self.color_background)
        if self.snake:
            self.snake.render(self.screen)
        if self.food:
            self.food.render(self.screen)
        if self.walls:
            self.walls.render(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps) #control of render velocity
        pygame.quit()  # <- clean close program







        # UPDATE GUID
        # Draw snak, food
        # Display score
        # refresh screen
        # control FPS

        # Back to MAIN LOOP










