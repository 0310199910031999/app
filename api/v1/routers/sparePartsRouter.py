from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shared.db import get_db
from mainContext.application.dtos.spare_part_dto import SparePartCreateDTO, SparePartUpdateDTO
from mainContext.application.use_cases.spare_part_use_cases import (
    CreateSparePart,
    GetSparePartById,
    GetAllSpareParts,
    UpdateSparePart,
    DeleteSparePart,
)
from mainContext.infrastructure.adapters.SparePartRepo import SparePartRepoImpl
from api.v1.schemas.spare_part import SparePartSchema, SparePartCreateSchema, SparePartUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

SparePartsRouter = APIRouter(prefix="/spare-parts", tags=["Spare Parts"])


@SparePartsRouter.post("/create", response_model=ResponseIntModel)
def create_spare_part(dto: SparePartCreateSchema, db: Session = Depends(get_db)):
    repo = SparePartRepoImpl(db)
    use_case = CreateSparePart(repo)
    spare_part_id = use_case.execute(SparePartCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=spare_part_id)


@SparePartsRouter.get("/get/{id}", response_model=SparePartSchema)
def get_spare_part_by_id(id: int, db: Session = Depends(get_db)):
    repo = SparePartRepoImpl(db)
    use_case = GetSparePartById(repo)
    spare_part = use_case.execute(id)
    if not spare_part:
        raise HTTPException(status_code=404, detail="Refacción no encontrada")
    return spare_part


@SparePartsRouter.get("/get_all", response_model=List[SparePartSchema])
def get_all_spare_parts(db: Session = Depends(get_db)):
    repo = SparePartRepoImpl(db)
    use_case = GetAllSpareParts(repo)
    return use_case.execute()


@SparePartsRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_spare_part(id: int, dto: SparePartUpdateSchema, db: Session = Depends(get_db)):
    repo = SparePartRepoImpl(db)
    use_case = UpdateSparePart(repo)
    updated = use_case.execute(id, SparePartUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Refacción no encontrada")
    return ResponseBoolModel(result=updated)


@SparePartsRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_spare_part(id: int, db: Session = Depends(get_db)):
    repo = SparePartRepoImpl(db)
    use_case = DeleteSparePart(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Refacción no encontrada")
    return ResponseBoolModel(result=deleted)
