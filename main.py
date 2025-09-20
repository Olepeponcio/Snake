
import pygame
import sys
import json
from snakeGame import Game
from menu import Menu
from score_manager import ScoreManager
from name_input import ask_player_name

pygame.init()

# Scpre Manager
score_manager = ScoreManager("scores.json", limit=5)

# cargar configuración del juego
with open("config.json") as f:
    config = json.load(f)

# estados posibles: "menu", "juego", "pause", "game_over"
estado = "menu"

# ventana principal
screen_conf = config["screen"]
screen = pygame.display.set_mode((screen_conf["width"], screen_conf["height"]))
pygame.display.set_caption("Snake Game")

while True:
    if estado == "menu":
        main_menu = Menu("main_menu.json")
        opcion = main_menu.run(screen)

        if opcion == "new_game":
            estado = "juego"
        elif opcion == "show_scores":
            score_menu = Menu("score_menu.json")
            # give top score +
            score = score_manager.get_scores()
            opcion_scores = score_menu.run(screen, extra_text = None)
            if opcion_scores == "menu":
                estado = "menu"
            elif opcion == "exit":
                pygame.quit()
                sys.exit()
        elif opcion == "exit":
            pygame.quit()
            sys.exit()

    elif estado == "juego":
        juego = Game(config)
        resultado = juego.run()  # puede devolver "pause" o "game_over"

        if resultado == "pause":
            estado = "pause"
        elif resultado == "game_over":
            estado = "game_over"

    elif estado == "pause":
        pause_menu = Menu("pause_menu.json")
        opcion = pause_menu.run(screen)

        if opcion == "resume":
            estado = "juego"   # volver a jugar
        elif opcion == "menu":
            estado = "menu"    # ir al menú principal
        elif opcion == "exit":
            pygame.quit()
            sys.exit()

    elif estado == "game_over":
        # check score with max score list
        if score_manager.qualifies(juego.score):
            player_name = ask_player_name(screen, screen_conf['width'], screen_conf['height'],
                                           juego.score)
            score_manager.add_score(player_name, juego.score)
        else:
            score_manager.add_score("player", juego.score)

        # show game over menu
        game_over_menu = Menu("game_over.json")
        opcion = game_over_menu.run(screen, extra_text=f"Score: {juego.score}")

        if opcion == "menu":
            estado = "menu"
        elif opcion == "exit":
            pygame.quit()
            sys.exit()
