# src/core/interceptors/base.py
from abc import ABC, abstractmethod

class BaseInterceptor(ABC):
    
    @abstractmethod
    def applies(self, text: str) -> bool:
        pass

    @abstractmethod
    def process(self, text: str) -> str:
        pass
