from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
from mainContext.application.dtos.Equipment.create_equipment_dto import CreateEquipmentDTO
from mainContext.application.use_cases.Equipment.list_equipment_by_client import ListEquipmentByClient
from mainContext.application.use_cases.Equipment.get_equipment_by_id import GetEquipmentById
from mainContext.application.use_cases.Equipment.create_equipment import CreateEquipment
from mainContext.application.use_cases.Equipment.delete_equipment import DeleteEquipment
from mainContext.application.dtos.Equipment.update_equipment_dto import UpdateEquipmentDTO
from mainContext.application.use_cases.Equipment.update_equipment import UpdateEquipmentUseCase
from mainContext.application.use_cases.Equipment.get_brands_and_types import GetBrandsAndTypes
from mainContext.application.use_cases.Equipment.get_equipment_by_property import GetEquipmentByProperty


# Importing Infrastructure Layer
from mainContext.infrastructure.adapters.EquipmentRepo import EquipmentRepoImpl

# Importing Schemas 
from api.v1.schemas.equipment import EquipmentSchema, BrandsTypesSchema




equipmentRouter = APIRouter(prefix="/equipment", tags=["Equipment"])

@equipmentRouter.get("/byClient/{client_id}", response_model=List[EquipmentSchema])
def list_equipment_by_client(client_id: int, db: Session = Depends(get_db)):
    repo = EquipmentRepoImpl(db)
    use_case = ListEquipmentByClient(repo)
    return use_case.execute(client_id)

@equipmentRouter.get("/brandsAndTypes", response_model=BrandsTypesSchema)
def get_brands_and_types(db: Session = Depends(get_db)):
    repo = EquipmentRepoImpl(db)
    use_case = GetBrandsAndTypes(repo)
    return use_case.execute()

@equipmentRouter.get("/byProperty/{property}", response_model=List[EquipmentSchema])
def get_equipment_by_property(property: str, db: Session = Depends(get_db)):
    repo = EquipmentRepoImpl(db)
    use_case = GetEquipmentByProperty(repo)
    return use_case.execute(property)


@equipmentRouter.get("/{equipment_id}", response_model=EquipmentSchema)
def get_equipment_by_id(equipment_id: int, db: Session = Depends(get_db)):
    repo = EquipmentRepoImpl(db)
    use_case = GetEquipmentById(repo)
    return use_case.execute(equipment_id)

@equipmentRouter.post("/", response_model=EquipmentSchema)
def create_equipment(dto: CreateEquipmentDTO, db: Session = Depends(get_db)):
    repo = EquipmentRepoImpl(db)
    use_case = CreateEquipment(repo)
    return use_case.execute(dto)

@equipmentRouter.delete("/{equipment_id}", response_model=bool)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    repo = EquipmentRepoImpl(db)
    use_case = DeleteEquipment(repo)
    return use_case.execute(equipment_id)

@equipmentRouter.put("/{equipment_id}", response_model=EquipmentSchema)
def update_equipment(equipment_id: int, dto: UpdateEquipmentDTO, db: Session = Depends(get_db)):
    repo = EquipmentRepoImpl(db)
    use_case = UpdateEquipmentUseCase(repo)
    update = use_case.execute(equipment_id, dto)
    if not update:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return update
