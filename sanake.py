"""Snake and Food inherit from GameObject → both implement update
(their own logic) and render (their way of drawing themselves on screen)."""
from email.quoprimime import body_length
from types import new_class

from game_object import GameObject


class Snake(GameObject):
    def __init__(self, config: dict):
        # load from a file
        self.color = tuple(config['color'])
        self.segment_size =config['segment_size']
        self.speed = config['speed']
        self.length = config['initial_length']
        self.position = config['start_position']
        self._MAX_POSITION = tuple(config['max_position'])

        # class attributes
        self.bodylist : list[Snake.Segment] = []
        # initialize bodylist
        for i in range(self.length):
            x = self.position[0] - i * self.segment_size
            y = self.position[1]
            self.bodylist.append(self.Segment(x, y))
        self.direction = (1,0)     #right defect

    # Segment control coord of snake body
    class Segment:
        def __init__(self, x = int, y= int):
            self.coords = tuple((x,y))

    def __str__(self):
        return f"Snake(length={len(self.bodylist)}, direction={self.direction})"


    def move(self):
        pass

    def grow(self):
        # vinculate to update
        self.length +=1

    def check_collision(self):
        pass



    # methods of GameOject
    def update(self):
        """The element at index 0 in the list takes the direction,
        must pop tail element"""
        dx, dy = self.direction
        head_x, head_y= self.bodylist[0].coords

        #new position of head
        new_x = head_x + dx * self.segment_size
        new_y = head_y + dy * self.segment_size

        #insert new head
        new_head = Snake.Segment(new_x, new_y)
        self.bodylist.insert(0,new_head)
        #pop tail segment
        if len(self.bodylist) > self.length:
            self.bodylist.pop()


    def render(self, surface):
        """surface as a pygame object"""
        import pygame
        for seg in self.bodylist:
            x, y = seg.coords
            rect = pygame.Rect(x, y, self.segment_size, self.segment_size)
            pygame.draw.rect(surface, self.color, rect)



