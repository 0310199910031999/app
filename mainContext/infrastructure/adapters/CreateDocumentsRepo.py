from sqlalchemy.orm import Session
from sqlalchemy import func 
from typing import List, Optional 
from mainContext.application.dtos.create_documents_dto import CreateDTO
from mainContext.application.ports.CreateDocumentsRepo import CreateDocumentsRepo
from mainContext.infrastructure.models import Equipment, Fole01, Foim01, Fosp01, Fosc01, Foos01, Fobc01, Foem01

from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from mainContext.application.services.file_generator import FileService


class CreateDocumentsRepoImpl(CreateDocumentsRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_documents(self, create_dto: CreateDTO) -> bool:
        try:
            file_model = None
            client_id = self.db.query(Equipment).filter_by(id=create_dto.equipment_id).first().client_id
            if not create_dto.GC and (create_dto.fosp or create_dto.fosc or create_dto.foos or create_dto.fobc or create_dto.foem):
                file_model = FileService.create_file(self.db, client_id)
            if create_dto.fole:
                modelFole = Fole01(
                    employee_id=create_dto.employee_id,
                    equipment_id=create_dto.equipment_id,
                    client_id = client_id,
                    date_created=create_dto.date_created,
                    status=create_dto.status,
                )
            if create_dto.foim:
                modelFoim = Foim01(
                    employee_id=create_dto.employee_id,
                    equipment_id=create_dto.equipment_id,
                    client_id = client_id,
                    date_created=create_dto.date_created,
                    status=create_dto.status,
                )
            if create_dto.fosp:
                modelFosp = Fosp01(
                    employee_id=create_dto.employee_id,
                    equipment_id=create_dto.equipment_id,
                    client_id = client_id,
                    file_id = file_model.id if file_model else None,
                    date_created=create_dto.date_created,
                    status=create_dto.status,
                    GC = create_dto.GC
                )
            if create_dto.fosc:
                modelFosc = Fosc01(
                    employee_id=create_dto.employee_id,
                    equipment_id=create_dto.equipment_id,
                    client_id = client_id,
                    file_id = file_model.id if file_model else None,
                    date_created=create_dto.date_created,
                    status=create_dto.status,
                    GC = create_dto.GC
                )
            if create_dto.foos:
                modelFoos = Foos01(
                    employee_id=create_dto.employee_id,
                    equipment_id=create_dto.equipment_id,
                    client_id = client_id,
                    file_id = file_model.id if file_model else None,
                    date_created=create_dto.date_created,
                    status=create_dto.status,
                    GC = create_dto.GC
                )
            if create_dto.fobc:
                modelFobc = Fobc01(
                    employee_id=create_dto.employee_id,
                    equipment_id=create_dto.equipment_id,
                    client_id = client_id,
                    file_id = file_model.id if file_model else None,
                    date_created=create_dto.date_created,
                    status=create_dto.status,
                )
            if create_dto.foem:
                modelFoem = Foem01(
                    employee_id=create_dto.employee_id,
                    equipment_id=create_dto.equipment_id,
                    client_id = client_id,
                    file_id = file_model.id if file_model else None,
                    date_created=create_dto.date_created,
                    status=create_dto.status,
                )
            
            self.db.add_all([
                model for model in [
                    modelFole if create_dto.fole else None,
                    modelFoim if create_dto.foim else None,
                    modelFosp if create_dto.fosp else None,
                    modelFosc if create_dto.fosc else None,
                    modelFoos if create_dto.foos else None,
                    modelFobc if create_dto.fobc else None,
                    modelFoem if create_dto.foem else None
                ] if model is not None
            ])
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al crear los documentos: {str(e)}")
            
        
