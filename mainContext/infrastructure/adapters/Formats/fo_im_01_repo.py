from mainContext.domain.models.Formats.fo_im_01 import FOIM01

from mainContext.application.ports.Formats.fo_im_01_repo import FOIM01Repo
from mainContext.application.dtos.Formats.fo_im_01_dto import FOIM01CreateDTO, FOIM01UpdateDTO, FOIM01SignatureDTO, FOIM01TableRowDTO

from mainContext.infrastructure.models import Foim01Answers as FOIM01AnswerModel, Foim01 as FOIM01Model, Equipment as EquipmentModel

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

# Paths for Signatures
SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-im-01")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-im-01"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)

class FOIM01RepoImpl(FOIM01Repo):
    def __init__(self, db: Session):
        self.db = db

    def _delete_existing_photos(self, model_id: int, save_dir: str, is_signature: bool = False):
        try:
            if is_signature:
                search_pattern = os.path.join(save_dir, f"foIM-{model_id}.*")

            for f in glob.glob(search_pattern):
                os.remove(f)
        except Exception as e:
            print(f"Error al eliminar fotos antiguas para ID {model_id}: {e}")
            raise

    def _save_base64_image(self, base64_string: str, model_id: int, save_dir: str, url_base: str, is_signature: bool = False) -> str | None:
        try:
            try:
                header, data = base64_string.split(",", 1)
            except ValueError:
                data = base64_string

            image_data = base64.b64decode(data)
            
            file_ext = ".png"

            if is_signature:
                filename = f"foIM-{model_id}{file_ext}"

            save_path = os.path.join(save_dir, filename)

            with open(save_path, "wb") as f:
                f.write(image_data)

            public_url = f"{url_base}/{filename}"
            return public_url

        except Exception as e:
            print(f"Error al guardar imagen Base64: {e}")
            return None
    
    def create_foim01(self, dto: FOIM01CreateDTO) -> int:
        try: 
            client_id = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first().client_id

            model = FOIM01Model(
                employee_id=dto.employee_id,
                equipment_id=dto.equipment_id,
                client_id = client_id,
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
                raise Exception("Error al registrar FO-IM-01 en la base de datos")
            return model.id
        except Exception as e: 
            self.db.rollback()
            raise Exception(f"Error al registrar FO-IM-01 en la base de datos: {str(e)}") 
    
    def get_foim01_by_id(self, id: int) -> FOIM01:
        model = self.db.query(FOIM01Model).filter_by(id=id).first()
        return FOIM01(
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
                rating_comment = model.rating_comment,
                answers = model.foim01_answers,
            )if model else None

    def delete_foim01(self, id: int) -> bool:
        model = self.db.query(FOIM01Model).filter_by(id=id).first()
        if not model:
            return False

        self._delete_existing_photos(model.id, SIGNATURE_SAVE_DIR, is_signature=True)

        answers = self.db.query(FOIM01AnswerModel).filter_by(foim01_id=id).all()
        for answer in answers:
            self.db.delete(answer)
        self.db.delete(model)
        self.db.commit()
        return True
    
    def update_foim01(self, id: int, dto: FOIM01UpdateDTO) -> bool:
        try:
            model = self.db.query(FOIM01Model).filter_by(id=id).first()
            if not model:
                return None

            model.hourometer = dto.hourometer
            model.observations = dto.observations
            model.reception_name = dto.reception_name

            existing_answers = model.foim01_answers
            incoming_answers = dto.foim01_answers

            for i, incoming in enumerate(incoming_answers):
                if i < len(existing_answers):
                    # Actualiza servicio existente
                    existing = existing_answers[i]
                    existing.foim_question_id = incoming.foim_question_id
                else:
                    # Crea nuevo servicio
                    new_service = FOIM01AnswerModel(
                        foim01_id=model.id,
                        service_id=incoming.foim_question_id,
                    )
                    self.db.add(new_service)

            # Elimina servicios sobrantes
            if len(existing_answers) > len(incoming_answers):
                for answer in existing_answers[len(incoming_answers):]:
                    self.db.delete(answer)

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e: 
            self.db.rollback()
            return False
        
    def get_list_foim01_by_equipment_id(self, equipment_id: int) -> List[FOIM01]:
        models = self.db.query(FOIM01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOIM01(
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
                answers= model.foim01_answers
            ) 
            for model in models
        ]
    
    def get_list_foim01_table(self, equipment_id: int) -> List[FOIM01TableRowDTO]:
        models = self.db.query(FOIM01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOIM01Model.id)).all()
        if not models:
            return []

        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else 'N/A'
            return 'N/A'

        return [
            FOIM01TableRowDTO(
                id=m.id,
                date_created=m.date_created,
                observations = m.observations,
                employee_name=get_full_name(m.employee),
                status=m.status
            )
            for m in models
        ]    
    
    def sign_foim01(self, id: int, dto: FOIM01SignatureDTO) -> bool:
        try: 
            model = self.db.query(FOIM01Model).filter_by(id=id).first()
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
            return True
        except Exception as e:
            print(f"Error en la operación de firma, revirtiendo: {e}")
            self.db.rollback()
            return False
