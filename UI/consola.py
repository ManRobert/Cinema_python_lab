from Service.CARD_SERVICE import CardService
from Service.FILM_SERVICE import FilmService
from Service.REZERVARE_SERVICE import RezervareService
import datetime

from Service.UNDO_REDO_SERVICE import UndoRedoService


class Consola:
    """
    Clasa responsabila de interactiunea cu utilizatorul
    """
    def __init__(self, filmservice: FilmService,
                 cardservice: CardService,
                 rezervareservice: RezervareService,
                 undoredoservice: UndoRedoService):

        self.__filmservice = filmservice
        self.__cardserice = cardservice
        self.__rezervareservice = rezervareservice
        self.__undoredoservice = undoredoservice

    def run_menu(self):
        while True:
            print("1. Crud film ")
            print("2. Crud card client ")
            print("3. Crud rezervare ")
            print("4. Cautare filme si clienti full text ")
            print("5. Generare filme random(cerinta lab) ")
            print("6. Afisarea tuturor rezervarilor dintr-un interval de ore")
            print("7. Afișarea filmelor ordonate descrescător"
                  " după numărul de rezervări")

            print("8. Afișarea cardurilor client ordonate descrescător după"
                  " numărul de puncte de pe card.")

            print("9. Ștergerea tuturor rezervărilor"
                  " dintr-un anumit interval de zile.")
            print("10. Incrementarea cu o valoare dată a punctelor"
                  " de pe toate cardurile a căror zi de naștere se"
                  " află într-un interval dat.")

            print("11. Stergere in cascada filme ")
            print("u. Undo")
            print("r. redo")

            print("x. Iesire")
            optiune = input("Dati optiunea ")

            if optiune == "1":
                self.run_menu_crud_film()
            elif optiune == "2":
                self.run_menu_crud_card_client()
            elif optiune == "3":
                self.run_menu_crud_rezervare()
            elif optiune == "4":
                self.run_cautare()
            elif optiune == "5":
                self.random_generare()
            elif optiune == "6":
                self.afisare_rezervari_ore()
            elif optiune == "7":
                self.afisare_ordonare()
            elif optiune == "8":
                self.afisare_ord_carduri()
            elif optiune == "9":
                self.sterge_rezervari()
            elif optiune == "10":
                self.incrementare()
            elif optiune == "11":
                self.stergere_in_cascada()
            elif optiune == "u":
                self.__undoredoservice.undo()
            elif optiune == "r":
                self.__undoredoservice.redo()
            elif optiune == "x":
                print("La revedere!")
                break
            else:
                print("Optiune gresita, alegeti din nou ")

    def run_menu_crud_film(self):
        while True:
            print("1. Adaugati film ")
            print("2. Stergeti film ")
            print("3. Modifica film ")
            print("a. Afiseaza filmele ")
            print("x. Iesire ")
            optiune = input("Dati optiunea ")
            if optiune == "1":
                self.ui_adauga_film()
            elif optiune == "2":
                self.ui_sterge_film()
            elif optiune == "3":
                self.ui_modifica_film()
            elif optiune == "a":
                self.ui_afisare_filme()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita ")

    def run_menu_crud_card_client(self):
        while True:
            print("1. Adaugati card ")
            print("2. Stergeti card ")
            print("3. Modifica card ")
            print("a. Afiseaza cardurile ")
            print("x. Iesire ")
            optiune = input("Dati optiunea ")
            if optiune == "1":
                self.ui_adauga_card()
            elif optiune == "2":
                self.ui_sterge_card()
            elif optiune == "3":
                self.ui_modifica_card()
            elif optiune == "a":
                self.ui_afisare_carduri()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita ")

    def run_menu_crud_rezervare(self):
        while True:
            print("1. Adaugati rezervare ")
            print("2. Stergeti rezervare ")
            print("3. Modifica rezervare ")
            print("a. Afiseaza rezervarile ")
            print("x. Iesire ")
            optiune = input("Dati optiunea ")
            if optiune == "1":
                self.ui_adauga_rezervare()
            elif optiune == "2":
                self.ui_sterge_rezervare()
            elif optiune == "3":
                self.ui_modifica_rezervare()
            elif optiune == "a":
                self.ui_afisare_rezervari()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita ")

    def ui_adauga_film(self):
        """
        citeste datele de adaugat
        :return: None
        """
        try:
            id_film = input("Dati id-ul filmului ")
            titlu = input("Dati titlul filmului ")
            an_aparitie = int(input("Dati anul aparitiei "))
            pret_bilet = int(input("Dati pretul unui bilet "))
            in_program = input("Filmul este in program ? Da sau Nu ")
            self.__filmservice.adauga(id_film, titlu,
                                      an_aparitie, pret_bilet, in_program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_film(self):
        """
        citeste id-ul filmului de sters
        :return: None
        """
        try:
            id_film = input("Dati id-ul filmului de sters ")
            self.__filmservice.sterge(id_film)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_film(self):
        """
        citeste modificarile ce vor fi aplicate
        :return: None
        """
        try:
            id_film = input("Dati id-ul filmului de modificat ")
            titlu = input("Dati noul titlu al filmului ")
            an_aparitie = int(input("Dati noul an al aparitiei "))
            pret_bilet = int(input("Dati noul pret al biletului "))
            in_program = input("Noul film este in program? ")
            self.__filmservice.modifica(id_film, titlu,
                                        an_aparitie, pret_bilet, in_program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_afisare_filme(self):
        """
        afiseaza valorile din dictionarul de filme
        :return: None
        """
        for film in self.__filmservice.get_all():
            print(film)

    def ui_adauga_card(self):
        """
        citeste datele de adaugat
        :return: None
        """
        try:
            id_card_client = input("Dati id-ul cardului ")
            nume = input("Dati numele clientului ")
            prenume = input("Dati prenumele clientului ")
            cnp = input("Dati CNP-ul clientului ")
            data_nasterii = input("Dati data nasterii in format dd/mm/yyyy ")
            data_nasterii = datetime.datetime.strptime(data_nasterii,
                                                       "%d/%m/%Y").date()
            data_inreg = input("Dati data inregistrarii in format dd/mm/yy ")
            data_inreg = datetime.datetime.strptime(data_inreg,
                                                    "%d/%m/%Y").date()
            puncte_acumulate = 0
            self.__cardserice.adauga(id_card_client, nume,
                                     prenume, cnp, data_nasterii,
                                     data_inreg, puncte_acumulate)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_card(self):
        """
        citeste id-ul cardului de sters
        :return: None
        """
        try:
            id_card_client = input("Dati id-ul cardului de sters ")
            self.__cardserice.sterge(id_card_client)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_card(self):
        """
         citeste modificarile ce vor fi aplicate
         :return: None
         """
        try:
            id_card_client = input("Dati id-ul cardului de modificat ")
            nume = input("Dati noul nume al clientului ")
            prenume = input("Dati noul prenume al clientului ")
            cnp = input("Dati noul CNP al clientului ")
            data_nasterii = input("Dati noua data de nastere"
                                  " in format dd/mm/yy ")
            data_nasterii = datetime.datetime.strptime(data_nasterii,
                                                       "%d/%m/%Y").date()
            data_inreg = input("Dati noua data de inregistrare"
                               " in format dd/mm/yy ")
            data_inreg = datetime.datetime.strptime(data_inreg,
                                                    "%d/%m/%Y").date()
            puncte_acumulate = int(input("Cate puncte doriti sa"
                                         " dati pe acest card ? "))
            self.__cardserice.modifica(id_card_client, nume,
                                       prenume, cnp, data_nasterii,
                                       data_inreg, puncte_acumulate)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_afisare_carduri(self):
        """
        afiseaza valorile din dictionarul de carduri
        :return: None
        """
        for card in self.__cardserice.get_all():
            print(card)

    def ui_adauga_rezervare(self):
        """
        citeste datele de adaugat
        data si ora nu sunt citite, se iau valorile de la acel moment
        :return: None
        """
        try:
            id_rezervare = input("Dati id-ul rezervarii ")
            id_film = input("Dati id-ul filmului ")
            id_card = input("Dati id-ul cardului ")
            data = datetime.date.today()
            data = data.strftime("%d/%m/%Y")
            data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
            ora = datetime.datetime.now()
            ora = ora.hour
            self.__rezervareservice.adauga(id_rezervare, id_film,
                                           id_card, data, ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_rezervare(self):
        """
        citeste id-ul rezervarii de sters
        :return: None
        """
        try:
            id_rezervare = input("Dati id-ul rezervarii de sters ")
            self.__rezervareservice.sterge(id_rezervare)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_rezervare(self):
        """
         citeste modificarile ce vor fi aplicate
         :return: None
         """
        try:
            id_rezervare = input("Dati id-ul rezervarii de modifcat ")
            id_film = input("Dati noul id al filmului ")
            id_card = input("Dati noul id al cardului ")
            data = datetime.date.today()
            data = data.strftime("%d/%m/%Y")
            data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
            ora = datetime.datetime.now()
            ora = ora.hour
            self.__rezervareservice.modifica(id_rezervare, id_film,
                                             id_card, data, ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_afisare_rezervari(self):
        """
        afiseaza valorile din dictionarul de rezervari
        :return: None
        """
        for rezervare in self.__rezervareservice.get_all():
            print(rezervare)

    def run_cautare(self):
        """
        se citeste textul care se va cauta
        se vor afisa potrivirile sau mesajul "Nu s-a gasit nicio potrivire "
        :return: None
        """
        text = input("Tastati textul pe care doriti sa-l cautati ")
        for lista in self.__filmservice.cautare_full_text(text):
            print(lista)
        lista = self.__filmservice.cautare_full_text(text)

        for lista2 in self.__cardserice.cautare_full_text(text):
            print(lista2)
        lista2 = self.__cardserice.cautare_full_text(text)

        lista_finala = []
        lista_finala = lista + lista2
        if len(lista_finala) == 0:
            print("Nu s-a gasit nicio potrivire")

    def random_generare(self):
        """
        citeste numarul de elemente ce vor fi generate random
        :return: None
        """
        try:
            numar = int(input("Dati numarul filmelor generate automat "))
            self.__filmservice.generare_random(numar, [], [], [],
                                               ok=True,
                                               ok2=True)
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)

    def afisare_rezervari_ore(self):
        """
        Citeste un interval orar
        Apeleaza functia de calcul
        Afiseaza rezervarile
        :return: None
        """
        try:
            ora1 = int(input("Dati prima ora "))
            ora2 = int(input("Dati a 2 a ora "))
            ora1 = datetime.time(ora1)
            ora1 = ora1.hour

            ora2 = datetime.time(ora2)
            ora2 = ora2.hour

            for rezervare in self.__rezervareservice.interval_orar(ora1, ora2):
                print(rezervare)
            rezultat = self.__rezervareservice.interval_orar(ora1, ora2)
            if len(rezultat) == 0:
                print("Nu exista rezervari intre orele date ")
        except ValueError as ve:
            print(ve)

    def afisare_ordonare(self):
        """
        Afiseaza filmele ordonate descrescator dupa nr de rezervari
        :return: None
        """
        for film in self.__rezervareservice.ordonare_filme():
            print(film)
        rezultat = self.__rezervareservice.ordonare_filme()
        if len(rezultat) == 0:
            print("Nu exista filme! ")

    def afisare_ord_carduri(self):
        for card in self.__cardserice.ordonare_carduri():
            print(card)
        rezultat = self.__cardserice.ordonare_carduri()
        if len(rezultat) == 0:
            print("Nu exista carduri! ")

    def sterge_rezervari(self):
        """
        Citeste 2 zile si sterge orice rezervare intre acele 2 zile,
        indiferent de luna,an
        :return: None
        """
        try:
            ziua1 = int(input("Dati ziua 1 (Numarul zilei din luna) "))
            ziua2 = int(input("Dati ziua 1 (Numarul zilei din luna) "))
            self.__rezervareservice.sterge_rezervari(ziua1, ziua2)
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)

    def incrementare(self):
        """
        Citeste 2 date care formeaza un interval, o valoare(increment)
        Apeleaza functia de calcul
        :return:
        """
        try:
            data1 = input("Dati data 1 in format dd/mm/yyyy ")
            data1 = datetime.datetime.strptime(data1, "%d/%m/%Y").date()

            data2 = input("Dati data 2 in formt dd/mm/yyyy ")
            data2 = datetime.datetime.strptime(data2, "%d/%m/%Y").date()

            valoare = int(input("Dati valoarea pentru incrementare "))
            self.__cardserice.incrementare_service(data1, data2, valoare)
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)

    def stergere_in_cascada(self):
        """
        citeste id-ul si apeleaza functia de calcul
        :return: None
        """
        try:
            id_film_sters = input("Dati id-ul filmului ")
            self.__rezervareservice.sterge_film_rezervare(id_film_sters)
            self.__filmservice.sterge(id_film_sters)

        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
