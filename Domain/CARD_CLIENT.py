from dataclasses import dataclass
from datetime import *

from Domain.ENTITATE import Entitate


@dataclass
class CardClient(Entitate):
    """
    Clasa care contine state-ul unui film
    """
    nume: str
    prenume: str
    CNP: str
    data_nasterii: date
    data_inregistrarii: date
    puncte_acumulate: int
