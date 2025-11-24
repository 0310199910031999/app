from abc import ABC, abstractmethod
from typing import List
from mainContext.application.dtos.file_dto import FileTableClosedDTO, FileTableOpenDTO, FileInvoiceDTO


class FileRepo(ABC):
    
    @abstractmethod
    def get_table_closed(self) -> List[FileTableClosedDTO]:
        """Obtiene todos los files con status 'Cerrado'"""
        pass
    
    @abstractmethod
    def get_table_open(self) -> List[FileTableOpenDTO]:
        """Obtiene todos los files con status 'Abierto'"""
        pass
    
    @abstractmethod
    def invoice_file(self, file_id: str, dto: FileInvoiceDTO) -> bool:
        """Marca un file como facturado"""
        pass
