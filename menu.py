import pygame
import json
import os, sys
from score_manager import ScoreManager


def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta a un recurso, compatible con PyInstaller.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Menu:
    def __init__(self, config_json):
        # cargar json (ruta a archivo o dict ya cargado)
        if isinstance(config_json, str):
            with open(config_json, "r") as f:
                self.config = json.load(f)
        else:
            self.config = config_json

        # básicos
        window_cfg = self.config.get("window", {})
        self.width = window_cfg.get("width", 800)
        self.height = window_cfg.get("height", 600)
        self.title = self.config.get("title", "Menu")
        self.options = self.config.get("options", [])

        # estilos
        style = self.config.get("style", {})
        self.font_title = self._load_font(style.get("title_font"), style.get("title_size", 60))
        self.font_option = self._load_font(style.get("option_font"), style.get("option_size", 40))

        colors = style.get("colors", {})
        self.color_bg = tuple(colors.get("background", (0, 0, 0)))
        self.color_title = tuple(colors.get("title", (255, 255, 255)))
        self.color_text = tuple(colors.get("text", (200, 200, 200)))
        self.color_highlight = tuple(colors.get("highlight", (0, 200, 0)))

        self.selection = 0
        self.running = True

    def _load_font(self, font_path, size):
        """Carga una fuente: si font_path es None o vacío, usa la fuente por defecto."""
        if not font_path or font_path == "null":
            return pygame.font.Font(None, size)
        try:
            return pygame.font.Font(resource_path(font_path), size)
        except FileNotFoundError:
            print(f"⚠️ Fuente no encontrada: {font_path}, usando default")
            return pygame.font.Font(None, size)

    def draw(self, screen, extra_text=None):
        screen.fill(self.color_bg)

        # título
        title_surf = self.font_title.render(self.title, True, self.color_title)
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 6))
        screen.blit(title_surf, title_rect)

        # caso especial: menú de puntuaciones
        if self.title.lower().startswith("mejores puntuaciones"):
            # usa score_manager externo (editable)
            base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
            scores_file = os.path.join(base_dir, "scores.json")
            score_manager = ScoreManager(scores_file)
            scores = score_manager.get_scores()

            start_y = title_rect.bottom + 30
            for i, score in enumerate(scores):
                text = f"{score['player']} - {score['score']}"
                score_surf = self.font_option.render(text, True, self.color_text)
                score_rect = score_surf.get_rect(center=(self.width // 2, start_y + i * 30))
                screen.blit(score_surf, score_rect)

            # dibujar opciones debajo de la lista
            start_y = self.height - 120
            for i, option in enumerate(self.options):
                color = self.color_highlight if i == self.selection else self.color_text
                opt_surf = self.font_option.render(option["label"], True, color)
                opt_rect = opt_surf.get_rect(center=(self.width // 2, start_y + i * 50))
                screen.blit(opt_surf, opt_rect)

        else:
            # texto extra (ej: marcador en game over)
            if extra_text:
                score_surf = self.font_option.render(extra_text, True, self.color_text)
                score_rect = score_surf.get_rect(center=(self.width // 2, title_rect.bottom + 40))
                screen.blit(score_surf, score_rect)

            # opciones normales
            start_y = self.height // 2
            for i, option in enumerate(self.options):
                color = self.color_highlight if i == self.selection else self.color_text
                opt_surf = self.font_option.render(option["label"], True, color)
                opt_rect = opt_surf.get_rect(center=(self.width // 2, start_y + i * 60))
                screen.blit(opt_surf, opt_rect)

        pygame.display.flip()

    def run(self, screen, extra_text=None):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selection = (self.selection - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selection = (self.selection + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selection]["action"]

            self.draw(screen, extra_text)
            clock.tick(30)
