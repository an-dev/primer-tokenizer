import abc
from dataclasses import dataclass


@dataclass
class Connector(abc.ABC):
    @abc.abstractmethod
    def tokenize(self, number: str, expiry_month: int, expiry_year: int, cvc: str = ''):
        pass

    @abc.abstractmethod
    def charge(self, amount: int, currency: str, description: str, token: str):
        pass
