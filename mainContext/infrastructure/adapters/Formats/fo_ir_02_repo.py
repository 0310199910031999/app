from mainContext.application.ports.Formats.fo_ir_02_repo import FOIR02Repo
from mainContext.application.dtos.Formats.fo_ir_02_dto import CreateFOIR02DTO, UpdateFOIR02DTO, FOIR02SignatureDTO, FOIR02TableRowDTO, FOIR02RequieredEquipment
from mainContext.domain.models.Formats.fo_ir_02 import FOIR02, FOIR02EquipmentChecklist as FOIR02EquipmentChecklistDomain, FOIR02RequiredEquipment

from mainContext.infrastructure.models import Foir02 as Foir02Model, Foir02EquipmentChecklist as Foir02EquipmentChecklistModel, Foir02RequieredEquipment as Foir02RequiredEquipmentModel, Employees, Vehicles


from typing import List 
from sqlalchemy.orm import Session, joinedload
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

import os
import base64
import glob

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_PATH)))

SIGNATURE_PATH = os.path.join(MAIN_CONTEXT_ROOT, 'static', 'img', 'signatures', 'fo-ir-02')
SIGNATURE_BASE_URL = '/static/img/signatures/fo-ir-02'
os.makedirs(SIGNATURE_PATH, exist_ok=True)


class FOIR02RepoImpl(FOIR02Repo):
    def __init__(self, db: Session):
        self.db = db
    
    def _delete_existing_signature(self, model_id: int, save_dir: str, is_employee: bool = False):
        prefix = f"foir02" + ("e" if is_employee else "s") + f"-{model_id}"
        pattern = os.path.join(save_dir, f"{prefix}*.png")
        for file_path in glob.glob(pattern):
            os.remove(file_path)
    
    def _save_signature(self, model_id: int, signature_base64: str, save_dir: str, is_employee: bool = False) -> str:        
        try:
            self._delete_existing_signature(model_id, save_dir, is_employee)
            try:
                header, data = signature_base64.split(",", 1)
            except ValueError:
                data = signature_base64
            image_data = base64.b64decode(data)
            
            prefix = f"foir02" + ("e" if is_employee else "s") + f"-{model_id}"
            filename = f"{prefix}.png"

            file_path = os.path.join(save_dir, filename)
            
            with open(file_path, "wb") as f:
                f.write(image_data)
                
            return f"{SIGNATURE_BASE_URL}/{filename}"
        except Exception as e:
            print(f"Error al guardar la firma: {e}")
            return None
    
    def create_foir02(self, dto: CreateFOIR02DTO) -> int:
        try:
            model = Foir02Model(
                vehicle_id=dto.vehicle_id,
                date_route=dto.date_route,
                status=dto.status
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar FO-IR-02 en la base de datos")
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al crear FO-IR-02: {str(e)}")
    
    def get_foir02_by_id(self, id: int) -> FOIR02:
        try:
            model = self.db.query(Foir02Model).options(
                joinedload(Foir02Model.foir02_equipment_checklist)
            ).filter_by(id=id).first()
            
            if not model:
                return None
            
            equipment_checklists = []
            for checklist in model.foir02_equipment_checklist:
                if checklist.equipment:
                    required_eq = FOIR02RequiredEquipment(
                        id=checklist.equipment.id,
                        amount=checklist.equipment.amount,
                        unit=checklist.equipment.unit,
                        type=checklist.equipment.type,
                        name=checklist.equipment.name
                    )
                    ec = FOIR02EquipmentChecklistDomain(
                        id=checklist.id,
                        required_equipment=required_eq,
                        status=checklist.status if checklist.status is not None else False,
                        comments=checklist.comments or ""
                    )
                    equipment_checklists.append(ec)
            
            return FOIR02(
                id=model.id,
                status=model.status,
                vehicle=model.vehicle,
                employee=model.employee,
                supervisor=model.supervisor,
                date_route=model.date_route,
                equipment_checklist=equipment_checklists
            )
        except Exception as e:
            raise Exception(f"Error al obtener FO-IR-02: {str(e)}")
    
    def delete_foir02(self, id: int) -> bool:
        try:
            model = self.db.query(Foir02Model).filter_by(id=id).first()
            if not model:
                return False
            
            # Eliminar firmas
            self._delete_existing_signature(model.id, SIGNATURE_PATH, is_employee=True)
            self._delete_existing_signature(model.id, SIGNATURE_PATH, is_employee=False)
            
            # Eliminar checklists de equipos
            checklists = self.db.query(Foir02EquipmentChecklistModel).filter_by(foir_id=id).all()
            for checklist in checklists:
                self.db.delete(checklist)
            
            # Eliminar registro principal
            self.db.delete(model)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar FO-IR-02: {str(e)}")
    
    def update_foir02(self, id: int, dto: UpdateFOIR02DTO) -> bool:
        try:
            model = self.db.query(Foir02Model).filter_by(id=id).first()
            if not model:
                return False
            
            model.employee_id = dto.employee_id
            model.supervisor_id = dto.supervisor_id
            
            # Sincronizar checklists de equipos
            existing_checklists = {c.equipment_id: c for c in model.foir02_equipment_checklist}
            incoming_equipment_ids = {c.required_equipment.id for c in dto.equipment_checklist}
            
            # Actualizar o crear checklists
            for incoming_checklist in dto.equipment_checklist:
                equipment_id = incoming_checklist.required_equipment.id
                
                if equipment_id in existing_checklists:
                    # Actualizar existente
                    existing = existing_checklists[equipment_id]
                    existing.status = incoming_checklist.status if incoming_checklist.status is not None else False
                    existing.comments = incoming_checklist.comments
                else:
                    # Crear nuevo
                    new_checklist = Foir02EquipmentChecklistModel(
                        foir_id=id,
                        equipment_id=equipment_id,
                        status=incoming_checklist.status if incoming_checklist.status is not None else False,
                        comments=incoming_checklist.comments
                    )
                    self.db.add(new_checklist)
            
            # Eliminar checklists que no están en los nuevos datos
            for equipment_id, checklist in existing_checklists.items():
                if equipment_id not in incoming_equipment_ids:
                    self.db.delete(checklist)
            
            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar FO-IR-02: {str(e)}")
    
    def get_list_foir02_table(self) -> List[FOIR02TableRowDTO]:
        try:
            models = self.db.query(Foir02Model).options(
                joinedload(Foir02Model.vehicle),
                joinedload(Foir02Model.employee),
                joinedload(Foir02Model.supervisor)
            ).order_by(desc(Foir02Model.date_route)).all()
            
            result = []
            for model in models:
                vehicle_name = model.vehicle.name if model.vehicle else "No asignado"
                employee_name = f"{model.employee.name or ''} {model.employee.lastname or ''}".strip() if model.employee else "No asignado"
                supervisor_name = f"{model.supervisor.name or ''} {model.supervisor.lastname or ''}".strip() if model.supervisor else "No asignado"
                
                dto = FOIR02TableRowDTO(
                    id=model.id,
                    status=model.status,
                    vehicle_name=vehicle_name,
                    employee_name=employee_name,
                    supervisor_name=supervisor_name,
                    date_route=model.date_route
                )
                result.append(dto)
            
            return result
        except SQLAlchemyError as e:
            raise Exception(f"Error al listar FO-IR-02: {str(e)}")
    
    def sign_foir02(self, id: int, dto: FOIR02SignatureDTO) -> bool:
        try:
            print(f"[DEBUG REPO] Buscando FOIR02 con ID: {id}")
            model = self.db.query(Foir02Model).filter_by(id=id).first()
            if not model:
                print(f"[DEBUG REPO] FOIR02 con ID {id} no encontrado")
                return False
            
            print(f"[DEBUG REPO] FOIR02 encontrado. is_employee={dto.is_employee}, is_supervisor={dto.is_supervisor}")
            
            # Validar que solo se firma una persona a la vez
            if dto.is_employee and dto.is_supervisor:
                raise Exception("No se puede firmar como empleado y supervisor al mismo tiempo")
            
            if not dto.is_employee and not dto.is_supervisor:
                raise Exception("Debe especificar si es firma de empleado o supervisor")
            
            if dto.is_employee:
                print(f"[DEBUG REPO] Procesando firma de empleado")
                # Eliminar firma anterior del empleado si existe
                if model.employee_signature_path:
                    self._delete_existing_signature(id, SIGNATURE_PATH, is_employee=True)
                
                signature_path = self._save_signature(
                    model_id=id,
                    signature_base64=dto.signature_base64,
                    save_dir=SIGNATURE_PATH,
                    is_employee=True
                )
                print(f"[DEBUG REPO] Firma de empleado guardada en: {signature_path}")
                if signature_path:
                    model.employee_signature_path = signature_path
                else:
                    raise Exception("Error al guardar la firma del empleado.")
            
            if dto.is_supervisor:
                print(f"[DEBUG REPO] Procesando firma de supervisor")
                # Eliminar firma anterior del supervisor si existe
                if model.supervisor_signature_path:
                    self._delete_existing_signature(id, SIGNATURE_PATH, is_employee=False)
                
                signature_path = self._save_signature(
                    model_id=id,
                    signature_base64=dto.signature_base64,
                    save_dir=SIGNATURE_PATH,
                    is_employee=False
                )
                print(f"[DEBUG REPO] Firma de supervisor guardada en: {signature_path}")
                if signature_path:
                    model.supervisor_signature_path = signature_path
                else:
                    raise Exception("Error al guardar la firma del supervisor.")
                
                # Cerrar documento automáticamente cuando firma el supervisor
                model.status = "Cerrado"
                print(f"[DEBUG REPO] Documento cerrado automáticamente")
            
            self.db.commit()
            self.db.refresh(model)
            print(f"[DEBUG REPO] Firma guardada exitosamente")
            return True
        except Exception as e:
            print(f"[ERROR REPO] Error en sign_foir02: {str(e)}")
            import traceback
            traceback.print_exc()
            self.db.rollback()
            raise Exception(f"Error al firmar FO-IR-02: {str(e)}")
    
    def get_foir02_required_equipment(self) -> List[FOIR02RequieredEquipment]:
        try:
            models = self.db.query(Foir02RequiredEquipmentModel).all()
            
            if not models:
                return []
            
            return [
                FOIR02RequieredEquipment(
                    id=model.id,
                    amount=model.amount,
                    unit=model.unit,
                    type=model.type,
                    name=model.name
                )
                for model in models
            ]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener equipos requeridos: {str(e)}")
    
