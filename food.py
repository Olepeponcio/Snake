"""Food and Food inherit from GameObject → both implement update
(their own logic) and render (their way of drawing themselves on screen
and have private atribute position and method randomize_position"""
from game_object import GameObject
import random

class Food(GameObject):
    def __init__(self, config: dict):
        # load from a file
        self.color = tuple(config['color'])
        self.size = config['size']
        # class attributes
        self.position = (0,0) # must randomize when start game

    def randomize_position(self):
        # self.position =
        pass

        # methods of GameOject
    def update(self):
        pass

    def render(self, surface):
        """surface as a pygame object"""
        pass

