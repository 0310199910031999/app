from sqlalchemy.orm import Session
from typing import List
from mainContext.application.ports.AppUserRepo import AppUserRepo
from mainContext.infrastructure.models import AppUsers, Clients

class AppUserWithClientRepo(AppUserRepo):
    def __init__(self, db: Session):
        self.db = db

    def listWithClientName(self) -> List[dict]:
        query = (
            self.db.query(
                AppUsers.id,
                AppUsers.name,
                AppUsers.lastname,
                AppUsers.email,
                AppUsers.phone_number,
                Clients.name.label("client_name")
            )
            .join(Clients, AppUsers.client_id == Clients.id)
            .all()
        )
        return [
            {
                "id": user.id,
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "phone_number": user.phone_number,
                "client_name": user.client_name
            }
            for user in query
        ]