from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import union_all, select, literal

from mainContext.application.ports.FileFormatsRepo import FileFormatsRepo
from mainContext.application.dtos.file_formats_dto import FileFormatDTO

from mainContext.infrastructure.models import (
    Fosp01, Fosc01, Foos01, Foem01, Foem011, Fobc01, Fopc02, Fopp02, Focr02,
    Equipment, EquipmentBrands, Employees
)


class FileFormatsRepoImpl(FileFormatsRepo):
    def __init__(self, db: Session):
        self.db = db
    
    def get_formats_by_file(self, file_id: str) -> List[FileFormatDTO]:
        """
        Obtiene todos los formatos asociados a un file_id en el orden especificado:
        FO-SP-01, FO-SC-01, FO-OS-01, FO-EM-01, FO-BC-01, FO-PC-02, FO-PP-02, FO-CR-02
        """
        formats = []
        
        # FO-SP-01 (FOSP01)
        formats.extend(self._get_fosp01_formats(file_id))
        
        # FO-SC-01 (FOSC01)
        formats.extend(self._get_fosc01_formats(file_id))
        
        # FO-OS-01 (FOOS01)
        formats.extend(self._get_foos01_formats(file_id))
        
        # FO-EM-01 (FOEM01 y FOEM01_1)
        formats.extend(self._get_foem01_formats(file_id))
        formats.extend(self._get_foem011_formats(file_id))
        
        # FO-BC-01 (FOBC01)
        formats.extend(self._get_fobc01_formats(file_id))
        
        # FO-PC-02 (FOPC02)
        formats.extend(self._get_fopc02_formats(file_id))
        
        # FO-PP-02 (FOPP02)
        formats.extend(self._get_fopp02_formats(file_id))
        
        # FO-CR-02 (FOCR02)
        formats.extend(self._get_focr02_formats(file_id))
        
        return formats
    
    def _get_fosp01_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-SP-01"""
        try:
            results = (
                self.db.query(Fosp01)
                .options(
                    joinedload(Fosp01.equipment).joinedload(Equipment.brand),
                    joinedload(Fosp01.employee)
                )
                .filter(Fosp01.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-SP-01",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.equipment),
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_fosp01_formats: {str(e)}")
            return []
    
    def _get_fosc01_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-SC-01"""
        try:
            results = (
                self.db.query(Fosc01)
                .options(
                    joinedload(Fosc01.equipment).joinedload(Equipment.brand),
                    joinedload(Fosc01.employee)
                )
                .filter(Fosc01.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-SC-01",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.equipment),
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_fosc01_formats: {str(e)}")
            return []
    
    def _get_foos01_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-OS-01"""
        try:
            results = (
                self.db.query(Foos01)
                .options(
                    joinedload(Foos01.equipment).joinedload(Equipment.brand),
                    joinedload(Foos01.employee)
                )
                .filter(Foos01.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-OS-01",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.equipment),
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_foos01_formats: {str(e)}")
            return []
    
    def _get_foem01_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-EM-01 (tabla foem01)"""
        try:
            results = (
                self.db.query(Foem01)
                .options(
                    joinedload(Foem01.equipment).joinedload(Equipment.brand),
                    joinedload(Foem01.employee)
                )
                .filter(Foem01.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-EM-01",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.equipment),
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_foem01_formats: {str(e)}")
            return []
    
    def _get_foem011_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-EM-01 (tabla foem01_1 sin equipment)"""
        try:
            results = (
                self.db.query(Foem011)
                .options(joinedload(Foem011.employee))
                .filter(Foem011.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-EM-01",
                    file_id=format.file_id,
                    equipment=None,
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_foem011_formats: {str(e)}")
            return []
    
    def _get_fobc01_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-BC-01"""
        try:
            results = (
                self.db.query(Fobc01)
                .options(
                    joinedload(Fobc01.equipment).joinedload(Equipment.brand),
                    joinedload(Fobc01.employee)
                )
                .filter(Fobc01.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-BC-01",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.equipment),
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_fobc01_formats: {str(e)}")
            return []
    
    def _get_fopc02_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-PC-02"""
        try:
            results = (
                self.db.query(Fopc02)
                .options(
                    joinedload(Fopc02.equipment).joinedload(Equipment.brand),
                    joinedload(Fopc02.employee)
                )
                .filter(Fopc02.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-PC-02",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.equipment),
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_fopc02_formats: {str(e)}")
            return []
    
    def _get_fopp02_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-PP-02. Equipment obtenido via relación con fopc"""
        try:
            results = (
                self.db.query(Fopp02)
                .options(
                    joinedload(Fopp02.fopc).joinedload(Fopc02.equipment).joinedload(Equipment.brand),
                    joinedload(Fopp02.employee)
                )
                .filter(Fopp02.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-PP-02",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.fopc.equipment) if format.fopc else None,
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_fopp02_formats: {str(e)}")
            return []
    
    def _get_focr02_formats(self, file_id: str) -> List[FileFormatDTO]:
        """Obtiene formatos FO-CR-02"""
        try:
            results = (
                self.db.query(Focr02)
                .options(
                    joinedload(Focr02.equipment).joinedload(Equipment.brand),
                    joinedload(Focr02.employee)
                )
                .filter(Focr02.file_id == file_id)
                .all()
            )
            
            return [
                FileFormatDTO(
                    id=format.id,
                    format="FO-CR-02",
                    file_id=format.file_id,
                    equipment=self._format_equipment(format.equipment),
                    date_created=format.date_created,
                    employee=self._format_employee(format.employee),
                    status=format.status
                )
                for format in results
            ]
        except Exception as e:
            print(f"Error en _get_focr02_formats: {str(e)}")
            return []
    
    def _format_equipment(self, equipment: Equipment) -> str:
        """Formatea equipment como 'Marca - Número Económico'"""
        if not equipment:
            return None
        
        brand = equipment.brand.name if equipment.brand else "N/A"
        economic_number = equipment.economic_number or "N/A"
        
        return f"{brand} - {economic_number}"
    
    def _format_employee(self, employee: Employees) -> str:
        """Formatea employee como 'Nombre Apellido'"""
        if not employee:
            return None
        
        name = employee.name or ""
        lastname = employee.lastname or ""
        
        return f"{name} {lastname}".strip() or None
