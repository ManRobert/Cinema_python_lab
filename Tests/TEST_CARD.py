from Domain.CARD_CLIENT import CardClient
from Domain.CARD_CLIENT_VALIDATOR import CardClientValidator
import datetime
from Repository.REPOSITORY_JSON import RepositoryJson


class TestCard:
    def test_card(self):
        # test citire din fisier
        f = "carduritest"
        cardrepository = RepositoryJson(f)
        assert cardrepository.read() == []
        # test adaugare un obiect card + scriere in fisier
        data_nasterii = datetime.datetime.strptime("02/02/2001",
                                                   "%d/%m/%Y").date()
        data_inregistrarii = datetime.datetime.strptime("02/02/2002",
                                                        "%d/%m/%Y").date()
        card = CardClient("1", "Marcelescu", "Marcel", "1111111111111",
                          data_nasterii, data_inregistrarii, 0)
        cardvalidator = CardClientValidator
        cardvalidator.valideaza(card)
        cardrepository.adauga(card)
        assert cardrepository.read("1") == card

        # test modifica card + afisare toate carduri
        card = CardClient("1", "Marcelescu", "Ricardo", "1111111111111",
                          data_nasterii, data_inregistrarii, 0)
        cardvalidator.valideaza(card)
        cardrepository.modifica(card)
        assert cardrepository.read("1") == card
        assert cardrepository.read() == \
               [CardClient(id_entitate='1',
                           nume='Marcelescu',
                           prenume='Ricardo',
                           CNP='1111111111111',
                           data_nasterii=datetime.date(2001, 2, 2),
                           data_inregistrarii=datetime.date(2002, 2, 2),
                           puncte_acumulate=0)]

        # test stergere card
        cardrepository.sterge("1")
        assert cardrepository.read() == []
