from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List
from mainContext.application.dtos.dashboard import DashboardDTO, ServiceDashDTO, ClientDashDTO, ServiceByDateDashDTO, LeasingEquipmentDashDTO, ServiceCodeDashDTO
from mainContext.application.ports.DashboardRepo import DashboardRepo
from mainContext.infrastructure.models import Fosp01, Fosc01, Foos01, Clients, Equipment, Fosc01Services, Fosp01Services, Foos01Services, Services, Foro05, EquipmentBrands
from datetime import datetime, timedelta

class DashboardRepoImpl(DashboardRepo):
    def __init__(self, db: Session):
        self.db = db

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
        )

        openServicesSP_results = openServicesSPQuery.all()
        openServicesSC_results = openServicesSCQuery.all()
        openServicesOS_results = openServicesOSQuery.all()

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

        openServices = len(grouped_sp_services) + len(grouped_sc_services) + len(grouped_os_services)

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



        # Active Clients

        activeClients = self.db.query(Clients).filter(Clients.status == "Cliente").count()

        bestClientsQuery = (

            self.db.query(

                Clients.id,

                Clients.name,

                func.count(Fosp01.id).label("fosp01_count"),

                func.count(Fosc01.id).label("fosc01_count"),

                func.count(Foos01.id).label("foos01_count")

            )

            .outerjoin(Fosp01, (Clients.id == Fosp01.client_id) & (Fosp01.status == "Cerrado") & (extract('month', Fosp01.date_signed) == datetime.now().month) & (extract('year', Fosp01.date_signed) == datetime.now().year))

            .outerjoin(Fosc01, (Clients.id == Fosc01.client_id) & (Fosc01.status == "Cerrado") & (extract('month', Fosc01.date_signed) == datetime.now().month) & (extract('year', Fosc01.date_signed) == datetime.now().year))

            .outerjoin(Foos01, (Clients.id == Foos01.client_id) & (Foos01.status == "Cerrado") & (extract('month', Foos01.date_signed) == datetime.now().month) & (extract('year', Foos01.date_signed) == datetime.now().year))

            .group_by(Clients.id, Clients.name)

            .having(

                (func.count(Fosp01.id) > 0) |

                (func.count(Fosc01.id) > 0) |

                (func.count(Foos01.id) > 0)

            )

            .order_by(

                (func.count(Fosp01.id) + func.count(Fosc01.id) + func.count(Foos01.id)).desc()

            )

            .limit(5)

            .all()

        )

        bestClients = [

            ClientDashDTO(id=client.id, name=client.name)

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

    