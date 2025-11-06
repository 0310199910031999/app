from fastapi import APIRouter, Depends
from typing import List 
from sqlalchemy.orm import Session 
from api.v1.schemas.create_documents import CreateDTO
from shared.db import get_db
from mainContext.application.use_cases.create_documents_use_case import CreateDocuments
from mainContext.infrastructure.adapters.CreateDocumentsRepo import CreateDocumentsRepoImpl

CreateDocumentsRouter = APIRouter(prefix="/createDocuments", tags=["CreateDocuments"])

@CreateDocumentsRouter.post("/")
def create_documents(create_dto: CreateDTO, db: Session = Depends(get_db)):
    repo = CreateDocumentsRepoImpl(db)
    use_case = CreateDocuments(repo)
    return use_case.execute(create_dto)