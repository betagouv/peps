from enum import IntEnum
from abc import abstractmethod

class PepsEnum(IntEnum):

    @property
    @abstractmethod
    def display_text(self):
        raise NotImplementedError('display_text method not implemented')
