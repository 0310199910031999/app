from sqlalchemy.orm import Session
from sqlalchemy import func, extract, or_, and_
from typing import List, Optional
from mainContext.application.dtos.dashboard import (
    DashboardDTO,
    ServiceDashDTO,
    ClientDashDTO,
    ServiceByDateDashDTO,
    ServiceByDateAndEmployeeDashDTO,
    ServicesByTypeDashDTO,
    ServicesByEmployeeDashDTO,
    ServicesByTypeAndEmployeeDashDTO,
    LeasingEquipmentDashDTO,
    ServiceCodeDashDTO,
    DateRangeDTO,
    BestClientsByDateDTO,
    ServicesByDateRangeDTO,
    BestServicesByDateDTO,
    MobileClientDashboardDTO,
    MobileActivityDTO,
    RatingSummaryDTO,
    SearchByIdDTO,
    SearchByIdResultDTO,
    SearchByIdRequestDTO,
)
from mainContext.application.ports.DashboardRepo import DashboardRepo
from mainContext.infrastructure.models import (
    Fosp01,
    Fosc01,
    Foos01,
    Foem01,
    Foem011,
    Fobc01,
    Fopc02,
    Fole01,
    Foim01,
    Foim03,
    Focr02,
    Fopp02,
    Foir02,
    Employees,
    Clients,
    Equipment,
    Fosc01Services,
    Fosp01Services,
    Foos01Services,
    Fole01Services,
    Services,
    Foro05,
    EquipmentBrands,
    Files,
)
from datetime import datetime, timedelta

class DashboardRepoImpl(DashboardRepo):
    def __init__(self, db: Session):
        self.db = db

    def _build_employee_name(self, employee_id: int, name: str, lastname: str) -> str:
        full_name = " ".join(part for part in [name, lastname] if part).strip()
        if full_name:
            return full_name
        return f"Empleado {employee_id}"

    def _get_service_totals_by_date_and_employee(self, model, date_range: DateRangeDTO):
        if model is Fole01:
            service_date_expr = model.date_signed
            date_filters = [
                model.date_signed.isnot(None),
                model.date_signed >= date_range.start_date,
                model.date_signed <= date_range.end_date,
            ]
        else:
            service_date_expr = func.date(model.date_signed)
            date_filters = [
                model.date_signed.isnot(None),
                service_date_expr >= date_range.start_date,
                service_date_expr <= date_range.end_date,
            ]

        return (
            self.db.query(
                service_date_expr.label("service_date"),
                model.employee_id.label("employee_id"),
                Employees.name.label("employee_name"),
                Employees.lastname.label("employee_lastname"),
                func.count(model.id).label("total"),
            )
            .outerjoin(Employees, model.employee_id == Employees.id)
            .filter(model.status == "Cerrado")
            .filter(model.client_id.notin_([11, 90]))
            .filter(model.employee_id.isnot(None))
            .filter(*date_filters)
            .group_by(service_date_expr, model.employee_id, Employees.name, Employees.lastname)
            .order_by(service_date_expr.asc(), model.employee_id.asc())
            .all()
        )

    def getDashboard(self) -> DashboardDTO:

        openServicesSPQuery = (
            self.db.query(
                Fosp01.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
                Services.code.label("service_code")
            )
            .join(Clients, Fosp01.client_id == Clients.id)
            .join(Equipment, Fosp01.equipment_id == Equipment.id)
            .join(Fosp01Services, Fosp01.id == Fosp01Services.fosp01_id)
            .join(Services, Fosp01Services.service_id == Services.id)
            .filter(Fosp01.status == "Abierto")
            .filter(Fosp01.client_id.notin_([11, 90]))
        )
        openServicesSCQuery = (
            self.db.query(
                Fosc01.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
                Services.code.label("service_code")
            )
            .join(Clients, Fosc01.client_id == Clients.id)
            .join(Equipment, Fosc01.equipment_id == Equipment.id)
            .join(Fosc01Services, Fosc01.id == Fosc01Services.fosc01_id)
            .join(Services, Fosc01Services.service_id == Services.id)
            .filter(Fosc01.status == "Abierto")
            .filter(Fosc01.client_id.notin_([11, 90]))
        )
        openServicesOSQuery = (
            self.db.query(
                Foos01.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
                Services.code.label("service_code")
            )
            .join(Clients, Foos01.client_id == Clients.id)
            .join(Equipment, Foos01.equipment_id == Equipment.id)
            .join(Foos01Services, Foos01.id == Foos01Services.foos01_id)
            .join(Services, Foos01Services.service_id == Services.id)
            .filter(Foos01.status == "Abierto")
            .filter(Foos01.client_id.notin_([11, 90]))
        )

        openServicesLEQuery = (
            self.db.query(
                Fole01.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
                Services.code.label("service_code")
            )
            .join(Clients, Fole01.client_id == Clients.id)
            .join(Equipment, Fole01.equipment_id == Equipment.id)
            .join(Fole01Services, Fole01.id == Fole01Services.fole01_id)
            .join(Services, Fole01Services.service_id == Services.id)
            .filter(Fole01.status == "Abierto")
            .filter(Fole01.client_id.notin_([11, 90]))
        )

        openServicesBCQuery = (
            self.db.query(
                Fobc01.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
            )
            .join(Clients, Fobc01.client_id == Clients.id)
            .join(Equipment, Fobc01.equipment_id == Equipment.id)
            .filter(Fobc01.status == "Abierto")
            .filter(Fobc01.client_id.notin_([11, 90]))
        )

        openServicesEMQuery = (
            self.db.query(
                Foem01.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
            )
            .join(Clients, Foem01.client_id == Clients.id)
            .join(Equipment, Foem01.equipment_id == Equipment.id)
            .filter(Foem01.status == "Abierto")
            .filter(Foem01.client_id.notin_([11, 90]))
        )

        openServicesIMQuery = (
            self.db.query(
                Foim01.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
            )
            .join(Clients, Foim01.client_id == Clients.id)
            .join(Equipment, Foim01.equipment_id == Equipment.id)
            .filter(Foim01.status == "Abierto")
            .filter(Foim01.client_id.notin_([11, 90]))
        )

        openServicesPCQuery = (
            self.db.query(
                Fopc02.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
            )
            .join(Clients, Fopc02.client_id == Clients.id)
            .join(Equipment, Fopc02.equipment_id == Equipment.id)
            .filter(Fopc02.status == "Abierto")
            .filter(Fopc02.client_id.notin_([11, 90]))
        )

        openServicesCRQuery = (
            self.db.query(
                Focr02.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
            )
            .join(Clients, Focr02.client_id == Clients.id)
            .join(Equipment, Focr02.equipment_id == Equipment.id)
            .filter(Focr02.status == "Abierto")
            .filter(Focr02.client_id.notin_([11, 90]))
        )

        openServicesIM03Query = (
            self.db.query(
                Foim03.id,
                Clients.name.label("client_name"),
                Equipment.economic_number.label("equipment_economic_number"),
            )
            .join(Clients, Foim03.client_id == Clients.id)
            .outerjoin(Equipment, Foim03.equipment_id == Equipment.id)
            .filter(Foim03.status == "Abierto")
            .filter(Foim03.client_id.notin_([11, 90]))
        )

        openServicesEM11Query = (
            self.db.query(
                Foem011.id,
                Clients.name.label("client_name"),
            )
            .join(Clients, Foem011.client_id == Clients.id)
            .filter(Foem011.status == "Abierto")
            .filter(Foem011.client_id.notin_([11, 90]))
        )

        openServicesSP_results = openServicesSPQuery.all()
        openServicesSC_results = openServicesSCQuery.all()
        openServicesOS_results = openServicesOSQuery.all()
        openServicesLE_results = openServicesLEQuery.all()
        openServicesBC_results = openServicesBCQuery.all()
        openServicesEM_results = openServicesEMQuery.all()
        openServicesIM_results = openServicesIMQuery.all()
        openServicesPC_results = openServicesPCQuery.all()
        openServicesCR_results = openServicesCRQuery.all()
        openServicesIM03_results = openServicesIM03Query.all()
        openServicesEM11_results = openServicesEM11Query.all()

        # Group services by ID to collect all codes for a single service entry
        grouped_sp_services = {}
        for service_id, client_name, equipment_economic_number, service_code in openServicesSP_results:
            if service_id not in grouped_sp_services:
                grouped_sp_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                    "codes": []
                }
            grouped_sp_services[service_id]["codes"].append(service_code)

        grouped_sc_services = {}
        for service_id, client_name, equipment_economic_number, service_code in openServicesSC_results:
            if service_id not in grouped_sc_services:
                grouped_sc_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                    "codes": []
                }
            grouped_sc_services[service_id]["codes"].append(service_code)

        grouped_os_services = {}
        for service_id, client_name, equipment_economic_number, service_code in openServicesOS_results:
            if service_id not in grouped_os_services:
                grouped_os_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                    "codes": []
                }
            grouped_os_services[service_id]["codes"].append(service_code)

        grouped_le_services = {}
        for service_id, client_name, equipment_economic_number, service_code in openServicesLE_results:
            if service_id not in grouped_le_services:
                grouped_le_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                    "codes": []
                }
            grouped_le_services[service_id]["codes"].append(service_code)

        grouped_bc_services = {}
        for service_id, client_name, equipment_economic_number in openServicesBC_results:
            if service_id not in grouped_bc_services:
                grouped_bc_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                }

        grouped_em_services = {}
        for service_id, client_name, equipment_economic_number in openServicesEM_results:
            if service_id not in grouped_em_services:
                grouped_em_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                }

        grouped_im_services = {}
        for service_id, client_name, equipment_economic_number in openServicesIM_results:
            if service_id not in grouped_im_services:
                grouped_im_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                }

        grouped_pc_services = {}
        for service_id, client_name, equipment_economic_number in openServicesPC_results:
            if service_id not in grouped_pc_services:
                grouped_pc_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                }

        grouped_cr_services = {}
        for service_id, client_name, equipment_economic_number in openServicesCR_results:
            if service_id not in grouped_cr_services:
                grouped_cr_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                }

        grouped_im03_services = {}
        for service_id, client_name, equipment_economic_number in openServicesIM03_results:
            if service_id not in grouped_im03_services:
                grouped_im03_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": equipment_economic_number,
                }

        grouped_em11_services = {}
        for service_id, client_name in openServicesEM11_results:
            if service_id not in grouped_em11_services:
                grouped_em11_services[service_id] = {
                    "client_name": client_name,
                    "equipment_economic_number": None,
                }

        openServices = (
            len(grouped_sp_services) + len(grouped_sc_services) + len(grouped_os_services) +
            len(grouped_le_services) + len(grouped_bc_services) + len(grouped_em_services) +
            len(grouped_im_services) + len(grouped_pc_services) + len(grouped_cr_services) +
            len(grouped_im03_services) + len(grouped_em11_services)
        )

        files = self.db.query(Files).count()



        listOpenServices = []
        for service_id, data in grouped_sp_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-SP-01",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=data["codes"]
            ))
        for service_id, data in grouped_sc_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-SC-01",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=data["codes"]
            ))
        for service_id, data in grouped_os_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-OS-01",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=data["codes"]
            ))
        for service_id, data in grouped_le_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-LE-01",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=data["codes"]
            ))
        for service_id, data in grouped_bc_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-BC-01",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=[]
            ))
        for service_id, data in grouped_em_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-EM-01",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=[]
            ))
        for service_id, data in grouped_im_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-IM-01",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=[]
            ))
        for service_id, data in grouped_pc_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-PC-02",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=[]
            ))
        for service_id, data in grouped_cr_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-CR-02",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=[]
            ))
        for service_id, data in grouped_im03_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-IM-03",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=[]
            ))
        for service_id, data in grouped_em11_services.items():
            listOpenServices.append(ServiceDashDTO(
                id=service_id,
                serviceName="FO-EM-01-1",
                clientName=data["client_name"],
                equipment=data["equipment_economic_number"],
                codes=[]
            ))


        # Active Clients

        activeClients = self.db.query(Clients).filter(Clients.status == "Cliente").count()

        # Best Clients - Top 5 clients with most services in the current year
        current_year = datetime.now().year
        
        # Subquery for FOSP01 services count per client
        fosp01_subq = (
            self.db.query(
                Fosp01.client_id,
                func.count(Fosp01.id).label("count")
            )
            .filter(Fosp01.status == "Cerrado")
            .filter(extract('year', Fosp01.date_signed) == current_year)
            .group_by(Fosp01.client_id)
            .subquery()
        )
        
        # Subquery for FOSC01 services count per client
        fosc01_subq = (
            self.db.query(
                Fosc01.client_id,
                func.count(Fosc01.id).label("count")
            )
            .filter(Fosc01.status == "Cerrado")
            .filter(extract('year', Fosc01.date_signed) == current_year)
            .group_by(Fosc01.client_id)
            .subquery()
        )
        
        # Subquery for FOOS01 services count per client
        foos01_subq = (
            self.db.query(
                Foos01.client_id,
                func.count(Foos01.id).label("count")
            )
            .filter(Foos01.status == "Cerrado")
            .filter(extract('year', Foos01.date_signed) == current_year)
            .group_by(Foos01.client_id)
            .subquery()
        )
        
        # Define total_services expression
        total_services_expr = (
            func.coalesce(fosp01_subq.c.count, 0) +
            func.coalesce(fosc01_subq.c.count, 0) +
            func.coalesce(foos01_subq.c.count, 0)
        )
        
        # Main query combining all service types
        bestClientsQuery = (
            self.db.query(
                Clients.id,
                Clients.name,
                total_services_expr.label("total_services")
            )
            .outerjoin(fosp01_subq, Clients.id == fosp01_subq.c.client_id)
            .outerjoin(fosc01_subq, Clients.id == fosc01_subq.c.client_id)
            .outerjoin(foos01_subq, Clients.id == foos01_subq.c.client_id)
            .filter(Clients.status == "Cliente")
            .filter(total_services_expr > 0)
            .filter(~Clients.id.in_([11, 90]))
            .order_by(total_services_expr.desc())
            .limit(5)
            .all()
        )

        bestClients = [
            ClientDashDTO(id=client.id, name=client.name, total_services=client.total_services)
            for client in bestClientsQuery
        ]

        

        # Active Equipment

        activeEquipment = self.db.query(Foos01.equipment_id).distinct().count()

        

        # Services by Date for the current month

        today = datetime.now()

        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(microseconds=1)



        services_by_date_query = (

            self.db.query(

                func.date(Fosp01.date_signed).label("service_date"),

                func.count(Fosp01.id).label("service_count")

            )

            .filter(Fosp01.status == "Cerrado")

            .filter(Fosp01.client_id.notin_([11, 90]))

            .filter(Fosp01.date_signed >= start_of_month)

            .filter(Fosp01.date_signed <= end_of_month)

            .group_by(func.date(Fosp01.date_signed))

            .order_by(func.date(Fosp01.date_signed))

            .all()

        )



        services_by_date_sc_query = (

            self.db.query(

                func.date(Fosc01.date_signed).label("service_date"),

                func.count(Fosc01.id).label("service_count")

            )

            .filter(Fosc01.status == "Cerrado")

            .filter(Fosc01.client_id.notin_([11, 90]))

            .filter(Fosc01.date_signed >= start_of_month)

            .filter(Fosc01.date_signed <= end_of_month)

            .group_by(func.date(Fosc01.date_signed))

            .order_by(func.date(Fosc01.date_signed))

            .all()

        )



        services_by_date_os_query = (

            self.db.query(

                func.date(Foos01.date_signed).label("service_date"),

                func.count(Foos01.id).label("service_count")

            )

            .filter(Foos01.status == "Cerrado")

            .filter(Foos01.client_id.notin_([11, 90]))

            .filter(Foos01.date_signed >= start_of_month)

            .filter(Foos01.date_signed <= end_of_month)

            .group_by(func.date(Foos01.date_signed))

            .order_by(func.date(Foos01.date_signed))

            .all()

        )



        services_by_date_map = {}

        for service_date_data in services_by_date_query:

            date_str = service_date_data.service_date.strftime("%Y-%m-%d")

            services_by_date_map[date_str] = services_by_date_map.get(date_str, 0) + service_date_data.service_count

        for service_date_data in services_by_date_sc_query:

            date_str = service_date_data.service_date.strftime("%Y-%m-%d")

            services_by_date_map[date_str] = services_by_date_map.get(date_str, 0) + service_date_data.service_count

        for service_date_data in services_by_date_os_query:

            date_str = service_date_data.service_date.strftime("%Y-%m-%d")

            services_by_date_map[date_str] = services_by_date_map.get(date_str, 0) + service_date_data.service_count



        servicesByDate = [

            ServiceByDateDashDTO(date=date_str, number=count)

            for date_str, count in sorted(services_by_date_map.items())

        ]



        # Operative Routes

        operativeRoutes = self.db.query(Foro05).filter(Foro05.status == "Abierto").count()



        # Leasing Equipment

        leasing_equipment_query = (
            self.db.query(
                Equipment.id,
                EquipmentBrands.name.label("brand_name"),
                Equipment.economic_number,
                Clients.name.label("client_name")
            )
            .join(Clients, Equipment.client_id == Clients.id)
            .join(EquipmentBrands, Equipment.brand_id == EquipmentBrands.id)
            .filter(Equipment.property == "DAL Dealer Group")
            .filter(Equipment.client_id != 11)
            .all()
        )

        numberleasingEquipment = len(leasing_equipment_query)

        leasingEquipment = [
            LeasingEquipmentDashDTO(
                id=eq.id,
                brand_name=eq.brand_name,
                economic_number=eq.economic_number,
                client_name=eq.client_name
            )
            for eq in leasing_equipment_query
        ]



        # Best Services Codes (Top 5 services with most occurrences in the last 30 days)

        

        thirty_days_ago = datetime.now() - timedelta(days=30)



        service_codes_sp_query = (

            self.db.query(

                Services.code,

                func.count(Services.code).label("code_count")

            )

            .join(Fosp01Services, Fosp01Services.service_id == Services.id)

            .join(Fosp01, Fosp01Services.fosp01_id == Fosp01.id)

            .filter(Fosp01.date_signed >= thirty_days_ago)

            .filter(Fosp01.client_id.notin_([11, 90]))

            .group_by(Services.code)

        )



        service_codes_sc_query = (

            self.db.query(

                Services.code,

                func.count(Services.code).label("code_count")

            )

            .join(Fosc01Services, Fosc01Services.service_id == Services.id)

            .join(Fosc01, Fosc01Services.fosc01_id == Fosc01.id)

            .filter(Fosc01.date_signed >= thirty_days_ago)

            .filter(Fosc01.client_id.notin_([11, 90]))

            .group_by(Services.code)

        )



        service_codes_os_query = (

            self.db.query(

                Services.code,

                func.count(Services.code).label("code_count")

            )

            .join(Foos01Services, Foos01Services.service_id == Services.id)

            .join(Foos01, Foos01Services.foos01_id == Foos01.id)

            .filter(Foos01.date_signed >= thirty_days_ago)

            .filter(Foos01.client_id.notin_([11, 90]))

            .group_by(Services.code)

        )



        all_service_codes = {}



        for code, count in service_codes_sp_query.all():

            all_service_codes[code] = all_service_codes.get(code, 0) + count

        for code, count in service_codes_sc_query.all():

            all_service_codes[code] = all_service_codes.get(code, 0) + count

        for code, count in service_codes_os_query.all():

            all_service_codes[code] = all_service_codes.get(code, 0) + count



        # Sort and get top 5

        listBestServices = [

            ServiceCodeDashDTO(code=code, count=count)

            for code, count in sorted(all_service_codes.items(), key=lambda item: item[1], reverse=True)[:5]

        ]



        return DashboardDTO(
            files=files,

            openServices=openServices,

            listOpenServices=listOpenServices,

            activeClients=activeClients,

            bestClients=bestClients,

            activeEquipment=activeEquipment,

            servicesByDate=servicesByDate,

            operativeRoutes=operativeRoutes,

            numberleasingEquipment=numberleasingEquipment,

            leasingEquipment=leasingEquipment,

            listBestServices=listBestServices

        )

    def getBestClientsByDate(self, date_range: DateRangeDTO) -> BestClientsByDateDTO:
        """
        Get top 5 clients with most closed services within the specified date range.
        """
        # Subquery for FOSP01 services count per client
        fosp01_subq = (
            self.db.query(
                Fosp01.client_id,
                func.count(Fosp01.id).label("count")
            )
            .filter(Fosp01.status == "Cerrado")
            .filter(Fosp01.client_id.notin_([11, 90]))
            .filter(Fosp01.date_signed >= date_range.start_date)
            .filter(Fosp01.date_signed <= date_range.end_date)
            .group_by(Fosp01.client_id)
            .subquery()
        )
        
        # Subquery for FOSC01 services count per client
        fosc01_subq = (
            self.db.query(
                Fosc01.client_id,
                func.count(Fosc01.id).label("count")
            )
            .filter(Fosc01.status == "Cerrado")
            .filter(Fosc01.client_id.notin_([11, 90]))
            .filter(Fosc01.date_signed >= date_range.start_date)
            .filter(Fosc01.date_signed <= date_range.end_date)
            .group_by(Fosc01.client_id)
            .subquery()
        )
        
        # Subquery for FOOS01 services count per client
        foos01_subq = (
            self.db.query(
                Foos01.client_id,
                func.count(Foos01.id).label("count")
            )
            .filter(Foos01.status == "Cerrado")
            .filter(Foos01.client_id.notin_([11, 90]))
            .filter(Foos01.date_signed >= date_range.start_date)
            .filter(Foos01.date_signed <= date_range.end_date)
            .group_by(Foos01.client_id)
            .subquery()
        )
        
        # Define total_services expression
        total_services_expr = (
            func.coalesce(fosp01_subq.c.count, 0) +
            func.coalesce(fosc01_subq.c.count, 0) +
            func.coalesce(foos01_subq.c.count, 0)
        )
        
        # Main query combining all service types
        bestClientsQuery = (
            self.db.query(
                Clients.id,
                Clients.name,
                total_services_expr.label("total_services")
            )
            .outerjoin(fosp01_subq, Clients.id == fosp01_subq.c.client_id)
            .outerjoin(fosc01_subq, Clients.id == fosc01_subq.c.client_id)
            .outerjoin(foos01_subq, Clients.id == foos01_subq.c.client_id)
            .filter(Clients.status == "Cliente")
            .filter(total_services_expr > 0)
            .filter(~Clients.id.in_([11, 90]))
            .order_by(total_services_expr.desc())
            .limit(5)
            .all()
        )

        bestClients = [
            ClientDashDTO(id=client.id, name=client.name, total_services=client.total_services)
            for client in bestClientsQuery
        ]

        return BestClientsByDateDTO(bestClients=bestClients)

    def getServicesByDateRange(self, date_range: DateRangeDTO) -> ServicesByDateRangeDTO:
        """
        Get closed service totals by service type and technician within the specified date range.
        """
        service_models = [
            ("fole01", Fole01),
            ("fosp01", Fosp01),
            ("fosc01", Fosc01),
            ("foos01", Foos01),
        ]
        service_order = {service_type: index for index, (service_type, _) in enumerate(service_models)}

        services_by_date = []
        totals_by_service_type_map = {service_type: 0 for service_type, _ in service_models}
        totals_by_employee_map = {}
        totals_by_service_type_and_employee_map = {}
        total_services = 0

        for service_type, model in service_models:
            rows = self._get_service_totals_by_date_and_employee(model, date_range)

            for row in rows:
                employee_name = row.employee_name or ""
                employee_lastname = row.employee_lastname or ""
                employee_full_name = self._build_employee_name(
                    row.employee_id,
                    employee_name,
                    employee_lastname,
                )
                date_str = row.service_date.strftime("%Y-%m-%d") if hasattr(row.service_date, "strftime") else str(row.service_date)

                services_by_date.append(
                    ServiceByDateAndEmployeeDashDTO(
                        date=date_str,
                        service_type=service_type,
                        employee_id=row.employee_id,
                        employee_name=employee_name,
                        employee_lastname=employee_lastname,
                        employee_full_name=employee_full_name,
                        total=row.total,
                    )
                )

                if row.employee_id not in totals_by_employee_map:
                    totals_by_employee_map[row.employee_id] = {
                        "employee_name": employee_name,
                        "employee_lastname": employee_lastname,
                        "employee_full_name": employee_full_name,
                        "total": 0,
                    }

                totals_by_employee_map[row.employee_id]["total"] += row.total
                totals_by_service_type_map[service_type] += row.total
                total_services += row.total

                type_employee_key = (service_type, row.employee_id)
                if type_employee_key not in totals_by_service_type_and_employee_map:
                    totals_by_service_type_and_employee_map[type_employee_key] = {
                        "employee_name": employee_name,
                        "employee_lastname": employee_lastname,
                        "employee_full_name": employee_full_name,
                        "total": 0,
                    }

                totals_by_service_type_and_employee_map[type_employee_key]["total"] += row.total

        services_by_date.sort(
            key=lambda item: (
                item.date,
                service_order[item.service_type],
                item.employee_full_name,
                item.employee_id,
            )
        )

        totals_by_service_type = [
            ServicesByTypeDashDTO(
                service_type=service_type,
                total=totals_by_service_type_map[service_type],
            )
            for service_type, _ in service_models
        ]

        totals_by_employee = [
            ServicesByEmployeeDashDTO(
                employee_id=employee_id,
                employee_name=data["employee_name"],
                employee_lastname=data["employee_lastname"],
                employee_full_name=data["employee_full_name"],
                total=data["total"],
            )
            for employee_id, data in sorted(
                totals_by_employee_map.items(),
                key=lambda item: (-item[1]["total"], item[1]["employee_full_name"], item[0]),
            )
        ]

        totals_by_service_type_and_employee = [
            ServicesByTypeAndEmployeeDashDTO(
                service_type=service_type,
                employee_id=employee_id,
                employee_name=data["employee_name"],
                employee_lastname=data["employee_lastname"],
                employee_full_name=data["employee_full_name"],
                total=data["total"],
            )
            for (service_type, employee_id), data in sorted(
                totals_by_service_type_and_employee_map.items(),
                key=lambda item: (
                    service_order[item[0][0]],
                    -item[1]["total"],
                    item[1]["employee_full_name"],
                    item[0][1],
                ),
            )
        ]

        return ServicesByDateRangeDTO(
            totalServices=total_services,
            servicesByDate=services_by_date,
            totalsByServiceType=totals_by_service_type,
            totalsByEmployee=totals_by_employee,
            totalsByServiceTypeAndEmployee=totals_by_service_type_and_employee,
        )

    def getBestServicesByDate(self, date_range: DateRangeDTO) -> BestServicesByDateDTO:
        """
        Get top 5 service codes with most occurrences within the specified date range.
        """
        service_codes_sp_query = (
            self.db.query(
                Services.code,
                func.count(Services.code).label("code_count")
            )
            .join(Fosp01Services, Fosp01Services.service_id == Services.id)
            .join(Fosp01, Fosp01Services.fosp01_id == Fosp01.id)
            .filter(Fosp01.date_signed >= date_range.start_date)
            .filter(Fosp01.date_signed <= date_range.end_date)
            .filter(Fosp01.client_id.notin_([11, 90]))
            .group_by(Services.code)
        )

        service_codes_sc_query = (
            self.db.query(
                Services.code,
                func.count(Services.code).label("code_count")
            )
            .join(Fosc01Services, Fosc01Services.service_id == Services.id)
            .join(Fosc01, Fosc01Services.fosc01_id == Fosc01.id)
            .filter(Fosc01.date_signed >= date_range.start_date)
            .filter(Fosc01.date_signed <= date_range.end_date)
            .filter(Fosc01.client_id.notin_([11, 90]))
            .group_by(Services.code)
        )

        service_codes_os_query = (
            self.db.query(
                Services.code,
                func.count(Services.code).label("code_count")
            )
            .join(Foos01Services, Foos01Services.service_id == Services.id)
            .join(Foos01, Foos01Services.foos01_id == Foos01.id)
            .filter(Foos01.date_signed >= date_range.start_date)
            .filter(Foos01.date_signed <= date_range.end_date)
            .filter(Foos01.client_id.notin_([11, 90]))
            .group_by(Services.code)
        )

        all_service_codes = {}

        for code, count in service_codes_sp_query.all():
            all_service_codes[code] = all_service_codes.get(code, 0) + count
        for code, count in service_codes_sc_query.all():
            all_service_codes[code] = all_service_codes.get(code, 0) + count
        for code, count in service_codes_os_query.all():
            all_service_codes[code] = all_service_codes.get(code, 0) + count

        # Sort and get top 5
        listBestServices = [
            ServiceCodeDashDTO(code=code, count=count)
            for code, count in sorted(all_service_codes.items(), key=lambda item: item[1], reverse=True)[:5]
        ]

        return BestServicesByDateDTO(listBestServices=listBestServices)

    def getClientMobileDashboard(self, client_id: int) -> MobileClientDashboardDTO:
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(microseconds=1)

        equipment_count = self.db.query(Equipment.id).filter(Equipment.client_id == client_id).count()
        focr02_count = (
            self.db.query(Focr02.id)
            .filter(Focr02.client_id == client_id, Focr02.status == "Activa")
            .count()
        )

        open_models = [Fosp01, Fosc01, Foos01, Foem01, Fobc01, Fopc02]
        open_services = sum(
            self.db.query(model.id)
            .filter(model.client_id == client_id, model.status == "Abierto")
            .count()
            for model in open_models
        )

        closed_models = [Fole01, Foim01, Fosp01, Fosc01, Foos01, Foem01, Fobc01]
        closed_services = sum(
            self.db.query(model.id)
            .filter(model.client_id == client_id, model.status == "Cerrado")
            .count()
            for model in closed_models
        )

        services_last_30_days_map = {}
        rating_counts = {1: 0, 2: 0, 3: 0}
        closed_30d_models = [Fosp01, Fosc01, Foos01, Foim01, Fole01]

        for model in closed_30d_models:
            date_col = func.coalesce(model.date_signed, model.date_created)

            date_rows = (
                self.db.query(func.date(date_col).label("service_date"), func.count(model.id))
                .filter(model.client_id == client_id)
                .filter(model.status == "Cerrado")
                .filter(date_col >= thirty_days_ago)
                .filter(date_col <= today)
                .group_by(func.date(date_col))
                .all()
            )

            for service_date, count in date_rows:
                date_key = service_date.strftime("%Y-%m-%d")
                services_last_30_days_map[date_key] = services_last_30_days_map.get(date_key, 0) + count

            rating_rows = (
                self.db.query(model.rating, func.count(model.id))
                .filter(model.client_id == client_id)
                .filter(model.status == "Cerrado")
                .filter(model.rating.in_([1, 2, 3]))
                .filter(date_col >= thirty_days_ago)
                .filter(date_col <= today)
                .group_by(model.rating)
                .all()
            )

            for rating, count in rating_rows:
                if rating in rating_counts:
                    rating_counts[rating] += count or 0

        services_last_30_days = [
            ServiceByDateDashDTO(date=date_str, number=count)
            for date_str, count in sorted(services_last_30_days_map.items())
        ]

        rating_summary = RatingSummaryDTO(
            rating_1=rating_counts[1],
            rating_2=rating_counts[2],
            rating_3=rating_counts[3],
        )

        activity_rows: List[MobileActivityDTO] = []

        def append_activity(model, fmt: str):
            rows = (
                self.db.query(
                    model.id,
                    model.date_signed,
                    model.date_created,
                    Employees.name,
                    Employees.lastname,
                    model.status,
                    model.equipment_id,
                )
                .outerjoin(Employees, model.employee_id == Employees.id)
                .filter(model.client_id == client_id)
                .filter(
                    or_(
                        and_(model.date_signed.isnot(None), model.date_signed >= start_of_month, model.date_signed <= end_of_month),
                        and_(model.date_signed.is_(None), model.date_created >= start_of_month, model.date_created <= end_of_month),
                    )
                )
                .all()
            )
            for row in rows:
                chosen_date = row.date_signed or row.date_created
                if chosen_date is None:
                    continue
                employee_name = "".join(filter(None, [row.name, " ", row.lastname])).strip()
                activity_rows.append(
                    MobileActivityDTO(
                        id=row.id,
                        format=fmt,
                        date=chosen_date.date() if hasattr(chosen_date, "date") else chosen_date,
                        employee_name=employee_name,
                        status=row.status or "",
                        equipment_id=row.equipment_id,
                    )
                )

        append_activity(Fole01, "fole01")
        append_activity(Foim01, "foim01")
        append_activity(Fosp01, "fosp01")
        append_activity(Fosc01, "fosc01")
        append_activity(Foos01, "foos01")
        append_activity(Foem01, "foem01")
        append_activity(Fobc01, "fobc01")

        # Ordenar por fecha descendente
        activity_rows.sort(key=lambda x: x.date, reverse=True)

        return MobileClientDashboardDTO(
            equipment_count=equipment_count,
            focr02_count=focr02_count,
            open_services=open_services,
            closed_services=closed_services,
            activity=activity_rows,
            services_last_30_days=services_last_30_days,
            rating_summary=rating_summary,
        )

    def search_by_id(self, request: SearchByIdRequestDTO) -> SearchByIdResultDTO:
        format_map = {
            "fobc01": (Fobc01, "FO-BC-01", True),
            "focr02": (Focr02, "FO-CR-02", True),
            "foem01": (Foem01, "FO-EM-01", True),
            "foem011": (Foem011, "FO-EM-01-1", True),
            "foim01": (Foim01, "FO-IM-01", False),
            "foim03": (Foim03, "FO-IM-03", False),
            "foir02": (Foir02, "FO-IR-02", False),
            "foro05": (Foro05, "FO-RO-05", False),
            "fole01": (Fole01, "FO-LE-01", False),
            "foos01": (Foos01, "FO-OS-01", True),
            "fopc02": (Fopc02, "FO-PC-02", True),
            "fopp02": (Fopp02, "FO-PP-02", True),
            "fosc01": (Fosc01, "FO-SC-01", True),
            "fosp01": (Fosp01, "FO-SP-01", True),
        }

        if request.format_filter:
            format_filter = request.format_filter.lower()
            if format_filter not in format_map:
                return SearchByIdResultDTO(results=[])
            models_to_search = {format_filter: format_map[format_filter]}
        else:
            models_to_search = format_map

        results = []
        record_id = request.record_id
        file_id = request.file_id

        if record_id is None and file_id is None:
            return SearchByIdResultDTO(results=[])

        for fmt, (model, display_name, has_file) in models_to_search.items():
            query = self.db.query(model.id)
            
            if record_id is not None:
                query = query.filter(model.id == record_id)
            elif file_id is not None and has_file:
                query = query.filter(model.file_id == file_id)
            elif file_id is not None and not has_file:
                continue

            result = query.first()
            if result:
                results.append(SearchByIdDTO(id=result.id, format=fmt, format_display=display_name))

        return SearchByIdResultDTO(results=results)
