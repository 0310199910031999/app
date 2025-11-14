from abc import ABC, abstractmethod
from mainContext.application.dtos.Formats.fo_ir_ro_combined_dto import CreateFOIRROCombinedDTO, FOIRROCombinedResponse, VehicleDTO, EmployeeDTO
from typing import List


class FOIRROCombinedRepo(ABC):
    """
    Puerto para crear FOIR02 y FORO05 simultáneamente y obtener vehículos.
    """
    
    @abstractmethod
    def create_foir_and_foro(self, dto: CreateFOIRROCombinedDTO) -> FOIRROCombinedResponse:
        """
        Crea un registro FOIR02 y un registro FORO05 con el mismo vehicle_id y route_date.
        Ambos deben crearse en una transacción para mantener la consistencia.
        
        Args:
            dto: DTO con los datos para crear ambos registros
            
        Returns:
            FOIRROCombinedResponse con los IDs de ambos registros creados
        """
        pass
    
    @abstractmethod
    def get_vehicles(self) -> List[VehicleDTO]:
        """
        Obtiene la lista de todos los vehículos disponibles.
        
        Returns:
            Lista de VehicleDTO con los datos de los vehículos
        """
        pass
    
    @abstractmethod
    def get_employees(self) -> List[EmployeeDTO]:
        """
        Obtiene la lista de todos los empleados disponibles.
        
        Returns:
            Lista de EmployeeDTO con los datos de los empleados
        """
        pass
