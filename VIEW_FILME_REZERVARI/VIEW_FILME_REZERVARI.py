from dataclasses import dataclass
from Domain.FILM import Film


@dataclass
class ViewFilmeRezervari:
    """
    Creeaza un format mai adecvat
    """
    filme: Film
    rezervari: int

    def __str__(self):
        return f'{self.filme} cu nr de rezervari {self.rezervari}'
