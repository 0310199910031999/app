from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_ir_ro_combined_dto import CreateFOIRROCombinedDTO, FOIRROCombinedResponse, VehicleDTO, EmployeeDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_ir_ro_combined import CreateFOIRROCombined, GetVehicles, GetEmployees

# Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_ir_ro_combined_repo import FOIRROCombinedRepoImpl

# Importing Schemas
from api.v1.schemas.Formats.fo_ir_ro_combined import CreateFOIRROCombinedSchema, FOIRROCombinedResponseSchema, VehicleSchema, EmployeeSchema

FOIRROCombinedRouter = APIRouter(prefix="/foir-ro-combined", tags=["FOIR-RO-Combined"])


@FOIRROCombinedRouter.post("/create", response_model=FOIRROCombinedResponseSchema)
def create_foir_and_foro(dto: CreateFOIRROCombinedSchema, db: Session = Depends(get_db)):
    """
    Crea simultáneamente un registro FO-IR-02 y un registro FO-RO-05.
    
    Ambos registros compartirán:
    - El mismo vehicle_id
    - El mismo employee_id
    - La misma route_date
    - El mismo status
    
    El FO-RO-05 se crea con checklists iniciales vacíos (todos en False).
    
    Args:
        dto: Datos necesarios para crear ambos registros
        db: Sesión de base de datos
        
    Returns:
        FOIRROCombinedResponseSchema con los IDs de ambos registros creados
        
    Raises:
        HTTPException 400: Si hay un error en la creación
    """
    try:
        repo = FOIRROCombinedRepoImpl(db)
        use_case = CreateFOIRROCombined(repo)
        result = use_case.execute(CreateFOIRROCombinedDTO(**dto.model_dump(exclude_none=True)))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIRROCombinedRouter.get("/vehicles", response_model=List[VehicleSchema])
def get_vehicles(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los vehículos disponibles.
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        Lista de VehicleSchema con los datos de todos los vehículos
        
    Raises:
        HTTPException 400: Si hay un error al obtener los vehículos
    """
    try:
        repo = FOIRROCombinedRepoImpl(db)
        use_case = GetVehicles(repo)
        vehicles = use_case.execute()
        return vehicles
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIRROCombinedRouter.get("/employees", response_model=List[EmployeeSchema])
def get_employees(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los empleados disponibles.
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        Lista de EmployeeSchema con los datos de todos los empleados
        
    Raises:
        HTTPException 400: Si hay un error al obtener los empleados
    """
    try:
        repo = FOIRROCombinedRepoImpl(db)
        use_case = GetEmployees(repo)
        employees = use_case.execute()
        return employees
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
