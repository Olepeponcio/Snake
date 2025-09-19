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
        # self.snake = None
        # self.food = None
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
        if self.snake:
            self.snake.update()
            print(self.snake)
        if self.food:
            self.food.update()
            print(self.food)

    def render(self):
        #background color
        self.screen.fill(self.color_background)
        if self.snake:
            self.snake.render(self.screen)
        if self.food:
            self.food.render(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps) #control of render velocity
        pygame.quit()  # <- clean close program







        # MAIN LOOP

        # captura events (keyborad)
        # Direction key pressed?
        # yes -> update direction

        # Move snake in current direction
        # Add new "head" forward path
        # Remove last "tail"
        # snake collides with food?

        # NO
        # YES
        # Generate new food at random position
        # Increase snake length
        # Increase score

        # Sanake collides with walls or itself
        # NO
        # YES
        # GAME OVER
        # SHOW FINAL SCORE
        # Pause/restart

        # UPDATE GUID
        # Draw snak, food
        # Display score
        # refresh screen
        # control FPS

        # Back to MAIN LOOP










