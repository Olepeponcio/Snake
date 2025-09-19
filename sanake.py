"""Snake and Food inherit from GameObject → both implement update
(their own logic) and render (their way of drawing themselves on screen)."""
from game_object import GameObject

class Snake(GameObject):
    def __init__(self):
        self.bodylist : list[Snake.Segment] = []
        self.direction = tuple()

    # Segment control coord of snake body
    class Segment:
        def __init__(self, x = int, y= int):
            self.coords = tuple((x,y))

    def __str__(self):
        return f"Snake(length={len(self.bodylist)}, direction={self.direction})"

    def move(self):
        pass

    def grow(self):
        pass

    def check_collision(self):
        pass
    # methods of GameOject

    def update(self):
        pass


    def render(self, surface):
        """surface as a pygame object"""
        pass



