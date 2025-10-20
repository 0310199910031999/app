from typing import List
from mainContext.application.ports.AppUserRepo import AppUserRepo

class ListAppUserWithClient:
    def __init__(self, app_user_repo: AppUserRepo):
        self.app_user_repo = app_user_repo

    def execute(self) -> List[dict]:
        return self.app_user_repo.listWithClientName()