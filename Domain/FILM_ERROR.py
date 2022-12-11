from dataclasses import dataclass


@dataclass
class FilmError(Exception):
    """
    Clasa de erori proprii
    """
    mesaj: str

    def __str__(self):
        return f'FilmError: {self.mesaj}'
