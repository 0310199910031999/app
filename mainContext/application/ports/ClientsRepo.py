from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.client_dto import ClientCardDTO, CreateClientDTO, UpdateClientDTO
from mainContext.domain.models.Client import Client

class ClientsRepo(ABC):
    @abstractmethod
    def listClientCards(self) -> List[ClientCardDTO]:
        pass

    @abstractmethod
    def getClientById(self, client_id: int) -> Optional[Client]:
        pass

    @abstractmethod
    def createClient(self, client: CreateClientDTO) -> int:
        pass

    @abstractmethod
    def deleteClient(self, client_id: int) -> bool:
        pass    

    @abstractmethod
    def updateClient(self, client_id: int, client: UpdateClientDTO) -> Optional[ClientCardDTO]:
        pass