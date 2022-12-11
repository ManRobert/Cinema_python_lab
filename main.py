from Domain.CARD_CLIENT_VALIDATOR import CardClientValidator
from Domain.FILM_VALIDATOR import FilmValidator
from Repository.REPOSITORY_JSON import RepositoryJson
from Service.CARD_SERVICE import CardService
from Service.FILM_SERVICE import FilmService
from Service.REZERVARE_SERVICE import RezervareService
from Service.UNDO_REDO_SERVICE import UndoRedoService
from Tests.TEST_ALL import test_all
from UI.consola import Consola


def main():
    filmrepositoryjson = RepositoryJson("filme")
    filmvalidator = FilmValidator()
    undoredoservice = UndoRedoService()

    cardrepositoryjson = RepositoryJson("carduri")
    cardvalidator = CardClientValidator()

    rezervarerepositoryjson = RepositoryJson("rezervari")

    filmservice = FilmService(filmrepositoryjson,
                              filmvalidator, undoredoservice)
    cardservice = CardService(cardrepositoryjson,
                              cardvalidator, undoredoservice)
    rezervareservice = RezervareService(rezervarerepositoryjson,
                                        filmrepositoryjson,
                                        cardrepositoryjson, undoredoservice)

    try:
        test_all()
    except Exception as e:
        print(e)
    consola = Consola(filmservice, cardservice, rezervareservice,
                      undoredoservice)
    consola.run_menu()


if __name__ == '__main__':
    main()
