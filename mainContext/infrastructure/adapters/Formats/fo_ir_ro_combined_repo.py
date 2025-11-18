from mainContext.application.ports.Formats.fo_ir_ro_combined_repo import FOIRROCombinedRepo
from mainContext.application.dtos.Formats.fo_ir_ro_combined_dto import CreateFOIRROCombinedDTO, FOIRROCombinedResponse, VehicleDTO, EmployeeDTO

from mainContext.infrastructure.models import (
    Foir02 as Foir02Model,
    Foro05 as Foro05Model,
    Foro05EmployeeChecklist as FORO05EmployeeChecklistModel,
    Foro05VehicleChecklist as FORO05VehicleChecklistModel,
    Vehicles as VehiclesModel,
    Employees as EmployeesModel
)

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List


class FOIRROCombinedRepoImpl(FOIRROCombinedRepo):
    """
    Implementación del repositorio para crear FOIR02 y FORO05 simultáneamente y obtener vehículos.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_foir_and_foro(self, dto: CreateFOIRROCombinedDTO) -> FOIRROCombinedResponse:
        """
        Crea un FOIR02 y un FORO05 en una sola transacción con el mismo ID.
        
        Args:
            dto: DTO con vehicle_id, employee_id, supervisor_id, route_date y status
            
        Returns:
            FOIRROCombinedResponse con los IDs de ambos registros (serán el mismo ID)
            
        Raises:
            Exception: Si falla la creación de cualquiera de los registros
        """
        try:
            # Crear FORO05 primero para obtener el ID
            foro05_model = Foro05Model(
                vehicle_id=dto.vehicle_id,
                employee_id=dto.employee_id,
                supervisor_id=dto.supervisor_id,
                route_date=dto.route_date,
                status=dto.status
            )
            self.db.add(foro05_model)
            self.db.flush()  # Flush para obtener el ID sin hacer commit
            
            if not foro05_model.id or foro05_model.id <= 0:
                raise Exception("Error al registrar FO-RO-05 en la base de datos")
            
            # Crear FOIR02 usando el mismo ID que FORO05
            foir02_model = Foir02Model(
                id=foro05_model.id,  # Usar el mismo ID que FORO05
                vehicle_id=dto.vehicle_id,
                employee_id=dto.employee_id,
                supervisor_id=dto.supervisor_id,
                date_route=dto.route_date,
                status=dto.status
            )
            self.db.add(foir02_model)
            self.db.flush()  # Flush para registrar sin hacer commit
            
            if not foir02_model.id or foir02_model.id <= 0:
                raise Exception("Error al registrar FO-IR-02 en la base de datos")
            
            # Crear checklists iniciales para FORO05
            employee_checklist = FORO05EmployeeChecklistModel(
                foro05_id=foro05_model.id,
                neat=False,
                full_uniform=False,
                clean_uniform=False,
                safty_boots=False,
                ddg_id=False,
                valid_license=False,
                presentation_card=False
            )
            
            vehicle_checklist = FORO05VehicleChecklistModel(
                foro05_id=foro05_model.id,
                checklist=False,
                clean_tools=False,
                tidy_tools=False,
                clean_vehicle=False,
                tidy_vehicle=False,
                fuel=False,
                documents=False
            )
            
            self.db.add(employee_checklist)
            self.db.add(vehicle_checklist)
            
            # Commit de toda la transacción
            self.db.commit()
            
            # Crear respuesta
            response = FOIRROCombinedResponse(
                foir02_id=foir02_model.id,
                foro05_id=foro05_model.id,
                vehicle_id=dto.vehicle_id,
                route_date=dto.route_date,
                status=dto.status
            )
            
            return response
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al crear FO-IR-02 y FO-RO-05: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error inesperado al crear registros: {str(e)}")
    
    def get_vehicles(self) -> List[VehicleDTO]:
        """
        Obtiene la lista de todos los vehículos disponibles.
        
        Returns:
            Lista de VehicleDTO con los datos de los vehículos
            
        Raises:
            Exception: Si hay un error al consultar la base de datos
        """
        try:
            vehicles = self.db.query(VehiclesModel).all()
            
            if not vehicles:
                return []
            
            return [
                VehicleDTO(
                    id=vehicle.id,
                    name=vehicle.name,
                    license_plate=vehicle.license_plate,
                    employee_id=vehicle.employee_id
                )
                for vehicle in vehicles
            ]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener vehículos: {str(e)}")
    
    def get_employees(self) -> List[EmployeeDTO]:
        """
        Obtiene la lista de todos los empleados disponibles.
        
        Returns:
            Lista de EmployeeDTO con los datos de los empleados
            
        Raises:
            Exception: Si hay un error al consultar la base de datos
        """
        try:
            employees = self.db.query(EmployeesModel).all()
            
            if not employees:
                return []
            
            return [
                EmployeeDTO(
                    id=employee.id,
                    role_id=employee.role_id,
                    name=employee.name,
                    lastname=employee.lastname,
                    email=employee.email
                )
                for employee in employees
            ]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener empleados: {str(e)}")
