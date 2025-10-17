from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.client_dto import ClientCardDTO
from mainContext.domain.models.Client import Client

class ClientsRepo(ABC):
    @abstractmethod
    def listClientCards(self) -> List[ClientCardDTO]:
        pass

    @abstractmethod
    def getClientById(self, client_id: int) -> Optional[Client]:
        pass

    