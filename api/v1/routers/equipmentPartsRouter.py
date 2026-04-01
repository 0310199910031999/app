from typing import List

from fastapi import APIRouter, Depends, HTTPException

from mainContext.application.dtos.equipment_part_dto import EquipmentPartCreateDTO, EquipmentPartUpdateDTO
from mainContext.application.use_cases.equipment_part_use_cases import (
    CreateEquipmentPart,
    GetEquipmentPartById,
    GetEquipmentPartsByEquipment,
    GetAllEquipmentParts,
    UpdateEquipmentPart,
    DeleteEquipmentPart,
)
from mainContext.infrastructure.dependencies import get_equipment_part_repo
from mainContext.infrastructure.adapters.EquipmentPartRepo import EquipmentPartRepoImpl
from api.v1.schemas.equipment_part import EquipmentPartSchema, EquipmentPartCreateSchema, EquipmentPartUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel


EquipmentPartsRouter = APIRouter(prefix="/equipment-parts", tags=["Equipment Parts"])


@EquipmentPartsRouter.post("/create", response_model=ResponseIntModel)
def create_equipment_part(dto: EquipmentPartCreateSchema, repo: EquipmentPartRepoImpl = Depends(get_equipment_part_repo)):
    use_case = CreateEquipmentPart(repo)
    part_id = use_case.execute(EquipmentPartCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=part_id)


@EquipmentPartsRouter.get("/get/{id}", response_model=EquipmentPartSchema)
def get_equipment_part_by_id(id: int, repo: EquipmentPartRepoImpl = Depends(get_equipment_part_repo)):
    use_case = GetEquipmentPartById(repo)
    part = use_case.execute(id)
    if not part:
        raise HTTPException(status_code=404, detail="Parte de equipo no encontrada")
    return part


@EquipmentPartsRouter.get("/by-equipment/{equipment_id}", response_model=List[EquipmentPartSchema])
def get_equipment_parts_by_equipment(equipment_id: int, repo: EquipmentPartRepoImpl = Depends(get_equipment_part_repo)):
    use_case = GetEquipmentPartsByEquipment(repo)
    return use_case.execute(equipment_id)


@EquipmentPartsRouter.get("/get_all", response_model=List[EquipmentPartSchema])
def get_all_equipment_parts(repo: EquipmentPartRepoImpl = Depends(get_equipment_part_repo)):
    use_case = GetAllEquipmentParts(repo)
    return use_case.execute()


@EquipmentPartsRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_equipment_part(id: int, dto: EquipmentPartUpdateSchema, repo: EquipmentPartRepoImpl = Depends(get_equipment_part_repo)):
    use_case = UpdateEquipmentPart(repo)
    updated = use_case.execute(id, EquipmentPartUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Parte de equipo no encontrada")
    return ResponseBoolModel(result=updated)


@EquipmentPartsRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_equipment_part(id: int, repo: EquipmentPartRepoImpl = Depends(get_equipment_part_repo)):
    use_case = DeleteEquipmentPart(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Parte de equipo no encontrada")
    return ResponseBoolModel(result=deleted)
