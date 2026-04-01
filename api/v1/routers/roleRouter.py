from fastapi import APIRouter, Depends, HTTPException
from typing import List

from mainContext.application.dtos.role_dto import RoleCreateDTO, RoleUpdateDTO
from mainContext.application.use_cases.role_use_cases import (
    CreateRole,
    GetRoleById,
    GetAllRoles,
    UpdateRole,
    DeleteRole
)
from mainContext.infrastructure.dependencies import get_role_repo
from mainContext.infrastructure.adapters.RoleRepo import RoleRepoImpl

from api.v1.schemas.role import RoleSchema, RoleCreateSchema, RoleUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

RoleRouter = APIRouter(prefix="/roles", tags=["Roles"])


@RoleRouter.post("/create", response_model=ResponseIntModel)
def create_role(dto: RoleCreateSchema, repo: RoleRepoImpl = Depends(get_role_repo)):
    """
    Crea un nuevo rol
    
    Campo requerido:
    - role_name: Nombre del rol
    """
    use_case = CreateRole(repo)
    role_id = use_case.execute(RoleCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=role_id)


@RoleRouter.get("/get/{id}", response_model=RoleSchema)
def get_role_by_id(id: int, repo: RoleRepoImpl = Depends(get_role_repo)):
    """
    Obtiene un rol por su ID
    """
    use_case = GetRoleById(repo)
    role = use_case.execute(id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@RoleRouter.get("/get_all", response_model=List[RoleSchema])
def get_all_roles(repo: RoleRepoImpl = Depends(get_role_repo)):
    """
    Obtiene todos los roles
    """
    use_case = GetAllRoles(repo)
    return use_case.execute()


@RoleRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_role(id: int, dto: RoleUpdateSchema, repo: RoleRepoImpl = Depends(get_role_repo)):
    """
    Actualiza los datos de un rol
    
    Campo actualizable:
    - role_name: Nombre del rol
    """
    use_case = UpdateRole(repo)
    updated = use_case.execute(id, RoleUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return ResponseBoolModel(result=updated)


@RoleRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_role(id: int, repo: RoleRepoImpl = Depends(get_role_repo)):
    """
    Elimina un rol
    """
    use_case = DeleteRole(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return ResponseBoolModel(result=deleted)
