"""Main class. Hosts the structure of the game's main loop.
Imports and calls the classes defined in Object-Oriented Programming."""

import json

from snakeGame import Game

with open("config.json") as f:
    config = json.load(f)

juego = Game(config)
juego.run()



