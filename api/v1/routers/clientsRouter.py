from fastapi import APIRouter, Depends
from typing import Any, List
from sqlalchemy.orm import Session
from api.v1.schemas.client import ClientInfoSchema, ClientPanelOverviewSchema, CreateClientDTO
from shared.db import get_db 
from mainContext.infrastructure.adapters.ClientsRepo import ClientsPanelOverviewRepo
from mainContext.application.use_cases.clientes_use_cases import ClientsPanelOverview, CreateClient
from mainContext.application.use_cases.clientInfo import ClientInfo


ClientsRouter = APIRouter(prefix="/clients", tags=["Clients"])

@ClientsRouter.get("/panelOverview", response_model=List[ClientPanelOverviewSchema])
def clients_panel_overview(db: Session = Depends(get_db)):
    repo = ClientsPanelOverviewRepo(db)
    use_case = ClientsPanelOverview(repo)
    return use_case.execute()


@ClientsRouter.get("/client/{client_id}", response_model=ClientInfoSchema)
def get_client_info(client_id: int, db: Session = Depends(get_db)):
    repo = ClientsPanelOverviewRepo(db)
    use_case = ClientInfo(repo)
    return use_case.execute(client_id)

@ClientsRouter.post("/client", response_model=int)
def create_client(client_data: CreateClientDTO, db: Session = Depends(get_db)):
    repo = ClientsPanelOverviewRepo(db)
    use_case = CreateClient(repo)
    return use_case.execute(client_data)

