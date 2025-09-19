import pygame
import sys
import json
from snakeGame import Game
from menu import Menu   # la clase unificada que carga JSON

pygame.init()

# cargar configuración del juego
with open("config.json") as f:
    config = json.load(f)

# estados posibles
estado = "menu"

# crear ventana principal
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
            print("Mostrar scores")
            estado = "menu"
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
            estado = "juego"
        elif opcion == "menu":
            estado = "menu"
        elif opcion == "exit":
            pygame.quit()
            sys.exit()

    elif estado == "game_over":
        game_over_menu = Menu("game_over.json")
        opcion = game_over_menu.run(screen, extra_text=f"Score: {juego.score}")

        if opcion == "menu":
            estado = "menu"
        elif opcion == "exit":
            pygame.quit()
            sys.exit()
