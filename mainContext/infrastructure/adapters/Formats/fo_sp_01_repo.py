from mainContext.domain.models.Formats.fo_sp_01 import FOSP01, FOSP01Service
from mainContext.domain.models.Formats.Service import Service
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.File import File

from mainContext.application.ports.Formats.fo_sp_01_repo import FOSP01Repo
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO, FOSP01UpdateDTO, FOSP01SignatureDTO, FOSP01TableRowDTO, FOSP01ServiceDTO

from mainContext.infrastructure.models import Fosp01Services as FOSP01ServiceModel, Fosp01 as FOSP01Model, Files as FileModel, Equipment as EquipmentModel

from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from mainContext.application.services.file_generator import FileService


class FOSP01RepoImpl(FOSP01Repo):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create_fosp01(self, dto: FOSP01CreateDTO) -> int:
        try: 
            client_id = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first().client_id

            file_model = FileService.create_file(self.db, client_id)

            model = FOSP01Model(
                employee_id=dto.employee_id,
                equipment_id=dto.equipment_id,
                client_id = client_id,
                file_id = file_model.id,
                date_created=dto.date_created,
                status=dto.status,
                hourometer=0.0,
                observations="",
                reception_name="",
                signature_path="",
                date_signed=None,
                rating=0,
                rating_comment=""
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)

            if not model.id or model.id <= 0:
                raise Exception("Error al registrar FO-SP-01 en la base de datos")
            return model.id
        except Exception as e: 
            self.db.rollback()
            raise Exception(f"Error al registrar FO-SP-01 en la base de datos: {str(e)}") 
    
    
    def get_fosp01_by_id(self, id: int) -> FOSP01:
        model = self.db.query(FOSP01Model).filter_by(id=id).first()
        return FOSP01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                file = model.file,
                date_created = model.date_created,
                hourometer = model.hourometer,
                observations = model.observations,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                rating = model.rating,
                rating_comment = model.rating_comment,
                services = model.fosp01_services,
                fopc_services_id= model.fopc_services_id
            )if model else None
    

    def delete_fosp01(self, id: int) -> bool:
        model = self.db.query(FOSP01Model).filter_by(id=id).first()
        if not model:
            return False
        services = self.db.query(FOSP01ServiceModel).filter_by(fosp01_id=id).all()
        for service in services:
            self.db.delete(service)
        file = self.db.query(FileModel).filter_by(id=model.file_id).first()
        if file:
            self.db.delete(file)
        self.db.delete(model)
        self.db.commit()
        return True
    
    def update_fosp01(self, id: int, dto: FOSP01UpdateDTO) -> bool:
        try:
            model = self.db.query(FOSP01Model).filter_by(id=id).first()
            if not model:
                return None

            model.hourometer = dto.hourometer
            model.observations = dto.observations
            model.reception_name = dto.reception_name

            existing_services = model.fosp01_services
            incoming_services = dto.fosp01_services

            for i, incoming in enumerate(incoming_services):
                if i < len(existing_services):
                    # Actualiza servicio existente
                    existing = existing_services[i]
                    existing.service_id = incoming.service_id
                else:
                    # Crea nuevo servicio
                    new_service = FOSP01ServiceModel(
                        fosp01_id=model.id,
                        service_id=incoming.service_id,
                    )
                    self.db.add(new_service)

            # Elimina servicios sobrantes
            if len(existing_services) > len(incoming_services):
                for service in existing_services[len(incoming_services):]:
                    self.db.delete(service)

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e: 
            self.db.rollback()
            return False
        
    def get_list_fosp01_by_equipment_id(self, equipment_id: int) -> List[FOSP01]:
        models = self.db.query(FOSP01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOSP01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                horometer = model.hourometer,
                observations = model.observations,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                date_created = model.date_created,
                rating = model.rating,
                rating_comment = model.rating_comment,
                services = model.fosp01_services
            ) 
            for model in models
        ]
    
    def get_list_fosp01_table(self, equipment_id: int) -> List[FOSP01TableRowDTO]:
        models = self.db.query(FOSP01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOSP01Model.id)).all()
        if not models:
            return []
        return [
            FOSP01TableRowDTO(
                id=m.id,
                file_id=m.file_id,
                date_created=m.date_created,
                observations = m.observations,
                codes=[s.service.code for s in m.fosp01_services],
                employee_name=m.employee.name + ' ' + m.employee.lastname,
                status=m.status
            )
            for m in models
        ]
    
    def sign_fosp01(self, id: int, dto: FOSP01SignatureDTO) -> bool:
        try: 
            model = self.db.query(FOSP01Model).filter_by(id=id).first()
            if not model:
                return None

            model.status = dto.status
            model.date_signed = dto.date_signed
            model.rating = dto.rating
            model.rating_comment = dto.rating_comment

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e: 
            self.db.rollback()
            return False


