from abc import abstractmethod, ABC


class EmailSender(ABC):
    @abstractmethod
    def send(self, email: str, billet: str) -> None:
        raise NotImplementedError("Subclass must implement send()")
