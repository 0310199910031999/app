from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class ServiceReviewDTO(BaseModel):
    id: int
    status: str
    comments: Optional[str] = None
    fo_type: str
    fo_id: int
    created_at: datetime


class ServiceReviewCreateDTO(BaseModel):
    status: str
    comments: Optional[str] = None
    fo_type: str
    fo_id: int


class ServiceReviewUpdateDTO(BaseModel):
    status: Optional[str] = None
    comments: Optional[str] = None


class ServiceReviewSummaryFilterDTO(BaseModel):
    start_date: date
    end_date: date
    fo_types: Optional[List[str]] = None
    statuses: Optional[List[str]] = None
    employee_ids: Optional[List[int]] = None


class ServiceReviewEmployeeFormatStatusDTO(BaseModel):
    fo_type: str
    status: str
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_lastname: Optional[str] = None
    employee_full_name: str
    total: int


class ServiceReviewFormatTotalDTO(BaseModel):
    fo_type: str
    total: int


class ServiceReviewStatusTotalDTO(BaseModel):
    status: str
    total: int


class ServiceReviewEmployeeTotalDTO(BaseModel):
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_lastname: Optional[str] = None
    employee_full_name: str
    total: int


class ServiceReviewSummaryDTO(BaseModel):
    totalReviews: int
    reviewsByEmployeeFormatStatus: List[ServiceReviewEmployeeFormatStatusDTO]
    totalsByFormat: List[ServiceReviewFormatTotalDTO]
    totalsByStatus: List[ServiceReviewStatusTotalDTO]
    totalsByEmployee: List[ServiceReviewEmployeeTotalDTO]