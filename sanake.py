from game_object import GameObject


class Snake(GameObject):
    def __init__(self, config: dict):
        # load from a file
        self.color = tuple(config['color'])
        self.segment_size = config['segment_size']
        self.speed = config['speed']
        self.length = config['initial_length']
        self.position = tuple(config['start_position'])
        self._MAX_POSITION = tuple(config['max_position'])

        # lista de segmentos
        self.bodylist: list[Snake.Segment] = []

        # inicializar cuerpo
        for i in range(self.length):
            x = self.position[0] - i * self.segment_size
            y = self.position[1]
            self.bodylist.append(self.Segment(x, y))

        # dirección inicial (derecha)
        self.direction = (1, 0)

    # -------------------------
    # SUBCLASE Segment
    # -------------------------
    class Segment:
        def __init__(self, x: int, y: int):
            self.coords = (x, y)

        @classmethod
        def from_tuple(cls, coords: tuple[int, int]):
            """Crea un Segment a partir de una tupla (x, y)."""
            return cls(coords[0], coords[1])

    # -------------------------
    # Métodos Snake
    # -------------------------
    def __str__(self):
        return f"Snake(length={len(self.bodylist)}, direction={self.direction})"

    def grow(self):
        self.length += 1

    def next_head_position(self):
        dx, dy = self.direction
        head_x, head_y = self.bodylist[0].coords
        return (head_x + dx * self.segment_size,
                head_y + dy * self.segment_size)

    def collides_with_walls(self, objeto):
        """Detecta colisión con muros"""
        pos = self.bodylist[0].coords
        return pos in objeto

    def collides_with_food(self, food):
        """Comprueba si algún segmento colisiona con la comida"""
        for seg in self.bodylist:
            if seg.coords == food.position:
                return True
        return False

    def collides_with_self(self):
        """Comprueba si la cabeza colisiona con el propio cuerpo"""
        head = self.bodylist[0]
        for seg in self.bodylist[1:]:
            if head.coords == seg.coords:
                return True
        return False

    # Métodos heredados de GameObject
    def update(self):
        """La cabeza se mueve en la dirección actual, se inserta un nuevo segmento
        y se elimina la cola si no creció."""
        dx, dy = self.direction
        head_x, head_y = self.bodylist[0].coords

        new_x = head_x + dx * self.segment_size
        new_y = head_y + dy * self.segment_size

        # insertar nueva cabeza
        new_head = Snake.Segment(new_x, new_y)
        self.bodylist.insert(0, new_head)

        # eliminar cola si no creció
        if len(self.bodylist) > self.length:
            self.bodylist.pop()

    def render(self, surface):
        """Dibuja la serpiente en pantalla"""
        import pygame
        for seg in self.bodylist:
            x, y = seg.coords
            rect = pygame.Rect(x, y, self.segment_size, self.segment_size)
            pygame.draw.rect(surface, self.color, rect)
