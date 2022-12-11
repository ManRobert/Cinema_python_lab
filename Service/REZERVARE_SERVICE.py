from Domain.ADD_OPERATION import AddOperation
from Domain.CARD_CLIENT import CardClient
from Domain.DELETE_OPERATION import DeleteOperation
from Domain.MODIFICARE_OPERATION import UpdateOperation
from Domain.MULTI_DELETE_OPERATION import MultiDeleteOperation
from Domain.REZERVARE import Rezervare
from Repository.REPOSITORY import Repository
from Service.UNDO_REDO_SERVICE import UndoRedoService
from VIEW_FILME_REZERVARI.VIEW_FILME_REZERVARI import ViewFilmeRezervari


class RezervareService:
    """
    Clasa responabila de functionalitati
    """
    def __init__(self, rezervarerepository: Repository,
                 filmrepository: Repository,
                 cardrepository: Repository,
                 undoredoservice: UndoRedoService):

        self.__rezrep = rezervarerepository
        self.filmrepository = filmrepository
        self.cardrepository = cardrepository
        self.__undoredoservice = undoredoservice

    def get_all(self):
        """
        returneaza valorile din dictonarul care retin rezervari
        :return: valorile
        """
        return self.__rezrep.read()

    def adauga(self, id_rezervare, id_film, id_card, data, ora):
        """
        Adauga o rezervare in dictionarul din repository
        :param id_rezervare: id ul rezervarii
        :param id_film: id-ul filmului
        :param id_card: id-ul cardului
        :param data: data
        :param ora: ora
        :return: None
        """
        rezervare = Rezervare(id_rezervare, id_film, id_card, data, ora)

        if self.filmrepository.read(id_film) is None:
            raise KeyError("Nu exista un film cu acest id! ")

        if self.cardrepository.read(id_card) is None:
            raise KeyError("Nu exista un card cu acest id! ")

        film = self.filmrepository.read(id_film)

        in_program = film.in_program
        if in_program != 'Da':
            raise KeyError("Nu se poate face rezervarea,"
                           " filmul nu mai este in program! ")

        cardul = self.cardrepository.read(id_card)
        idul = rezervare.id_card
        nume = cardul.nume
        prenume = cardul.prenume
        cnp = cardul.CNP
        data_nasterii = cardul.data_nasterii
        data_inregistrarii = cardul.data_inregistrarii
        puncte = cardul.puncte_acumulate
        pret = film.pret_bilet
        puncte = puncte + int(0.1 * pret)

        card_nou = CardClient(idul, nume, prenume, cnp,
                              data_nasterii, data_inregistrarii, puncte)

        self.cardrepository.modifica(card_nou)

        self.__rezrep.adauga(rezervare)
        self.__undoredoservice.add_undo_operation(
            AddOperation(self.__rezrep, rezervare))

    def sterge(self, id_rezervare):
        """
        sterge o rezervare
        :param id_rezervare: id-ul rezervarii de sters
        :return: None
        """
        if self.cardrepository.read(id_rezervare):
            self.__undoredoservice.add_undo_operation(
                DeleteOperation(self.__rezrep,
                                self.__rezrep.read(id_rezervare)))
        self.__rezrep.sterge(id_rezervare)

    def modifica(self, id_rezervare, id_film, id_card, data, ora):
        """
        Modifica o rezervare in dictionarul din repository
        :param id_rezervare: id ul rezervarii
        :param id_film: id-ul filmului
        :param id_card: id-ul cardului
        :param data: data
        :param ora: ora
        :return: None
        """
        rezervare_veche = self.__rezrep.read(id_rezervare)
        rezervare = Rezervare(id_rezervare, id_film, id_card, data, ora)

        if self.filmrepository.read(id_film) is None:
            raise KeyError("Nu exista un film cu acest id! ")

        if self.cardrepository.read(id_card) is None:
            raise KeyError("Nu exista un card cu acest id! ")

        film = self.filmrepository.read(id_film)

        in_program = film.in_program
        if in_program != 'Da':
            raise KeyError("Nu se poate face rezervarea,"
                           " filmul nu mai este in program! ")

        self.__rezrep.modifica(rezervare)
        self.__undoredoservice.add_undo_operation(
            UpdateOperation(self.__rezrep, rezervare, rezervare_veche))

    def interval_orar(self, ora1, ora2):
        """
        Determina ce rezervari sunt intre 2 ore,indiferent de zi
        :param ora1: ora1, time
        :param ora2: ora2, time
        :return:
        """
        lista = list(filter(lambda x: ora1 <= x.ora <= ora2,
                            self.__rezrep.read()))
        return lista

    def nr_rezervari(self, id_de_film):
        """
        Determina numarul de rezervari ale unui film
        :param id_de_film: id-ul filmului
        :return: numarul rezervarilor
        """
        numar = 0
        for rezervare in self.__rezrep.read():
            if id_de_film == rezervare.id_film:
                numar += 1
        return numar

    def ordonare_filme(self):
        """
        Returneaza numarul de rezervari pentru un film
        :return: Filmele ordonate
        """
        rezultat = []
        nr_rezervari = {}

        for film in self.filmrepository.read():
            nr_rezervari[film.id_entitate] = \
                self.nr_rezervari(film.id_entitate)

        for film in self.filmrepository.read():
            rezultat.append(ViewFilmeRezervari(
                self.filmrepository.read(film.id_entitate),
                nr_rezervari[film.id_entitate]
            ))
        return sorted(rezultat,
                      key=lambda
                      numar_rezervari: -numar_rezervari.rezervari)

    def sterge_rezervari(self, ziua1, ziua2):
        """
        Sterge orice rezervare care are ziua intre ziua1 si ziua2
        :param ziua1: ziua1
        :param ziua2: ziua1
        :return: None
        """
        lista = []
        if ziua1 < 1 or ziua1 > 31:
            raise ValueError("Ziua 1 nu e buna ")
        if ziua2 < 1 or ziua2 > 31:
            raise ValueError("Ziua 2 nu e buna ")

        for rezervare in self.__rezrep.read():
            if ziua1 <= rezervare.data.day <= ziua2:
                lista.append(self.__rezrep.read(rezervare.id_entitate))
                self.sterge(rezervare.id_entitate)

                self.__undoredoservice.delete_operation()

        self.__undoredoservice.add_undo_operation(
            MultiDeleteOperation(self.__rezrep, lista))

    def sterge_film_rezervare(self, id_de_film):
        """
        Sterge filmul cu id-ul primit
        Sterge toate rezervariile care contin filmul cu id-ul primit
        :param id_de_film: id de film
        :return: None
        """
        lista = []
        for rezervare in self.__rezrep.read():
            if rezervare.id_film == id_de_film:
                lista.append(self.__rezrep.read(rezervare.id_entitate))
                self.__rezrep.sterge(rezervare.id_entitate)

        self.__undoredoservice.add_undo_operation(
            MultiDeleteOperation(self.__rezrep, lista))
