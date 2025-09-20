"""Food and Food inherit from GameObject → both implement update
(their own logic) and render (their way of drawing themselves on screen
and have private atribute position and method randomize_position"""
from game_object import GameObject
import random
from collections import deque


class Food(GameObject):
    def __init__(self, config: dict):
        # load from a file
        # argument is a object
        self._MAX_POSITION = tuple(config['max_position'])
        self.color = tuple(config['color'])
        self.size = config['size']
        # class attributes
        self.position = (0, 0)  # must randomize when start game

    def __str__(self):
        return f"Food(position={self.position})"

    def randomize_position(self, walls_blocks=None, snake=None, require_reachable=False):
        """
        Coloca la comida en una celda libre del grid.
        - walls_blocks: iterable de tuplas (x, y) ocupadas por muros.
        - snake: objeto Snake (con bodylist[0] cabeza y .coords por segmento).
        - require_reachable: si True, solo elige celdas alcanzables desde la cabeza.
        """
        max_width, max_height = self._MAX_POSITION
        cell = self.size

        # 1) construir todas las celdas válidas (quepan completas en pantalla)
        max_x = (max_width - cell) // cell
        max_y = (max_height - cell) // cell
        todas = [(x * cell, y * cell) for x in range(max_x + 1) for y in range(max_y + 1)]

        # 2) posiciones bloqueadas: muros + cuerpo de la serpiente
        bloqueadas = set(walls_blocks or [])
        if snake:
            bloqueadas.update(seg.coords for seg in snake.bodylist)  # incluye cabeza y cuerpo

        candidatas = [p for p in todas if p not in bloqueadas]
        if not candidatas:
            raise ValueError("No hay celdas libres para colocar la comida.")

        # 3) opcional: filtrar por alcanzables con BFS desde la cabeza
        if require_reachable and snake:
            start = snake.bodylist[0].coords  # cabeza
            libres = set(candidatas)  # grafo de navegables

            def vecinos(pos):
                x, y = pos
                for dx, dy in ((cell, 0), (-cell, 0), (0, cell), (0, -cell)):
                    np = (x + dx, y + dy)
                    if np in libres:
                        yield np

            # BFS
            visit = set()
            q = deque([start]) if start in libres else deque(v for v in vecinos(start))
            while q:
                u = q.popleft()
                if u in visit:
                    continue
                visit.add(u)
                for v in vecinos(u):
                    if v not in visit:
                        q.append(v)

            alcanzables = [p for p in candidatas if p in visit]
            if alcanzables:
                candidatas = alcanzables
            # si no hay alcanzables, caemos al conjunto general de candidatas (mejor que romper)

        # 4) elegir aleatoria
        self.position = random.choice(candidatas)

        # methods of GameOject

    def update(self):
        pass

    def render(self, surface):
        """surface as a pygame object"""
        import pygame
        x, y = self.position
        rect = pygame.Rect(x, y, self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)
