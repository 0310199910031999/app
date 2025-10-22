from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.Formats.fo_bc_01_dto import FOBC01CreateDTO, FOBC01UpdateDTO, FOBC01SignatureDTO

from mainContext.application.use_cases.Formats.fo_bc_01 import CreateFOBC01, UpdateFOBC01, GetFOBC01ById, DeleteFOBC01, SignFOBC01, GetListFOBC01Table

from mainContext.infrastructure.adapters.Formats.fo_bc_01_repo import FOBC01RepoImpl
from api.v1.schemas.Formats.fo_bc_01 import FOBC01UpdateSchema, FOBC01Schema, FOBC01TableRowSchema, FOBC01CreateSchema, FOBC01SignatureSchema

from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel

FOBC01Router = APIRouter(prefix="/fobc01", tags=["FOBC01"])

@FOBC01Router.post("create", response_model=ResponseIntModel)
def create_fobc01(dto: FOBC01CreateSchema, db: Session = Depends(get_db)):
    repo = FOBC01RepoImpl(db)
    use_case = CreateFOBC01(repo)
    created = use_case.execute(FOBC01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOBC01Router.get("get_by_id/{id}", response_model=FOBC01Schema)
def get_fobc01_by_id(id : int, db: Session = Depends(get_db)):
    repo = FOBC01RepoImpl(db)
    use_case = GetFOBC01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOBC01 not found")
    return get

@FOBC01Router.get("get_table/{equipment_id}", response_model=List[FOBC01TableRowSchema])
def get_list_fobc01_table(equipment_id: int, db: Session = Depends(get_db)):
    repo = FOBC01RepoImpl(db)
    use_case = GetListFOBC01Table(repo)
    return use_case.execute(equipment_id)

@FOBC01Router.put("update/{fobc01_id}")
def update_fobc01(fobc01_id: int, dto: FOBC01UpdateSchema, db: Session = Depends(get_db)):
    repo = FOBC01RepoImpl(db)
    use_case = UpdateFOBC01(repo)
    updated = use_case.execute(fobc01_id, FOBC01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOBC01 not found")
    return ResponseBoolModel(result=updated)

@FOBC01Router.delete("delete/{id}")
def delete_fobc01(id: int, db: Session = Depends(get_db)):
    repo = FOBC01RepoImpl(db)
    use_case = DeleteFOBC01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOBC01Router.put("sign/{fobc01_id}")
def sign_fobc01(fobc01_id: int, dto: FOBC01SignatureSchema, db: Session = Depends(get_db)):
    repo = FOBC01RepoImpl(db)
    use_case = SignFOBC01(repo)
    signed = use_case.execute(fobc01_id, FOBC01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOBC01 not found")
    return ResponseBoolModel(result=signed)