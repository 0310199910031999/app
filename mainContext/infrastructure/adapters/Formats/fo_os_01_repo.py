from mainContext.domain.models.Formats.fo_os_01 import FOOS01, FOOS01Service
from mainContext.domain.models.Formats.Service import Service
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.File import File

from mainContext.application.ports.Formats.fo_os_01_repo import FOOS01Repo
from mainContext.application.dtos.Formats.fo_os_01_dto import FOOS01CreateDTO, FOOS01UpdateDTO, FOOS01SignatureDTO, FOOS01TableRowDTO, FOOS01ServiceDTO

from mainContext.infrastructure.models import Foos01Services as FOOS01ServiceModel, Foos01 as FOOS01Model, Files as FileModel, Equipment as EquipmentModel

from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from mainContext.application.services.file_generator import FileService


class FOOS01RepoImpl(FOOS01Repo):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create_foos01(self, dto: FOOS01CreateDTO) -> int:
        try: 
            client_id = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first().client_id

            file_model = FileService.create_file(self.db, client_id)

            model = FOOS01Model(
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
                raise Exception("Error al registrar FO-OS-01 en la base de datos")
            return model.id
        except Exception as e: 
            self.db.rollback()
            raise Exception(f"Error al registrar FO-OS-01 en la base de datos: {str(e)}") 
    
    
    def get_foos01_by_id(self, id: int) -> FOOS01:
        model = self.db.query(FOOS01Model).filter_by(id=id).first()
        return FOOS01(
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
                services = model.foos01_services,
                fopc_services_id= model.fopc_services_id
            )if model else None
    

    def delete_foos01(self, id: int) -> bool:
        model = self.db.query(FOOS01Model).filter_by(id=id).first()
        if not model:
            return False
        services = self.db.query(FOOS01ServiceModel).filter_by(foos01_id=id).all()
        for service in services:
            self.db.delete(service)
        file = self.db.query(FileModel).filter_by(id=model.file_id).first()
        if file:
            self.db.delete(file)
        self.db.delete(model)
        self.db.commit()
        return True
    
    def update_foos01(self, id: int, dto: FOOS01UpdateDTO) -> bool:
        try:
            model = self.db.query(FOOS01Model).filter_by(id=id).first()
            if not model:
                return None

            model.hourometer = dto.hourometer
            model.observations = dto.observations
            model.reception_name = dto.reception_name

            existing_services = model.foos01_services
            incoming_services = dto.foos01_services

            for i, incoming in enumerate(incoming_services):
                if i < len(existing_services):
                    # Actualiza servicio existente
                    existing = existing_services[i]
                    existing.service_id = incoming.service_id
                    existing.service_description = incoming.service_description

                else:
                    # Crea nuevo servicio
                    new_service = FOOS01ServiceModel(
                        foos01_id=model.id,
                        service_id=incoming.service_id,
                        service_description = incoming.service_description
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
        
    def get_list_foos01_by_equipment_id(self, equipment_id: int) -> List[FOOS01]:
        models = self.db.query(FOOS01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOOS01(
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
                services = model.foos01_services
            ) 
            for model in models
        ]
    
    def get_list_foos01_table(self, equipment_id: int) -> List[FOOS01TableRowDTO]:
        models = self.db.query(FOOS01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOOS01Model.id)).all()
        
        if not models:
            return []
        
        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else 'N/A'
            return 'N/A'
        
        return [
            FOOS01TableRowDTO(
                id=m.id,
                # Se valida m.file para obtener el folio
                file_id=m.file.folio if m.file else None, 
                date_created=m.date_created,
                observations = m.observations,
                codes=[s.service.code for s in m.foos01_services],
                # Se valida m.employee para obtener el nombre completo
                employee_name=get_full_name(m.employee),
                status=m.status
            )
            for m in models
        ]
    
    def sign_foos01(self, id: int, dto: FOOS01SignatureDTO) -> bool:
        try: 
            model = self.db.query(FOOS01Model).filter_by(id=id).first()
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


