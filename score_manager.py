import json
import os

class ScoreManager:
    def __init__(self, filepath="scores.json", limit=5):
        self.filepath = filepath
        self.limit = limit
        self.scores = self.load()

    def load(self):
        """Carga las puntuaciones desde el archivo JSON."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r") as f:
            try:
                data = json.load(f)
                return data.get("scores", [])
            except json.JSONDecodeError:
                return []

    def save(self):
        """Guarda las puntuaciones en el archivo JSON."""
        with open(self.filepath, "w") as f:
            json.dump({"scores": self.scores}, f, indent=4)

    def qualifies(self, new_score):
        """Comprueba si una nueva puntuación entra en el top."""
        if len(self.scores) < self.limit:
            return True
        return new_score > self.scores[-1]["score"]

    def add_score(self, player_name, new_score):
        """Añade una puntuación y actualiza el top."""
        self.scores.append({"player": player_name, "score": new_score})
        self.scores = sorted(self.scores, key=lambda s: s["score"], reverse=True)[:self.limit]
        self.save()

    def get_scores(self):
        """Devuelve la lista de puntuaciones ordenada."""
        return self.scores
