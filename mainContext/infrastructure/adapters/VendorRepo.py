from mainContext.domain.models.Vendor import Vendor
from mainContext.application.ports.VendorRepo import VendorRepo
from mainContext.infrastructure.models import Vendors as VendorModel
from typing import List
from sqlalchemy.orm import Session

class VendorRepoImpl(VendorRepo):
    def __init__(self, db: Session):
        self.db = db

    def get_all_vendors(self) -> List[Vendor]:
        try:
            models = self.db.query(VendorModel).all()
            
            return [
                Vendor(
                    id=model.id,
                    name=model.name,
                    rfc=model.rfc,
                    contact_person=model.contact_person,
                    phone_number=model.phone_number,
                    email=model.email
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener vendors: {str(e)}")
