from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExportFormatFiltersDTO(BaseModel):
    fo_cr_02: bool = False
    fo_em_01: bool = False
    fo_im_01: bool = False
    fo_im_03: bool = False
    fo_le_01: bool = False
    fo_os_01: bool = False
    fo_pc_02: bool = False
    fo_pp_02: bool = False
    fo_sc_01: bool = False
    fo_sp_01: bool = False


class ExportRequestDTO(BaseModel):
    client_id: int
    equipment_id: int
    start_date: date
    end_date: date
    requesting_user_id: int
    format_filters: ExportFormatFiltersDTO


class ExportJobCreateDTO(BaseModel):
    id: str
    requested_by_user_id: int
    client_id: int
    equipment_id: int
    start_date: date
    end_date: date
    format_filters: dict = Field(default_factory=dict)
    status: str = 'queued'
    stage: str = 'queued'
    progress_pct: int = 0
    total_documents: int = 0
    processed_documents: int = 0


class ExportJobProgressDTO(BaseModel):
    status: str
    stage: str
    progress_pct: int
    processed_documents: int = 0
    total_documents: int = 0
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    error_message: Optional[str] = None


class ExportJobCompleteDTO(BaseModel):
    zip_filename: str
    zip_path: str
    zip_size_bytes: int
    download_token_hash: str
    token_expires_at: datetime
    processed_documents: int
    total_documents: int


class ExportJobDTO(BaseModel):
    id: str
    requested_by_user_id: int
    client_id: int
    equipment_id: int
    status: str
    stage: str
    progress_pct: int
    total_documents: int
    processed_documents: int
    start_date: date
    end_date: date
    format_filters: dict
    zip_filename: Optional[str] = None
    zip_path: Optional[str] = None
    zip_size_bytes: Optional[int] = None
    download_token_hash: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    download_count: int = 0
    last_download_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    updated_at: datetime


class ExportDocumentRowDTO(BaseModel):
    format_key: str
    format_label: str
    format_name: str
    format_folder_name: str
    document_id: int
    equipment_id: int
    client_id: int
    date_created: date
    folder_equipment_name: str
    filename: str
    excel_row: dict
