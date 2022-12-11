from Domain.FILM import Film
from Domain.FILM_ERROR import FilmError


class FilmValidator:
    """
    Clasa care contine o metoda care valideaza un film
    """
    @staticmethod
    def valideaza(film: Film):
        """
        Metoda care valideaza un film
        :param film: obiect film
        :return: nu returneaza nimic,dar poate trimite erori
        """
        errors = []
        if film.an_aparitie < 1888 or film.an_aparitie > 2021:
            errors.append("Anul aparitiei gresit ! "
                          "Primul film din lume a aparut in 1888, "
                          "Iar ultimul in 2021 ")
        if film.pret_bilet <= 0:
            errors.append("Pretul pentru un film "
                          "trebuie sa fie mai mare decat 0 ")
        if film.in_program not in ['Da', 'Nu']:
            errors.append("La filmul este in program "
                          "se raspunde doar cu Da sau Nu ")

        if len(errors) > 0:
            raise FilmError(str(errors))
