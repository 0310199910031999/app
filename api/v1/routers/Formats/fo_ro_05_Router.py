from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_ro_05_dto import FORO05CreateDTO, FORO05UpdateDTO, FORO05SignatureDTO, FORO05TableRowDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_ro_05 import CreateFORO05, UpdateFORO05, GetFORO05ById, GetListFORO05Table, DeleteFORO05, SignFORO05

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_ro_05_repo import FORO05RepoImpl

#importing Schemas
from api.v1.schemas.Formats.fo_ro_05 import FORO05UpdateSchema, FORO05Schema, FORO05TableRowSchema, FORO05CreateSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel

FORO05Router = APIRouter(prefix="/foro05", tags=["FORO05"])

@FORO05Router.post("create", response_model=ResponseIntModel)
def create_foro05(dto: FORO05CreateSchema, db: Session = Depends(get_db)):
    repo = FORO05RepoImpl(db)
    use_case = CreateFORO05(repo)
    created = use_case.execute(FORO05CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FORO05Router.get("get_by_id/{id}", response_model=FORO05Schema)
def get_foro05_by_id(id : int, db: Session = Depends(get_db)):
    repo = FORO05RepoImpl(db)
    use_case = GetFORO05ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FORO05 not found")
    return get

@FORO05Router.get("get_table/", response_model=List[FORO05TableRowSchema])
def get_list_foro05_table(db: Session = Depends(get_db)):
    repo = FORO05RepoImpl(db)
    use_case = GetListFORO05Table(repo)
    return use_case.execute()

@FORO05Router.put("update/{foro05_id}")
def update_foro05(foro05_id: int, dto: FORO05UpdateSchema, db: Session = Depends(get_db)):
    repo = FORO05RepoImpl(db)
    use_case = UpdateFORO05(repo)
    updated = use_case.execute(foro05_id, FORO05UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FORO05 not found")
    return ResponseBoolModel(result=updated)

@FORO05Router.delete("delete/{id}")
def delete_foro05(id: int, db: Session = Depends(get_db)):
    repo = FORO05RepoImpl(db)
    use_case = DeleteFORO05(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FORO05Router.put("sign/{foro05_id}")
def sign_foro05(foro05_id: int, dto: FORO05SignatureDTO, db: Session = Depends(get_db)):
    repo = FORO05RepoImpl(db)
    use_case = SignFORO05(repo)
    signed = use_case.execute(foro05_id, FORO05SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FORO05 not found")
    return ResponseBoolModel(result=signed)
