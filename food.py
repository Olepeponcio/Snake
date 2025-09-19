"""Food and Food inherit from GameObject → both implement update
(their own logic) and render (their way of drawing themselves on screen
and have private atribute position and method randomize_position"""
from game_object import GameObject
import random

class Food(GameObject):
    def __init__(self, config: dict):
        # load from a file
        # argument is a object
        self._MAX_POSITION = tuple(config['max_position'])
        self.color = tuple(config['color'])
        self.size = config['size']
        # class attributes
        self.position = (0,0) # must randomize when start game

    def __str__(self):
        return f"Food(position={self.position})"

    def randomize_position(self):
        max_x = (self._MAX_POSITION[0] - self.size) // self.size
        max_y = (self._MAX_POSITION[1] - self.size) // self.size

        x = random.randint(0, max_x) * self.size
        y = random.randint(0, max_y) * self.size

        self.position = (x, y)

        # methods of GameOject
    def update(self):
      pass


    def render(self, surface):
        """surface as a pygame object"""
        import pygame
        x, y = self.position
        rect = pygame.Rect(x, y, self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)

