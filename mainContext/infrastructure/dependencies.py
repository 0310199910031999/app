from fastapi import Depends
from sqlalchemy.orm import Session
from shared.db import get_db

# --- Adapter imports (concrete implementations) ---
from mainContext.infrastructure.adapters.AppRequestRepo import AppRequestRepoImpl
from mainContext.infrastructure.adapters.AppUserRepo import AppUserRepoImpl
from mainContext.infrastructure.adapters.AuthEmployeeRepo import AuthEmployeeRepoImpl
from mainContext.infrastructure.adapters.ClientsRepo import ClientsPanelOverviewRepo
from mainContext.infrastructure.adapters.CreateDocumentsRepo import CreateDocumentsRepoImpl
from mainContext.infrastructure.adapters.DashboardRepo import DashboardRepoImpl
from mainContext.infrastructure.adapters.EmployeeRepo import EmployeeRepoImpl
from mainContext.infrastructure.adapters.EquipmentBrandRepo import EquipmentBrandRepoImpl
from mainContext.infrastructure.adapters.EquipmentPartRepo import EquipmentPartRepoImpl
from mainContext.infrastructure.adapters.EquipmentRepo import EquipmentRepoImpl
from mainContext.infrastructure.adapters.EquipmentTypeRepo import EquipmentTypeRepoImpl
from mainContext.infrastructure.adapters.FileFormatsRepo import FileFormatsRepoImpl
from mainContext.infrastructure.adapters.FileRepo import FileRepoImpl
from mainContext.infrastructure.adapters.FoimQuestionRepo import FoimQuestionRepoImpl
from mainContext.infrastructure.adapters.Foir02RequiredEquipmentRepo import Foir02RequiredEquipmentRepoImpl
from mainContext.infrastructure.adapters.RoleRepo import RoleRepoImpl
from mainContext.infrastructure.adapters.ServiceRecordRepo import ServiceRecordRepoImpl
from mainContext.infrastructure.adapters.ServiceRepo import ServiceRepoImpl
from mainContext.infrastructure.adapters.SparePartCategoryRepo import SparePartCategoryRepoImpl
from mainContext.infrastructure.adapters.SparePartRepo import SparePartRepoImpl
from mainContext.infrastructure.adapters.vehicle_repo import VehicleRepoImpl
from mainContext.infrastructure.adapters.VendorRepo import VendorRepoImpl

# --- Formats adapter imports ---
from mainContext.infrastructure.adapters.Formats.fo_cr_02_repo import FOCR02RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_bc_01_repo import FOBC01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_im_01_repo import FOIM01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_em_01_repo import FOEM01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_em_01_1_repo import FOEM011RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_im_03_repo import FOIM03RepoImpl
from mainContext.infrastructure.adapters.Formats.service_repo import ServiceRepoImpl as FormatsServiceRepoImpl
from mainContext.infrastructure.adapters.Formats.fo_sp_01_repo import FOSP01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_sc_01_repo import FOSC01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_ro_05_repo import FORO05RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_le_01_repo import FOLE01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_ir_ro_combined_repo import FOIRROCombinedRepoImpl
from mainContext.infrastructure.adapters.Formats.fo_ir_02_repo import FOIR02RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_pc_02_repo import FOPC02RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_os_01_repo import FOOS01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_pp_02_repo import FOPP02RepoImpl


# --- Repository dependency providers ---

def get_app_request_repo(db: Session = Depends(get_db)) -> AppRequestRepoImpl:
    return AppRequestRepoImpl(db)

def get_app_user_repo(db: Session = Depends(get_db)) -> AppUserRepoImpl:
    return AppUserRepoImpl(db)

def get_auth_employee_repo(db: Session = Depends(get_db)) -> AuthEmployeeRepoImpl:
    return AuthEmployeeRepoImpl(db)

def get_clients_repo(db: Session = Depends(get_db)) -> ClientsPanelOverviewRepo:
    return ClientsPanelOverviewRepo(db)

def get_create_documents_repo(db: Session = Depends(get_db)) -> CreateDocumentsRepoImpl:
    return CreateDocumentsRepoImpl(db)

def get_dashboard_repo(db: Session = Depends(get_db)) -> DashboardRepoImpl:
    return DashboardRepoImpl(db)

def get_employee_repo(db: Session = Depends(get_db)) -> EmployeeRepoImpl:
    return EmployeeRepoImpl(db)

def get_equipment_brand_repo(db: Session = Depends(get_db)) -> EquipmentBrandRepoImpl:
    return EquipmentBrandRepoImpl(db)

def get_equipment_part_repo(db: Session = Depends(get_db)) -> EquipmentPartRepoImpl:
    return EquipmentPartRepoImpl(db)

def get_equipment_repo(db: Session = Depends(get_db)) -> EquipmentRepoImpl:
    return EquipmentRepoImpl(db)

def get_equipment_type_repo(db: Session = Depends(get_db)) -> EquipmentTypeRepoImpl:
    return EquipmentTypeRepoImpl(db)

def get_file_formats_repo(db: Session = Depends(get_db)) -> FileFormatsRepoImpl:
    return FileFormatsRepoImpl(db)

def get_file_repo(db: Session = Depends(get_db)) -> FileRepoImpl:
    return FileRepoImpl(db)

def get_foim_question_repo(db: Session = Depends(get_db)) -> FoimQuestionRepoImpl:
    return FoimQuestionRepoImpl(db)

def get_foir02_required_equipment_repo(db: Session = Depends(get_db)) -> Foir02RequiredEquipmentRepoImpl:
    return Foir02RequiredEquipmentRepoImpl(db)

def get_role_repo(db: Session = Depends(get_db)) -> RoleRepoImpl:
    return RoleRepoImpl(db)

def get_service_record_repo(db: Session = Depends(get_db)) -> ServiceRecordRepoImpl:
    return ServiceRecordRepoImpl(db)

def get_service_repo(db: Session = Depends(get_db)) -> ServiceRepoImpl:
    return ServiceRepoImpl(db)

def get_spare_part_category_repo(db: Session = Depends(get_db)) -> SparePartCategoryRepoImpl:
    return SparePartCategoryRepoImpl(db)

def get_spare_part_repo(db: Session = Depends(get_db)) -> SparePartRepoImpl:
    return SparePartRepoImpl(db)

def get_vehicle_repo(db: Session = Depends(get_db)) -> VehicleRepoImpl:
    return VehicleRepoImpl(db)

def get_vendor_repo(db: Session = Depends(get_db)) -> VendorRepoImpl:
    return VendorRepoImpl(db)


# --- Formats repository dependency providers ---

def get_focr02_repo(db: Session = Depends(get_db)) -> FOCR02RepoImpl:
    return FOCR02RepoImpl(db)

def get_fobc01_repo(db: Session = Depends(get_db)) -> FOBC01RepoImpl:
    return FOBC01RepoImpl(db)

def get_foim01_repo(db: Session = Depends(get_db)) -> FOIM01RepoImpl:
    return FOIM01RepoImpl(db)

def get_foem01_repo(db: Session = Depends(get_db)) -> FOEM01RepoImpl:
    return FOEM01RepoImpl(db)

def get_foem01_1_repo(db: Session = Depends(get_db)) -> FOEM011RepoImpl:
    return FOEM011RepoImpl(db)

def get_foim03_repo(db: Session = Depends(get_db)) -> FOIM03RepoImpl:
    return FOIM03RepoImpl(db)

def get_formats_service_repo(db: Session = Depends(get_db)) -> FormatsServiceRepoImpl:
    return FormatsServiceRepoImpl(db)

def get_fosp01_repo(db: Session = Depends(get_db)) -> FOSP01RepoImpl:
    return FOSP01RepoImpl(db)

def get_fosc01_repo(db: Session = Depends(get_db)) -> FOSC01RepoImpl:
    return FOSC01RepoImpl(db)

def get_foro05_repo(db: Session = Depends(get_db)) -> FORO05RepoImpl:
    return FORO05RepoImpl(db)

def get_fole01_repo(db: Session = Depends(get_db)) -> FOLE01RepoImpl:
    return FOLE01RepoImpl(db)

def get_foirro_combined_repo(db: Session = Depends(get_db)) -> FOIRROCombinedRepoImpl:
    return FOIRROCombinedRepoImpl(db)

def get_foir02_repo(db: Session = Depends(get_db)) -> FOIR02RepoImpl:
    return FOIR02RepoImpl(db)

def get_fopc02_repo(db: Session = Depends(get_db)) -> FOPC02RepoImpl:
    return FOPC02RepoImpl(db)

def get_foos01_repo(db: Session = Depends(get_db)) -> FOOS01RepoImpl:
    return FOOS01RepoImpl(db)

def get_fopp02_repo(db: Session = Depends(get_db)) -> FOPP02RepoImpl:
    return FOPP02RepoImpl(db)
