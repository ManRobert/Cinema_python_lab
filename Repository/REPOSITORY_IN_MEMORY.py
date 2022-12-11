from Domain.ENTITATE import Entitate
from Repository.REPOSITORY import Repository


class RepositoryInMemory(Repository):
    """
    clasa cu metode care lucreaza la CRUD
    """
    def __init__(self):
        """
        Creeaza un dictionar
        """
        self.entitati = {}

    def read(self, id_entitate=None):
        """
        Citeste valorile din dictionarul entitate
         sau returneaza o anume entitate
        :param id_entitate: id-ul entitatii(cheie)
        :return: Valorile dictionarului sau o anume entitate
        """
        if id_entitate is None:
            return list(self.entitati.values())
        if id_entitate in self.entitati:
            return self.entitati[id_entitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        """
        Adauga in dictionar
        :param entitate: obiect entitate
        :return: Nu returneaza nimic dar poate arunca eroare
        """
        if self.read(entitate.id_entitate) is not None:
            raise KeyError("Aceasta entitate exista deja! ")
        self.entitati[entitate.id_entitate] = entitate

    def sterge(self, id_entitate):
        """
        Sterge o entitate din dictionar (daca exista)
        :param id_entitate: id-ul entitatii
        :return: Nu returneaza nimic dar poate arunca eroare
        """
        if self.read(id_entitate) is None:
            raise KeyError("Aceasta entitate nu exista! ")
        del self.entitati[id_entitate]

    def modifica(self, entitate: Entitate):
        """
        Modifica un film
        :param entitate: obiect entitate
        :return: Nu returneaza nimic dar poate arunca eroare
        """
        if self.read(entitate.id_entitate) is None:
            raise KeyError("Aceasta entitate nu exista! ")
        self.entitati[entitate.id_entitate] = entitate
