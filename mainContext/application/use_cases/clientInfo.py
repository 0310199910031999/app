from typing import List
from mainContext.application.ports.ClientsRepo import ClientsRepo
from mainContext.domain.models import Client

class ClientInfo:
    def __init__(self, clients_repo: ClientsRepo):
        self.clients_repo = clients_repo

    def execute(self, client_id: int) -> Client:
        return self.clients_repo.getClientById(client_id)