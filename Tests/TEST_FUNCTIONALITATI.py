from Repository.REPOSITORY import Repository
from Service.CARD_SERVICE import CardService
from Service.FILM_SERVICE import FilmService
import datetime
from Domain.REZERVARE import Rezervare
from Repository.REPOSITORY_JSON import RepositoryJson
from Service.REZERVARE_SERVICE import RezervareService
from Service.UNDO_REDO_SERVICE import UndoRedoService


class TestFunctionalitati:
    def __init__(self, filmservice: FilmService,
                 rezervareservice: RezervareService,
                 filmrepository: Repository,
                 cardrepository: Repository,
                 cardservice: CardService,
                 rezervarerep: Repository,
                 undoredoservice: UndoRedoService):

        self.__rezervareservice = rezervareservice
        self.__filmservice = filmservice
        self.__filmrepository = filmrepository
        self.__cardrepository = cardrepository
        self.__cardservice = cardservice
        self.__rezervarerep = rezervarerep
        self.__undoredoservice = undoredoservice

    # test adaugare random filme
    def test_adaugare_plus_cautare(self):
        self.__filmservice.generare_random(3, [], [],
                                           [],
                                           ok=True,
                                           ok2=True)

        lista = self.__filmservice.get_all()
        assert len(lista) > 0

        # test cautare full text filme
        text = "Spider"
        lista = self.__filmservice.cautare_full_text(text)
        assert len(lista) == 3
        self.__undoredoservice.undo()
        lista = self.__filmservice.get_all()
        assert len(lista) == 0

    # test afisare rezervari dintr-un interval + ordonari  + stergere rezer.
    def test_multe_functionalitati(self):
        self.__filmservice.adauga("1", "Superman1", 2000, 200, "Da")

        self.__filmservice.adauga("2", "Superman2", 2000, 200, "Da")

        data_nasterii = datetime.datetime.strptime("02/02/2001",
                                                   "%d/%m/%Y").date()
        data_inregistrarii = datetime.datetime.strptime("02/02/2002",
                                                        "%d/%m/%Y").date()

        self.__cardservice.adauga("1", "Marcelescu", "Marcel",
                                  "1111111111111",
                                  data_nasterii, data_inregistrarii, 0)

        self.__cardservice.adauga("2", "Marcelescu", "Marcel", "2222222222222",
                                  data_nasterii, data_inregistrarii, 2)

        f = "rezervaritest"
        rezervarerepository = RepositoryJson(f)
        data = datetime.date.today()
        data = data.strftime("%d/%m/%Y")
        data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
        ora = datetime.datetime.now()
        rezervare = Rezervare("1", "1", "1", data, ora)
        self.__rezervareservice.adauga("1", "1", "1", data, ora)
        assert rezervarerepository.read("1") == rezervare

        rezultat = self.__rezervareservice.interval_orar(rezervare.ora,
                                                         rezervare.ora)
        assert len(rezultat) == 1

        data = datetime.date.today()
        data = data.strftime("%d/%m/%Y")
        data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
        ora = datetime.datetime.now()
        self.__rezervareservice.adauga("2", "2", "2", data, ora)

        data = datetime.date.today()
        data = data.strftime("%d/%m/%Y")
        data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
        ora = datetime.datetime.now()
        self.__rezervareservice.adauga("3", "2", "2", data, ora)

        lista = self.__rezervareservice.ordonare_filme()

        i = 2
        for film in lista:
            assert film.rezervari == i
            i -= 1

        lista = self.__cardservice.ordonare_carduri()
        assert lista[0].puncte_acumulate == 42
        assert lista[1].puncte_acumulate == 20

        self.__undoredoservice.undo()
        self.__undoredoservice.undo()
        self.__undoredoservice.undo()
        self.__undoredoservice.undo()
        self.__undoredoservice.undo()
        self.__undoredoservice.undo()
        self.__undoredoservice.undo()
        self.__undoredoservice.redo()

        lista = self.__filmrepository.read()
        assert len(lista) == 1
        self.__undoredoservice.undo()

        lista = self.__cardrepository.read()
        assert len(lista) == 0

        lista = self.__rezervarerep.read()
        assert len(lista) == 0

        data = datetime.date.today()
        data = data.strftime("%d/%m/%Y")
        data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
        ora = datetime.datetime.now()
        rezervare = Rezervare("1", "1", "1", data, ora)
        self.__rezervarerep.adauga(rezervare)

        # test sterge rezervari dintr-un anumit interval
        ziua1 = 1
        ziua2 = 31
        self.__rezervareservice.sterge_rezervari(ziua1, ziua2)
        assert self.__rezervarerep.read() == []
        self.__undoredoservice.undo()
        assert self.__rezervarerep.read() != []
        self.__undoredoservice.redo()

    # test incrementare puncte de pe card
    def test_incrementare(self):

        data_nasterii = datetime.datetime.strptime("02/02/2001",
                                                   "%d/%m/%Y").date()
        data_inregistrarii = datetime.datetime.strptime("02/02/2002",
                                                        "%d/%m/%Y").date()

        self.__cardservice.adauga("1", "Marcelescu", "Marcel",
                                  "1111111111111",
                                  data_nasterii, data_inregistrarii, 0)

        self.__cardservice.adauga("2", "Marcelescu", "Marcel", "2222222222222",
                                  data_nasterii, data_inregistrarii, 2)

        data1 = "01/01/2000"
        data1 = datetime.datetime.strptime(data1, "%d/%m/%Y").date()

        data2 = "31/12/2021"
        data2 = datetime.datetime.strptime(data2, "%d/%m/%Y").date()

        valoare = 1000
        self.__cardservice.incrementare_service(data1, data2, valoare)
        val = 1000

        for card in self.__cardrepository.read():
            assert card.puncte_acumulate == val
            val += 2

        self.__cardrepository.sterge("1")
        self.__cardrepository.sterge("2")
