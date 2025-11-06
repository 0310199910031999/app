from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from mainContext.application.dtos.client_dto import ClientCardDTO, CreateClientDTO
from mainContext.application.ports.ClientsRepo import ClientsRepo
from mainContext.infrastructure.models import Clients, Equipment
from mainContext.domain.models.Client import Client

class ClientsPanelOverviewRepo(ClientsRepo):
    def __init__(self, db: Session):
        self.db = db

    def listClientCards(self) -> List[ClientCardDTO]:
        query = (
            self.db.query(
                Clients.id,
                Clients.status,
                Clients.name,
                Clients.rfc,
                Clients.contact_person,
                Clients.phone_number,
                func.count(Equipment.id)
                    .filter(Equipment.property == "Cliente")
                    .label("numberClientEquipment"),
                func.count(Equipment.id)
                    .filter(Equipment.property == "DAL Dealer Group")
                    .label("numberDALEquipment"),
            )
            .join(Equipment, Equipment.client_id == Clients.id, isouter=True)
            .group_by(Clients.id)
        )

        return [
            ClientCardDTO(
                id=client.id,
                status = client.status,
                name=client.name,
                rfc=client.rfc,
                contact_person=client.contact_person,
                phone_number=client.phone_number,
                numberClientEquipment=client.numberClientEquipment,
                numberDALEquipment=client.numberDALEquipment,
            )
            for client in query
        ]

    def getClientById(self, client_id: int) -> Optional[Client]:
        client = self.db.query(Clients).filter(Clients.id == client_id).first()
        if client:
            return Client(
                id=client.id,
                name=client.name,
                rfc=client.rfc,
                address=client.address,
                contact_person=client.contact_person,
                phone_number=client.phone_number,
                email=client.email,
                status=client.status
            )
        return None

    def createClient(self, client: CreateClientDTO) -> int:
        new_client = Clients(
            name=client.name,
            rfc=client.rfc,
            address=client.address,
            phone_number=client.phone_number,
            contact_person=client.contact_person,
            email=client.email,
            status=client.status
        )
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        return new_client.id
        
        

