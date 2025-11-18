from typing import List
from mainContext.domain.models.Formats.fo_bc_01 import FOBC01

from mainContext.application.dtos.Formats.fo_bc_01_dto import FOBC01CreateDTO, FOBC01UpdateDTO, FOBC01SignatureDTO, FOBC01TableRowDTO
from mainContext.application.ports.Formats.fo_bc_01_repo import FOBC01Repo

from mainContext.infrastructure.models import Fobc01 as FOBC01Model, Equipment as EquipmentModel, Files as FileModel

from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from mainContext.application.services.file_generator import FileService

class FOBC01RepoImpl(FOBC01Repo):
    def __init__(self, db: Session):
        self.db = db
    
    def create_fobc01(self, dto: FOBC01CreateDTO) -> int:
        try:
            client_id = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first().client_id

            file_model = FileService.create_file(self.db, client_id)

            model = FOBC01Model(
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
            if model.id is None:
                raise Exception("Error al registrar FO-BC-01 en la base de datos")
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al registrar FO-BC-01 en la base de datos: {str(e)}")

    def get_fobc01_by_id(self, id: int) -> FOBC01:
        model = self.db.query(FOBC01Model).filter_by(id=id).first()
        return FOBC01(
            id = model.id,
            employee = model.employee,
            equipment = model.equipment,
            client = model.client,
            file=model.file,
            date_created = model.date_created,
            hourometer = model.hourometer,
            observations = model.observations,
            status = model.status,
            reception_name =model.reception_name,
            signature_path = model.signature_path,
            date_signed = model.date_signed,
            rating = model.rating,
            rating_comment = model.rating_comment
        ) if model else None

    def delete_fobc01(self, id: int) -> bool:
        model = self.db.query(FOBC01Model).filter_by(id=id).first()
        if not model:
            return False
        
        file = self.db.query(FileModel).filter_by(id=model.file_id).first()
        if file:
            self.db.delete(file)
        self.db.delete(model)
        self.db.commit()
        return True

    def update_fobc01(self, fobc01_id: int, dto: FOBC01UpdateDTO) -> bool:
        try:
            model = self.db.query(FOBC01Model).filter_by(id=fobc01_id).first()
            if not model:
                return False

            model.hourometer = dto.hourometer
            model.observations = dto.observations
            model.reception_name = dto.reception_name

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            return False

    def get_list_fobc01_by_equipment_id(self, equipment_id: int) -> List[FOBC01]:
        models = self.db.query(FOBC01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOBC01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                date_created = model.date_created,
                hourometer = model.hourometer,
                observations = model.observations,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                rating = model.rating,
                rating_comment = model.rating_comment
            )
            for model in models
        ]

    def get_list_fobc01_table(self, equipment_id: int) -> List[FOBC01TableRowDTO]:
        models = self.db.query(FOBC01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOBC01Model.id)).all()
        
        if not models:
            return []
        
        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else 'N/A'
            return 'N/A'
        
        return [
            FOBC01TableRowDTO(
                id=m.id,
                file_id=m.file.folio if m.file else None, 
                date_created=m.date_created,
                observations = m.observations,
                employee_name=get_full_name(m.employee),
                status=m.status
            )
            for m in models
        ]

    def sign_fobc01(self, id: int, dto: FOBC01SignatureDTO) -> bool:
        try:
            model = self.db.query(FOBC01Model).filter_by(id=id).first()
            if not model:
                return False

            model.status = dto.status
            model.date_signed = dto.date_signed
            model.rating = dto.rating
            model.rating_comment = dto.rating_comment

            self.db.commit()
            self.db.refresh(model)
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id and dto.status == "Cerrado":
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOBC01] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            return False
            


