from mainContext.application.dtos.Formats.fo_ir_ro_combined_dto import CreateFOIRROCombinedDTO, FOIRROCombinedResponse, VehicleDTO, EmployeeDTO
from mainContext.application.ports.Formats.fo_ir_ro_combined_repo import FOIRROCombinedRepo
from typing import List


class CreateFOIRROCombined:
    """
    Caso de uso para crear simultáneamente un FOIR02 y un FORO05.
    """
    
    def __init__(self, repo: FOIRROCombinedRepo):
        self.repo = repo
    
    def execute(self, dto: CreateFOIRROCombinedDTO) -> FOIRROCombinedResponse:
        """
        Ejecuta la creación de ambos registros.
        
        Args:
            dto: DTO con los datos necesarios
            
        Returns:
            FOIRROCombinedResponse con los IDs de ambos registros creados
        """
        return self.repo.create_foir_and_foro(dto)


class GetVehicles:
    """
    Caso de uso para obtener la lista de vehículos.
    """
    
    def __init__(self, repo: FOIRROCombinedRepo):
        self.repo = repo
    
    def execute(self) -> List[VehicleDTO]:
        """
        Obtiene la lista de todos los vehículos.
        
        Returns:
            Lista de VehicleDTO con los datos de los vehículos
        """
        return self.repo.get_vehicles()


class GetEmployees:
    """
    Caso de uso para obtener la lista de empleados.
    """
    
    def __init__(self, repo: FOIRROCombinedRepo):
        self.repo = repo
    
    def execute(self) -> List[EmployeeDTO]:
        """
        Obtiene la lista de todos los empleados.
        
        Returns:
            Lista de EmployeeDTO con los datos de los empleados
        """
        return self.repo.get_employees()
