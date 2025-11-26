from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.equipment_brand_dto import EquipmentBrandCreateDTO, EquipmentBrandUpdateDTO
from mainContext.application.use_cases.equipment_brand_use_cases import (
    CreateEquipmentBrand,
    GetEquipmentBrandById,
    GetAllEquipmentBrands,
    UpdateEquipmentBrand,
    DeleteEquipmentBrand
)
from mainContext.infrastructure.adapters.EquipmentBrandRepo import EquipmentBrandRepoImpl

from api.v1.schemas.equipment_brand import EquipmentBrandSchema, EquipmentBrandCreateSchema, EquipmentBrandUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

EquipmentBrandRouter = APIRouter(prefix="/equipment-brands", tags=["Equipment Brands"])


@EquipmentBrandRouter.post("/create", response_model=ResponseIntModel)
def create_equipment_brand(dto: EquipmentBrandCreateSchema, db: Session = Depends(get_db)):
    """
    Crea una nueva marca de equipo
    
    Campos requeridos:
    - name: Nombre de la marca
    - img_path: Ruta de la imagen (opcional)
    """
    repo = EquipmentBrandRepoImpl(db)
    use_case = CreateEquipmentBrand(repo)
    equipment_brand_id = use_case.execute(EquipmentBrandCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=equipment_brand_id)


@EquipmentBrandRouter.get("/get/{id}", response_model=EquipmentBrandSchema)
def get_equipment_brand_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una marca de equipo por su ID
    """
    repo = EquipmentBrandRepoImpl(db)
    use_case = GetEquipmentBrandById(repo)
    equipment_brand = use_case.execute(id)
    if not equipment_brand:
        raise HTTPException(status_code=404, detail="Equipment Brand not found")
    return equipment_brand


@EquipmentBrandRouter.get("/get_all", response_model=List[EquipmentBrandSchema])
def get_all_equipment_brands(db: Session = Depends(get_db)):
    """
    Obtiene todas las marcas de equipo
    """
    repo = EquipmentBrandRepoImpl(db)
    use_case = GetAllEquipmentBrands(repo)
    return use_case.execute()


@EquipmentBrandRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_equipment_brand(id: int, dto: EquipmentBrandUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de una marca de equipo
    
    Campos actualizables:
    - name: Nombre de la marca
    - img_path: Ruta de la imagen
    """
    repo = EquipmentBrandRepoImpl(db)
    use_case = UpdateEquipmentBrand(repo)
    updated = use_case.execute(id, EquipmentBrandUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Equipment Brand not found")
    return ResponseBoolModel(result=updated)


@EquipmentBrandRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_equipment_brand(id: int, db: Session = Depends(get_db)):
    """
    Elimina una marca de equipo
    """
    repo = EquipmentBrandRepoImpl(db)
    use_case = DeleteEquipmentBrand(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipment Brand not found")
    return ResponseBoolModel(result=deleted)
