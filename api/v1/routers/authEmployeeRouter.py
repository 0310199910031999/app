from fastapi import APIRouter, Depends
from typing import List 
from sqlalchemy.orm import Session 
from api.v1.schemas.auth_employee import AuthEmployeeDTO, EmployeeAuthResponseDTO
from shared.db import get_db
from mainContext.application.use_cases.auth_employe_use_case import AuthEmployee
from mainContext.infrastructure.adapters.AuthEmployeeRepo import AuthEmployeeRepoImpl

AuthEmployeeRouter = APIRouter(prefix="/auth", tags=["Auth"])

@AuthEmployeeRouter.post("/", response_model= EmployeeAuthResponseDTO)
def auth_employee(auth_dto: AuthEmployeeDTO, db: Session = Depends(get_db)):
    repo = AuthEmployeeRepoImpl(db)
    use_case = AuthEmployee(repo)
    return use_case.execute(auth_dto)