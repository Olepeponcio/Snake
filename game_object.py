"""GameObject: abstract class with mandatory methods
update() and render(surface)"""
from abc import ABC, abstractmethod

class GameObject(ABC):

    @abstractmethod
    def update(self):
        """update of the game object abstract"""
        pass

    @abstractmethod
    def render(self, surface):
        """surface as a pygame object"""
        pass