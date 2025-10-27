from mainContext.domain.models.Formats.fo_le_01 import FOLE01, FOLE01Service
from mainContext.domain.models.Formats.Service import Service
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment

from mainContext.application.ports.Formats.fo_le_01_repo import FOLE01Repo
from mainContext.application.dtos.Formats.fo_le_01_dto import FOLE01CreateDTO, FOLE01UpdateDTO, FOLE01SignatureDTO, FOLE01TableRowDTO, FOLE01ServiceDTO

from mainContext.infrastructure.models import Fole01Services as FOLE01ServiceModel, Fole01 as FOLE01Model, Equipment as EquipmentModel

from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

import os
import base64
import glob

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)))

# Paths for Evidence
EVIDENCE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "evidence", "fo-le-01")
EVIDENCE_URL_BASE = "/static/img/evidence/fo-le-01"
os.makedirs(EVIDENCE_SAVE_DIR, exist_ok=True)

# Paths for Signatures
SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-le-01")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-le-01"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)


class FOLE01RepoImpl(FOLE01Repo):
    def __init__(self, db: Session):
        self.db = db

    def create_fole01(self, dto: FOLE01CreateDTO) -> int:
        try:
            client_id = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first().client_id
            model = FOLE01Model(
                employee_id=dto.employee_id,
                equipment_id=dto.equipment_id,
                client_id=client_id,
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
            if model.id is None:
                raise Exception("Error al registrar FOLE01 en la base de datos")
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al registrar FOLE01 en la base de datos: {str(e)}")

    def get_fole01_by_id(self, id: int) -> FOLE01:
        model = self.db.query(FOLE01Model).filter_by(id=id).first()
        return FOLE01(
            id=model.id,
            employee=model.employee,
            equipment=model.equipment,
            client=model.client,
            horometer=model.hourometer,
            technical_action=model.technical_action,
            status=model.status,
            reception_name=model.reception_name,
            signature_path=model.signature_path,
            date_signed=model.date_signed,
            date_created=model.date_created,
            rating=model.rating,
            rating_comment=model.rating_comment,
            services=model.fole01_services
        ) if model else None

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

    def _delete_existing_photos(self, model_id: int, save_dir: str):
        try:
            search_pattern = os.path.join(save_dir, f"{model_id}-*")
            for f in glob.glob(search_pattern):
                os.remove(f)
        except Exception as e:
            print(f"Error al eliminar fotos antiguas para ID {model_id}: {e}")
            raise

    def _save_base64_image(self, base64_string: str, model_id: int, photo_index: int, save_dir: str, url_base: str, is_signature: bool = False) -> str | None:
        try:
            try:
                header, data = base64_string.split(",", 1)
            except ValueError:
                data = base64_string

            image_data = base64.b64decode(data)
            
            file_ext = ".jpg"
            if "header" in locals():
                if "image/png" in header:
                    file_ext = ".png"
                elif "image/jpeg" in header:
                    file_ext = ".jpeg"
            if is_signature:
                file_ext = ".png"

            filename = f"fole-{model_id}{file_ext}" if is_signature else f"{model_id}-{photo_index}{file_ext}"
            save_path = os.path.join(save_dir, filename)

            with open(save_path, "wb") as f:
                f.write(image_data)

            public_url = f"{url_base}/{filename}"
            return public_url

        except Exception as e:
            print(f"Error al guardar imagen Base64: {e}")
            return None

    def update_fole01(self, id: int, dto: FOLE01UpdateDTO) -> bool:
        try:
            model = self.db.query(FOLE01Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.evidence_photos_base64:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR)
                for index, b64_photo in enumerate(dto.evidence_photos_base64, start=1):
                    url = self._save_base64_image(b64_photo, model.id, index, EVIDENCE_SAVE_DIR, EVIDENCE_URL_BASE)
                    if not url:
                        raise Exception(f"Fallo crítico al guardar la imagen #{index} para el ID {model.id}")
            elif dto.evidence_photos_base64 == []:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR)

            model.hourometer = dto.hourometer
            model.technical_action = dto.technical_action
            model.reception_name = dto.reception_name

            existing_services = model.fole01_services
            incoming_services = dto.fole01_services

            for i, incoming in enumerate(incoming_services):
                if i < len(existing_services):
                    existing = existing_services[i]
                    existing.service_id = incoming.service_id
                    existing.diagnose_description = incoming.diagnose_description
                    existing.description_service = incoming.description_service
                    existing.priority = incoming.priority
                else:
                    new_service = FOLE01ServiceModel(
                        fole01_id=model.id,
                        service_id=incoming.service_id,
                        diagnose_description=incoming.diagnose_description,
                        description_service=incoming.description_service,
                        priority=incoming.priority
                    )
                    self.db.add(new_service)

            if len(existing_services) > len(incoming_services):
                for service in existing_services[len(incoming_services):]:
                    self.db.delete(service)

            self.db.commit()
            self.db.refresh(model)
            return True
        
        except Exception as e:
            print(f"Error en la operación, revirtiendo: {e}")
            self.db.rollback()
            return False

    def get_list_fole01_by_equipment_id(self, equipment_id: int) -> List[FOLE01]:
        models = self.db.query(FOLE01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOLE01(
                id=model.id,
                employee=model.employee,
                equipment=model.equipment,
                client=model.client,
                horometer=model.hourometer,
                technical_action=model.technical_action,
                status=model.status,
                reception_name=model.reception_name,
                signature_path=model.signature_path,
                date_signed=model.date_signed,
                date_created=model.date_created,
                rating=model.rating,
                rating_comment=model.rating_comment,
                services=model.fole01_services
            )
            for model in models
        ]

    def get_list_fole01_table(self, equipment_id: int) -> List[FOLE01TableRowDTO]:
        models = self.db.query(FOLE01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOLE01Model.id)).all()
        if not models:
            return []

        results = []
        for m in models:
            employee_name = "No asignado"
            if m.employee:
                parts = [m.employee.name, m.employee.lastname]
                employee_name = " ".join(p for p in parts if p) or "No asignado"

            economic_number = "N/A"
            if m.equipment:
                economic_number = m.equipment.economic_number or "N/A"

            codes = [s.service.code for s in m.fole01_services if s.service]

            results.append(
                FOLE01TableRowDTO(
                    id=m.id,
                    economic_number=economic_number,
                    date_created=m.date_created,
                    codes=codes,
                    employee_name=employee_name,
                    status=m.status
                )
            )
        return results

    def sign_fole01(self, id: int, dto: FOLE01SignatureDTO) -> bool:
        try:
            model = self.db.query(FOLE01Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.signature_base64:
                self._delete_existing_photos(model.id, SIGNATURE_SAVE_DIR)
                url = self._save_base64_image(dto.signature_base64, model.id, 0, SIGNATURE_SAVE_DIR, SIGNATURE_URL_BASE, is_signature=True)
                if url:
                    model.signature_path = url
                else:
                    raise Exception(f"Fallo crítico al guardar la firma para el ID {model.id}")

            model.status = dto.status
            model.date_signed = dto.date_signed
            model.rating = dto.rating
            model.rating_comment = dto.rating_comment

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            print(f"Error en la operación de firma, revirtiendo: {e}")
            self.db.rollback()
            return False


