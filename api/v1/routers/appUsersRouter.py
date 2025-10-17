from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from shared.db import get_db 
from mainContext.infrastructure.adapters.AppUserWithClientRepo import AppUserWithClientRepo
from mainContext.application.use_cases.listAppUserWithClient import ListAppUserWithClient

AppUserRouter = APIRouter(prefix="/appUsers", tags=["AppUsers"])

@AppUserRouter.get("/withClient", response_model=List[dict])
def list_app_users_with_client(db: Session = Depends(get_db)):
    repo = AppUserWithClientRepo(db)
    use_case = ListAppUserWithClient(repo)
    return use_case.execute()