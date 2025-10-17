from mainContext.domain.models.Formats.fo_le_01 import FOLE01, FOLE01Service
from mainContext.domain.models.Formats.Service import Service
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment

from mainContext.application.ports.Formats.fo_le_01_repo import FOLE01Repo
from mainContext.application.dtos.Formats.fo_le_01_dto import FOLE01CreateDTO, FOLE01UpdateDTO, FOLE01SignatureDTO, FOLE01TableRawDTO, FOLE01ServiceDTO

from mainContext.infrastructure.models import Fole01Services as FOLE01ServiceModel, Fole01 as FOLE01Model
from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc

class FOLE01RepoImpl(FOLE01Repo):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create_fole01(self, dto: FOLE01CreateDTO) -> FOLE01:
        model = FOLE01Model(
            employee_id=dto.employee_id,
            equipment_id=dto.equipment_id,
            date_created=dto.date_created,
            status=dto.status,
            hourometer=0.0,
            technical_action="",
            reception_name="",
            signature_path="",
            date_signed=None,
            rating=0,
            rating_comment=""
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return FOLE01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                horometer = model.hourometer,
                technical_action = model.technical_action,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                date_created = model.date_created,
                rating = model.rating,
                rating_comment = model.rating_comment,
                services = model.fole01_services
            )
    
    def get_fole01_by_id(self, id: int) -> FOLE01:
        model = self.db.query(FOLE01Model).filter_by(id=id).first()
        return FOLE01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                horometer = model.hourometer,
                technical_action = model.technical_action,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                date_created = model.date_created,
                rating = model.rating,
                rating_comment = model.rating_comment,
                services = model.fole01_services
            )if model else None
    

    def delete_fole01(self, id: int) -> bool:
        model = self.db.query(FOLE01Model).filter_by(id=id).first()
        if not model:
            return False
        services = self.db.query(FOLE01ServiceModel).filter_by(fole01_id=id).all()
        for service in services:
            self.db.delete(service)
        self.db.delete(model)
        self.db.commit()
        return True
    
    def update_fole01(self, id: int, dto: FOLE01UpdateDTO) -> FOLE01:
        model = self.db.query(FOLE01Model).filter_by(id=id).first()
        if not model:
            return None

        model.hourometer = dto.hourometer
        model.technical_action = dto.technical_action
        model.reception_name = dto.reception_name

        existing_services = model.fole01_services
        incoming_services = dto.services

        for i, incoming in enumerate(incoming_services):
            if i < len(existing_services):
                # Actualiza servicio existente
                existing = existing_services[i]
                existing.service_id = incoming.service_id
                existing.diagnose_description = incoming.diagnose_description
                existing.description_service = incoming.description_service
                existing.priority = incoming.priority
            else:
                # Crea nuevo servicio
                new_service = FOLE01ServiceModel(
                    fole01_id=model.id,
                    service_id=incoming.service_id,
                    diagnose_description=incoming.diagnose_description,
                    description_service=incoming.description_service,
                    priority=incoming.priority
                )
                self.db.add(new_service)

        # Elimina servicios sobrantes
        if len(existing_services) > len(incoming_services):
            for service in existing_services[len(incoming_services):]:
                self.db.delete(service)

        self.db.commit()
        self.db.refresh(model)
        return FOLE01(
            id = model.id,
            employee = model.employee,
            equipment = model.equipment,
            horometer = model.hourometer,
            technical_action = model.technical_action,
            status = model.status,
            reception_name = model.reception_name,
            signature_path = model.signature_path,
            date_signed = model.date_signed,
            date_created = model.date_created,
            rating = model.rating,
            rating_comment = model.rating_comment,
            services = model.fole01_services
        )
    
    def get_list_fole01_by_equipment_id(self, equipment_id: int) -> List[FOLE01]:
        models = self.db.query(FOLE01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOLE01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                horometer = model.hourometer,
                technical_action = model.technical_action,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                date_created = model.date_created,
                rating = model.rating,
                rating_comment = model.rating_comment,
                services = model.fole01_services
            ) 
            for model in models
        ]
    
    def get_list_fole01_table(self, equipment_id: int) -> List[FOLE01TableRawDTO]:
        models = self.db.query(FOLE01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOLE01Model.id)).all()
        if not models:
            return []
        return [
            FOLE01TableRawDTO(
                id=m.id,
                economic_number=m.equipment.economic_number,
                date_created=m.date_created,
                codes=[s.service.code for s in m.fole01_services],
                employee_name=m.employee.name + ' ' + m.employee.lastname,
                status=m.status
            )
            for m in models
        ]
    
    def sign_fole01(self, id: int, dto: FOLE01SignatureDTO) -> FOLE01:
        model = self.db.query(FOLE01Model).filter_by(id=id).first()
        if not model:
            return None

        model.status = dto.status
        model.date_signed = dto.date_signed
        model.rating = dto.rating
        model.rating_comment = dto.rating_comment

        self.db.commit()
        self.db.refresh(model)
        return model.to_domain()


