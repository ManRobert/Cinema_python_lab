from Domain.ENTITATE import Entitate
from Domain.UNDO_REDO_OPERATION import UndoRedoOperation
from Repository.REPOSITORY import Repository


class UpdateOperation(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 obiect_nou: Entitate, obiect_vechi: Entitate):
        self.repository = repository
        self.obiect_nou = obiect_nou
        self.obiect_vechi = obiect_vechi

    def do_undo(self):
        self.repository.modifica(self.obiect_vechi)

    def do_redo(self):
        self.repository.modifica(self.obiect_nou)
