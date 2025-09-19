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

    def randomize_position(self, blocked_positions=None):
        """
        Coloca el objeto en una posición aleatoria dentro de la pantalla.
        blocked_positions: lista de tuplas (x, y) que deben evitarse (ej: muros, snake).
        """
        max_width, max_height = self._MAX_POSITION
        cell_size = self.size

        # número máximo de celdas en cada eje
        cells_x = (max_width - cell_size) // cell_size
        cells_y = (max_height - cell_size) // cell_size

        # todas las celdas posibles
        todas_celdas = [
            (x * cell_size, y * cell_size)
            for x in range(cells_x + 1)
            for y in range(cells_y + 1)
        ]

        # excluir posiciones bloqueadas
        if blocked_positions:
            bloqueadas = set(blocked_positions)
            celdas_validas = [pos for pos in todas_celdas if pos not in bloqueadas]
        else:
            celdas_validas = todas_celdas

        if not celdas_validas:
            raise ValueError("No hay celdas libres para colocar el objeto.")
        self.position = random.choice(celdas_validas)

        # methods of GameOject
    def update(self):
      pass


    def render(self, surface):
        """surface as a pygame object"""
        import pygame
        x, y = self.position
        rect = pygame.Rect(x, y, self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)

