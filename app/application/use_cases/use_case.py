from abc import ABC, abstractmethod


class UseCase(ABC):
    @abstractmethod
    def execute(self, *args):
        """Método para executar o Use Case"""
        pass
