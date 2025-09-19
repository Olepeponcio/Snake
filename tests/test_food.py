# tests/test_food.py
import unittest
from food import Food
import json

class TestFoodRandomizePosition(unittest.TestCase):

    def setUp(self):
        with open("config.json") as f:
            config = json.load(f)
        self.food = Food(config["food"])

    def test_positions_within_bounds(self):
        """Siempre dentro de la ventana y en la rejilla."""
        for _ in range(1000):
            self.food.randomize_position()
            x, y = self.food.position

            # Dentro de la ventana
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLess(x, self.food._MAX_POSITION[0])
            self.assertLess(y, self.food._MAX_POSITION[1])

            # Alineado a la rejilla (múltiplos de size)
            self.assertEqual(x % self.food.size, 0, f"x no cuadra: {x}")
            self.assertEqual(y % self.food.size, 0, f"y no cuadra: {y}")

    def test_when_window_not_multiple_of_cell(self):
        """Si la ventana no es múltiplo de size, no debe salirse."""
        self.food._MAX_POSITION = (610, 405)  # NO múltiplos de 20
        cell = self.food.size
        width, height = self.food._MAX_POSITION
        # Última celda válida truncada a rejilla:
        max_x_allowed = (width // cell) * cell - cell
        max_y_allowed = (height // cell) * cell - cell

        for _ in range(500):
            self.food.randomize_position()
            x, y = self.food.position
            self.assertLessEqual(x, max_x_allowed)
            self.assertLessEqual(y, max_y_allowed)
            self.assertEqual(x % cell, 0)
            self.assertEqual(y % cell, 0)

    # OPCIONAL: tests deterministas parcheando randint (ajusta el target según tu import)
    # Si en food.py tienes "import random" a nivel de módulo, usa 'food.random.randint'.
    # Si importas random dentro del método, 'random.randint' suele bastar.
    # from unittest.mock import patch
    # @patch('food.random.randint', return_value=0)
    # def test_min_cell(self, mock_randint):
    #     self.food.randomize_position()
    #     self.assertEqual(self.food.position, (0, 0))

    # @patch('food.random.randint', side_effect=[29, 19])  # con 600x400 y size=20 → última celda
    # def test_max_cell(self, mock_randint):
    #     self.food._MAX_POSITION = (600, 400)
    #     self.food.randomize_position()
    #     self.assertEqual(self.food.position, (580, 380))


if __name__ == '__main__':
    unittest.main()
