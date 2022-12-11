from Domain.ENTITATE import Entitate
from Domain.UNDO_REDO_OPERATION import UndoRedoOperation
from Repository.REPOSITORY import Repository


class AddOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiect_adaugat: Entitate):
        self.__repository = repository
        self.__obiect_adaugat = obiect_adaugat

    def do_undo(self):
        self.__repository.sterge(self.__obiect_adaugat.id_entitate)

    def do_redo(self):
        self.__repository.adauga(self.__obiect_adaugat)
