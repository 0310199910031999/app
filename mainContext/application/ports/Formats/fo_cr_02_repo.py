from abc import ABC, abstractmethod
from mainContext.application.dtos.Formats.fo_cr_02_dto import (
    CreateFOCR02DTO, UpdateFOCR02DTO, FOCR02SignatureDTO, FOCR02TableRowDTO, FOCRAddEquipmentDTO
)
from mainContext.domain.models.Formats.fo_cr_02 import FOCR02
from typing import List


class FOCR02Repo(ABC):
    """
    Puerto (interfaz) para el repositorio de FOCR02.
    Define los métodos que debe implementar cualquier adaptador.
    """
    
    @abstractmethod
    def create_focr02(self, dto: CreateFOCR02DTO) -> int:
        """Crear un nuevo FOCR02"""
        pass
    
    @abstractmethod
    def get_focr02_by_id(self, id: int) -> FOCR02:
        """Obtener FOCR02 por ID"""
        pass
    
    @abstractmethod
    def get_focr02_table(self) -> List[FOCR02TableRowDTO]:
        """Obtener tabla con todos los FOCR02"""
        pass
    
    @abstractmethod
    def update_focr02(self, id: int, dto: UpdateFOCR02DTO) -> bool:
        """Actualizar FOCR02"""
        pass
    
    @abstractmethod
    def delete_focr02(self, id: int) -> bool:
        """Eliminar FOCR02"""
        pass
    
    @abstractmethod
    def sign_focr02(self, id: int, dto: FOCR02SignatureDTO) -> bool:
        """Firmar y cerrar FOCR02"""
        pass
    
    @abstractmethod
    def get_focr_additional_equipment(self) -> List[FOCRAddEquipmentDTO]:
        """Obtener lista de equipos adicionales para FOCR"""
        pass
