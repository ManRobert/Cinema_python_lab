import jsonpickle

from Domain.ENTITATE import Entitate
from Repository.REPOSITORY_IN_MEMORY import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __readfile(self):
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __writefile(self):
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))

    def read(self, id_entitate=None):
        self.entitati = self.__readfile()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate):
        self.entitati = self.__readfile()
        super().adauga(entitate)
        self.__writefile()

    def sterge(self, id_entitate):
        self.entitati = self.__readfile()
        super().sterge(id_entitate)
        self.__writefile()

    def modifica(self, entitate: Entitate):
        self.entitati = self.__readfile()
        super().modifica(entitate)
        self.__writefile()
