from fastapi import APIRouter, Depends
from typing import List 
from api.v1.schemas.create_documents import CreateDTO
from mainContext.application.use_cases.create_documents_use_case import CreateDocuments
from mainContext.infrastructure.dependencies import get_create_documents_repo
from mainContext.infrastructure.adapters.CreateDocumentsRepo import CreateDocumentsRepoImpl

CreateDocumentsRouter = APIRouter(prefix="/createDocuments", tags=["CreateDocuments"])

@CreateDocumentsRouter.post("/")
def create_documents(create_dto: CreateDTO, repo: CreateDocumentsRepoImpl = Depends(get_create_documents_repo)):
    use_case = CreateDocuments(repo)
    return use_case.execute(create_dto)