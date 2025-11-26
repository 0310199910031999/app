from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO
from mainContext.application.use_cases.employee_use_cases import (
    CreateEmployee,
    GetEmployeeById,
    GetAllEmployees,
    UpdateEmployee,
    DeleteEmployee
)
from mainContext.infrastructure.adapters.EmployeeRepo import EmployeeRepoImpl

from api.v1.schemas.employee import EmployeeSchema, EmployeeCreateSchema, EmployeeUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

EmployeeRouter = APIRouter(prefix="/employees", tags=["Employees"])


@EmployeeRouter.post("/create", response_model=ResponseIntModel)
def create_employee(dto: EmployeeCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo empleado
    
    Campos requeridos:
    - role_id: ID del rol
    - name: Nombre
    - lastname: Apellido
    - email: Correo electrónico
    - password: Contraseña
    """
    repo = EmployeeRepoImpl(db)
    use_case = CreateEmployee(repo)
    employee_id = use_case.execute(EmployeeCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=employee_id)


@EmployeeRouter.get("/get/{id}", response_model=EmployeeSchema)
def get_employee_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un empleado por su ID
    """
    repo = EmployeeRepoImpl(db)
    use_case = GetEmployeeById(repo)
    employee = use_case.execute(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@EmployeeRouter.get("/get_all", response_model=List[EmployeeSchema])
def get_all_employees(db: Session = Depends(get_db)):
    """
    Obtiene todos los empleados con sus roles
    """
    repo = EmployeeRepoImpl(db)
    use_case = GetAllEmployees(repo)
    return use_case.execute()


@EmployeeRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_employee(id: int, dto: EmployeeUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un empleado
    
    Campos actualizables:
    - role_id: ID del rol
    - name: Nombre
    - lastname: Apellido
    - email: Correo electrónico
    - password: Contraseña
    - session_token: Token de sesión
    """
    repo = EmployeeRepoImpl(db)
    use_case = UpdateEmployee(repo)
    updated = use_case.execute(id, EmployeeUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return ResponseBoolModel(result=updated)


@EmployeeRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_employee(id: int, db: Session = Depends(get_db)):
    """
    Elimina un empleado
    """
    repo = EmployeeRepoImpl(db)
    use_case = DeleteEmployee(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return ResponseBoolModel(result=deleted)
