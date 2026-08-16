from mainContext.application.ports.AppVersionRepo import AppVersionRepo
from mainContext.application.dtos.app_version_dto import AppVersionDTO, AppVersionCreateDTO, AppVersionUpdateDTO
from typing import List, Optional

class CreateAppVersion:
    def __init__(self, repo: AppVersionRepo):
        self.repo = repo

    def execute(self, dto: AppVersionCreateDTO) -> int:
        return self.repo.create_app_version(dto)

class GetAppVersionById:
    def __init__(self, repo: AppVersionRepo):
        self.repo = repo

    def execute(self, id: int) -> Optional[AppVersionDTO]:
        return self.repo.get_app_version_by_id(id)

class GetAllAppVersions:
    def __init__(self, repo: AppVersionRepo):
        self.repo = repo

    def execute(self) -> List[AppVersionDTO]:
        return self.repo.get_all_app_versions()

class UpdateAppVersion:
    def __init__(self, repo: AppVersionRepo):
        self.repo = repo

    def execute(self, id: int, dto: AppVersionUpdateDTO) -> bool:
        return self.repo.update_app_version(id, dto)

class DeleteAppVersion:
    def __init__(self, repo: AppVersionRepo):
        self.repo = repo

    def execute(self, id: int) -> bool:
        return self.repo.delete_app_version(id)

class CheckVersion:
    def __init__(self, repo: AppVersionRepo):
        self.repo = repo

    def execute(self, version: float) -> bool:
        latest = self.repo.get_latest_version_number()
        if latest is None:
            return True
        return version >= latest
