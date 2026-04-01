from fastapi import APIRouter, Depends
from typing import Any, List
from api.v1.schemas.client import ClientInfoSchema, ClientPanelOverviewSchema, CreateClientSchema, UpdateClientSchema
from mainContext.infrastructure.dependencies import get_clients_repo
from mainContext.infrastructure.adapters.ClientsRepo import ClientsPanelOverviewRepo
from mainContext.application.use_cases.clientes_use_cases import ClientsPanelOverview, CreateClient, DeleteClient, UpdateClient
from mainContext.application.use_cases.clientInfo import ClientInfo


ClientsRouter = APIRouter(prefix="/clients", tags=["Clients"])

@ClientsRouter.get("/panelOverview", response_model=List[ClientPanelOverviewSchema])
def clients_panel_overview(repo: ClientsPanelOverviewRepo = Depends(get_clients_repo)):
    use_case = ClientsPanelOverview(repo)
    return use_case.execute()


@ClientsRouter.get("/client/{client_id}", response_model=ClientInfoSchema)
def get_client_info(client_id: int, repo: ClientsPanelOverviewRepo = Depends(get_clients_repo)):
    use_case = ClientInfo(repo)
    return use_case.execute(client_id)

@ClientsRouter.post("/client", response_model=int)
def create_client(client_data: CreateClientSchema, repo: ClientsPanelOverviewRepo = Depends(get_clients_repo)):
    use_case = CreateClient(repo)
    return use_case.execute(client_data)

@ClientsRouter.delete("/client/{client_id}", response_model=bool)
def delete_client(client_id: int, repo: ClientsPanelOverviewRepo = Depends(get_clients_repo)):
    use_case = DeleteClient(repo)
    return use_case.execute(client_id)

@ClientsRouter.put("/client/{client_id}", response_model=ClientPanelOverviewSchema)
def update_client(client_id: int, client_data: UpdateClientSchema, repo: ClientsPanelOverviewRepo = Depends(get_clients_repo)):
    use_case = UpdateClient(repo)
    return use_case.execute(client_id, client_data)

