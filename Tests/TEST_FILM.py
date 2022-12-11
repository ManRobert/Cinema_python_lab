from Domain.FILM import Film
from Domain.FILM_VALIDATOR import FilmValidator
from Repository.REPOSITORY import Repository
from Repository.REPOSITORY_JSON import RepositoryJson


class TestFilm:
    def __init__(self, filmrepository: Repository):
        self.__filmrepository = filmrepository

    def test_film(self):
        # test citire din fisier
        f = "filmetest"
        filmrepository = RepositoryJson(f)
        assert self.__filmrepository.read() == []

        # test adaugare un obiect film + scriere in fisier
        film = Film("1", "Superman2", 2000, 200, "Da")
        filmvalidator = FilmValidator()
        filmvalidator.valideaza(film)
        filmrepository.adauga(film)
        assert filmrepository.read("1") == film

        # test modifica film + afisare toate filmele
        film = Film("1", "Batman2", 2010, 500, "Nu")
        filmvalidator.valideaza(film)
        filmrepository.modifica(film)
        assert filmrepository.read("1") == film
        assert filmrepository.read() == \
               [Film(id_entitate='1',
                     titlu='Batman2',
                     an_aparitie=2010,
                     pret_bilet=500,
                     in_program='Nu')]

        # test stergere film
        filmrepository.sterge("1")
        assert filmrepository.read() == []
