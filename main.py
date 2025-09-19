"""Main class. Hosts the structure of the game's main loop.
Imports and calls the classes defined in Object-Oriented Programming."""
import pygame
import sys
import json
from snakeGame import Game
from menu_inicial import MainMenu

pygame.init()

# cargar configuraciones
with open("config.json") as f:
    config = json.load(f)

with open("main_menu.json") as f:
    main_m = json.load(f)

# bucle maestro de estados
estado = "menu"

while True:
    if estado == "menu":
        main_menu = MainMenu(main_m)
        opcion = main_menu.ejecutar()

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
        resultado = juego.run()

        if resultado == "game_over":
            estado = "menu"






