"""Initialize Pygame (window, clock, colors, fonts).
Create instances of your GameObjects (Snake, Food, etc.).
Handle the main loop:
Capture keyboard events.
Update objects.
Render them on the main Surface.
Control FPS (frames per second).
Manage game over and restart."""

import pygame
import math
from sanake import Snake
from food import Food
from walls import Walls


class Game:
    def __init__(self, config: dict):

        self.resultado = ""
        pygame.init()

        # load JSAON parameters
        screen_conf = config["screen"]
        self.width =screen_conf["width"]
        self.height = screen_conf['height']
        # velocity control of snake in game
        self.fps_base = screen_conf["fps"]
        self.fps_increment = screen_conf.get("fps_increment", 1)  # cuanto aumenta al comer
        self.fps = self.fps_base
        self.max_fps = screen_conf.get("max_fps", 60)  # limite superior opcional
        # Fuente para el marcador (puedes meterlo en config si quieres)
        self.font = pygame.font.Font(None, 36)  # None = fuente por defecto

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
        self.food.randomize_position(self.walls.blocks)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "game_over"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pause"
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if self.snake.direction != (0, 1):
                        self.snake.direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.snake.direction != (0,-1):
                        self.snake.direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.snake.direction != (1, 0):
                        self.snake.direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if  self.snake.direction != (-1, 0):
                        self.snake.direction = (1, 0)

    def update(self):
        if self.snake:
            self.snake.update()
        if self.food:
            self.food.update()

        # Sanake collides with walls or itself
        if self.snake.collides_with_walls(self.walls.blocks):
            self.running = False
            return "game_over"
            # SHOW FINAL SCORE
        elif self.snake.collides_with_self():
            self.running = False
            return "game_over"


        # snake collides with food?
        elif self.snake.collides_with_food(self.food):
            """evita la colisión con muros, con la propia serpiente y límites
            fuera de rango"""
            # Generate new food at random position
            # tuples list walls, exclude body list, not spawns out of range
            self.food.randomize_position(self.walls.blocks, snake= self.snake,
                                         require_reachable=True)
            # Increase snake length
            self.snake.grow()
            # Increase score
            self.score += 1
            # progresive high velocity
            self.fps = min(
                self.fps_base + int(5 * math.log1p(self.score)),  # 5 = factor de aceleracion
                self.max_fps
            )

    def render_score(self, x=10, y=10):
        """
        Renderiza el marcador en la posición (x, y).
        """
        text_surface = self.font.render(f"Score: {self.score}", True, (0, 255, 0))
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def render_controls(self, x=10, y=10):
        font_controls = pygame.font.Font(None, 40)  # None = fuente por defecto, size = px
        text_surface = font_controls.render("Controls: W-A-S-D / Arrows", True, (0, 255, 0))
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    # UPDATE GUID
    def render(self):
        #background color
        self.screen.fill(self.color_background)
        if self.snake:
            self.snake.render(self.screen)
        if self.food:
            self.food.render(self.screen)
        if self.walls:
            self.walls.render(self.screen)
        self.render_score(self.width -100, self.height - 25)  # esquina superior izquierda
        self.render_controls(0, self.height - 25)
        pygame.display.flip()

    def run(self):
        while self.running:

            menu = self.handle_events()
            resultado = self.update()  # recoger retorno

            if resultado == "game_over" or menu == "game_over":
                return "game_over"  # devolver estado al bucle maestro
            elif menu =="pause":
                return "pause"

            self.render()
            self.clock.tick(self.fps)  # control de velocidad de render












