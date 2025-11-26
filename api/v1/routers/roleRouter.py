from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.role_dto import RoleCreateDTO, RoleUpdateDTO
from mainContext.application.use_cases.role_use_cases import (
    CreateRole,
    GetRoleById,
    GetAllRoles,
    UpdateRole,
    DeleteRole
)
from mainContext.infrastructure.adapters.RoleRepo import RoleRepoImpl

from api.v1.schemas.role import RoleSchema, RoleCreateSchema, RoleUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

RoleRouter = APIRouter(prefix="/roles", tags=["Roles"])


@RoleRouter.post("/create", response_model=ResponseIntModel)
def create_role(dto: RoleCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo rol
    
    Campo requerido:
    - role_name: Nombre del rol
    """
    repo = RoleRepoImpl(db)
    use_case = CreateRole(repo)
    role_id = use_case.execute(RoleCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=role_id)


@RoleRouter.get("/get/{id}", response_model=RoleSchema)
def get_role_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un rol por su ID
    """
    repo = RoleRepoImpl(db)
    use_case = GetRoleById(repo)
    role = use_case.execute(id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@RoleRouter.get("/get_all", response_model=List[RoleSchema])
def get_all_roles(db: Session = Depends(get_db)):
    """
    Obtiene todos los roles
    """
    repo = RoleRepoImpl(db)
    use_case = GetAllRoles(repo)
    return use_case.execute()


@RoleRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_role(id: int, dto: RoleUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un rol
    
    Campo actualizable:
    - role_name: Nombre del rol
    """
    repo = RoleRepoImpl(db)
    use_case = UpdateRole(repo)
    updated = use_case.execute(id, RoleUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return ResponseBoolModel(result=updated)


@RoleRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_role(id: int, db: Session = Depends(get_db)):
    """
    Elimina un rol
    """
    repo = RoleRepoImpl(db)
    use_case = DeleteRole(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return ResponseBoolModel(result=deleted)
