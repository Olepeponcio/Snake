import pygame
import sys
import json

pygame.init()

class MainMenu:
    def __init__(self, config_json):
        # Parsear JSON (puede ser ruta a archivo o dict ya cargado)
        if isinstance(config_json, str):
            with open(config_json, "r") as f:
                self.config = json.load(f)
        else:
            self.config = config_json

        # Ventana
        self.width = self.config["window"]["width"]
        self.height = self.config["window"]["height"]
        self.ventana = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.config["title"])

        # Fuente
        font_path = self.config["style"]["font"]
        font_size = self.config["style"]["font_size"]
        self.fuente = pygame.font.Font(font_path, font_size)

        # Colores
        colors = self.config["style"]["colors"]
        self.color_bg = tuple(colors["background"])
        self.color_text = tuple(colors["text"])
        self.color_highlight = tuple(colors["highlight"])

        # Opciones
        self.title = self.config["title"]
        self.options = self.config["options"]
        self.seleccion = 0
        self.running = True

    def dibujar(self):
        self.ventana.fill(self.color_bg)

        # Dibujar título (centrado arriba)
        titulo_surf = self.fuente.render(self.title, True, self.color_text)
        titulo_rect = titulo_surf.get_rect(center=(self.width // 2, 80))
        self.ventana.blit(titulo_surf, titulo_rect)

        # Calcular centrado vertical de las opciones
        espaciado = 50
        altura_total = len(self.options) * espaciado
        inicio_y = (self.height - altura_total) // 2 + 100  # +100 para dejar hueco debajo del título

        for i, opcion in enumerate(self.options):
            color = self.color_highlight if i == self.seleccion else self.color_text
            superficie = self.fuente.render(opcion["label"], True, color)

            # ahora calculamos la posición Y dinámicamente
            y = inicio_y + i * espaciado
            rect = superficie.get_rect(center=(self.width // 2, y))
            self.ventana.blit(superficie, rect)

        pygame.display.flip()

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.seleccion = (self.seleccion - 1) % len(self.options)
                elif evento.key == pygame.K_DOWN:
                    self.seleccion = (self.seleccion + 1) % len(self.options)
                elif evento.key == pygame.K_RETURN:
                    return self.options[self.seleccion]["action"]
        return None

    def ejecutar(self):
        while self.running:
            accion = self.manejar_eventos()
            if accion:
                return accion
            self.dibujar()


