from mainContext.domain.models.Formats.fo_le_01 import FOLE01, FOLE01Service
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.Formats.Service import Service

from mainContext.application.dtos.Formats.fo_le_01_dto import (
    FOLE01CreateDTO,
    FOLE01UpdateDTO,
    FOLE01ServiceDTO,
    FOLE01SignatureDTO,
    FOLE01TableRowDTO
)




def map_create_dto_to_fole01(dto: FOLE01CreateDTO, employee: Employee, equipment: Equipment) -> FOLE01:
    return FOLE01(
        id=0,  # o generado por la base de datos
        employee=employee,
        equipment=equipment,
        horometer=0.0,
        technical_action="",
        status=dto.status,
        reception_name="",
        signature_path="",
        date_signed=None,
        date_created=dto.date_created,
        rating=0,
        rating_comment="",
        services=[]
    )

#update
def apply_update_dto_to_fole01(fole01: FOLE01, dto: FOLE01UpdateDTO) -> None:
    fole01.horometer = dto.hourometer
    fole01.technical_action = dto.technical_action
    fole01.reception_name = dto.reception_name

    fole01.services = [
        FOLE01Service(
            id=0,  # o generado por la base de datos
            service=Service(  # construimos el objeto Service directamente
                id=sdto.service_id,
                code="",  # puedes dejarlo vacío si no lo necesitas en el dominio
                name="",  # igual aquí
                description=""  # opcional
            ),
            diagnose_description=sdto.diagnose_description,
            description_service=sdto.description_service,
            priority=sdto.priority
        )
        for sdto in dto.services
    ]


def map_fole01_to_table_raw_dto(fole01: FOLE01) -> FOLE01TableRowDTO:
    return FOLE01TableRowDTO(
        id=fole01.id,
        economic_number=fole01.equipment.economic_number,
        date_created=fole01.date_created,
        codes=[s.service.code for s in fole01.services],
        employee_name=fole01.employee.name,
        status=fole01.status
    )