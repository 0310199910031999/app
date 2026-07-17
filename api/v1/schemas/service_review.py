from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class ServiceReviewSchema(BaseModel):
    id: int
    status: str
    comments: Optional[str] = None
    fo_type: str
    fo_id: int
    created_at: datetime


class ServiceReviewCreateSchema(BaseModel):
    status: str
    comments: Optional[str] = None
    fo_type: str
    fo_id: int


class ServiceReviewUpdateSchema(BaseModel):
    status: Optional[str] = None
    comments: Optional[str] = None


class ServiceReviewSummaryFilterSchema(BaseModel):
    start_date: date
    end_date: date
    fo_types: Optional[List[str]] = None
    statuses: Optional[List[str]] = None
    employee_ids: Optional[List[int]] = None


class ServiceReviewEmployeeFormatStatusSchema(BaseModel):
    fo_type: str
    status: str
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_lastname: Optional[str] = None
    employee_full_name: str
    total: int


class ServiceReviewFormatTotalSchema(BaseModel):
    fo_type: str
    total: int


class ServiceReviewStatusTotalSchema(BaseModel):
    status: str
    total: int


class ServiceReviewEmployeeTotalSchema(BaseModel):
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_lastname: Optional[str] = None
    employee_full_name: str
    total: int


class ServiceReviewSummarySchema(BaseModel):
    totalReviews: int
    reviewsByEmployeeFormatStatus: List[ServiceReviewEmployeeFormatStatusSchema]
    totalsByFormat: List[ServiceReviewFormatTotalSchema]
    totalsByStatus: List[ServiceReviewStatusTotalSchema]
    totalsByEmployee: List[ServiceReviewEmployeeTotalSchema]


class ServiceReviewPendingFilterSchema(BaseModel):
    start_date: date
    end_date: date


class ServiceReviewPendingEmployeeSchema(BaseModel):
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_lastname: Optional[str] = None
    employee_full_name: str


class ServiceReviewPendingClientSchema(BaseModel):
    client_id: Optional[int] = None
    client_name: Optional[str] = None


class ServiceReviewPendingItemSchema(BaseModel):
    id: int
    fo_type: str
    fo_type_display: str
    date: date
    employee: ServiceReviewPendingEmployeeSchema
    client: ServiceReviewPendingClientSchema


class ServiceReviewPendingResultSchema(BaseModel):
    totalPending: int
    items: List[ServiceReviewPendingItemSchema]