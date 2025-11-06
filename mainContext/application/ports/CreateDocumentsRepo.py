from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.create_documents_dto import CreateDTO

class CreateDocumentsRepo(ABC):
    @abstractmethod
    def create_documents(self, create_dto: CreateDTO) -> bool:
        pass
