from mainContext.domain.models.Formats.fo_pp_02 import FOPP02

from mainContext.application.ports.Formats.fo_pp_02_repo import FOPP02Repo
from mainContext.application.dtos.Formats.fo_pp_02_dto import (
    FOPP02CreateDTO,
    FOPP02UpdateDTO,
    FOPP02SignatureDTO,
    FOPP02TableRowDTO,
    GetFOPP02ByFOPCDTO,
    FOPP02ByFOPCResponseDTO
)

from mainContext.infrastructure.models import (
    Fopp02 as FOPP02Model,
    Fopc02 as FOPC02Model,
    ClientEquipmentProperty as ClientEquipmentPropertyModel,
    Equipment as EquipmentModel,
    Employees as EmployeeModel
)

from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

import os
import base64
import glob

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)))

# Paths for Signatures
SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-pp-02")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-pp-02"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)


class FOPP02RepoImpl(FOPP02Repo):
    def __init__(self, db: Session):
        self.db = db

    def _delete_existing_signature(self, model_id: int, signature_type: str):
        """
        Elimina firma existente
        signature_type: 'TecDep', 'CliDep', 'TecDel', 'CliDel'
        """
        try:
            search_pattern = os.path.join(SIGNATURE_SAVE_DIR, f"fopp02{signature_type}-{model_id}.*")
            for f in glob.glob(search_pattern):
                os.remove(f)
        except Exception as e:
            print(f"Error al eliminar firma {signature_type} para ID {model_id}: {e}")
            raise

    def _save_signature(self, base64_string: str, model_id: int, signature_type: str) -> str | None:
        """
        Guarda firma en base64
        signature_type: 'TecDep', 'CliDep', 'TecDel', 'CliDel'
        """
        try:
            try:
                header, data = base64_string.split(",", 1)
            except ValueError:
                data = base64_string

            image_data = base64.b64decode(data)
            file_ext = ".png"

            filename = f"fopp02{signature_type}-{model_id}{file_ext}"
            save_path = os.path.join(SIGNATURE_SAVE_DIR, filename)

            with open(save_path, "wb") as f:
                f.write(image_data)

            public_url = f"{SIGNATURE_URL_BASE}/{filename}"
            return public_url

        except Exception as e:
            print(f"Error al guardar firma {signature_type}: {e}")
            return None

    def create_fopp02(self, dto: FOPP02CreateDTO) -> int:
        try:
            # Obtener file_id del FOPC02 si existe
            fopc = self.db.query(FOPC02Model).filter_by(id=dto.fopc_id).first()
            file_id = fopc.file_id if fopc else dto.file_id

            model = FOPP02Model(
                employee_id=dto.employee_id,
                fopc_id=dto.fopc_id,
                property_id=dto.property_id,
                status=dto.status,
                file_id=file_id,
                date_created=datetime.now(),
                departure_date=None,
                departure_description=None,
                delivery_date=None,
                delivery_description=None,
                departure_signature_path=None,
                departure_employee_signature_path=None,
                delivery_signature_path=None,
                delivery_employee_signature_path=None,
                name_auth_departure=None,
                name_delivery=None,
                observations=None,
                vendor_id=None
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)

            if not model.id or model.id <= 0:
                raise Exception("Error al registrar FOPP02 en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear FOPP02: {str(e)}")

    def get_fopp02_by_id(self, id: int) -> FOPP02:
        try:
            model = (
                self.db.query(FOPP02Model)
                .options(
                    joinedload(FOPP02Model.employee),
                    joinedload(FOPP02Model.fopc),
                    joinedload(FOPP02Model.property),
                    joinedload(FOPP02Model.vendor)
                )
                .filter_by(id=id)
                .first()
            )
            
            if not model:
                return None
            
            return FOPP02(
                id=model.id,
                vendor_id=model.vendor_id,
                property_id=model.property_id,
                departure_date=model.departure_date,
                departure_description=model.departure_description,
                delivery_date=model.delivery_date,
                delivery_description=model.delivery_description,
                departure_signature_path=model.departure_signature_path,
                departure_employee_signature_path=model.departure_employee_signature_path,
                delivery_signature_path=model.delivery_signature_path,
                delivery_employee_signature_path=model.delivery_employee_signature_path,
                observations=model.observations,
                employee_id=model.employee_id,
                status=model.status,
                name_auth_departure=model.name_auth_departure,
                name_delivery=model.name_delivery,
                fopc_id=model.fopc_id,
                file_id=model.file_id,
                date_created=model.date_created,
                employee=model.employee,
                fopc=model.fopc,
                property=model.property,
                vendor=model.vendor
            )
        except Exception as e:
            raise Exception(f"Error al obtener FOPP02: {str(e)}")

    def delete_fopp02(self, id: int) -> bool:
        try:
            model = self.db.query(FOPP02Model).filter_by(id=id).first()
            if not model:
                return False

            # Eliminar todas las firmas
            self._delete_existing_signature(model.id, "TecDep")
            self._delete_existing_signature(model.id, "CliDep")
            self._delete_existing_signature(model.id, "TecDel")
            self._delete_existing_signature(model.id, "CliDel")

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar FOPP02: {str(e)}")

    def update_fopp02(self, id: int, dto: FOPP02UpdateDTO) -> bool:
        try:
            model = self.db.query(FOPP02Model).filter_by(id=id).first()
            if not model:
                return False

            # Actualizar campos básicos
            if dto.departure_date is not None:
                model.departure_date = dto.departure_date
            if dto.departure_description is not None:
                model.departure_description = dto.departure_description
            if dto.delivery_date is not None:
                model.delivery_date = dto.delivery_date
            if dto.delivery_description is not None:
                model.delivery_description = dto.delivery_description
            if dto.name_auth_departure is not None:
                model.name_auth_departure = dto.name_auth_departure
            if dto.name_delivery is not None:
                model.name_delivery = dto.name_delivery
            if dto.observations is not None:
                model.observations = dto.observations

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar FOPP02: {str(e)}")

    def get_list_fopp02_by_fopc_id(self, fopc_id: int) -> List[FOPP02]:
        try:
            models = (
                self.db.query(FOPP02Model)
                .filter_by(fopc_id=fopc_id)
                .options(
                    joinedload(FOPP02Model.employee),
                    joinedload(FOPP02Model.fopc),
                    joinedload(FOPP02Model.property),
                    joinedload(FOPP02Model.vendor)
                )
                .all()
            )
            
            return [
                FOPP02(
                    id=model.id,
                    vendor_id=model.vendor_id,
                    property_id=model.property_id,
                    departure_date=model.departure_date,
                    departure_description=model.departure_description,
                    delivery_date=model.delivery_date,
                    delivery_description=model.delivery_description,
                    departure_signature_path=model.departure_signature_path,
                    departure_employee_signature_path=model.departure_employee_signature_path,
                    delivery_signature_path=model.delivery_signature_path,
                    delivery_employee_signature_path=model.delivery_employee_signature_path,
                    observations=model.observations,
                    employee_id=model.employee_id,
                    status=model.status,
                    name_auth_departure=model.name_auth_departure,
                    name_delivery=model.name_delivery,
                    fopc_id=model.fopc_id,
                    file_id=model.file_id,
                    date_created=model.date_created,
                    employee=model.employee,
                    fopc=model.fopc,
                    property=model.property,
                    vendor=model.vendor
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener lista de FOPP02: {str(e)}")

    def get_list_fopp02_table(self, fopc_id: int) -> List[FOPP02TableRowDTO]:
        try:
            models = (
                self.db.query(FOPP02Model)
                .filter_by(fopc_id=fopc_id)
                .options(
                    joinedload(FOPP02Model.employee),
                    joinedload(FOPP02Model.property)
                )
                .order_by(desc(FOPP02Model.id))
                .all()
            )

            if not models:
                return []

            def get_full_name(employee):
                if employee:
                    full_name = f"{employee.name or ''} {employee.lastname or ''}".strip()
                    return full_name if full_name else 'N/A'
                return 'N/A'

            def get_equipment_name(property_obj):
                if property_obj:
                    brand = property_obj.brand or 'N/A'
                    model = property_obj.model or 'N/A'
                    return f"{brand} {model}"
                return 'N/A'

            return [
                FOPP02TableRowDTO(
                    id=m.id,
                    status=m.status or "N/A",
                    file=m.file_id or "N/A",
                    equipment_name=get_equipment_name(m.property),
                    employee_name=get_full_name(m.employee),
                    date_created=m.date_created or datetime.now()
                )
                for m in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener tabla de FOPP02: {str(e)}")

    def sign_fopp02_departure(self, id: int, dto: FOPP02SignatureDTO) -> bool:
        """
        Firma de salida (departure)
        - is_employee=True: firma del empleado (TecDep)
        - is_employee=False: firma del cliente (CliDep)
        """
        try:
            model = self.db.query(FOPP02Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.signature_base64:
                if dto.is_employee:
                    # Firma del empleado en departure
                    self._delete_existing_signature(model.id, "TecDep")
                    url = self._save_signature(dto.signature_base64, model.id, "TecDep")
                    if url:
                        model.departure_employee_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma TecDep para el ID {model.id}")
                else:
                    # Firma del cliente en departure
                    self._delete_existing_signature(model.id, "CliDep")
                    url = self._save_signature(dto.signature_base64, model.id, "CliDep")
                    if url:
                        model.departure_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma CliDep para el ID {model.id}")

            # Verificar si todas las firmas están completas para cerrar el documento
            if (model.departure_signature_path and 
                model.departure_employee_signature_path and 
                model.delivery_signature_path and 
                model.delivery_employee_signature_path):
                model.status = "Cerrado"

            self.db.commit()
            self.db.refresh(model)
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id and model.status == "Cerrado":
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOPP02] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except Exception as e:
            print(f"Error en la operación de firma departure, revirtiendo: {e}")
            self.db.rollback()
            return False

    def sign_fopp02_delivery(self, id: int, dto: FOPP02SignatureDTO) -> bool:
        """
        Firma de entrega (delivery)
        - is_employee=True: firma del empleado (TecDel)
        - is_employee=False: firma del cliente (CliDel)
        """
        try:
            model = self.db.query(FOPP02Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.signature_base64:
                if dto.is_employee:
                    # Firma del empleado en delivery
                    self._delete_existing_signature(model.id, "TecDel")
                    url = self._save_signature(dto.signature_base64, model.id, "TecDel")
                    if url:
                        model.delivery_employee_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma TecDel para el ID {model.id}")
                else:
                    # Firma del cliente en delivery
                    self._delete_existing_signature(model.id, "CliDel")
                    url = self._save_signature(dto.signature_base64, model.id, "CliDel")
                    if url:
                        model.delivery_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma CliDel para el ID {model.id}")

            # Verificar si todas las firmas están completas para cerrar el documento
            if (model.departure_signature_path and 
                model.departure_employee_signature_path and 
                model.delivery_signature_path and 
                model.delivery_employee_signature_path):
                model.status = "Cerrado"

            self.db.commit()
            self.db.refresh(model)
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id and model.status == "Cerrado":
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOPP02] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except Exception as e:
            print(f"Error en la operación de firma delivery, revirtiendo: {e}")
            self.db.rollback()
            return False

    def get_fopp02_by_fopc(self, dto: GetFOPP02ByFOPCDTO) -> List[FOPP02ByFOPCResponseDTO]:
        """
        Obtiene todos los FOPP02 asociados a un FOPC02
        """
        try:
            models = (
                self.db.query(FOPP02Model)
                .filter_by(fopc_id=dto.fopc_id)
                .all()
            )

            return [
                FOPP02ByFOPCResponseDTO(
                    id=model.id,
                    date_created=model.date_created,
                    status=model.status,
                    file_id=model.file_id
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener FOPP02 por FOPC: {str(e)}")
