from Domain.UNDO_REDO_OPERATION import UndoRedoOperation
from Repository.REPOSITORY import Repository


class MultiDeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiecte_sterse):
        self.repository = repository
        self.obiecte_sterse = obiecte_sterse

    def do_undo(self):
        for entitate in self.obiecte_sterse:
            self.repository.adauga(entitate)

    def do_redo(self):
        for entitate in self.obiecte_sterse:
            self.repository.sterge(entitate.id_entitate)
