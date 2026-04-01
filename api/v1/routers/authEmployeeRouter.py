from fastapi import APIRouter, Depends
from typing import List 
from api.v1.schemas.auth_employee import AuthEmployeeDTO, EmployeeAuthResponseDTO
from mainContext.infrastructure.dependencies import get_auth_employee_repo
from mainContext.infrastructure.adapters.AuthEmployeeRepo import AuthEmployeeRepoImpl
from mainContext.application.use_cases.auth_employe_use_case import AuthEmployee

AuthEmployeeRouter = APIRouter(prefix="/auth", tags=["Auth"])

@AuthEmployeeRouter.post("/", response_model= EmployeeAuthResponseDTO)
def auth_employee(auth_dto: AuthEmployeeDTO, repo: AuthEmployeeRepoImpl = Depends(get_auth_employee_repo)):
    use_case = AuthEmployee(repo)
    return use_case.execute(auth_dto)