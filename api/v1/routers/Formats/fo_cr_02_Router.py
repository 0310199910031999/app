from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_cr_02_dto import (
    CreateFOCR02DTO, UpdateFOCR02DTO, FOCR02SignatureDTO, FOCR02TableRowDTO, FOCRAddEquipmentDTO
)
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_cr_02 import (
    CreateFOCR02, UpdateFOCR02, GetFOCR02ById, GetFOCR02Table, DeleteFOCR02, SignFOCR02, GetFOCRAdditionalEquipment
)

# Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_cr_02_repo import FOCR02RepoImpl

# Importing Schemas
from api.v1.schemas.Formats.fo_cr_02 import (
    CreateFOCR02Schema, UpdateFOCR02Schema, FOCR02SignatureSchema, FOCR02TableRowSchema, FOCR02Schema, FOCRAddEquipmentSchema
)
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

FOCR02Router = APIRouter(prefix="/focr02", tags=["FOCR02"])


@FOCR02Router.post("/create", response_model=ResponseIntModel)
def create_focr02(dto: CreateFOCR02Schema, db: Session = Depends(get_db)):
    try:
        repo = FOCR02RepoImpl(db)
        use_case = CreateFOCR02(repo)
        created = use_case.execute(CreateFOCR02DTO(**dto.model_dump()))
        return ResponseIntModel(id=created)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOCR02Router.get("/get_by_id/{id}", response_model=FOCR02Schema)
def get_focr02_by_id(id: int, db: Session = Depends(get_db)):
    try:
        repo = FOCR02RepoImpl(db)
        use_case = GetFOCR02ById(repo)
        focr02 = use_case.execute(id)
        if not focr02:
            raise HTTPException(status_code=404, detail="FOCR02 not found")
        return focr02
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOCR02Router.get("/get_table/", response_model=List[FOCR02TableRowSchema])
def get_focr02_table(db: Session = Depends(get_db)):
    try:
        repo = FOCR02RepoImpl(db)
        use_case = GetFOCR02Table(repo)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOCR02Router.put("/update/{focr02_id}")
def update_focr02(focr02_id: int, dto: UpdateFOCR02Schema, db: Session = Depends(get_db)):
    try:
        repo = FOCR02RepoImpl(db)
        use_case = UpdateFOCR02(repo)
        updated = use_case.execute(focr02_id, UpdateFOCR02DTO(**dto.model_dump(exclude_none=True)))
        if not updated:
            raise HTTPException(status_code=404, detail="FOCR02 not found")
        return ResponseBoolModel(result=updated)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOCR02Router.delete("/delete/{id}")
def delete_focr02(id: int, db: Session = Depends(get_db)):
    try:
        repo = FOCR02RepoImpl(db)
        use_case = DeleteFOCR02(repo)
        deleted = use_case.execute(id)
        return ResponseBoolModel(result=deleted)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOCR02Router.put("/sign/{focr02_id}")
def sign_focr02(focr02_id: int, dto: FOCR02SignatureSchema, db: Session = Depends(get_db)):
    try:
        repo = FOCR02RepoImpl(db)
        use_case = SignFOCR02(repo)
        signed = use_case.execute(focr02_id, FOCR02SignatureDTO(**dto.model_dump()))
        if not signed:
            raise HTTPException(status_code=404, detail="FOCR02 not found")
        return ResponseBoolModel(result=signed)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOCR02Router.get("/additional_equipment/", response_model=List[FOCRAddEquipmentSchema])
def get_focr_additional_equipment(db: Session = Depends(get_db)):
    try:
        repo = FOCR02RepoImpl(db)
        use_case = GetFOCRAdditionalEquipment(repo)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
