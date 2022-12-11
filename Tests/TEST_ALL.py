from Domain.CARD_CLIENT_VALIDATOR import CardClientValidator
from Domain.FILM_VALIDATOR import FilmValidator
from Repository.REPOSITORY_JSON import RepositoryJson
from Service.CARD_SERVICE import CardService
from Service.FILM_SERVICE import FilmService
from Service.REZERVARE_SERVICE import RezervareService
from Service.UNDO_REDO_SERVICE import UndoRedoService
from Tests.TEST_CARD import TestCard
from Tests.TEST_FILM import TestFilm
from Tests.TEST_FUNCTIONALITATI import TestFunctionalitati
from Tests.TEST_REZERVARE import TestRezervare

filmrepositoryjson = RepositoryJson("filmetest")
rezrep = RepositoryJson("rezervaritest")
undoredoservice = UndoRedoService()
filmvalidator = FilmValidator()
filmservice = FilmService(filmrepositoryjson, filmvalidator, undoredoservice)
cardrepository = RepositoryJson("carduritest")
rezervareservice = RezervareService(rezrep, filmrepositoryjson,
                                    cardrepository, undoredoservice)
cardvalidator = CardClientValidator()
cardservice = CardService(cardrepository, cardvalidator, undoredoservice)


def test_all():
    TestFilm(filmrepositoryjson).test_film()
    TestCard().test_card()
    TestRezervare().test_rezervare()

    TestFunctionalitati(filmservice,
                        rezervareservice,
                        filmrepositoryjson,
                        cardrepository,
                        cardservice,
                        rezrep,
                        undoredoservice)\
        .test_adaugare_plus_cautare()

    TestFunctionalitati(filmservice, rezervareservice,
                        filmrepositoryjson, cardrepository,
                        cardservice, rezrep,
                        undoredoservice).test_multe_functionalitati()

    TestFunctionalitati(filmservice, rezervareservice,
                        filmrepositoryjson, cardrepository,
                        cardservice, rezrep,
                        undoredoservice).test_incrementare()

    print(" ")
    print("Film Crud a trecut testele! ")
    print(" ")
    print("Card Crud a trecut testele! ")
    print(" ")
    print("Rezervare Crud a trecut testele! ")
    print(" ")
    print("Functionalitatile au trecut testele! ")
    print(" ")
