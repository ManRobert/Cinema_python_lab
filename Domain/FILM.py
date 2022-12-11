from dataclasses import dataclass

from Domain.ENTITATE import Entitate


@dataclass
class Film(Entitate):
    """
    Clasa care contine state-ul unui film
    """
    titlu: str
    an_aparitie: int
    pret_bilet: int
    in_program: str
