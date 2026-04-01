from fastapi import APIRouter, Depends, HTTPException
from typing import List

from mainContext.application.dtos.foir02_required_equipment_dto import Foir02RequiredEquipmentCreateDTO, Foir02RequiredEquipmentUpdateDTO
from mainContext.application.use_cases.foir02_required_equipment_use_cases import (
    CreateFoir02RequiredEquipment,
    GetFoir02RequiredEquipmentById,
    GetAllFoir02RequiredEquipment,
    UpdateFoir02RequiredEquipment,
    DeleteFoir02RequiredEquipment
)
from mainContext.infrastructure.dependencies import get_foir02_required_equipment_repo
from mainContext.infrastructure.adapters.Foir02RequiredEquipmentRepo import Foir02RequiredEquipmentRepoImpl

from api.v1.schemas.foir02_required_equipment import Foir02RequiredEquipmentSchema, Foir02RequiredEquipmentCreateSchema, Foir02RequiredEquipmentUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

Foir02RequiredEquipmentRouter = APIRouter(prefix="/foir02-required-equipment", tags=["FOIR02 Required Equipment"])


@Foir02RequiredEquipmentRouter.post("/create", response_model=ResponseIntModel)
def create_foir02_required_equipment(dto: Foir02RequiredEquipmentCreateSchema, repo: Foir02RequiredEquipmentRepoImpl = Depends(get_foir02_required_equipment_repo)):
    """
    Crea un nuevo equipo requerido FOIR02
    
    Campos requeridos:
    - amount: Cantidad
    - unit: Unidad
    - type: Tipo
    - name: Nombre
    """
    use_case = CreateFoir02RequiredEquipment(repo)
    foir02_required_equipment_id = use_case.execute(Foir02RequiredEquipmentCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=foir02_required_equipment_id)


@Foir02RequiredEquipmentRouter.get("/get/{id}", response_model=Foir02RequiredEquipmentSchema)
def get_foir02_required_equipment_by_id(id: int, repo: Foir02RequiredEquipmentRepoImpl = Depends(get_foir02_required_equipment_repo)):
    """
    Obtiene un equipo requerido FOIR02 por su ID
    """
    use_case = GetFoir02RequiredEquipmentById(repo)
    foir02_required_equipment = use_case.execute(id)
    if not foir02_required_equipment:
        raise HTTPException(status_code=404, detail="FOIR02 Required Equipment not found")
    return foir02_required_equipment


@Foir02RequiredEquipmentRouter.get("/get_all", response_model=List[Foir02RequiredEquipmentSchema])
def get_all_foir02_required_equipment(repo: Foir02RequiredEquipmentRepoImpl = Depends(get_foir02_required_equipment_repo)):
    """
    Obtiene todos los equipos requeridos FOIR02
    """
    use_case = GetAllFoir02RequiredEquipment(repo)
    return use_case.execute()


@Foir02RequiredEquipmentRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_foir02_required_equipment(id: int, dto: Foir02RequiredEquipmentUpdateSchema, repo: Foir02RequiredEquipmentRepoImpl = Depends(get_foir02_required_equipment_repo)):
    """
    Actualiza los datos de un equipo requerido FOIR02
    
    Campos actualizables:
    - amount: Cantidad
    - unit: Unidad
    - type: Tipo
    - name: Nombre
    """
    use_case = UpdateFoir02RequiredEquipment(repo)
    updated = use_case.execute(id, Foir02RequiredEquipmentUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOIR02 Required Equipment not found")
    return ResponseBoolModel(result=updated)


@Foir02RequiredEquipmentRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_foir02_required_equipment(id: int, repo: Foir02RequiredEquipmentRepoImpl = Depends(get_foir02_required_equipment_repo)):
    """
    Elimina un equipo requerido FOIR02
    """
    use_case = DeleteFoir02RequiredEquipment(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="FOIR02 Required Equipment not found")
    return ResponseBoolModel(result=deleted)
