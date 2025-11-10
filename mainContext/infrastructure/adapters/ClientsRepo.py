from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from mainContext.application.dtos.client_dto import ClientCardDTO, CreateClientDTO, UpdateClientDTO
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
                Clients.email,
                Clients.address,
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
                email=client.email,
                address=client.address,
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
        
    def deleteClient(self, client_id: int) -> bool:
        client = self.db.query(Clients).filter(Clients.id == client_id).first()
        if not client:
            return False
        self.db.delete(client)
        self.db.commit()
        return True    
    
    def updateClient(self, client_id: int, client_update: UpdateClientDTO) -> Optional[ClientCardDTO]:
        existing_client = self.db.query(Clients).filter(Clients.id == client_id).first()
        if not existing_client:
            return None

        for field, value in client_update.dict(exclude_unset=True).items():
            setattr(existing_client, field, value)

        self.db.commit()
        self.db.refresh(existing_client)

        # Re-query to get the counts for numberClientEquipment and numberDALEquipment
        updated_client_data = (
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
            .filter(Clients.id == client_id)
            .group_by(Clients.id)
            .first()
        )

        if updated_client_data:
            return ClientCardDTO(
                id=updated_client_data.id,
                status=updated_client_data.status,
                name=updated_client_data.name,
                rfc=updated_client_data.rfc,
                contact_person=updated_client_data.contact_person,
                phone_number=updated_client_data.phone_number,
                numberClientEquipment=updated_client_data.numberClientEquipment,
                numberDALEquipment=updated_client_data.numberDALEquipment,
            )
        return None
        
