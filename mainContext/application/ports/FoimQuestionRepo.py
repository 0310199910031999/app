from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.foim_question_dto import FoimQuestionDTO, FoimQuestionCreateDTO, FoimQuestionUpdateDTO

class FoimQuestionRepo(ABC):
    @abstractmethod
    def create_foim_question(self, dto: FoimQuestionCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_foim_question_by_id(self, id: int) -> Optional[FoimQuestionDTO]:
        pass
    
    @abstractmethod
    def get_all_foim_questions(self) -> List[FoimQuestionDTO]:
        pass
    
    @abstractmethod
    def update_foim_question(self, id: int, dto: FoimQuestionUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_foim_question(self, id: int) -> bool:
        pass
