import json
import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta a un recurso, compatible con PyInstaller.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class ScoreManager:
    def __init__(self, filepath="resources/scores.json", limit=5):
        self.filepath = resource_path(filepath)
        self.limit = limit
        self.scores = self.load()

    def load(self):
        """Carga las puntuaciones desde el archivo JSON."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("scores", [])
        except (json.JSONDecodeError, OSError):
            return []

    def save(self):
        """Guarda las puntuaciones en el archivo JSON."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump({"scores": self.scores}, f, indent=4, ensure_ascii=False)
        except OSError as e:
            print(f"⚠️ No se pudo guardar el archivo de scores: {e}")

    def qualifies(self, new_score: int) -> bool:
        """Comprueba si una nueva puntuación entra en el top."""
        if len(self.scores) < self.limit:
            return True
        return new_score > self.scores[-1]["score"]

    def add_score(self, player_name: str, new_score: int):
        """Añade una puntuación y actualiza el top."""
        self.scores.append({"player": player_name, "score": new_score})
        # ordenar y limitar
        self.scores = sorted(self.scores, key=lambda s: s["score"], reverse=True)[:self.limit]
        self.save()

    def get_scores(self):
        """Devuelve la lista de puntuaciones ordenada."""
        return self.scores
