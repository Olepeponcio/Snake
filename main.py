import sys
import os
import pygame
import json
from snakeGame import Game
from menu import Menu
from score_manager import ScoreManager
from name_input import ask_player_name

pygame.init()


import sys
import os
import pygame
import json
from snakeGame import Game
from menu import Menu
from score_manager import ScoreManager
from name_input import ask_player_name

pygame.init()


def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta a un recurso, compatible con PyInstaller.
    Cuando se empaqueta con PyInstaller, sys._MEIPASS apunta a la carpeta temporal.
    En desarrollo, usa la ruta del archivo actual.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# -------------------------
# Configuración principal
# -------------------------
config_file = resource_path("resources/config.json")
with open(config_file, "r", encoding="utf-8") as f:
    config = json.load(f)

# -------------------------
# ScoreManager con scores.json externo
# -------------------------
if getattr(sys, 'frozen', False):  # ejecutable
    base_dir = os.path.dirname(sys.executable)
else:  # desarrollo
    base_dir = os.path.dirname(os.path.abspath(__file__))

scores_file = os.path.join(base_dir, "scores.json")
score_manager = ScoreManager(scores_file, limit=5)

# -------------------------
# Rutas de menús y name_input (empaquetados)
# -------------------------
main_menu_file = resource_path("resources/main_menu.json")
pause_menu_file = resource_path("resources/pause_menu.json")
game_over_file = resource_path("resources/game_over.json")
scores_menu_file = resource_path("resources/scores_menu.json")
name_input_file = resource_path("resources/name_input.json")

# -------------------------
# Ventana principal
# -------------------------
screen_conf = config["screen"]
screen = pygame.display.set_mode((screen_conf["width"], screen_conf["height"]))
pygame.display.set_caption("Snake Game")

# -------------------------
# Variables de control
# -------------------------
estado = "menu"
saved_state = None
juego = None



# bucle maestro
while True:
    if estado == "menu":
        main_menu = Menu(main_menu_file)
        opcion = main_menu.run(screen)

        if opcion == "new_game":
            estado = "juego"
        elif opcion == "show_scores":
            if not os.path.exists(scores_file):
                with open(scores_file, "w", encoding="utf-8") as f:
                    json.dump({"scores": []}, f, indent=4, ensure_ascii=False)

            scores_menu = Menu(scores_menu_file)
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

        # si no existe un objeto juego (nueva partida), crea uno

        if not saved_state or not hasattr(juego, "snake"):
            juego = Game(config)

        # si había un estado guardado, restaurarlo antes de correr

        if saved_state:
            juego.set_state(saved_state)

            saved_state = None

        resultado = juego.run()  # devuelve "pause" o "game_over"

        if resultado == "pause":

            estado = "pause"

            saved_state = juego.get_state()  # guarda snapshot al pausar

        elif resultado == "game_over":

            estado = "game_over"


    elif estado == "pause":

        pause_menu = Menu(pause_menu_file)

        opcion = pause_menu.run(screen)

        if opcion == "resume":

            estado = "juego"  # retomará con saved_state en el bloque "juego"

        elif opcion == "menu":

            estado = "menu"

            saved_state = None  # descartamos snapshot

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
                config_file=name_input_file  # usa el json de name_input
            )
            score_manager.add_score(player_name, juego.score)

        game_over_menu = Menu(game_over_file)
        opcion = game_over_menu.run(screen, extra_text=f"Score: {juego.score}")

        if opcion == "menu":
            estado = "menu"
        elif opcion == "exit":
            pygame.quit()
            sys.exit()
