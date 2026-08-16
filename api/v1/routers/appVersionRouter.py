from fastapi import APIRouter, Depends, HTTPException
from typing import List

from mainContext.application.dtos.app_version_dto import AppVersionCreateDTO, AppVersionUpdateDTO
from mainContext.application.use_cases.app_version_use_cases import (
    CreateAppVersion,
    GetAppVersionById,
    GetAllAppVersions,
    UpdateAppVersion,
    DeleteAppVersion,
    CheckVersion
)
from mainContext.infrastructure.dependencies import get_app_version_repo
from mainContext.infrastructure.adapters.AppVersionRepo import AppVersionRepoImpl

from api.v1.schemas.app_version import AppVersionSchema, AppVersionCreateSchema, AppVersionUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

AppVersionRouter = APIRouter(prefix="/app-versions", tags=["App Versions"])


@AppVersionRouter.post("/create", response_model=ResponseIntModel)
def create_app_version(dto: AppVersionCreateSchema, repo: AppVersionRepoImpl = Depends(get_app_version_repo)):
    use_case = CreateAppVersion(repo)
    version_id = use_case.execute(AppVersionCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=version_id)


@AppVersionRouter.get("/get/{id}", response_model=AppVersionSchema)
def get_app_version_by_id(id: int, repo: AppVersionRepoImpl = Depends(get_app_version_repo)):
    use_case = GetAppVersionById(repo)
    version = use_case.execute(id)
    if not version:
        raise HTTPException(status_code=404, detail="App version not found")
    return version


@AppVersionRouter.get("/get_all", response_model=List[AppVersionSchema])
def get_all_app_versions(repo: AppVersionRepoImpl = Depends(get_app_version_repo)):
    use_case = GetAllAppVersions(repo)
    return use_case.execute()


@AppVersionRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_app_version(id: int, dto: AppVersionUpdateSchema, repo: AppVersionRepoImpl = Depends(get_app_version_repo)):
    use_case = UpdateAppVersion(repo)
    updated = use_case.execute(id, AppVersionUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="App version not found")
    return ResponseBoolModel(result=updated)


@AppVersionRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_app_version(id: int, repo: AppVersionRepoImpl = Depends(get_app_version_repo)):
    use_case = DeleteAppVersion(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="App version not found")
    return ResponseBoolModel(result=deleted)


@AppVersionRouter.get("/check_version/{version}", response_model=ResponseBoolModel)
def check_version(version: float, repo: AppVersionRepoImpl = Depends(get_app_version_repo)):
    use_case = CheckVersion(repo)
    result = use_case.execute(version)
    return ResponseBoolModel(result=result)
