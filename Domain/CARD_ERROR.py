from dataclasses import dataclass


@dataclass
class CardError(Exception):
    """
    Clasa de erori proprii
    """
    mesaj: str

    def __str__(self):
        return f'CardError: {self.mesaj}'
