from mainContext.application.ports.FoimQuestionRepo import FoimQuestionRepo
from mainContext.application.dtos.foim_question_dto import FoimQuestionDTO, FoimQuestionCreateDTO, FoimQuestionUpdateDTO
from typing import List, Optional

class CreateFoimQuestion:
    def __init__(self, repo: FoimQuestionRepo):
        self.repo = repo
    
    def execute(self, dto: FoimQuestionCreateDTO) -> int:
        return self.repo.create_foim_question(dto)

class GetFoimQuestionById:
    def __init__(self, repo: FoimQuestionRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[FoimQuestionDTO]:
        return self.repo.get_foim_question_by_id(id)

class GetAllFoimQuestions:
    def __init__(self, repo: FoimQuestionRepo):
        self.repo = repo
    
    def execute(self) -> List[FoimQuestionDTO]:
        return self.repo.get_all_foim_questions()

class UpdateFoimQuestion:
    def __init__(self, repo: FoimQuestionRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: FoimQuestionUpdateDTO) -> bool:
        return self.repo.update_foim_question(id, dto)

class DeleteFoimQuestion:
    def __init__(self, repo: FoimQuestionRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_foim_question(id)
