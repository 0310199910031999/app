from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.equipment_type_dto import EquipmentTypeCreateDTO, EquipmentTypeUpdateDTO
from mainContext.application.use_cases.equipment_type_use_cases import (
    CreateEquipmentType,
    GetEquipmentTypeById,
    GetAllEquipmentTypes,
    UpdateEquipmentType,
    DeleteEquipmentType
)
from mainContext.infrastructure.adapters.EquipmentTypeRepo import EquipmentTypeRepoImpl

from api.v1.schemas.equipment_type import EquipmentTypeSchema, EquipmentTypeCreateSchema, EquipmentTypeUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

EquipmentTypeRouter = APIRouter(prefix="/equipment-types", tags=["Equipment Types"])


@EquipmentTypeRouter.post("/create", response_model=ResponseIntModel)
def create_equipment_type(dto: EquipmentTypeCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo tipo de equipo
    
    Campo requerido:
    - name: Nombre del tipo de equipo
    """
    repo = EquipmentTypeRepoImpl(db)
    use_case = CreateEquipmentType(repo)
    equipment_type_id = use_case.execute(EquipmentTypeCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=equipment_type_id)


@EquipmentTypeRouter.get("/get/{id}", response_model=EquipmentTypeSchema)
def get_equipment_type_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un tipo de equipo por su ID
    """
    repo = EquipmentTypeRepoImpl(db)
    use_case = GetEquipmentTypeById(repo)
    equipment_type = use_case.execute(id)
    if not equipment_type:
        raise HTTPException(status_code=404, detail="Equipment Type not found")
    return equipment_type


@EquipmentTypeRouter.get("/get_all", response_model=List[EquipmentTypeSchema])
def get_all_equipment_types(db: Session = Depends(get_db)):
    """
    Obtiene todos los tipos de equipo
    """
    repo = EquipmentTypeRepoImpl(db)
    use_case = GetAllEquipmentTypes(repo)
    return use_case.execute()


@EquipmentTypeRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_equipment_type(id: int, dto: EquipmentTypeUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un tipo de equipo
    
    Campo actualizable:
    - name: Nombre del tipo de equipo
    """
    repo = EquipmentTypeRepoImpl(db)
    use_case = UpdateEquipmentType(repo)
    updated = use_case.execute(id, EquipmentTypeUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Equipment Type not found")
    return ResponseBoolModel(result=updated)


@EquipmentTypeRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_equipment_type(id: int, db: Session = Depends(get_db)):
    """
    Elimina un tipo de equipo
    """
    repo = EquipmentTypeRepoImpl(db)
    use_case = DeleteEquipmentType(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipment Type not found")
    return ResponseBoolModel(result=deleted)
