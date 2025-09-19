import pygame
import json

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
        """Carga una fuente: si font_path es None, 'null' o '', usa la fuente por defecto."""
        if not font_path or font_path == "null":
            return pygame.font.Font(None, size)
        return pygame.font.Font(font_path, size)

    def draw(self, screen, extra_text=None):
        screen.fill(self.color_bg)

        # título
        title_surf = self.font_title.render(self.title, True, self.color_title)
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 4))
        screen.blit(title_surf, title_rect)

        # texto extra (ej: marcador)
        if extra_text:
            score_surf = self.font_option.render(extra_text, True, self.color_text)
            score_rect = score_surf.get_rect(center=(self.width // 2, title_rect.bottom + 40))
            screen.blit(score_surf, score_rect)

        # opciones
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
