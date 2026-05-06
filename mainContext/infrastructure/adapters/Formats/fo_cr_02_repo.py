from mainContext.application.ports.Formats.fo_cr_02_repo import FOCR02Repo
from mainContext.application.dtos.Formats.fo_cr_02_dto import (
    CreateFOCR02DTO, UpdateFOCR02DTO, FOCR02SignatureDTO, FOCR02ReturnSignatureDTO, FOCR02TableRowDTO, FOCRAddEquipmentDTO
)
from mainContext.domain.models.Formats.fo_cr_02 import FOCR02
from mainContext.application.services.file_generator import FileService

from mainContext.infrastructure.models import (
    Focr02 as FOCR02Model,
    FocrAddEquipment as FOCRAddEquipmentModel,
    Employees as EmployeesModel,
    Equipment as EquipmentModel,
    Clients as ClientsModel,
    Files as FilesModel,
    Foos01 as FOOS01Model
)

from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import date, datetime
from sqlalchemy.exc import SQLAlchemyError

import os
import base64
import threading
from mainContext.infrastructure.adapters.Formats.file_cleanup_helper import cleanup_file_if_orphaned

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_PATH)))

SIGNATURE_PATH = os.path.join(MAIN_CONTEXT_ROOT, 'static', 'img', 'signatures', 'fo-cr-02')
SIGNATURE_BASE_URL = '/static/img/signatures/fo-cr-02'
os.makedirs(SIGNATURE_PATH, exist_ok=True)


class FOCR02RepoImpl(FOCR02Repo):
    def __init__(self, db: Session):
        self.db = db

    def _model_to_dict(self, model: FOCR02Model):
        """Mapea el modelo FOCR02 a un diccionario listo para los esquemas de respuesta."""
        if not model:
            return None

        return {
            "id": model.id,
            "client": {
                "id": model.client.id,
                "name": model.client.name,
                "rfc": model.client.rfc,
                "address": model.client.address,
                "phone_number": model.client.phone_number,
                "contact_person": model.client.contact_person,
                "email": model.client.email,
                "status": model.client.status,
            }
            if model.client
            else None,
            "employee": {
                "id": model.employee.id,
                "name": model.employee.name,
                "lastname": model.employee.lastname,
            }
            if model.employee
            else None,
            "equipment": {
                "id": model.equipment.id,
                "client_id": model.equipment.client_id,
                "type_id": model.equipment.type_id,
                "brand_id": model.equipment.brand_id,
                "model": model.equipment.model,
                "mast": model.equipment.mast,
                "serial_number": model.equipment.serial_number,
                "hourometer": model.equipment.hourometer,
                "doh": model.equipment.doh,
                "economic_number": model.equipment.economic_number,
                "capacity": model.equipment.capacity,
                "addition": model.equipment.addition,
                "motor": model.equipment.motor,
                "property": model.equipment.property,
                "brand": {
                    "id": model.equipment.brand.id,
                    "name": model.equipment.brand.name,
                    "img_path": model.equipment.brand.img_path,
                }
                if model.equipment.brand
                else None,
                "type": {
                    "id": model.equipment.type.id,
                    "name": model.equipment.type.name,
                }
                if model.equipment.type
                else None,
            }
            if model.equipment
            else None,
            "file": {
                "id": model.file.id,
                "folio": model.file.folio,
                "status": model.file.status,
            }
            if model.file
            else None,
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
                "addition": model.additional_equipment.addition,
            }
            if model.additional_equipment
            else None,
            "reception_name": model.reception_name,
            "date_created": model.date_created.date() if model.date_created else None,
            "status": model.status,
            "signature_path": model.signature_path,
            "date_signed": model.date_signed.date() if model.date_signed else None,
            "return_reception_name": model.return_reception_name,
            "return_signature_path": model.return_signature_path,
            "return_date_signed": model.return_date_signed.date() if model.return_date_signed else None,
            "return_observations": model.return_observations,
        }
    
    def _delete_existing_signature(self, model_id: int, save_dir: str):
        """Elimina la firma de entrega anterior si existe"""
        file_path = os.path.join(save_dir, f"focr02-{model_id}.png")
        if os.path.exists(file_path):
            os.remove(file_path)

    def _delete_existing_return_signature(self, model_id: int, save_dir: str):
        """Elimina la firma de devolución anterior si existe"""
        file_path = os.path.join(save_dir, f"focr02-{model_id}-return.png")
        if os.path.exists(file_path):
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

    def _save_return_signature(self, model_id: int, signature_base64: str, save_dir: str) -> str:
        """Guarda la firma de devolución en base64 como PNG"""
        try:
            self._delete_existing_return_signature(model_id, save_dir)
            try:
                header, data = signature_base64.split(",", 1)
            except ValueError:
                data = signature_base64
            image_data = base64.b64decode(data)

            filename = f"focr02-{model_id}-return.png"
            file_path = os.path.join(save_dir, filename)

            with open(file_path, "wb") as f:
                f.write(image_data)

            return f"{SIGNATURE_BASE_URL}/{filename}"
        except Exception as e:
            print(f"Error al guardar la firma de devolución: {e}")
            return None

    def _format_equipment_name(self, equipment: EquipmentModel) -> str:
        brand_name = equipment.brand.name if equipment.brand else ""
        model_name = equipment.model or ""
        combined = " ".join(filter(None, [brand_name, model_name])).strip()
        return combined if combined else brand_name or model_name
    
    def create_focr02(self, dto: CreateFOCR02DTO) -> int:
        try:
            # Crear el archivo mediante FileService (retorna None para clientes internos como 11 y 90)
            file = FileService.create_file(self.db, client_id=dto.client_id, status="Abierto")
            file_id = file.id if file else None

            # Actualizar el client_id del equipamiento
            equipment = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first()
            if equipment:
                equipment.client_id = dto.client_id

            model = FOCR02Model(
                client_id=dto.client_id,
                equipment_id=dto.equipment_id,
                employee_id=dto.employee_id,
                file_id=file_id,
                additional_equipment_id=None,  # Se añade en update
                date_created=datetime.today(),
                status="Abierto"
            )
            self.db.add(model)
            # Crear FOOS01 asociado al mismo file
            foos_model = FOOS01Model(
                client_id=dto.client_id,
                equipment_id=dto.equipment_id,
                employee_id=dto.employee_id,
                file_id=file_id,
                date_created=date.today(),
                status="Abierto",
                hourometer=0.0,
                observations="",
                reception_name="",
                signature_path="",
                date_signed=None,
                rating=0,
                rating_comment="",
                fopc_services_id=None,
                GC=""
            )
            self.db.add(foos_model)
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
                joinedload(FOCR02Model.equipment).joinedload(EquipmentModel.brand),
                joinedload(FOCR02Model.equipment).joinedload(EquipmentModel.type),
                joinedload(FOCR02Model.client),
                joinedload(FOCR02Model.additional_equipment),
                joinedload(FOCR02Model.file)
            ).filter_by(id=id).first()
            
            return self._model_to_dict(model)
        except Exception as e:
            raise Exception(f"Error al obtener FOCR02: {str(e)}")

    def get_focr02_by_client_id(self, client_id: int):
        try:
            models = (
                self.db.query(FOCR02Model)
                .options(
                    joinedload(FOCR02Model.employee),
                    joinedload(FOCR02Model.equipment).joinedload(EquipmentModel.brand),
                    joinedload(FOCR02Model.equipment).joinedload(EquipmentModel.type),
                    joinedload(FOCR02Model.client),
                    joinedload(FOCR02Model.additional_equipment),
                    joinedload(FOCR02Model.file),
                )
                .filter_by(client_id=client_id)
                .all()
            )

            return [self._model_to_dict(model) for model in models]
        except Exception as e:
            raise Exception(f"Error al obtener FOCR02 por cliente: {str(e)}")
    
    def get_focr02_table(self) -> List[FOCR02TableRowDTO]:
        try:
            models = self.db.query(FOCR02Model).options(
                joinedload(FOCR02Model.employee),
                joinedload(FOCR02Model.equipment).joinedload(EquipmentModel.brand),
                joinedload(FOCR02Model.client),
                joinedload(FOCR02Model.file)
            ).all()
            
            if not models:
                return []
            
            return [
                FOCR02TableRowDTO(
                    id=m.id,
                    status=m.status,
                    equipment_name=self._format_equipment_name(m.equipment) if m.equipment else "",
                    employee_name=f"{m.employee.name} {m.employee.lastname}" if m.employee else "",
                    date_created=m.date_created.date() if m.date_created else None,
                    client_name=m.client.name if m.client else None,
                    file_id=m.file.id if m.file else None,
                    file_status=m.file.status if m.file else None,
                    file_folio=m.file.folio if m.file else None
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
            
            if dto.reception_name:
                model.reception_name = dto.reception_name
            if dto.employee_id:
                model.employee_id = dto.employee_id
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
            
            # Eliminar firmas si existen
            if model.signature_path:
                self._delete_existing_signature(id, SIGNATURE_PATH)
            if model.return_signature_path:
                self._delete_existing_return_signature(id, SIGNATURE_PATH)

            file_id = model.file_id
            # Restaurar cliente del equipo a 11
            if model.equipment_id:
                equipment = self.db.query(EquipmentModel).filter_by(id=model.equipment_id).first()
                if equipment:
                    if equipment.client_id == model.client_id:
                        equipment.client_id = 11
            
            # Eliminar FOOS01 asociados al mismo file_id
            foos_entries = []
            if file_id:
                foos_entries = self.db.query(FOOS01Model).filter_by(file_id=file_id).all()
                for foos in foos_entries:
                    self.db.delete(foos)

            self.db.delete(model)
            self.db.flush()

            # Eliminar file solo si no hay otros documentos relacionados
            cleanup_file_if_orphaned(self.db, file_id)

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

            # Cambiar a "En Renta" (equipo entregado, pendiente de devolución)
            model.status = "En Renta"
            model.date_signed = datetime.now()
            model.employee_id = dto.employee_id

            self.db.commit()
            self.db.refresh(model)

            # Enviar email de notificación de entrega (asíncrono)
            self._send_notification_email(model, "entrega")

            return True
        except Exception as e:
            raise Exception(f"Error al firmar FOCR02: {str(e)}")

    def return_sign_focr02(self, id: int, dto: FOCR02ReturnSignatureDTO) -> bool:
        try:
            model = self.db.query(FOCR02Model).filter_by(id=id).first()
            if not model:
                return False

            if model.status != "En Renta":
                raise Exception("Solo se puede firmar devolución de un documento en estado 'En Renta'")

            return_signature_path = self._save_return_signature(
                model_id=id,
                signature_base64=dto.signature_base64,
                save_dir=SIGNATURE_PATH
            )
            if return_signature_path:
                model.return_signature_path = return_signature_path
            else:
                raise Exception("Error al guardar la firma de devolución.")

            model.return_reception_name = dto.return_reception_name
            model.return_observations = dto.return_observations
            model.return_date_signed = datetime.now()
            model.status = "Cerrado"
            model.employee_id = dto.employee_id

            # Restaurar client_id del equipo a 11 (devuelto a DAL)
            if model.equipment_id:
                equipment = self.db.query(EquipmentModel).filter_by(id=model.equipment_id).first()
                if equipment and equipment.client_id == model.client_id:
                    equipment.client_id = 11

            self.db.commit()
            self.db.refresh(model)

            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id:
                try:
                    FileService.check_and_close_group_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOCR02] Advertencia: No se pudo verificar el file: {str(e)}")

            # Enviar email de notificación de devolución (asíncrono)
            self._send_notification_email(model, "devolucion")

            return True
        except Exception as e:
            raise Exception(f"Error al firmar devolución FOCR02: {str(e)}")

    def _send_notification_email(self, model: FOCR02Model, tipo: str):
        """Envía email de notificación al cliente de forma asíncrona"""
        if not model.client_id:
            return
        if not (model.client and model.client.email and model.equipment):
            return

        client_email = model.client.email
        contact_person = model.client.contact_person or "Cliente"
        brand_name = model.equipment.brand.name if model.equipment.brand else "N/A"
        economic_number = model.equipment.economic_number or "N/A"
        file_id = model.file.folio if model.file else str(model.file_id)

        if tipo == "entrega":
            subject = f"FO-CR-02 Entrega {brand_name} #{economic_number} {file_id}"
            accion = "Carta Responsiva Entrega de Equipo"
        else:
            subject = f"FO-CR-02 Devolución {brand_name} #{economic_number} {file_id}"
            accion = "Carta Responsiva Devolución de Equipo"

        from config import settings
        report_url = f"{settings.BASE_URL}/focr02/{model.id}/reporte"
        message = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h4 style="color: #0066cc;">
                    Estimad@ {contact_person}, te hacemos llegar la {accion},
                    puedes consultarla aquí.
                </h4>
                <div style="margin: 30px 0; text-align: center;">
                    <a href="{report_url}"
                        style="background-color: #0066cc;
                                color: white;
                                padding: 12px 30px;
                                text-decoration: none;
                                border-radius: 5px;
                                display: inline-block;">
                        Descargar aquí
                    </a>
                </div>
                <p style="color: #666; font-size: 12px; margin-top: 40px;">
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
                    company_id=model.client_id
                )
            except Exception as e:
                print(f"[FOCR02] Advertencia: No se pudo enviar email: {str(e)}")

        email_thread = threading.Thread(target=send_email_async, daemon=True)
        email_thread.start()

        try:
            from shared.mobile_notification_worker import enqueue_document_push_notification

            enqueue_document_push_notification(
                client_id=model.client_id,
                document_type="focr02",
                document_id=model.id,
                equipment_id=model.equipment_id,
                file_id=model.file_id,
                title=subject,
                report_url=report_url,
                event="document_signed",
                status=model.status,
            )
        except Exception as e:
            print(f"[FOCR02] Advertencia: No se pudo encolar notificación push: {str(e)}")
    
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
