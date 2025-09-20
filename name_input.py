import pygame
import json
import os, sys


def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta a un recurso, compatible con PyInstaller.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def ask_player_name(screen, width, height, score, config_file="resources/name_input.json"):
    """
    Pantalla para introducir el nombre del jugador cuando consigue un nuevo récord.
    Configurable desde JSON: fuentes, colores y posiciones.
    """

    # cargar JSON de configuración
    config_path = resource_path(config_file)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    style = config["style"]
    layout = config["layout"]

    # cargar fuentes con resource_path
    def load_font(path, size):
        if not path or path == "null":
            return pygame.font.Font(None, size)
        try:
            return pygame.font.Font(resource_path(path), size)
        except FileNotFoundError:
            print(f"⚠️ Fuente no encontrada: {path}, usando default")
            return pygame.font.Font(None, size)

    font_title = load_font(style.get("font"), style.get("title_size", 60))
    font_text = load_font(style.get("font"), style.get("text_size", 40))

    # colores
    colors = style["colors"]
    bg_color = tuple(colors.get("background", (0, 0, 0)))
    title_color = tuple(colors.get("title", (255, 215, 0)))
    score_color = tuple(colors.get("score", (255, 255, 255)))
    text_color = tuple(colors.get("text", (200, 200, 200)))

    # lógica del input
    input_text = ""
    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500
    MAX_CHARS = 16
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "player"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text if input_text else "player"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    char = event.unicode
                    if char.strip() != "" and len(input_text) < MAX_CHARS:
                        input_text += char

        # parpadeo cursor
        cursor_timer += clock.get_time()
        if cursor_timer >= cursor_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # limpiar pantalla
        screen.fill(bg_color)

        # título
        title_surf = font_title.render("New Record!", True, title_color)
        screen.blit(title_surf, title_surf.get_rect(center=(width // 2, layout["title_y"])))

        # puntuación
        score_surf = font_text.render(f"Score: {score}", True, score_color)
        screen.blit(score_surf, score_surf.get_rect(center=(width // 2, layout["score_y"])))

        # input + cursor
        display_text = input_text + ("|" if cursor_visible else "")
        if not input_text:
            display_text = "Write your battle name..."
        input_surf = font_text.render(display_text, True, text_color)
        screen.blit(input_surf, input_surf.get_rect(center=(width // 2, layout["input_y"])))

        pygame.display.flip()
        clock.tick(30)
