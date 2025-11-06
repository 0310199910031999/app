from typing import List
from mainContext.application.dtos.create_documents_dto import CreateDTO
from mainContext.application.ports.CreateDocumentsRepo import CreateDocumentsRepo

class CreateDocuments:
    def __init__(self, create_documents_repo: CreateDocumentsRepo):
        self.create_documents_repo = create_documents_repo

    def execute(self, create_dto: CreateDTO) -> bool:
        return self.create_documents_repo.create_documents(create_dto)