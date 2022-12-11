from Domain.ENTITATE import Entitate
from Domain.UNDO_REDO_OPERATION import UndoRedoOperation
from Repository.REPOSITORY import Repository


class DeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiect_sters: Entitate):
        self.__repository = repository
        self.__obiect_sters = obiect_sters

    def do_undo(self):
        self.__repository.adauga(self.__obiect_sters)

    def do_redo(self):
        self.__repository.sterge(self.__obiect_sters.id_entitate)
