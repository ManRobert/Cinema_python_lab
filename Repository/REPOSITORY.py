from typing import Protocol, Type, Union, Optional, List

from Domain.ENTITATE import Entitate


class Repository(Protocol):
    def read(self, id_entitate=None)\
            -> Type[Union[Optional[Entitate], List[Entitate]]]:
        ...

    def adauga(self, entitate: Entitate) -> None:
        ...

    def sterge(self, id_entitate: str) -> None:
        ...

    def modifica(self, entitate: Entitate) -> None:
        ...
