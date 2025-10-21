from mainContext.domain.models.Formats.fo_em_01 import FOEM01

from mainContext.application.ports.Formats.fo_em_01_repo import FOEM01Repo
from mainContext.application.dtos.Formats.fo_em_01_dto import FOEM01CreatedDTO, FOEM01TableRowDTO, FOEM01SignatureDTO, FOEM01UpdateDTO

from mainContext.infrastructure.models import Foem01 as FOEM01Model, Equipment as EquipmentModel, Foem01Materials as FOEM01MaterialModel, Files as FileModel
from mainContext.application.services.file_generator import FileService


from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

class FOEM01RepoImpl(FOEM01Repo):
    def __init__(self, db: Session):
        self.db = db
    
    def create_foem01(self, dto: FOEM01CreatedDTO) -> int:
        try:
            client_id = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first().client_id

            file_model = FileService.create_file(self.db, client_id)


            model = FOEM01Model(
                employee_id=dto.employee_id,
                equipment_id=dto.equipment_id,
                client_id = client_id,
                file_id = file_model.id,
                date_created=dto.date_created,
                status=dto.status,
                hourometer=0.0,
                reception_name="",
                signature_path="",
                date_signed=None
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            if model.id is None:
                raise Exception("Error al registrar FO-EM-01 en la base de datos")
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al registrar FO-EM-01 en la base de datos: {str(e)}")

    def get_foem01_by_id(self, id: int) -> FOEM01:
        model = self.db.query(FOEM01Model).filter_by(id=id).first()
        return FOEM01(
            id = model.id,
            employee = model.employee,
            equipment = model.equipment,
            client = model.client,
            file=model.file,
            date_created = model.date_created,
            hourometer = model.hourometer,
            status = model.status,
            reception_name = model.reception_name,
            signature_path = model.signature_path,
            date_signed = model.date_signed,
            materials = model.foem01_materials
        ) if model else None

    def delete_foem01(self, id: int) -> bool:
        model = self.db.query(FOEM01Model).filter_by(id=id).first()
        if not model:
            return False
        materials = self.db.query(FOEM01MaterialModel).filter_by(foem01_id=id).all()
        for material in materials:
            self.db.delete(material)

        file = self.db.query(FileModel).filter_by(id=model.file_id).first()
        if file:
            self.db.delete(file)
        self.db.delete(model)
        self.db.commit()
        return True

    def update_foem01(self, foem01_id: int, dto: FOEM01UpdateDTO) -> bool:
        try:
            model = self.db.query(FOEM01Model).filter_by(id=foem01_id).first()
            if not model:
                return False

            model.hourometer = dto.hourometer
            model.reception_name = dto.reception_name

            existing_materials = model.foem01_materials
            incoming_materials = dto.foem01_materials

            for i, incoming in enumerate(incoming_materials):
                if i < len(existing_materials):
                    # Actualiza material existente
                    existing = existing_materials[i]
                    existing.amount = incoming.amount
                    existing.um = incoming.um
                    existing.part_number = incoming.part_number
                    existing.description = incoming.description
                else:
                    # Crea nuevo material
                    new_material = FOEM01MaterialModel(
                        foem01_id=model.id,
                        amount=incoming.amount,
                        um=incoming.um,
                        part_number=incoming.part_number,
                        description=incoming.description
                    )
                    self.db.add(new_material)

            # Elimina materiales sobrantes
            if len(existing_materials) > len(incoming_materials):
                for material in existing_materials[len(incoming_materials):]:
                    self.db.delete(material)

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            return False

    def get_list_foem01_by_equipment_id(self, equipment_id: int) -> List[FOEM01]:
        models = self.db.query(FOEM01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOEM01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                date_created = model.date_created,
                hourometer = model.hourometer,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                materials = model.foem01_materials
            )
            for model in models
        ]

    def get_list_foem01_table(self, equipment_id: int) -> List[FOEM01TableRowDTO]:
        models = self.db.query(FOEM01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOEM01Model.id)).all()
        
        if not models:
            return []
        
        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else 'N/A'
            return 'N/A'
        
        return [
            FOEM01TableRowDTO(
                id=m.id,
                # Se valida m.file para obtener el folio
                file_id=m.file.folio if m.file else None, 
                date_created=m.date_created,
                # Se valida m.employee para obtener el nombre completo
                employee_name=get_full_name(m.employee),
                status=m.status
            )
            for m in models
        ]

    def sign_foem01(self, id: int, dto: FOEM01SignatureDTO) -> bool:
        try:
            model = self.db.query(FOEM01Model).filter_by(id=id).first()
            if not model:
                return False

            model.status = dto.status
            model.date_signed = dto.date_signed

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            return False
        
    