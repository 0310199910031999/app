from typing import List
from mainContext.application.dtos.client_dto import ClientCardDTO
from mainContext.application.ports.ClientsRepo import ClientsRepo

class ClientsPanelOverview:
    def __init__(self, clients_repo: ClientsRepo):
        self.clients_repo = clients_repo

    def execute(self) -> List[ClientCardDTO]:
        return self.clients_repo.listClientCards()