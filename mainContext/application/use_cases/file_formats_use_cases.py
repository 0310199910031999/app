from typing import List
from mainContext.application.ports.FileFormatsRepo import FileFormatsRepo
from mainContext.application.dtos.file_formats_dto import FileFormatDTO


class GetFormatsByFile:
    """Use case para obtener todos los formatos asociados a un file"""
    
    def __init__(self, repo: FileFormatsRepo):
        self.repo = repo
    
    def execute(self, file_id: str) -> List[FileFormatDTO]:
        """
        Ejecuta el caso de uso para obtener formatos por file_id
        
        Args:
            file_id: ID del file
            
        Returns:
            Lista de FileFormatDTO con todos los formatos asociados
        """
        return self.repo.get_formats_by_file(file_id)
