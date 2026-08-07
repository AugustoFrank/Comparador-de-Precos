from abc import ABC, abstractmethod
from app.models.produto import Produto

class ScraperBase(ABC):
    @abstractmethod
    async def extrair(self, url: str) -> Produto:
        pass