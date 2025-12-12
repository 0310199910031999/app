from abc import ABC, abstractmethod
from typing import List
from mainContext.application.dtos.file_formats_dto import FileFormatDTO


class FileFormatsRepo(ABC):
    """Puerto para obtener formatos asociados a un file"""
    
    @abstractmethod
    def get_formats_by_file(self, file_id: str) -> List[FileFormatDTO]:
        """
        Obtiene todos los formatos asociados a un file_id específico
        
        Args:
            file_id: ID del file
            
        Returns:
            Lista de FileFormatDTO con todos los formatos asociados
        """
        pass
