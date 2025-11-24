from mainContext.domain.models.Formats.fo_pc_02 import FOPC02, ClientEquipmentProperty

from mainContext.application.ports.Formats.fo_pc_02_repo import FOPC02Repo
from mainContext.application.dtos.Formats.fo_pc_02_dto import (
    CreateFOPC02DTO,
    UpdateFOPc02DTO,
    FOPC02SignatureDTO,
    FOPC02TableRowDTO,
    GetFOPC02ByDocumentDTO,
    FOPC02ByDocumentResponseDTO
)

from mainContext.infrastructure.models import (
    Fopc02 as FOPC02Model, 
    Equipment as EquipmentModel,
    FopcServices as FopcServicesModel,
    Foos01 as FOOS01Model,
    Fosp01 as FOSP01Model,
    Fosc01 as FOSC01Model,
    ClientEquipmentProperty as ClientEquipmentPropertyModel
)

from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from mainContext.infrastructure.adapters.Formats.file_cleanup_helper import cleanup_file_if_orphaned
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

import os
import base64
import glob

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)))

# Paths for Signatures (No hay evidencias en FOPC02)
SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-pc-02")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-pc-02"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)


class FOPC02RepoImpl(FOPC02Repo):
    def __init__(self, db: Session):
        self.db = db

    def _delete_existing_signature(self, model_id: int, signature_type: str):
        """
        Elimina firma existente
        signature_type: 'TecExt', 'TecRet', 'CliExt', 'CliRet'
        """
        try:
            search_pattern = os.path.join(SIGNATURE_SAVE_DIR, f"fopc02{signature_type}-{model_id}.*")
            for f in glob.glob(search_pattern):
                os.remove(f)
        except Exception as e:
            print(f"Error al eliminar firma {signature_type} para ID {model_id}: {e}")
            raise

    def _save_signature(self, base64_string: str, model_id: int, signature_type: str) -> str | None:
        """
        Guarda firma en base64
        signature_type: 'TecExt', 'TecRet', 'CliExt', 'CliRet'
        """
        try:
            try:
                header, data = base64_string.split(",", 1)
            except ValueError:
                data = base64_string

            image_data = base64.b64decode(data)
            file_ext = ".png"

            filename = f"fopc02{signature_type}-{model_id}{file_ext}"
            save_path = os.path.join(SIGNATURE_SAVE_DIR, filename)

            with open(save_path, "wb") as f:
                f.write(image_data)

            public_url = f"{SIGNATURE_URL_BASE}/{filename}"
            return public_url

        except Exception as e:
            print(f"Error al guardar firma {signature_type}: {e}")
            return None

    def _get_or_create_fopc_services(self, document_type: str, document_id: int) -> tuple[int, str | None]:
        """
        Obtiene o crea un registro en fopc_services y actualiza el documento correspondiente
        """
        try:
            # Determinar el modelo según document_type
            if document_type == "foos01":
                document_model = self.db.query(FOOS01Model).filter_by(id=document_id).first()
            elif document_type == "fosp01":
                document_model = self.db.query(FOSP01Model).filter_by(id=document_id).first()
            elif document_type == "fosc01":
                document_model = self.db.query(FOSC01Model).filter_by(id=document_id).first()
            else:
                raise ValueError(f"document_type inválido: {document_type}")

            if not document_model:
                raise ValueError(f"No se encontró el documento {document_type} con id {document_id}")

            file_id = getattr(document_model, "file_id", None)

            # Si el documento ya tiene un fopc_services_id, usarlo
            if document_model.fopc_services_id:
                return document_model.fopc_services_id, file_id

            # Crear nuevo registro en fopc_services
            fopc_services = FopcServicesModel()
            self.db.add(fopc_services)
            self.db.flush()  # Para obtener el ID

            # Actualizar el documento con el fopc_services_id
            document_model.fopc_services_id = fopc_services.id
            self.db.flush()

            return fopc_services.id, file_id

        except Exception as e:
            raise Exception(f"Error al obtener/crear fopc_services: {str(e)}")

    def create_fopc02(self, dto: CreateFOPC02DTO) -> int:
        try:
            # Obtener o crear fopc_services y actualizar el documento relacionado
            fopc_services_id, document_file_id = self._get_or_create_fopc_services(dto.document_type, dto.document_id)

            # Crear el modelo FOPC02
            model = FOPC02Model(
                client_id=dto.client_id,
                employee_id=dto.employee_id,
                equipment_id=dto.equipment_id,
                fopc_services_id=fopc_services_id,
                status="Abierto",
                departure_date=None,
                departure_description=None,
                return_date=None,
                return_description=None,
                departure_signature_path=None,
                departure_employee_signature_path=None,
                return_signature_path=None,
                return_employee_signature_path=None,
                name_auth_departure=None,
                name_recipient=None,
                observations=None,
                property_id=None,
                file_id=document_file_id,
                date_created=datetime.now()
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)

            if not model.id or model.id <= 0:
                raise Exception("Error al registrar FO-PC-02 en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al registrar FO-PC-02 en la base de datos: {str(e)}")

    def get_fopc02_by_id(self, id: int) -> FOPC02:
        model = self.db.query(FOPC02Model).filter_by(id=id).first()
        if not model:
            return None

        property_obj = None
        if model.property:
            property_obj = ClientEquipmentProperty(
                id=model.property.id,
                property=model.property.property,
                brand=model.property.brand,
                model=model.property.model,
                serial_number=model.property.serial_number
            )

        return FOPC02(
            id=model.id,
            client=model.client,
            employee=model.employee,
            equipment=model.equipment,
            property=property_obj,
            departure_date=model.departure_date,
            departure_description=model.departure_description,
            return_date=model.return_date,
            return_description=model.return_description,
            departure_signature_path=model.departure_signature_path,
            departure_employee_signature_path=model.departure_employee_signature_path,
            return_signature_path=model.return_signature_path,
            return_employee_signature_path=model.return_employee_signature_path,
            status=model.status,
            name_auth_departure=model.name_auth_departure,
            name_recipient=model.name_recipient,
            observations=model.observations,
            file_id=model.file_id,
            fopc_services_id=model.fopc_services_id
        )

    def delete_fopc02(self, id: int) -> bool:
        model = self.db.query(FOPC02Model).filter_by(id=id).first()
        if not model:
            return False

        # Eliminar todas las firmas
        self._delete_existing_signature(model.id, "TecExt")
        self._delete_existing_signature(model.id, "TecRet")
        self._delete_existing_signature(model.id, "CliExt")
        self._delete_existing_signature(model.id, "CliRet")

        # Eliminar property si existe
        if model.property_id:
            property_model = self.db.query(ClientEquipmentPropertyModel).filter_by(id=model.property_id).first()
            if property_model:
                self.db.delete(property_model)

        file_id = model.file_id
        self.db.delete(model)
        self.db.flush()
        
        # Eliminar file solo si no hay otros documentos relacionados
        cleanup_file_if_orphaned(self.db, file_id)
        
        self.db.commit()
        return True

    def update_fopc02(self, id: int, dto: UpdateFOPc02DTO) -> bool:
        try:
            model = self.db.query(FOPC02Model).filter_by(id=id).first()
            if not model:
                return False

            # Actualizar campos básicos
            if dto.departure_date is not None:
                model.departure_date = dto.departure_date
            if dto.departure_description is not None:
                model.departure_description = dto.departure_description
            if dto.return_date is not None:
                model.return_date = dto.return_date
            if dto.return_description is not None:
                model.return_description = dto.return_description
            if dto.name_auth_departure is not None:
                model.name_auth_departure = dto.name_auth_departure
            if dto.name_recipient is not None:
                model.name_recipient = dto.name_recipient
            if dto.observations is not None:
                model.observations = dto.observations

            # Actualizar o crear property
            if dto.property is not None:
                if model.property_id:
                    # Actualizar property existente
                    property_model = self.db.query(ClientEquipmentPropertyModel).filter_by(id=model.property_id).first()
                    if property_model:
                        property_model.property = dto.property.property
                        property_model.brand = dto.property.brand
                        property_model.model = dto.property.model
                        property_model.serial_number = dto.property.serial_number
                else:
                    # Crear nuevo property
                    new_property = ClientEquipmentPropertyModel(
                        property=dto.property.property,
                        brand=dto.property.brand,
                        model=dto.property.model,
                        serial_number=dto.property.serial_number
                    )
                    self.db.add(new_property)
                    self.db.flush()
                    model.property_id = new_property.id

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            print(f"Error en la operación de actualización, revirtiendo: {e}")
            self.db.rollback()
            return False

    def get_list_fopc02_by_equipment_id(self, equipment_id: int) -> List[FOPC02]:
        models = self.db.query(FOPC02Model).filter_by(equipment_id=equipment_id).all()
        result = []
        for model in models:
            property_obj = None
            if model.property:
                property_obj = ClientEquipmentProperty(
                    id=model.property.id,
                    property=model.property.property,
                    brand=model.property.brand,
                    model=model.property.model,
                    serial_number=model.property.serial_number
                )
            
            result.append(FOPC02(
                id=model.id,
                client=model.client,
                employee=model.employee,
                equipment=model.equipment,
                property=property_obj,
                departure_date=model.departure_date,
                departure_description=model.departure_description,
                return_date=model.return_date,
                return_description=model.return_description,
                departure_signature_path=model.departure_signature_path,
                departure_employee_signature_path=model.departure_employee_signature_path,
                return_signature_path=model.return_signature_path,
                return_employee_signature_path=model.return_employee_signature_path,
                status=model.status,
                name_auth_departure=model.name_auth_departure,
                name_recipient=model.name_recipient,
                observations=model.observations,
                file_id=model.file_id,
                fopc_services_id=model.fopc_services_id
            ))
        return result

    def get_list_fopc02_table(self, equipment_id: int) -> List[FOPC02TableRowDTO]:
        models = self.db.query(FOPC02Model).filter_by(equipment_id=equipment_id).order_by(desc(FOPC02Model.id)).all()
        
        if not models:
            return []
        
        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else 'N/A'
            return 'N/A'
        
        def get_equipment_name(equipment):
            if equipment and equipment.type:
                return equipment.type.name or 'N/A'
            return 'N/A'
        
        return [
            FOPC02TableRowDTO(
                id=m.id,
                file=m.file_id if m.file_id else 'N/A',
                equipment_name=get_equipment_name(m.equipment),
                employee_name=get_full_name(m.employee),
                date_created=m.departure_date if m.departure_date else datetime.now()
            )
            for m in models
        ]

    def sign_fopc02_departure(self, id: int, dto: FOPC02SignatureDTO) -> bool:
        """
        Firma de salida (departure)
        - is_employee=True: firma del empleado (TecExt)
        - is_employee=False: firma del cliente (CliExt)
        """
        try:
            model = self.db.query(FOPC02Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.signature_base64:
                if dto.is_employee:
                    # Firma del empleado en departure
                    self._delete_existing_signature(model.id, "TecExt")
                    url = self._save_signature(dto.signature_base64, model.id, "TecExt")
                    if url:
                        model.departure_employee_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma TecExt para el ID {model.id}")
                else:
                    # Firma del cliente en departure
                    self._delete_existing_signature(model.id, "CliExt")
                    url = self._save_signature(dto.signature_base64, model.id, "CliExt")
                    if url:
                        model.departure_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma CliExt para el ID {model.id}")

            # Verificar si todas las firmas están completas para cerrar el documento
            if (model.departure_signature_path and 
                model.departure_employee_signature_path and 
                model.return_signature_path and 
                model.return_employee_signature_path):
                model.status = "Cerrado"

            self.db.commit()
            self.db.refresh(model)
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id and model.status == "Cerrado":
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOPC02] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except Exception as e:
            print(f"Error en la operación de firma departure, revirtiendo: {e}")
            self.db.rollback()
            return False

    def sign_fopc02_return(self, id: int, dto: FOPC02SignatureDTO) -> bool:
        """
        Firma de retorno (return)
        - is_employee=True: firma del empleado (TecRet)
        - is_employee=False: firma del cliente (CliRet)
        """
        try:
            model = self.db.query(FOPC02Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.signature_base64:
                if dto.is_employee:
                    # Firma del empleado en return
                    self._delete_existing_signature(model.id, "TecRet")
                    url = self._save_signature(dto.signature_base64, model.id, "TecRet")
                    if url:
                        model.return_employee_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma TecRet para el ID {model.id}")
                else:
                    # Firma del cliente en return
                    self._delete_existing_signature(model.id, "CliRet")
                    url = self._save_signature(dto.signature_base64, model.id, "CliRet")
                    if url:
                        model.return_signature_path = url
                    else:
                        raise Exception(f"Fallo crítico al guardar la firma CliRet para el ID {model.id}")

            # Verificar si todas las firmas están completas para cerrar el documento
            if (model.departure_signature_path and 
                model.departure_employee_signature_path and 
                model.return_signature_path and 
                model.return_employee_signature_path):
                model.status = "Cerrado"

            self.db.commit()
            self.db.refresh(model)
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id and model.status == "Cerrado":
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOPC02] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except Exception as e:
            print(f"Error en la operación de firma return, revirtiendo: {e}")
            self.db.rollback()
            return False

    def get_fopc02_by_document(self, dto: GetFOPC02ByDocumentDTO) -> List[FOPC02ByDocumentResponseDTO]:
        """
        Obtiene todos los FOPC02 asociados a un documento (FOOS01, FOSP01 o FOSC01)
        a través del fopc_services_id compartido
        """
        try:
            # Determinar el modelo según document_type
            document_type = dto.document_type.lower()
            if document_type == "foos01":
                document_model = self.db.query(FOOS01Model).filter_by(id=dto.document_id).first()
            elif document_type == "fosp01":
                document_model = self.db.query(FOSP01Model).filter_by(id=dto.document_id).first()
            elif document_type == "fosc01":
                document_model = self.db.query(FOSC01Model).filter_by(id=dto.document_id).first()
            else:
                raise ValueError(f"document_type inválido: {dto.document_type}")

            if not document_model or not document_model.fopc_services_id:
                return []

            # Buscar todos los FOPC02 con el mismo fopc_services_id
            fopc02_models = (
                self.db.query(FOPC02Model)
                .filter_by(fopc_services_id=document_model.fopc_services_id)
                .order_by(desc(FOPC02Model.id))
                .all()
            )

            # Construir respuesta
            result = []
            for model in fopc02_models:
                result.append(FOPC02ByDocumentResponseDTO(
                    id=model.id,
                    date_created=model.date_created,
                    status=model.status,
                    file_id=model.file_id
                ))

            return result

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error al obtener FOPC02 por documento: {e}")
            return []
