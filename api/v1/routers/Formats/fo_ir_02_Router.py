from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_ir_02_dto import CreateFOIR02DTO, UpdateFOIR02DTO, FOIR02SignatureDTO, FOIR02TableRowDTO, FOIR02RequieredEquipment
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_ir_02 import CreateFOIR02, UpdateFOIR02, GetFOIR02ById, GetListFOIR02Table, DeleteFOIR02, SignFOIR02, GetFOIR02RequiredEquipment

# Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_ir_02_repo import FOIR02RepoImpl

# Importing Schemas
from api.v1.schemas.Formats.fo_ir_02 import FOIR02UpdateSchema, FOIR02Schema, FOIR02TableRowSchema, FOIR02CreateSchema, FOIR02SignatureSchema, FOIR02RequiredEquipmentSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

FOIR02Router = APIRouter(prefix="/foir02", tags=["FOIR02"])


@FOIR02Router.post("create", response_model=ResponseIntModel)
def create_foir02(dto: FOIR02CreateSchema, db: Session = Depends(get_db)):
    try:
        repo = FOIR02RepoImpl(db)
        use_case = CreateFOIR02(repo)
        created = use_case.execute(CreateFOIR02DTO(**dto.model_dump(exclude_none=True)))
        return ResponseIntModel(id=created)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIR02Router.get("get_by_id/{id}", response_model=FOIR02Schema)
def get_foir02_by_id(id: int, db: Session = Depends(get_db)):
    try:
        repo = FOIR02RepoImpl(db)
        use_case = GetFOIR02ById(repo)
        foir02 = use_case.execute(id)
        if not foir02:
            raise HTTPException(status_code=404, detail="FOIR02 not found")
        return foir02
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIR02Router.get("get_table/", response_model=List[FOIR02TableRowSchema])
def get_list_foir02_table(db: Session = Depends(get_db)):
    try:
        repo = FOIR02RepoImpl(db)
        use_case = GetListFOIR02Table(repo)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIR02Router.put("update/{foir02_id}")
def update_foir02(foir02_id: int, dto: FOIR02UpdateSchema, db: Session = Depends(get_db)):
    try:
        repo = FOIR02RepoImpl(db)
        use_case = UpdateFOIR02(repo)
        updated = use_case.execute(foir02_id, UpdateFOIR02DTO(**dto.model_dump(exclude_none=True)))
        if not updated:
            raise HTTPException(status_code=404, detail="FOIR02 not found")
        return ResponseBoolModel(result=updated)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIR02Router.delete("delete/{id}")
def delete_foir02(id: int, db: Session = Depends(get_db)):
    try:
        repo = FOIR02RepoImpl(db)
        use_case = DeleteFOIR02(repo)
        deleted = use_case.execute(id)
        return ResponseBoolModel(result=deleted)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIR02Router.put("sign/{foir02_id}")
def sign_foir02(foir02_id: int, dto: FOIR02SignatureSchema, db: Session = Depends(get_db)):
    try:
        repo = FOIR02RepoImpl(db)
        use_case = SignFOIR02(repo)
        signed = use_case.execute(foir02_id, FOIR02SignatureDTO(**dto.model_dump(exclude_none=True)))
        if not signed:
            raise HTTPException(status_code=404, detail="FOIR02 not found")
        return ResponseBoolModel(result=signed)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOIR02Router.get("required_equipment/", response_model=List[FOIR02RequiredEquipmentSchema])
def get_foir02_required_equipment(db: Session = Depends(get_db)):
    try:
        repo = FOIR02RepoImpl(db)
        use_case = GetFOIR02RequiredEquipment(repo)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
