from Domain.UNDO_REDO_OPERATION import UndoRedoOperation
from Repository.REPOSITORY import Repository


class MultiAdaugareOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiecte_adaugate):
        self.repository = repository
        self.obiecte_adaugate = obiecte_adaugate

    def do_undo(self):
        for entitate in self.obiecte_adaugate:
            self.repository.sterge(entitate.id_entitate)

    def do_redo(self):
        for entitate in self.obiecte_adaugate:
            self.repository.adauga(entitate)
