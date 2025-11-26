from mainContext.application.ports.VendorRepo import VendorRepo
from mainContext.application.dtos.vendor_dto import VendorDTO, VendorCreateDTO, VendorUpdateDTO
from mainContext.infrastructure.models import Vendors as VendorModel
from typing import List, Optional
from sqlalchemy.orm import Session

class VendorRepoImpl(VendorRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_vendor(self, dto: VendorCreateDTO) -> int:
        try:
            model = VendorModel(
                name=dto.name,
                rfc=dto.rfc,
                contact_person=dto.contact_person,
                phone_number=dto.phone_number,
                email=dto.email,
                address=dto.address
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar vendor en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear vendor: {str(e)}")

    def get_vendor_by_id(self, id: int) -> Optional[VendorDTO]:
        try:
            model = self.db.query(VendorModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return VendorDTO(
                id=model.id,
                name=model.name,
                rfc=model.rfc,
                contact_person=model.contact_person,
                phone_number=model.phone_number,
                email=model.email,
                address=model.address
            )
        except Exception as e:
            raise Exception(f"Error al obtener vendor: {str(e)}")

    def get_all_vendors(self) -> List[VendorDTO]:
        try:
            models = self.db.query(VendorModel).all()
            
            return [
                VendorDTO(
                    id=model.id,
                    name=model.name,
                    rfc=model.rfc,
                    contact_person=model.contact_person,
                    phone_number=model.phone_number,
                    email=model.email,
                    address=model.address
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener vendors: {str(e)}")

    def update_vendor(self, id: int, dto: VendorUpdateDTO) -> bool:
        try:
            model = self.db.query(VendorModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.name is not None:
                model.name = dto.name
            if dto.rfc is not None:
                model.rfc = dto.rfc
            if dto.contact_person is not None:
                model.contact_person = dto.contact_person
            if dto.phone_number is not None:
                model.phone_number = dto.phone_number
            if dto.email is not None:
                model.email = dto.email
            if dto.address is not None:
                model.address = dto.address

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar vendor: {str(e)}")

    def delete_vendor(self, id: int) -> bool:
        try:
            model = self.db.query(VendorModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar vendor: {str(e)}")
