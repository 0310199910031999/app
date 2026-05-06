from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExportFormatFiltersSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    fo_cr_02: bool = Field(default=False, alias='fo-cr-02')
    fo_em_01: bool = Field(default=False, alias='fo-em-01')
    fo_im_01: bool = Field(default=False, alias='fo-im-01')
    fo_im_03: bool = Field(default=False, alias='fo-im-03')
    fo_le_01: bool = Field(default=False, alias='fo-le-01')
    fo_os_01: bool = Field(default=False, alias='fo-os-01')
    fo_pc_02: bool = Field(default=False, alias='fo-pc-02')
    fo_pp_02: bool = Field(default=False, alias='fo-pp-02')
    fo_sc_01: bool = Field(default=False, alias='fo-sc-01')
    fo_sp_01: bool = Field(default=False, alias='fo-sp-01')

    @model_validator(mode='after')
    def validate_selected_formats(self):
        if not any(self.model_dump().values()):
            raise ValueError('At least one format filter must be enabled')
        return self


class ExportRequestSchema(BaseModel):
    client_id: int
    equipment_id: int
    start_date: date
    end_date: date
    requesting_user_id: int
    format_filters: ExportFormatFiltersSchema

    @model_validator(mode='after')
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError('end_date must be greater than or equal to start_date')
        return self


class ExportAcceptedSchema(BaseModel):
    job_id: str
    status: str
    stage: str
    message: Optional[str] = None


class ExportStatusSchema(BaseModel):
    job_id: str
    status: str
    stage: str
    progress_pct: int
    processed_documents: int
    total_documents: int
    message: Optional[str] = None
    download_ready: bool = False
    expires_at: Optional[datetime] = None
    download_url: Optional[str] = None
    error_message: Optional[str] = None


class ExportJobItemSchema(BaseModel):
    job_id: str
    requested_by_user_id: int
    client_id: int
    equipment_id: int
    start_date: date
    end_date: date
    format_filters: dict
    status: str
    stage: str
    progress_pct: int
    processed_documents: int
    total_documents: int
    message: Optional[str] = None
    download_ready: bool = False
    expires_at: Optional[datetime] = None
    error_message: Optional[str] = None
    download_count: int = 0
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    updated_at: datetime
    can_retry: bool = False


class ExportJobListSchema(BaseModel):
    items: list[ExportJobItemSchema]


class ExportRetryAcceptedSchema(ExportAcceptedSchema):
    source_job_id: str


class ExportDownloadSchema(BaseModel):
    job_id: str
    expires_at: Optional[datetime] = None
    download_url: Optional[str] = None
