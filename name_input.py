import pygame

import pygame
import json

def ask_player_name(screen, width, height, score, config_file="name_input.json"):
    """
    Pantalla para introducir el nombre del jugador cuando consigue un nuevo récord.
    Configurable desde JSON: fuentes, colores y posiciones.
    """

    # cargar JSON
    with open(config_file, "r") as f:
        config = json.load(f)

    style = config["style"]
    layout = config["layout"]

    # fuentes
    font_title = pygame.font.Font(style.get("font"), style.get("title_size", 60))
    font_text = pygame.font.Font(style.get("font"), style.get("text_size", 40))

    # colores
    bg_color = tuple(style["colors"].get("background", (0, 0, 0)))
    title_color = tuple(style["colors"].get("title", (255, 215, 0)))
    score_color = tuple(style["colors"].get("score", (255, 255, 255)))
    text_color = tuple(style["colors"].get("text", (200, 200, 200)))

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
        title_surf = font_title.render("¡New Record!", True, title_color)
        screen.blit(title_surf, title_surf.get_rect(center=(width // 2, layout["title_y"])))

        # puntuación
        score_surf = font_text.render(f"Score: {score}", True, score_color)
        screen.blit(score_surf, score_surf.get_rect(center=(width // 2, layout["score_y"])))

        # input + cursor
        display_text = input_text + ("|" if cursor_visible else "")
        if not input_text:
            display_text = "Writte your battle name..."
        input_surf = font_text.render(display_text, True, text_color)
        screen.blit(input_surf, input_surf.get_rect(center=(width // 2, layout["input_y"])))

        pygame.display.flip()
        clock.tick(30)
