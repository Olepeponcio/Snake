"""Main class.
Gestor de estados: Menu ↔ Juego ↔ Game Over ↔ Menu
"""

import pygame
import sys
import json
from snakeGame import Game
from menu_inicial import MainMenu

pygame.init()

# Cargar configuraciones
with open("config.json") as f:
    config = json.load(f)

with open("main_menu.json") as f:
    main_m = json.load(f)

# Estados posibles: "menu", "juego"
estado = "menu"

while True:
    if estado == "menu":
        main_menu = MainMenu(main_m)
        opcion = main_menu.ejecutar()

        if opcion == "new_game":
            estado = "juego"
        elif opcion == "show_scores":
            print("Mostrar scores")  # aquí puedes enlazar a otra pantalla
            estado = "menu"
        elif opcion == "exit":
            pygame.quit()
            sys.exit()

    elif estado == "juego":
        juego = Game(config)
        resultado = juego.run()  # run devuelve "game_over" al perder

        if resultado == "game_over":
            estado = "menu"
