from mainContext.domain.models.Formats.fo_sp_01 import FOSP01

from mainContext.application.ports.Formats.fo_sp_01_repo import FOSP01Repo
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO, FOSP01UpdateDTO, FOSP01SignatureDTO, FOSP01TableRowDTO

from mainContext.infrastructure.models import Fosp01Services as FOSP01ServiceModel, Fosp01 as FOSP01Model, Files as FileModel, Equipment as EquipmentModel
from mainContext.infrastructure.adapters.Formats.file_cleanup_helper import cleanup_file_if_orphaned

from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from mainContext.application.services.file_generator import FileService

import os
import base64
import glob

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)))

# Paths for Evidence
EVIDENCE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "evidence", "fo-sp-01")
EVIDENCE_URL_BASE = "/static/img/evidence/fo-sp-01"
os.makedirs(EVIDENCE_SAVE_DIR, exist_ok=True)

# Paths for Signatures
SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-sp-01")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-sp-01"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)


class FOSP01RepoImpl(FOSP01Repo):
    def __init__(self, db: Session):
        self.db = db

    def _delete_existing_photos(self, model_id: int, save_dir: str, photo_type: str = None, is_signature: bool = False):
        try:
            if is_signature:
                search_pattern = os.path.join(save_dir, f"fosp-{model_id}.*")
            elif photo_type:
                search_pattern = os.path.join(save_dir, f"{model_id}-fosp-{photo_type}-*")
            else:
                search_pattern = os.path.join(save_dir, f"{model_id}-*")

            for f in glob.glob(search_pattern):
                os.remove(f)
        except Exception as e:
            print(f"Error al eliminar fotos antiguas para ID {model_id}: {e}")
            raise

    def _save_base64_image(self, base64_string: str, model_id: int, save_dir: str, url_base: str, photo_index: int = 0, photo_type: str = None, is_signature: bool = False) -> str | None:
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

            if is_signature:
                filename = f"fosp-{model_id}{file_ext}"
            elif photo_type:
                filename = f"{model_id}-fosp-{photo_type}-{photo_index}{file_ext}"
            else:
                filename = f"{model_id}-{photo_index}{file_ext}"

            save_path = os.path.join(save_dir, filename)

            with open(save_path, "wb") as f:
                f.write(image_data)

            public_url = f"{url_base}/{filename}"
            return public_url

        except Exception as e:
            print(f"Error al guardar imagen Base64: {e}")
            return None

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
                rating_comment="",
                GC = dto.GC
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
                fopc_services_id= model.fopc_services_id,
                GC  = model.GC
            )if model else None
    
    def delete_fosp01(self, id: int) -> bool:
        model = self.db.query(FOSP01Model).filter_by(id=id).first()
        if not model:
            return False
        
        self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR, photo_type="antes")
        self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR, photo_type="despues")
        self._delete_existing_photos(model.id, SIGNATURE_SAVE_DIR, is_signature=True)

        services = self.db.query(FOSP01ServiceModel).filter_by(fosp01_id=id).all()
        for service in services:
            self.db.delete(service)
        
        file_id = model.file_id
        self.db.delete(model)
        self.db.flush()
        
        # Eliminar file solo si no hay otros documentos relacionados
        cleanup_file_if_orphaned(self.db, file_id)
        
        self.db.commit()
        return True
    
    def update_fosp01(self, id: int, dto: FOSP01UpdateDTO) -> bool:
        try:
            model = self.db.query(FOSP01Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.evidence_photos_before_base64:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR, "antes")
                for index, b64_photo in enumerate(dto.evidence_photos_before_base64, start=1):
                    url = self._save_base64_image(b64_photo, model.id, EVIDENCE_SAVE_DIR, EVIDENCE_URL_BASE, photo_index=index, photo_type="antes")
                    if not url:
                        raise Exception(f"Fallo crítico al guardar la imagen 'antes' #{index} para el ID {model.id}")
            elif dto.evidence_photos_before_base64 == []:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR, "antes")

            if dto.evidence_photos_after_base64:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR, "despues")
                for index, b64_photo in enumerate(dto.evidence_photos_after_base64, start=1):
                    url = self._save_base64_image(b64_photo, model.id, EVIDENCE_SAVE_DIR, EVIDENCE_URL_BASE, photo_index=index, photo_type="despues")
                    if not url:
                        raise Exception(f"Fallo crítico al guardar la imagen 'despues' #{index} para el ID {model.id}")
            elif dto.evidence_photos_after_base64 == []:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR, "despues")

            model.hourometer = dto.hourometer
            model.observations = dto.observations
            model.reception_name = dto.reception_name

            existing_services = model.fosp01_services
            incoming_services = dto.fosp01_services

            for i, incoming in enumerate(incoming_services):
                if i < len(existing_services):
                    existing = existing_services[i]
                    existing.service_id = incoming.service_id
                else:
                    new_service = FOSP01ServiceModel(
                        fosp01_id=model.id,
                        service_id=incoming.service_id,
                    )
                    self.db.add(new_service)

            if len(existing_services) > len(incoming_services):
                for service in existing_services[len(incoming_services):]:
                    self.db.delete(service)

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            print(f"Error en la operación de actualización, revirtiendo: {e}")
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
        
        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else 'N/A'
            return 'N/A'
        
        return [
            FOSP01TableRowDTO(
                id=m.id,
                file_id=m.file.folio if m.file else None, 
                date_created=m.date_created,
                observations = m.observations,
                codes=[s.service.code for s in m.fosp01_services],
                employee_name=get_full_name(m.employee),
                status=m.status
            )
            for m in models
        ]
    
    def sign_fosp01(self, id: int, dto: FOSP01SignatureDTO) -> bool:
        try: 
            model = self.db.query(FOSP01Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.signature_base64:
                self._delete_existing_photos(model.id, SIGNATURE_SAVE_DIR, is_signature=True)
                url = self._save_base64_image(dto.signature_base64, model.id, SIGNATURE_SAVE_DIR, SIGNATURE_URL_BASE, is_signature=True)
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
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id and dto.status == "Cerrado":
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOSP01] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except Exception as e:
            print(f"Error en la operación de firma, revirtiendo: {e}")
            self.db.rollback()
            return False