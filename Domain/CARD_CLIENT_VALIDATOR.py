from Domain.CARD_CLIENT import CardClient
import datetime

from Domain.CARD_ERROR import CardError


class CardClientValidator:
    """
    Clasa care contine o metoda care valideaza un card
    """
    @staticmethod
    def valideaza(card_client: CardClient):
        """
        Metoda care valideaza un card
        :param card_client: obiect card
        :return: nu returneaza nimic,dar poate trimite erori
        """
        errors = []
        if len(card_client.CNP) != 13:
            errors.append("CNP-ul trebuie sa aiba exact 13 cifre! ")

        for cifra in card_client.CNP:
            if cifra < '0' or cifra > '9':
                errors.append("CNP-ul trebuie sa contina doar cifre! ")

        data_minim = "01/01/1885"
        data_minim = datetime.datetime.strptime(data_minim, "%d/%m/%Y").date()
        data_maxim = datetime.date.today()
        data_maxim = data_maxim.strftime("%d/%m/%Y")
        data_maxim = datetime.datetime.strptime(data_maxim, "%d/%m/%Y").date()
        if card_client.data_nasterii < data_minim or\
                card_client.data_nasterii > data_maxim:
            errors.append("Data nasterii gresita!Introduceti o data reala!")

        if card_client.data_inregistrarii < data_minim or\
                card_client.data_inregistrarii > data_maxim:
            errors.append("Data inregistarii imposibila !"
                          " Introduceti o data reala !")

        if card_client.data_inregistrarii <= card_client.data_nasterii:
            errors.append("Nu se poate ca data inregistrarii sa fie"
                          " mai mica sau egala cu data nasterii !")

        if len(errors) > 0:
            raise CardError(str(errors))
