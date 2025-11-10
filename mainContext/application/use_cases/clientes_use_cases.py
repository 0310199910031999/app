from typing import List
from mainContext.application.dtos.client_dto import ClientCardDTO, CreateClientDTO, UpdateClientDTO
from mainContext.application.ports.ClientsRepo import ClientsRepo

class ClientsPanelOverview:
    def __init__(self, clients_repo: ClientsRepo):
        self.clients_repo = clients_repo

    def execute(self) -> List[ClientCardDTO]:
        return self.clients_repo.listClientCards()

class CreateClient:
    def __init__(self, clients_repo: ClientsRepo):
        self.clients_repo = clients_repo

    def execute(self, client: CreateClientDTO) -> int:
        return self.clients_repo.createClient(client)
    
class DeleteClient:
    def __init__(self, clients_repo: ClientsRepo):
        self.clients_repo = clients_repo

    def execute(self, client_id: int) -> bool:
        return self.clients_repo.deleteClient(client_id)
    
    
class UpdateClient:
    def __init__(self, clients_repo: ClientsRepo):
        self.clients_repo = clients_repo

    def execute(self, client_id: int, client: UpdateClientDTO) -> ClientCardDTO:
        return self.clients_repo.updateClient(client_id, client)
        