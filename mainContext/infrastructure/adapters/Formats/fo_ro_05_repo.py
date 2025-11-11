from mainContext.domain.models.Formats.fo_ro_05 import FORO05
from mainContext.application.dtos.Formats.fo_ro_05_dto import FORO05CreateDTO, FORO05UpdateDTO, FORO05SignatureDTO, FORO05TableRowDTO, ClientDTO, EquipmentDTO, ServiceDTO
from mainContext.application.ports.Formats.fo_ro_05_repo import FORO05Repo

from mainContext.infrastructure.models import Foro05 as FORO05Model, Foro05Services as FORO05ServiceModel, Foro05EmployeeChecklist as FORO05EmployeeChecklistModel, Foro05VehicleChecklist as FORO05VehicleChecklistModel, Foro05ServiceSuplies as FORO05ServiceSupliesModel, Equipment as EquipmentModel, Clients as ClientModel, Services as ServiceModel






from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

import os
import base64
import glob

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)))

#PATHS FOR SIGNATURES EMPLOYEE - SUPERVISOR

SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-ro-05")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-ro-05"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)

class FORO05RepoImpl(FORO05Repo):
    def __init__(self, db: Session):
        self.db = db
    
    def _delete_existing_photos(self, model_id: int, save_dir: str, is_employee: bool = False):
        prefix = f"foro05" + ("e" if is_employee else "s") + f"-{model_id}"
        pattern = os.path.join(save_dir, f"{prefix}*.png")
        for file_path in glob.glob(pattern):
            os.remove(file_path)
    
    def _save_signature(self, model_id: int, signature_base64: str, save_dir: str, is_employee: bool = False) -> str:        
        try:
            self._delete_existing_photos(model_id, save_dir, is_employee)
            try:
                header, data = signature_base64.split(",", 1)
            except ValueError:
                data = signature_base64
            image_data = base64.b64decode(data)
            
            prefix = f"foro05" + ("e" if is_employee else "s") + f"-{model_id}"
            filename = f"{prefix}.png"

            file_path = os.path.join(save_dir, filename)
            
            with open(file_path, "wb") as f:
                f.write(data)
                
            return f"{SIGNATURE_URL_BASE}/{filename}"
        except Exception as e:
            print(f"Error al guardar la firma: {e}")
            return None
        
    def create_foro05(self, dto: FORO05CreateDTO) -> int:
        try:
            model = FORO05Model(
                route_date=dto.route_date,
                status=dto.status            
            )
            employeeCheck = FORO05EmployeeChecklistModel(
                foro05_id=model.id,
                neat=False,
                full_uniform=False,
                clean_uniform=False,
                safty_boots=False,
                ddg_id=False,
                valid_license=False,
                presentation_card=False
            )
            vehicleCheck = FORO05VehicleChecklistModel(
                foro05_id=model.id,
                checklist=False,
                clean_tools=False,
                tidy_tools=False,
                clean_vehicle=False,
                tidy_vehicle=False,
                fuel=False,
                documents=False
            )
            model.foro05_employee_checklist = [employeeCheck]
            model.foro05_vehicle_checklist = [vehicleCheck]

            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al crear FORO05: {e}")

    def get_foro05_by_id(self, id: int) -> FORO05:
        model = self.db.query(FORO05Model).filter_by(id=id).first()
        if not model:
            return None
        return FORO05(
            id=model.id,
            employee=model.employee,
            supervisor=model.supervisor,
            vehicle=model.vehicle,
            route_date=model.route_date,
            status=model.status,
            comments=model.comments,
            employee_checklist=model.foro05_employee_checklist,
            vehicle_checklist=model.foro05_vehicle_checklist,
            services=model.foro05_services,
            signature_path_employee=model.signature_path_employee,
            signature_path_supervisor=model.signature_path_supervisor
        )

    def delete_foro05(self, id: int) -> bool:
        try:
            model = self.db.query(FORO05Model).filter_by(id=id).first()
            if not model:
                return False
            
            self._delete_existing_photos(model.id, SIGNATURE_SAVE_DIR, is_employee=True)
            self._delete_existing_photos(model.id, SIGNATURE_SAVE_DIR, is_employee=False)

            employeeCheckList = self.db.query(FORO05EmployeeChecklistModel).filter_by(foro05_id=id).first()
            if employeeCheckList:
                self.db.delete(employeeCheckList)

            vehicleCheckList = self.db.query(FORO05VehicleChecklistModel).filter_by(foro05_id=id).first()
            if vehicleCheckList:
                self.db.delete(vehicleCheckList)

            services = self.db.query(FORO05ServiceModel).filter_by(foro_id=id).all()

            for service in services:
                self.db.delete(service.foro05_service_suplies)

            for service in services:
                self.db.delete(service)

            self.db.delete(model)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar FORO05: {e}")

    def update_foro05(self, foro05_id: int, dto: FORO05UpdateDTO) -> bool:
        try:
            model = self.db.query(FORO05Model).filter_by(id=foro05_id).first()
            if not model:
                return False

            # Update main attributes
            model.route_date = dto.route_date
            model.comments = dto.comments

            # Update Employee Checklist
            if model.foro05_employee_checklist:
                checklist_dto = dto.employee_checklist
                model.foro05_employee_checklist.neat = checklist_dto.neat
                model.foro05_employee_checklist.full_uniform = checklist_dto.full_uniform
                model.foro05_employee_checklist.clean_uniform = checklist_dto.clean_uniform
                model.foro05_employee_checklist.safty_boots = checklist_dto.safty_boots
                model.foro05_employee_checklist.ddg_id = checklist_dto.ddg_id
                model.foro05_employee_checklist.valid_license = checklist_dto.valid_license
                model.foro05_employee_checklist.presentation_card = checklist_dto.presentation_card

            # Update Vehicle Checklist
            if model.foro05_vehicle_checklist:
                checklist_dto = dto.vehicle_checklist
                model.foro05_vehicle_checklist.checklist = checklist_dto.checklist
                model.foro05_vehicle_checklist.clean_tools = checklist_dto.clean_tools
                model.foro05_vehicle_checklist.tidy_tools = checklist_dto.tidy_tools
                model.foro05_vehicle_checklist.clean_vehicle = checklist_dto.clean_vehicle
                model.foro05_vehicle_checklist.tidy_vehicle = checklist_dto.tidy_vehicle
                model.foro05_vehicle_checklist.fuel = checklist_dto.fuel
                model.foro05_vehicle_checklist.documents = checklist_dto.documents
            
            # --- Synchronize Services ---
            existing_services_map = {(s.client_id, s.equipment_id, s.service_id): s for s in model.foro05_services}
            incoming_services_keys = set()

            for service_dto in dto.services:
                key = (service_dto.client_id, service_dto.equipment_id, service_dto.service_id)
                incoming_services_keys.add(key)

                if key in existing_services_map:
                    # --- UPDATE EXISTING SERVICE ---
                    service_model = existing_services_map[key]
                    service_model.start_time = service_dto.start_time
                    service_model.end_time = service_dto.end_time
                    service_model.equipment = service_dto.equipment
                    service_model.file_id = service_dto.file_id

                    # --- Synchronize Service Supplies ---
                    existing_supplies_map = {s.name: s for s in service_model.foro05_service_suplies}
                    incoming_supplies_names = {s.name for s in service_dto.service_suplies}

                    for supply_dto in service_dto.service_suplies:
                        if supply_dto.name in existing_supplies_map:
                            # Update existing supply
                            supply_model = existing_supplies_map[supply_dto.name]
                            supply_model.status = supply_dto.status
                        else:
                            # Add new supply
                            new_supply = FORO05ServiceSupliesModel(
                                name=supply_dto.name,
                                status=supply_dto.status,
                                foro05_service_id=service_model.id,
                                foro05_id=foro05_id
                            )
                            self.db.add(new_supply)
                    
                    # Delete old supplies
                    for supply_name, supply_model in existing_supplies_map.items():
                        if supply_name not in incoming_supplies_names:
                            self.db.delete(supply_model)
                else:
                    # --- ADD NEW SERVICE ---
                    new_service = FORO05ServiceModel(
                        foro05_id=foro05_id,
                        client_id=service_dto.client_id,
                        equipment_id=service_dto.equipment_id,
                        service_id=service_dto.service_id,
                        file_id=service_dto.file_id,
                        start_time=service_dto.start_time,
                        end_time=service_dto.end_time,
                        equipment=service_dto.equipment
                    )
                    self.db.add(new_service)
                    self.db.flush()  # Flush to get new_service.id

                    # Add its supplies
                    for supply_dto in service_dto.service_suplies:
                        new_supply = FORO05ServiceSupliesModel(
                            name=supply_dto.name,
                            status=supply_dto.status,
                            foro05_service_id=new_service.id,
                            foro05_id=foro05_id
                        )
                        self.db.add(new_supply)

            services_to_delete_keys = set(existing_services_map.keys()) - incoming_services_keys
            for key_to_delete in services_to_delete_keys:
                service_to_delete = existing_services_map[key_to_delete]
                for supply in service_to_delete.foro05_service_suplies:
                    self.db.delete(supply)
                self.db.delete(service_to_delete)

            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar FORO05: {e}")

    def get_list_foro05_table(self) -> List[FORO05TableRowDTO]:
        try:
            models = (
                self.db.query(FORO05Model)
                .options(
                    joinedload(FORO05Model.employee),
                    joinedload(FORO05Model.supervisor),
                    joinedload(FORO05Model.vehicle)
                )
                .order_by(desc(FORO05Model.route_date))
                .all()
            )
            
            dto_list = []
            for model in models:
                dto = FORO05TableRowDTO(
                    id=model.id,
                    route_date=model.route_date,
                    status=model.status,
                    employee_name=model.employee.name if model.employee else "No asignado",
                    supervisor_name=model.supervisor.name if model.supervisor else "No asignado",
                    vehicle=model.vehicle.name if model.vehicle else "No asignado"
                )
                dto_list.append(dto)
            return dto_list
        except SQLAlchemyError as e:
            raise Exception(f"Error al listar FORO05: {e}")

    def sign_foro05(self, foro05_id: int, dto: FORO05SignatureDTO) -> bool:
        try:
            model = self.db.query(FORO05Model).filter_by(id=foro05_id).first()
            if not model:
                return False

            if dto.employee:
                signature_path = self._save_signature(
                    model_id=foro05_id,
                    signature_base64=dto.signature_base64,
                    save_dir=SIGNATURE_SAVE_DIR,
                    is_employee=True
                )
                if signature_path:
                    model.signature_path_employee = signature_path
                else:
                    raise Exception("Error al guardar la firma del empleado.")

            if dto.supervisor:
                signature_path = self._save_signature(
                    model_id=foro05_id,
                    signature_base64=dto.signature_base64,
                    save_dir=SIGNATURE_SAVE_DIR,
                    is_employee=False  # For supervisor
                )
                if signature_path:
                    model.signature_path_supervisor = signature_path
                else:
                    raise Exception("Error al guardar la firma del supervisor.")
                
                # Close the document if supervisor signs
                model.status = dto.status

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al firmar FORO05: {e}")

    def get_list_clients(self) -> List[ClientDTO]:
        try:
            models = self.db.query(ClientModel).filter_by(status='Cliente').all()
            if not models:
                return []
            return [ClientDTO(id=model.id, name=model.name) for model in models]
        except Exception as e:
            raise Exception(f"Error al listar clientes: {e}")
        
    def get_list_equipments(self, client_id):
        try: 
            models = self.db.query(EquipmentModel).filter_by(client_id=client_id).all()
            if not models:
                return []
            return [EquipmentDTO(id=model.id, name=model.brand.name + " " + model.economic_number) for model in models]
        except Exception as e:
            raise Exception(f"Error al listar equipos: {e}")

    def get_list_services(self) -> List[ServiceDTO]:
        try:
            models = self.db.query(ServiceModel).all()
            if not models:
                return []
            return [ServiceDTO(id=model.id, code_name=model.code) for model in models]
        except Exception as e:
            raise Exception(f"Error al listar servicios: {e}")
            
