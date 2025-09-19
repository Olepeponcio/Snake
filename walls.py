"""Food and Food inherit from GameObject → both implement update
(their own logic) and render (their way of drawing themselves on screen
and have private atribute position and method randomize_position"""
from game_object import  GameObject

class Walls(GameObject):
    """generate collison walls to the level"""
    def __init__(self, conf: dict):
        self.blocks = []
        self._MAX_WIDTH = conf['width']
        self._MAX_HEIGHT = conf['height']
        self.size = conf['size']
        self.color = tuple(conf['color'])

        for x in range(0, self._MAX_WIDTH, self.size):
            self.blocks.append((x, 0))
            self.blocks.append((x, self._MAX_HEIGHT - self.size))
        for y in range(0, self._MAX_HEIGHT, self.size):
            self.blocks.append((0, y))
            self.blocks.append((self._MAX_WIDTH - self.size, y))

    def render(self, surface):
        import pygame
        for (x, y) in self.blocks:
            pygame.draw.rect(surface, self.color, (x, y, self.size, self.size))

    def update(self):
        pass