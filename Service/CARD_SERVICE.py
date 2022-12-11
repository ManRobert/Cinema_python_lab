from Domain.ADD_OPERATION import AddOperation
from Domain.CARD_CLIENT import CardClient
from Domain.CARD_CLIENT_VALIDATOR import CardClientValidator
from Domain.DELETE_OPERATION import DeleteOperation
from Domain.MODIFICARE_OPERATION import UpdateOperation
from Domain.MULTI_UPDATE_OPERATION import MultiUpdateOperation
from Repository.REPOSITORY import Repository
from Service.UNDO_REDO_SERVICE import UndoRedoService


class CardService:
    """
    Clasa responsabila de functionalitati
    """

    def __init__(self, cardrepository: Repository,
                 cardvalidator: CardClientValidator,
                 undoredoservice: UndoRedoService):
        self.__cardrepository = cardrepository
        self.__cardvalidator = cardvalidator
        self.__undoredoservice = undoredoservice

    def get_all(self):
        """
        returneaza valorile din dictonarul care retine carduri
        :return: valorile
        """
        return self.__cardrepository.read()

    def adauga(self, id_card_client, nume, prenume,
               cnp, data_nasterii, data_inregistrarii, puncte_acumulate):
        """
        adauga un card in dictionarul din repository
        :param id_card_client: id-ul cardului
        :param nume: numele de pe card
        :param prenume: prenumele de pe card
        :param cnp: cnp-ul de pe card
        :param data_nasterii: data nasterii
        :param data_inregistrarii: data inregistrarii
        :param puncte_acumulate: punctele de pe card
        :return: None
        """
        card = CardClient(id_card_client, nume, prenume, cnp,
                          data_nasterii, data_inregistrarii, puncte_acumulate)
        self.__cardvalidator.valideaza(card)
        for crd in self.__cardrepository.read():
            if crd.CNP == card.CNP:
                raise KeyError("CNP-ul acesta nu este unic! ")

        self.__cardrepository.adauga(card)
        self.__undoredoservice.add_undo_operation(
            AddOperation(self.__cardrepository, card))

    def sterge(self, id_card_client):
        """
        sterge un card
        :param id_card_client: id ul cardului
        :return: None
        """
        if self.__cardrepository.read(id_card_client):
            self.__undoredoservice.add_undo_operation(
                DeleteOperation(self.__cardrepository,
                                self.__cardrepository.read(id_card_client)))
        self.__cardrepository.sterge(id_card_client)

    def modifica(self, id_card_client, nume, prenume,
                 cnp, data_nasterii, data_inregistrarii, puncte_acumulate):
        """
        Modifica un card din dictionarul din repository
        :param id_card_client: id-ul cardului
        :param nume: numele de pe card
        :param prenume: prenumele de pe card
        :param cnp: cnp-ul de pe card
        :param data_nasterii: data nasterii
        :param data_inregistrarii: data inregistrarii
        :param puncte_acumulate: punctele de pe card
        :return: None
        """
        card_vechi = self.__cardrepository.read(id_card_client)
        card = CardClient(id_card_client, nume, prenume, cnp,
                          data_nasterii, data_inregistrarii, puncte_acumulate)
        self.__cardvalidator.valideaza(card)
        self.__cardrepository.modifica(card)
        self.__undoredoservice.add_undo_operation(
            UpdateOperation(self.__cardrepository, card, card_vechi))

    @staticmethod
    def verificare(text, element):
        """
        verifica daca textul se regaseste intr-un camp al obiectului
        :param text: text
        :param element: obiectul
        :return: True/False
        """

        return text in str(element.nume) or\
            text in str(element.prenume) or\
            text in str(element.CNP) or\
            text in str(element.data_nasterii) or\
            text in str(element.data_inregistrarii) or\
            text in str(element.puncte_acumulate)

    def cautare_full_text(self, text=None):
        """
        cauta orice aparitie a textului in valori
        :param text: str
        :return: lista cu cardurile in care s-a regasit textul
        """

        lista = list(filter(lambda x: self.verificare(text, x),
                            self.__cardrepository.read()))
        return lista

    def ordonare_carduri(self):
        """
        Afiseaza cardurile ordonate descrescator dupa nr de puncte
        :return: cardurile ordonate
        """
        return self.sorted_man(self.__cardrepository.read(),
                               key=lambda card: card.puncte_acumulate,
                               reverse=True)

    def incrementare_service(self, data1, data2, valoare):
        """
        Functia incrementeaza punctele de pe card cu valoarea primita
        Daca data nasteri este intre cele 2 date primite
        :param data1: data1
        :param data2: data2
        :param valoare: valoare pt increment
        :return:None
        """
        lista_veche = self.__cardrepository.read()
        lista = []
        if data1 >= data2:
            raise ValueError("Data 1 trebuie sa fie mai mica decat data2!")
        if valoare <= 0:
            raise ValueError("Valoarea de increment "
                             "trebuie sa fie mai mare decat 0 !")

        for card in self.__cardrepository.read():
            if data1 <= card.data_nasterii <= data2:
                puncte_noi = card.puncte_acumulate + valoare
                self.modifica(card.id_entitate, card.nume, card.prenume,
                              card.CNP, card.data_nasterii,
                              card.data_inregistrarii, puncte_noi)
                lista.append(self.__cardrepository.read(card.id_entitate))

                self.__undoredoservice.delete_operation()

        self.__undoredoservice.add_undo_operation(
            MultiUpdateOperation(self.__cardrepository, lista, lista_veche))

    @staticmethod
    def sorted_man(lista, key, reverse: bool):
        if reverse:
            for i in range(0, len(lista) - 1):
                for j in range(i + 1, len(lista)):
                    if key(lista[i]) < key(lista[j]):
                        lista[i], lista[j] = lista[j], lista[i]
        else:
            for i in range(1, len(lista) - 2):
                for j in range(i + 1, len(lista) - 1):
                    if key(lista[i] > lista[j]):
                        lista[i], lista[j] = lista[j], lista[i]
        return lista
