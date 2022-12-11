from abc import ABC
from dataclasses import dataclass


@dataclass
class Entitate(ABC):
    """
    Clasa abstracta, "parinte"
    """
    id_entitate: str
