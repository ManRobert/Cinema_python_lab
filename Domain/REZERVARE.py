from dataclasses import dataclass
import datetime

from Domain.ENTITATE import Entitate


@dataclass
class Rezervare(Entitate):
    """
    Clasa care contine state-ul unei rezervari
    """
    id_film: str
    id_card: str
    data: datetime
    ora: datetime
