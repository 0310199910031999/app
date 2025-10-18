from mainContext.domain.models.Formats.fo_sp_01 import FOSP01, FOSP01Service
from mainContext.domain.models.Formats.Service import Service
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment

from mainContext.application.ports.Formats.fo_sp_01_repo import FOSP01Repo
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO, FOSP01UpdateDTO, FOSP01SignatureDTO, FOSP01TableRowDTO, FOSP01ServiceDTO

from mainContext.infrastructure.models import Fole01Services as FOSP01ServiceModel, Fole01 as FOSP01Model
from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc

class FOSP01RepoImpl(FOSP01Repo):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create_fole01(self, dto: FOSP01CreateDTO) -> FOSP01:
        model = FOSP01Model(
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
        return FOSP01(
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
    
    def get_fole01_by_id(self, id: int) -> FOSP01:
        model = self.db.query(FOSP01Model).filter_by(id=id).first()
        return FOSP01(
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
        model = self.db.query(FOSP01Model).filter_by(id=id).first()
        if not model:
            return False
        services = self.db.query(FOSP01ServiceModel).filter_by(fole01_id=id).all()
        for service in services:
            self.db.delete(service)
        self.db.delete(model)
        self.db.commit()
        return True
    
    def update_fole01(self, id: int, dto: FOSP01UpdateDTO) -> FOSP01:
        model = self.db.query(FOSP01Model).filter_by(id=id).first()
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
                new_service = FOSP01ServiceModel(
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
        return FOSP01(
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
    
    def get_list_fole01_by_equipment_id(self, equipment_id: int) -> List[FOSP01]:
        models = self.db.query(FOSP01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOSP01(
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
    
    def get_list_fole01_table(self, equipment_id: int) -> List[FOSP01TableRawDTO]:
        models = self.db.query(FOSP01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOSP01Model.id)).all()
        if not models:
            return []
        return [
            FOSP01TableRawDTO(
                id=m.id,
                economic_number=m.equipment.economic_number,
                date_created=m.date_created,
                codes=[s.service.code for s in m.fole01_services],
                employee_name=m.employee.name + ' ' + m.employee.lastname,
                status=m.status
            )
            for m in models
        ]
    
    def sign_fole01(self, id: int, dto: FOSP01SignatureDTO) -> FOSP01:
        model = self.db.query(FOSP01Model).filter_by(id=id).first()
        if not model:
            return None

        model.status = dto.status
        model.date_signed = dto.date_signed
        model.rating = dto.rating
        model.rating_comment = dto.rating_comment

        self.db.commit()
        self.db.refresh(model)
        return model.to_domain()


