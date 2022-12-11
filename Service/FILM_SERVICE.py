from Domain.ADD_OPERATION import AddOperation
from Domain.DELETE_OPERATION import DeleteOperation
from Domain.FILM import Film
from Domain.FILM_VALIDATOR import FilmValidator
import random

from Domain.MODIFICARE_OPERATION import UpdateOperation
from Domain.MULTI_ADAUGARE_OPERATION import MultiAdaugareOperation
from Repository.REPOSITORY import Repository
from Service.UNDO_REDO_SERVICE import UndoRedoService


class FilmService:
    """
    Clasa responsabila de functionalitati
    """

    def __init__(self, filmrepository: Repository,
                 filmvalidator: FilmValidator,
                 undoredoservice: UndoRedoService):
        self.__filmrepository = filmrepository
        self.__filmvalidator = filmvalidator
        self.__undoredoservice = undoredoservice

    def get_all(self):
        """
        returneaza valorile din dictonarul care retine filme
        :return: valorile
        """
        return self.__filmrepository.read()

    def adauga(self, id_film, titlu, an_aparitie, pret_bilet, in_program):
        """
        Adauga un film in dictionarul din repository
        :param id_film: id film
        :param titlu: titlul filmului
        :param an_aparitie: anul aparitiei
        :param pret_bilet: pretul unui bilet
        :param in_program: Da sau nu in functie de existenta acestuia
        :return: None
        """
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.__filmvalidator.valideaza(film)
        self.__filmrepository.adauga(film)
        self.__undoredoservice.add_undo_operation(
            AddOperation(self.__filmrepository, film))

    def sterge(self, id_film):
        """
        sterge un film
        :param id_film: id film
        :return: None
        """
        if self.__filmrepository.read(id_film):
            self.__undoredoservice.add_undo_operation(
                DeleteOperation(self.__filmrepository,
                                self.__filmrepository.read(id_film)))

        self.__filmrepository.sterge(id_film)

    def modifica(self, id_film, titlu, an_aparitie, pret_bilet, in_program):
        """
        Modifica un film din dictionarul din repository
        :param id_film: id film
        :param titlu: titlul filmului
        :param an_aparitie: anul aparitiei
        :param pret_bilet: pretul unui bilet
        :param in_program: Da sau nu in functie de existenta acestuia
        :return: None
        """
        film_vechi = self.__filmrepository.read(id_film)
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.__filmvalidator.valideaza(film)
        self.__filmrepository.modifica(film)
        self.__undoredoservice.add_undo_operation(
            UpdateOperation(self.__filmrepository, film, film_vechi))

    def cautare_full_text(self, text=None):
        """
        cauta orice aparitie a textului in valori
        :param text: str
        :return: lista cu filmele in care s-a regasit textul
        """
        lista = []
        for film in self.__filmrepository.read():
            valori = [film.id_entitate, film.titlu, film.an_aparitie,
                      film.pret_bilet, film.in_program]

            if text in str(valori):
                lista.append(self.__filmrepository.read(film.id_entitate))
        return lista

    def generare_random(self, numar, lista, filme, in_program, ok, ok2):
        """
        genereaza random n = numar filme valide
        :param ok2: variabila pt verificare
        :param ok: variabila pt verificare
        :param in_program: in program
        :param filme: filmele
        :param lista: lista de filme generate
        :param numar: int
        :return: None
        """
        if ok:
            for i in range(0, 10000):
                filme.append("Spiderman" + str(i))
            in_program = ["Da", "Nu"]
            ok = False

        if numar > 0:
            while True:
                idul = str(random.randint(1888, 2021))
                titlu = random.choice(filme)
                an_aparitie = random.randint(1888, 2021)
                pret = random.randint(0, 2000)
                program = random.choice(in_program)
                if self.__filmrepository.read(idul) is None:
                    break
            film = Film(idul, titlu, an_aparitie, pret, program)
            self.__filmrepository.adauga(film)
            lista.append(film)
            if ok2:
                self.__undoredoservice.add_undo_operation(
                    MultiAdaugareOperation(self.__filmrepository, lista))
                ok2 = False
            return self.generare_random(numar - 1,
                                        lista, filme, in_program, ok, ok2)
        else:
            return None
