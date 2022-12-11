import datetime
from Domain.REZERVARE import Rezervare
from Repository.REPOSITORY_JSON import RepositoryJson


class TestRezervare:
    def test_rezervare(self):
        # test citire din fisier
        f = "rezervaritest"
        rezervarerepository = RepositoryJson(f)
        assert rezervarerepository.read() == []

        # test adaugare un obiect rezervare + scriere in fisier
        data = datetime.date.today()
        data = data.strftime("%d/%m/%Y")
        data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
        ora = datetime.datetime.now()
        rezervare = Rezervare("1", "1", "1", data, ora)
        rezervarerepository.adauga(rezervare)
        assert rezervarerepository.read("1") == rezervare

        # test modifica rezervare + afisare rezervari
        rezervare = Rezervare("1", "1", "1", data, ora)
        rezervarerepository.modifica(rezervare)
        assert rezervarerepository.read("1") == rezervare

        # test stergere rezervare
        rezervarerepository.sterge("1")
        assert rezervarerepository.read() == []
