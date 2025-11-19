from mainContext.application.ports.Formats.fo_cr_02_repo import FOCR02Repo
from mainContext.application.dtos.Formats.fo_cr_02_dto import (
    CreateFOCR02DTO, UpdateFOCR02DTO, FOCR02SignatureDTO, FOCR02TableRowDTO, FOCRAddEquipmentDTO
)
from mainContext.domain.models.Formats.fo_cr_02 import FOCR02
from mainContext.application.services.file_generator import FileService

from mainContext.infrastructure.models import (
    Focr02 as FOCR02Model,
    FocrAddEquipment as FOCRAddEquipmentModel,
    Employees as EmployeesModel,
    Equipment as EquipmentModel,
    Clients as ClientsModel
)

from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import date, datetime
from sqlalchemy.exc import SQLAlchemyError

import os
import base64
import glob

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_PATH)))

SIGNATURE_PATH = os.path.join(MAIN_CONTEXT_ROOT, 'static', 'img', 'signatures', 'fo-cr-02')
SIGNATURE_BASE_URL = '/static/img/signatures/fo-cr-02'
os.makedirs(SIGNATURE_PATH, exist_ok=True)


class FOCR02RepoImpl(FOCR02Repo):
    def __init__(self, db: Session):
        self.db = db
    
    def _delete_existing_signature(self, model_id: int, save_dir: str):
        """Elimina la firma anterior si existe"""
        prefix = f"focr02-{model_id}"
        pattern = os.path.join(save_dir, f"{prefix}*.png")
        for file_path in glob.glob(pattern):
            os.remove(file_path)
    
    def _save_signature(self, model_id: int, signature_base64: str, save_dir: str) -> str:
        """Guarda la firma en base64 como PNG"""
        try:
            self._delete_existing_signature(model_id, save_dir)
            try:
                header, data = signature_base64.split(",", 1)
            except ValueError:
                data = signature_base64
            image_data = base64.b64decode(data)
            
            filename = f"focr02-{model_id}.png"
            file_path = os.path.join(save_dir, filename)
            
            with open(file_path, "wb") as f:
                f.write(image_data)
                
            return f"{SIGNATURE_BASE_URL}/{filename}"
        except Exception as e:
            print(f"Error al guardar la firma: {e}")
            return None
    
    def create_focr02(self, dto: CreateFOCR02DTO) -> int:
        try:
            # Crear el archivo mediante FileService
            file = FileService.create_file(self.db, client_id=dto.client_id, status="Abierto")
            
            # Actualizar el client_id del equipamiento
            equipment = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first()
            if equipment:
                equipment.client_id = dto.client_id
            
            model = FOCR02Model(
                client_id=dto.client_id,
                equipment_id=dto.equipment_id,
                employee_id=dto.employee_id,
                file_id=file.id,
                additional_equipment_id=None,  # Se añade en update
                date_created=datetime.now(),
                status="Abierto"
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar FOCR02 en la base de datos")
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al registrar FOCR02: {str(e)}")
    
    def get_focr02_by_id(self, id: int):
        try:
            model = self.db.query(FOCR02Model).options(
                joinedload(FOCR02Model.employee),
                joinedload(FOCR02Model.equipment),
                joinedload(FOCR02Model.client),
                joinedload(FOCR02Model.additional_equipment)
            ).filter_by(id=id).first()
            
            if not model:
                return None
            
            # Retornar como diccionario para que Pydantic lo valide correctamente
            return {
                "id": model.id,
                "client": {
                    "id": model.client.id,
                    "name": model.client.name
                } if model.client else None,
                "employee": {
                    "id": model.employee.id,
                    "name": model.employee.name,
                    "lastname": model.employee.lastname
                } if model.employee else None,
                "equipment": {
                    "id": model.equipment.id,
                    "model": model.equipment.model
                } if model.equipment else None,
                "file_id": model.file_id,
                "focr_add_equipment": {
                    "id": model.additional_equipment.id,
                    "equipment": model.additional_equipment.equipment,
                    "brand": model.additional_equipment.brand,
                    "model": model.additional_equipment.model,
                    "serial_number": model.additional_equipment.serial_number,
                    "equipment_type": model.additional_equipment.equipment_type,
                    "economic_number": model.additional_equipment.economic_number,
                    "capability": model.additional_equipment.capability,
                    "addition": model.additional_equipment.addition
                } if model.additional_equipment else None,
                "reception_name": model.reception_name,
                "date_created": model.date_created.date() if model.date_created else None,
                "status": model.status,
                "signature_path": model.signature_path,
                "date_signed": model.date_signed.date() if model.date_signed else None
            }
        except Exception as e:
            raise Exception(f"Error al obtener FOCR02: {str(e)}")
    
    def get_focr02_table(self) -> List[FOCR02TableRowDTO]:
        try:
            models = self.db.query(FOCR02Model).options(
                joinedload(FOCR02Model.employee),
                joinedload(FOCR02Model.equipment)
            ).all()
            
            if not models:
                return []
            
            return [
                FOCR02TableRowDTO(
                    id=m.id,
                    status=m.status,
                    equipment_name=m.equipment.model if m.equipment else "",
                    employee_name=f"{m.employee.name} {m.employee.lastname}" if m.employee else "",
                    date_created=m.date_created.date() if m.date_created else None
                )
                for m in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener tabla FOCR02: {str(e)}")
    
    def update_focr02(self, id: int, dto: UpdateFOCR02DTO) -> bool:
        try:
            model = self.db.query(FOCR02Model).filter_by(id=id).first()
            if not model:
                return False
            
            if dto.equipment_id:
                model.equipment_id = dto.equipment_id
            if dto.employee_id:
                model.employee_id = dto.employee_id
            if dto.reception_name:
                model.reception_name = dto.reception_name
            
            # Manejar additional_equipment
            if dto.additional_equipment:
                # Buscar o crear el equipo adicional
                existing_add_eq = self.db.query(FOCRAddEquipmentModel).filter(
                    FOCRAddEquipmentModel.equipment == dto.additional_equipment.equipment,
                    FOCRAddEquipmentModel.serial_number == dto.additional_equipment.serial_number
                ).first()
                
                if existing_add_eq:
                    # Usar el existente
                    model.additional_equipment_id = existing_add_eq.id
                else:
                    # Crear uno nuevo
                    new_add_eq = FOCRAddEquipmentModel(
                        equipment=dto.additional_equipment.equipment,
                        brand=dto.additional_equipment.brand,
                        model=dto.additional_equipment.model,
                        serial_number=dto.additional_equipment.serial_number,
                        equipment_type=dto.additional_equipment.equipment_type,
                        economic_number=dto.additional_equipment.economic_number,
                        capability=dto.additional_equipment.capability,
                        addition=dto.additional_equipment.addition
                    )
                    self.db.add(new_add_eq)
                    self.db.flush()
                    model.additional_equipment_id = new_add_eq.id
            
            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar FOCR02: {str(e)}")
    
    def delete_focr02(self, id: int) -> bool:
        try:
            model = self.db.query(FOCR02Model).filter_by(id=id).first()
            if not model:
                return False
            
            # Eliminar firma si existe
            if model.signature_path:
                self._delete_existing_signature(id, SIGNATURE_PATH)
            
            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar FOCR02: {str(e)}")
    
    def sign_focr02(self, id: int, dto: FOCR02SignatureDTO) -> bool:
        try:
            model = self.db.query(FOCR02Model).filter_by(id=id).first()
            if not model:
                return False
            
            signature_path = self._save_signature(
                model_id=id,
                signature_base64=dto.signature_base64,
                save_dir=SIGNATURE_PATH
            )
            if signature_path:
                model.signature_path = signature_path
            else:
                raise Exception("Error al guardar la firma.")
            
            # Cerrar documento automáticamente
            model.status = "Cerrado"
            model.date_signed = datetime.now()
            
            self.db.commit()
            self.db.refresh(model)
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id:
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOCR02] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al firmar FOCR02: {str(e)}")
    
    def get_focr_additional_equipment(self) -> List[FOCRAddEquipmentDTO]:
        try:
            models = self.db.query(FOCRAddEquipmentModel).all()
            
            if not models:
                return []
            
            return [
                FOCRAddEquipmentDTO(
                    equipment=m.equipment,
                    brand=m.brand,
                    model=m.model,
                    serial_number=m.serial_number,
                    equipment_type=m.equipment_type,
                    economic_number=m.economic_number,
                    capability=m.capability,
                    addition=m.addition
                )
                for m in models
            ]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener equipos adicionales: {str(e)}")
