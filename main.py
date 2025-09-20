
import sys
import os
import pygame
import json
from snakeGame import Game
from menu import Menu
from score_manager import ScoreManager
from name_input import ask_player_name

pygame.init()

# Scpre Manager
score_manager = ScoreManager("resources/scores.json", limit=5)

# cargar configuración del juego
with open("config.json") as f:
    config = json.load(f)

# estados posibles: "menu", "juego", "pause", "game_over"
estado = "menu"

# check .json files
import json
import glob

for file in glob.glob("resources/*.json"):
    try:
        with open(file, "r") as f:
            json.load(f)
        print(f"{file}: OK")
    except json.JSONDecodeError as e:
        print(f"{file}: ERROR -> {e}")


# rutas de cada menu en resources
# path_config = os.path.join("resources", "config.json")
path_main_menu = os.path.join("resources", "main_menu.json")
path_pause_menu = os.path.join("resources", "pause_menu.json")
path_game_over = os.path.join("resources", "game_over.json")
path_scores_menu = os.path.join("resources", "scores_menu.json")
path_name_input = os.path.join("resources", "name_input.json")


# ventana principal
screen_conf = config["screen"]
screen = pygame.display.set_mode((screen_conf["width"], screen_conf["height"]))
pygame.display.set_caption("Snake Game")

# bucle maestro
while True:
    if estado == "menu":
        main_menu = Menu(path_main_menu)
        opcion = main_menu.run(screen)

        if opcion == "new_game":
            estado = "juego"
        elif opcion == "show_scores":
            scores_menu = Menu(path_scores_menu)
            opcion_scores = scores_menu.run(screen)
            if opcion_scores == "menu":
                estado = "menu"
            elif opcion_scores == "exit":
                pygame.quit()
                sys.exit()
        elif opcion == "exit":
            pygame.quit()
            sys.exit()

    elif estado == "juego":
        juego = Game(config)
        resultado = juego.run()  # devuelve "pause" o "game_over"

        if resultado == "pause":
            estado = "pause"
        elif resultado == "game_over":
            estado = "game_over"

    elif estado == "pause":
        pause_menu = Menu(path_pause_menu)
        opcion = pause_menu.run(screen)

        if opcion == "resume":
            estado = "juego"
        elif opcion == "menu":
            estado = "menu"
        elif opcion == "exit":
            pygame.quit()
            sys.exit()

    elif estado == "game_over":
        # si la puntuacion entra al top 5
        if score_manager.qualifies(juego.score):
            player_name = ask_player_name(
                screen,
                screen_conf["width"],
                screen_conf["height"],
                juego.score,
                config_file=path_name_input  # usa el json de name_input
            )
            score_manager.add_score(player_name, juego.score)

        game_over_menu = Menu(path_game_over)
        opcion = game_over_menu.run(screen, extra_text=f"Score: {juego.score}")

        if opcion == "menu":
            estado = "menu"
        elif opcion == "exit":
            pygame.quit()
            sys.exit()