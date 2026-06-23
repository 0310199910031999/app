from mainContext.domain.models.Formats.fo_ro_05 import FORO05
from mainContext.application.dtos.Formats.fo_ro_05_dto import FORO05CalendarDayDTO, FORO05CalendarFilterDTO, FORO05CalendarRowDTO, FORO05CreateDTO, FORO05UpdateDTO, FORO05SignatureDTO, FORO05TableRowDTO, EquipmentDTO, ClientDTO, ServiceDTO, VendorDTO
from mainContext.application.ports.Formats.fo_ro_05_repo import FORO05Repo
from typing import List
from datetime import timedelta

class CreateFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, dto: FORO05CreateDTO) -> int:
        return self.repo.create_foro05(dto)

class GetFORO05ById:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, id: int) -> FORO05:
        return self.repo.get_foro05_by_id(id)

class DeleteFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, id: int) -> bool:
        return self.repo.delete_foro05(id)

class UpdateFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, foro05_id: int, dto: FORO05UpdateDTO) -> bool:
        return self.repo.update_foro05(foro05_id, dto)

class GetListFORO05Table:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self) -> List[FORO05TableRowDTO]:
        return self.repo.get_list_foro05_table()


class GetFORO05CalendarServices:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, filters: FORO05CalendarFilterDTO) -> List[FORO05CalendarDayDTO]:
        rows = self.repo.get_foro05_calendar_rows(filters)
        grouped: dict = {}

        for row in rows:
            day_rows = grouped.setdefault(row.fecha, [])
            day_rows.append(row)

        current_date = filters.start_date
        response = []

        while current_date <= filters.end_date:
            response.append(
                FORO05CalendarDayDTO(
                    route_date=current_date,
                    services=grouped.get(current_date, []),
                )
            )
            current_date += timedelta(days=1)

        return response

class SignFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, id: int, dto: FORO05SignatureDTO) -> bool:
        return self.repo.sign_foro05(id, dto)

class GetListClients:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self) -> List[ClientDTO]:
        return self.repo.get_list_clients()

class GetListEquipments:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, client_id: int) -> List[EquipmentDTO]:
        return self.repo.get_list_equipments(client_id)

class GetListServices:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self) -> List[ServiceDTO]:
        return self.repo.get_list_services()

class GetListVendors:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self) -> List[VendorDTO]:
        return self.repo.get_list_vendors()

