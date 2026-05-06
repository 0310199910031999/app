from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from typing import List

import base64
import glob
import os
import threading

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from mainContext.application.dtos.Formats.fo_em_01_1_dto import FOEM011CreateDTO, FOEM011TableRowDTO, FOEM011SignatureDTO, FOEM011UpdateDTO
from mainContext.application.ports.Formats.fo_em_01_1_repo import FOEM011Repo
from mainContext.application.services.file_generator import FileService
from mainContext.domain.models.Formats.fo_em_01_1 import FOEM011
from mainContext.infrastructure.adapters.Formats.file_cleanup_helper import cleanup_file_if_orphaned
from mainContext.infrastructure.models import Foem011 as FOEM011Model, Foem011Materials as FOEM011MaterialModel


CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)))

EVIDENCE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "evidence", "fo-em-01-1")
EVIDENCE_URL_BASE = "/static/img/evidence/fo-em-01-1"
os.makedirs(EVIDENCE_SAVE_DIR, exist_ok=True)

SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-em-01-1")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-em-01-1"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)


class FOEM011RepoImpl(FOEM011Repo):
    def __init__(self, db: Session):
        self.db = db

    def _delete_existing_photos(self, model_id: int, save_dir: str, is_signature: bool = False):
        try:
            if is_signature:
                search_pattern = os.path.join(save_dir, f"foEM-1-{model_id}.*")
            else:
                search_pattern = os.path.join(save_dir, f"{model_id}-*")

            for file_path in glob.glob(search_pattern):
                os.remove(file_path)
        except Exception as e:
            print(f"Error al eliminar fotos antiguas para ID {model_id}: {e}")
            raise

    def _save_base64_image(self, base64_string: str, model_id: int, save_dir: str, url_base: str, is_signature: bool = False, photo_index: int = 0) -> str | None:
        try:
            try:
                header, data = base64_string.split(",", 1)
            except ValueError:
                header = ""
                data = base64_string

            image_data = base64.b64decode(data)

            if is_signature:
                file_ext = ".png"
                filename = f"foEM-1-{model_id}{file_ext}"
            else:
                file_ext = ".jpg"
                if "image/png" in header:
                    file_ext = ".png"
                elif "image/jpeg" in header:
                    file_ext = ".jpeg"
                filename = f"{model_id}-{photo_index}{file_ext}"

            save_path = os.path.join(save_dir, filename)

            with open(save_path, "wb") as file_handle:
                file_handle.write(image_data)

            return f"{url_base}/{filename}"
        except Exception as e:
            print(f"Error al guardar imagen Base64: {e}")
            return None

    def _save_single_image_wrapper(self, args: tuple) -> tuple:
        b64_photo, model_id, index = args
        try:
            url = self._save_base64_image(b64_photo, model_id, EVIDENCE_SAVE_DIR, EVIDENCE_URL_BASE, photo_index=index)
            if not url:
                return (index, False, f"Fallo al guardar imagen #{index}")
            return (index, True, url)
        except Exception as e:
            return (index, False, str(e))

    def create_foem01_1(self, dto: FOEM011CreateDTO) -> int:
        try:
            file_model = FileService.create_file(self.db, dto.client_id)

            model = FOEM011Model(
                employee_id=dto.employee_id,
                client_id=dto.client_id,
                file_id=file_model.id if file_model else None,
                date_created=dto.date_created,
                status=dto.status,
                hourometer=0.0,
                reception_name="",
                signature_path="",
                date_signed=None,
                observations="",
                rating=None,
                rating_comment=None,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            if model.id is None:
                raise Exception("Error al registrar FO-EM-01_1 en la base de datos")
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al registrar FO-EM-01_1 en la base de datos: {str(e)}")

    def get_foem01_1_by_id(self, id: int) -> FOEM011:
        model = self.db.query(FOEM011Model).filter_by(id=id).first()
        if not model:
            return None

        evidence_pattern = os.path.join(EVIDENCE_SAVE_DIR, f"{model.id}-*")
        evidence_files = sorted(glob.glob(evidence_pattern))
        evidence_photos = [f"{EVIDENCE_URL_BASE}/{os.path.basename(file_path)}" for file_path in evidence_files]

        return FOEM011(
            id=model.id,
            employee=model.employee,
            file=model.file,
            client=model.client,
            date_created=model.date_created,
            hourometer=model.hourometer,
            status=model.status,
            reception_name=model.reception_name,
            signature_path=model.signature_path,
            date_signed=model.date_signed,
            materials=model.foem01_1_materials,
            observations=model.observations,
            rating=model.rating,
            rating_comment=model.rating_comment,
            evidence_photos=evidence_photos if evidence_photos else None,
        )

    def delete_foem01_1(self, id: int) -> bool:
        model = self.db.query(FOEM011Model).filter_by(id=id).first()
        if not model:
            return False

        self._delete_existing_photos(model.id, SIGNATURE_SAVE_DIR, is_signature=True)
        self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR)

        materials = self.db.query(FOEM011MaterialModel).filter_by(foem01_1_id=id).all()
        for material in materials:
            self.db.delete(material)

        file_id = model.file_id
        self.db.delete(model)
        self.db.flush()

        cleanup_file_if_orphaned(self.db, file_id)

        self.db.commit()
        return True

    def update_foem01_1(self, foem01_1_id: int, dto: FOEM011UpdateDTO) -> bool:
        try:
            model = self.db.query(FOEM011Model).filter_by(id=foem01_1_id).first()
            if not model:
                return False

            if dto.evidence_photos_base64:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR)

                image_tasks = [
                    (b64_photo, model.id, index)
                    for index, b64_photo in enumerate(dto.evidence_photos_base64, start=1)
                ]

                with ThreadPoolExecutor(max_workers=min(len(image_tasks), 4)) as executor:
                    futures = [executor.submit(self._save_single_image_wrapper, task) for task in image_tasks]

                    for future in as_completed(futures):
                        index, success, message = future.result()
                        if not success:
                            raise Exception(f"Fallo crítico al guardar la imagen #{index}: {message}")
            elif dto.evidence_photos_base64 == []:
                self._delete_existing_photos(model.id, EVIDENCE_SAVE_DIR)

            model.hourometer = dto.hourometer
            model.reception_name = dto.reception_name
            model.employee_id = dto.employee_id
            model.observations = dto.observations

            existing_materials = model.foem01_1_materials
            incoming_materials = dto.foem01_1_materials

            for index, incoming in enumerate(incoming_materials):
                if index < len(existing_materials):
                    existing = existing_materials[index]
                    existing.amount = incoming.amount
                    existing.um = incoming.um
                    existing.part_number = incoming.part_number
                    existing.description = incoming.description
                else:
                    new_material = FOEM011MaterialModel(
                        foem01_1_id=model.id,
                        amount=incoming.amount,
                        um=incoming.um,
                        part_number=incoming.part_number,
                        description=incoming.description,
                    )
                    self.db.add(new_material)

            if len(existing_materials) > len(incoming_materials):
                for material in existing_materials[len(incoming_materials):]:
                    self.db.delete(material)

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError:
            self.db.rollback()
            return False

    def get_list_foem01_1_by_client_id(self, client_id: int) -> List[FOEM011]:
        models = self.db.query(FOEM011Model).filter_by(client_id=client_id).all()
        return [
            FOEM011(
                id=model.id,
                employee=model.employee,
                file=model.file,
                client=model.client,
                date_created=model.date_created,
                hourometer=model.hourometer,
                status=model.status,
                reception_name=model.reception_name,
                signature_path=model.signature_path,
                date_signed=model.date_signed,
                materials=model.foem01_1_materials,
                observations=model.observations,
                rating=model.rating,
                rating_comment=model.rating_comment,
                evidence_photos=None,
            )
            for model in models
        ]

    def get_list_foem01_1_table(self, client_id: int) -> List[FOEM011TableRowDTO]:
        models = self.db.query(FOEM011Model).filter_by(client_id=client_id).order_by(desc(FOEM011Model.id)).all()

        if not models:
            return []

        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else "N/A"
            return "N/A"

        return [
            FOEM011TableRowDTO(
                id=model.id,
                file_id=model.file.folio if model.file else None,
                date_created=model.date_created,
                employee_name=get_full_name(model.employee),
                status=model.status,
                rating=model.rating,
                rating_comment=model.rating_comment,
            )
            for model in models
        ]

    def sign_foem01_1(self, id: int, dto: FOEM011SignatureDTO) -> bool:
        try:
            model = self.db.query(FOEM011Model).filter_by(id=id).first()
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
            model.employee_id = dto.employee_id
            model.rating = dto.rating
            model.rating_comment = dto.rating_comment

            self.db.commit()
            self.db.refresh(model)

            if model.file_id and dto.status == "Cerrado":
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOEM011] Advertencia: No se pudo verificar el file: {str(e)}")

            if dto.status == "Cerrado" and model.client_id:
                if model.client and model.client.email:
                    client_email = model.client.email
                    contact_person = model.client.contact_person or "Cliente"
                    client_name = model.client.name or "Cliente"
                    file_id = model.file.folio if model.file else str(model.file_id)
                    subject = f"FO-EM-01 {client_name} {file_id}"

                    from config import settings
                    report_url = f"{settings.BASE_URL}/foem01_1/{model.id}/reporte"
                    message = f"""
                    <html>
                    <body style=\"font-family: Arial, sans-serif;\">
                        <div style=\"max-width: 600px; margin: 0 auto; padding: 20px;\">
                            <h4 style=\"color: #0066cc;\">
                                Estimad@ {contact_person}, te hacemos llegar la entrega de material realizada,
                                puedes consultarlo aquí.
                            </h4>
                            <div style=\"margin: 30px 0; text-align: center;\">
                                <a href=\"{report_url}\"
                                    style=\"background-color: #0066cc;
                                            color: white;
                                            padding: 12px 30px;
                                            text-decoration: none;
                                            border-radius: 5px;
                                            display: inline-block;\">
                                    Descargar aquí
                                </a>
                            </div>
                            <p style=\"color: #666; font-size: 12px; margin-top: 40px;\">
                                Este es un correo automático, por favor no responder.
                            </p>
                        </div>
                    </body>
                    </html>
                    """

                    def send_email_async():
                        try:
                            from shared.email_service import EmailService
                            EmailService.send_email(
                                to=client_email,
                                subject=subject,
                                message=message,
                                company_id=model.client_id,
                            )
                        except Exception as e:
                            print(f"[FOEM011] Advertencia: No se pudo enviar email: {str(e)}")

                    email_thread = threading.Thread(target=send_email_async, daemon=True)
                    email_thread.start()

                    try:
                        from shared.mobile_notification_worker import enqueue_document_push_notification

                        enqueue_document_push_notification(
                            client_id=model.client_id,
                            document_type="foem01_1",
                            document_id=model.id,
                            equipment_id=None,
                            file_id=model.file_id,
                            title=subject,
                            report_url=report_url,
                            event="document_signed",
                            status=model.status,
                        )
                    except Exception as e:
                        print(f"[FOEM011] Advertencia: No se pudo encolar notificación push: {str(e)}")

            return True
        except SQLAlchemyError as e:
            print(f"Error en la operación de firma, revirtiendo: {e}")
            self.db.rollback()
            return False