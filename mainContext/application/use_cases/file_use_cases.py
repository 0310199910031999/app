from typing import List
from mainContext.application.ports.FileRepo import FileRepo
from mainContext.application.dtos.file_dto import FileTableClosedDTO, FileTableOpenDTO, FileInvoiceDTO


class GetTableClosed:
    """Use case para obtener la tabla de files cerrados"""
    
    def __init__(self, repo: FileRepo):
        self.repo = repo
    
    def execute(self) -> List[FileTableClosedDTO]:
        return self.repo.get_table_closed()


class GetTableOpen:
    """Use case para obtener la tabla de files abiertos con servicios"""
    
    def __init__(self, repo: FileRepo):
        self.repo = repo
    
    def execute(self) -> List[FileTableOpenDTO]:
        return self.repo.get_table_open()


class InvoiceFile:
    """Use case para facturar un file"""
    
    def __init__(self, repo: FileRepo):
        self.repo = repo
    
    def execute(self, file_id: str, dto: FileInvoiceDTO) -> bool:
        return self.repo.invoice_file(file_id, dto)
