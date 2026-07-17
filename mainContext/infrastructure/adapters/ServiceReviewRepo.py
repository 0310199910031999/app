import datetime
from typing import Dict, List, Optional

from sqlalchemy import exists, func, or_
from sqlalchemy.orm import Session

from mainContext.application.dtos.service_review_dto import (
    ServiceReviewCreateDTO,
    ServiceReviewDTO,
    ServiceReviewEmployeeFormatStatusDTO,
    ServiceReviewEmployeeTotalDTO,
    ServiceReviewFormatTotalDTO,
    ServiceReviewPendingClientDTO,
    ServiceReviewPendingEmployeeDTO,
    ServiceReviewPendingFilterDTO,
    ServiceReviewPendingItemDTO,
    ServiceReviewPendingResultDTO,
    ServiceReviewStatusTotalDTO,
    ServiceReviewSummaryDTO,
    ServiceReviewSummaryFilterDTO,
    ServiceReviewUpdateDTO,
)
from mainContext.application.ports.ServiceReviewRepo import ServiceReviewRepo
from mainContext.infrastructure.models import (
    Clients,
    Employees,
    Fobc01,
    Foem01,
    Foim01,
    Fole01,
    Foos01,
    Fopc02,
    Fopp02,
    Fosc01,
    Fosp01,
    ServiceReviews as ServiceReviewModel,
)


class ServiceReviewRepoImpl(ServiceReviewRepo):
    SUPPORTED_FORMATS: Dict[str, Dict[str, object]] = {
        "fole01": {"model": Fole01, "employee_field": "employee_id", "date_field": "date_signed", "display_name": "FO-LE-01", "client_field": "client_id"},
        "foim01": {"model": Foim01, "employee_field": "employee_id", "date_field": "date_signed", "display_name": "FO-IM-01", "client_field": "client_id"},
        "fosp01": {"model": Fosp01, "employee_field": "employee_id", "date_field": "date_signed", "display_name": "FO-SP-01", "client_field": "client_id"},
        "fosc01": {"model": Fosc01, "employee_field": "employee_id", "date_field": "date_signed", "display_name": "FO-SC-01", "client_field": "client_id"},
        "foos01": {"model": Foos01, "employee_field": "employee_id", "date_field": "date_signed", "display_name": "FO-OS-01", "client_field": "client_id"},
        "foem01": {"model": Foem01, "employee_field": "employee_id", "date_field": "date_signed", "display_name": "FO-EM-01", "client_field": "client_id"},
        "fobc01": {"model": Fobc01, "employee_field": "employee_id", "date_field": "date_signed", "display_name": "FO-BC-01", "client_field": "client_id"},
        "fopc02": {"model": Fopc02, "employee_field": "employee_id", "date_field": "return_date", "display_name": "FO-PC-02", "client_field": "client_id"},
        "fopp02": {"model": Fopp02, "employee_field": "employee_id", "date_field": "delivery_date", "display_name": "FO-PP-02", "client_field": None},
    }

    def __init__(self, db: Session):
        self.db = db
        self._format_order = {
            fo_type: index for index, fo_type in enumerate(self.SUPPORTED_FORMATS.keys())
        }

    def _normalize_fo_type(self, fo_type: str) -> str:
        normalized = (fo_type or "").strip().lower()
        if not normalized:
            raise ValueError("fo_type es requerido")
        return normalized

    def _normalize_status(self, status: str) -> str:
        normalized = (status or "").strip()
        if not normalized:
            raise ValueError("status es requerido")
        return normalized

    def _normalize_comments(self, comments: Optional[str]) -> Optional[str]:
        if comments is None:
            return None

        normalized = comments.strip()
        return normalized or None

    def _build_employee_name(
        self,
        employee_id: Optional[int],
        name: Optional[str],
        lastname: Optional[str],
    ) -> str:
        full_name = " ".join(part for part in [name, lastname] if part).strip()
        if full_name:
            return full_name
        if employee_id is not None:
            return f"Empleado {employee_id}"
        return "Empleado no asignado"

    def _get_format_definition(self, fo_type: str) -> tuple[str, Dict[str, object]]:
        normalized = self._normalize_fo_type(fo_type)
        definition = self.SUPPORTED_FORMATS.get(normalized)
        if definition is None:
            supported = ", ".join(self.SUPPORTED_FORMATS.keys())
            raise ValueError(
                f"fo_type '{normalized}' no soportado. Usa uno de: {supported}"
            )
        return normalized, definition

    def _validate_target_exists(self, fo_type: str, fo_id: int) -> str:
        normalized, definition = self._get_format_definition(fo_type)
        model = definition["model"]
        exists = self.db.query(model.id).filter(model.id == fo_id).first() is not None
        if not exists:
            raise ValueError(f"No existe un registro {normalized} con id {fo_id}")
        return normalized

    def _normalize_summary_filters(
        self, filters: ServiceReviewSummaryFilterDTO
    ) -> tuple[List[str], Optional[List[str]], Optional[List[int]], datetime.datetime, datetime.datetime]:
        if filters.end_date < filters.start_date:
            raise ValueError("end_date debe ser mayor o igual a start_date")

        selected_formats: List[str] = []
        if filters.fo_types:
            seen_formats = set()
            for fo_type in filters.fo_types:
                normalized, _ = self._get_format_definition(fo_type)
                if normalized not in seen_formats:
                    seen_formats.add(normalized)
                    selected_formats.append(normalized)
        else:
            selected_formats = list(self.SUPPORTED_FORMATS.keys())

        statuses = None
        if filters.statuses:
            statuses = []
            seen_statuses = set()
            for status in filters.statuses:
                normalized_status = self._normalize_status(status)
                if normalized_status not in seen_statuses:
                    seen_statuses.add(normalized_status)
                    statuses.append(normalized_status)

        employee_ids = None
        if filters.employee_ids:
            employee_ids = list(dict.fromkeys(filters.employee_ids))

        start_at = datetime.datetime.combine(filters.start_date, datetime.time.min)
        end_at = datetime.datetime.combine(
            filters.end_date + datetime.timedelta(days=1),
            datetime.time.min,
        )

        return selected_formats, statuses, employee_ids, start_at, end_at

    def _to_dto(self, model: ServiceReviewModel) -> ServiceReviewDTO:
        return ServiceReviewDTO(
            id=model.id,
            status=model.status,
            comments=model.comments,
            fo_type=model.fo_type,
            fo_id=model.fo_id,
            created_at=model.created_at,
        )

    def create_service_review(self, dto: ServiceReviewCreateDTO) -> int:
        try:
            normalized_fo_type = self._validate_target_exists(dto.fo_type, dto.fo_id)
            existing = (
                self.db.query(ServiceReviewModel.id)
                .filter_by(fo_type=normalized_fo_type, fo_id=dto.fo_id)
                .first()
            )
            if existing:
                raise ValueError(
                    "Ya existe un service review para ese fo_type y fo_id"
                )

            model = ServiceReviewModel(
                status=self._normalize_status(dto.status),
                comments=self._normalize_comments(dto.comments),
                fo_type=normalized_fo_type,
                fo_id=dto.fo_id,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.id
        except ValueError:
            self.db.rollback()
            raise
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al crear service review: {exc}")

    def get_service_review_by_id(self, review_id: int) -> Optional[ServiceReviewDTO]:
        try:
            model = self.db.query(ServiceReviewModel).filter_by(id=review_id).first()
            if not model:
                return None
            return self._to_dto(model)
        except Exception as exc:
            raise Exception(f"Error al obtener service review: {exc}")

    def get_service_review_by_target(
        self, fo_type: str, fo_id: int
    ) -> Optional[ServiceReviewDTO]:
        try:
            normalized_fo_type, _ = self._get_format_definition(fo_type)
            model = (
                self.db.query(ServiceReviewModel)
                .filter_by(fo_type=normalized_fo_type, fo_id=fo_id)
                .order_by(ServiceReviewModel.created_at.desc(), ServiceReviewModel.id.desc())
                .first()
            )
            if not model:
                return None
            return self._to_dto(model)
        except ValueError:
            raise
        except Exception as exc:
            raise Exception(f"Error al obtener service review por formato: {exc}")

    def get_all_service_reviews(self) -> List[ServiceReviewDTO]:
        try:
            models = (
                self.db.query(ServiceReviewModel)
                .order_by(ServiceReviewModel.created_at.desc(), ServiceReviewModel.id.desc())
                .all()
            )
            return [self._to_dto(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar service reviews: {exc}")

    def update_service_review(self, review_id: int, dto: ServiceReviewUpdateDTO) -> bool:
        try:
            if dto.status is None and dto.comments is None:
                raise ValueError("No hay campos para actualizar")

            model = self.db.query(ServiceReviewModel).filter_by(id=review_id).first()
            if not model:
                return False

            if dto.status is not None:
                model.status = self._normalize_status(dto.status)
            if dto.comments is not None:
                model.comments = self._normalize_comments(dto.comments)

            self.db.commit()
            self.db.refresh(model)
            return True
        except ValueError:
            self.db.rollback()
            raise
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al actualizar service review: {exc}")

    def delete_service_review(self, review_id: int) -> bool:
        try:
            model = self.db.query(ServiceReviewModel).filter_by(id=review_id).first()
            if not model:
                return False
            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al eliminar service review: {exc}")

    def get_service_reviews_summary(
        self, filters: ServiceReviewSummaryFilterDTO
    ) -> ServiceReviewSummaryDTO:
        try:
            (
                selected_formats,
                statuses,
                employee_ids,
                start_at,
                end_at,
            ) = self._normalize_summary_filters(filters)

            reviews_by_employee_format_status: List[ServiceReviewEmployeeFormatStatusDTO] = []
            totals_by_format_map = {fo_type: 0 for fo_type in selected_formats}
            totals_by_status_map = {status: 0 for status in statuses} if statuses else {}
            totals_by_employee_map = {}
            total_reviews = 0

            for fo_type in selected_formats:
                definition = self.SUPPORTED_FORMATS[fo_type]
                model = definition["model"]
                employee_id_column = getattr(model, definition["employee_field"])

                query = (
                    self.db.query(
                        ServiceReviewModel.status.label("review_status"),
                        employee_id_column.label("employee_id"),
                        Employees.name.label("employee_name"),
                        Employees.lastname.label("employee_lastname"),
                        func.count(ServiceReviewModel.id).label("total"),
                    )
                    .join(model, ServiceReviewModel.fo_id == model.id)
                    .outerjoin(Employees, employee_id_column == Employees.id)
                    .filter(ServiceReviewModel.fo_type == fo_type)
                    .filter(ServiceReviewModel.created_at >= start_at)
                    .filter(ServiceReviewModel.created_at < end_at)
                )

                if statuses:
                    query = query.filter(ServiceReviewModel.status.in_(statuses))
                if employee_ids:
                    query = query.filter(employee_id_column.in_(employee_ids))

                rows = (
                    query.group_by(
                        ServiceReviewModel.status,
                        employee_id_column,
                        Employees.name,
                        Employees.lastname,
                    )
                    .all()
                )

                for row in rows:
                    employee_name = row.employee_name or None
                    employee_lastname = row.employee_lastname or None
                    employee_full_name = self._build_employee_name(
                        row.employee_id,
                        employee_name,
                        employee_lastname,
                    )

                    reviews_by_employee_format_status.append(
                        ServiceReviewEmployeeFormatStatusDTO(
                            fo_type=fo_type,
                            status=row.review_status,
                            employee_id=row.employee_id,
                            employee_name=employee_name,
                            employee_lastname=employee_lastname,
                            employee_full_name=employee_full_name,
                            total=row.total,
                        )
                    )

                    totals_by_format_map[fo_type] += row.total
                    totals_by_status_map[row.review_status] = (
                        totals_by_status_map.get(row.review_status, 0) + row.total
                    )

                    if row.employee_id not in totals_by_employee_map:
                        totals_by_employee_map[row.employee_id] = {
                            "employee_name": employee_name,
                            "employee_lastname": employee_lastname,
                            "employee_full_name": employee_full_name,
                            "total": 0,
                        }

                    totals_by_employee_map[row.employee_id]["total"] += row.total
                    total_reviews += row.total

            reviews_by_employee_format_status.sort(
                key=lambda item: (
                    self._format_order.get(item.fo_type, len(self._format_order)),
                    item.status,
                    item.employee_full_name,
                    item.employee_id if item.employee_id is not None else -1,
                )
            )

            totals_by_format = [
                ServiceReviewFormatTotalDTO(
                    fo_type=fo_type,
                    total=totals_by_format_map[fo_type],
                )
                for fo_type in selected_formats
            ]

            status_order = statuses if statuses else sorted(totals_by_status_map.keys())
            totals_by_status = [
                ServiceReviewStatusTotalDTO(
                    status=status,
                    total=totals_by_status_map.get(status, 0),
                )
                for status in status_order
            ]

            totals_by_employee = [
                ServiceReviewEmployeeTotalDTO(
                    employee_id=employee_id,
                    employee_name=data["employee_name"],
                    employee_lastname=data["employee_lastname"],
                    employee_full_name=data["employee_full_name"],
                    total=data["total"],
                )
                for employee_id, data in sorted(
                    totals_by_employee_map.items(),
                    key=lambda item: (
                        -item[1]["total"],
                        item[1]["employee_full_name"],
                        item[0] if item[0] is not None else -1,
                    ),
                )
            ]

            return ServiceReviewSummaryDTO(
                totalReviews=total_reviews,
                reviewsByEmployeeFormatStatus=reviews_by_employee_format_status,
                totalsByFormat=totals_by_format,
                totalsByStatus=totals_by_status,
                totalsByEmployee=totals_by_employee,
            )
        except ValueError:
            raise
        except Exception as exc:
            raise Exception(f"Error al obtener resumen de service reviews: {exc}")

    def get_pending_service_reviews(
        self, filters: ServiceReviewPendingFilterDTO
    ) -> ServiceReviewPendingResultDTO:
        try:
            if filters.end_date < filters.start_date:
                raise ValueError("end_date debe ser mayor o igual a start_date")

            start_at = datetime.datetime.combine(filters.start_date, datetime.time.min)
            end_at = datetime.datetime.combine(
                filters.end_date + datetime.timedelta(days=1),
                datetime.time.min,
            )

            items: List[ServiceReviewPendingItemDTO] = []

            for fo_type, definition in self.SUPPORTED_FORMATS.items():
                model = definition["model"]
                date_col = getattr(model, definition["date_field"])
                employee_col = getattr(model, definition["employee_field"])
                display_name = definition["display_name"]
                client_field = definition["client_field"]

                review_exists_subq = (
                    exists()
                    .where(ServiceReviewModel.fo_type == fo_type)
                    .where(ServiceReviewModel.fo_id == model.id)
                )

                if client_field is not None:
                    client_col = getattr(model, client_field)
                    query = self.db.query(
                        model.id.label("doc_id"),
                        date_col.label("doc_date"),
                        employee_col.label("employee_id"),
                        Employees.name.label("employee_name"),
                        Employees.lastname.label("employee_lastname"),
                        client_col.label("client_id"),
                        Clients.name.label("client_name"),
                    )
                    query = query.outerjoin(Employees, employee_col == Employees.id)
                    query = query.outerjoin(Clients, client_col == Clients.id)
                    query = query.filter(
                        or_(client_col.is_(None), ~client_col.in_([11, 90]))
                    )
                else:
                    query = self.db.query(
                        model.id.label("doc_id"),
                        date_col.label("doc_date"),
                        employee_col.label("employee_id"),
                        Employees.name.label("employee_name"),
                        Employees.lastname.label("employee_lastname"),
                        Fopc02.client_id.label("client_id"),
                        Clients.name.label("client_name"),
                    )
                    query = query.outerjoin(Employees, employee_col == Employees.id)
                    query = query.outerjoin(Fopc02, model.fopc_id == Fopc02.id)
                    query = query.outerjoin(Clients, Fopc02.client_id == Clients.id)
                    query = query.filter(
                        or_(Fopc02.client_id.is_(None), ~Fopc02.client_id.in_([11, 90]))
                    )

                query = (
                    query.filter(model.status == "Cerrado")
                    .filter(date_col.isnot(None))
                    .filter(date_col >= start_at)
                    .filter(date_col < end_at)
                    .filter(~review_exists_subq)
                )

                rows = query.all()

                for row in rows:
                    doc_date = row.doc_date
                    date_value = (
                        doc_date.date() if hasattr(doc_date, "date") else doc_date
                    )
                    employee_name = row.employee_name or None
                    employee_lastname = row.employee_lastname or None
                    employee_full_name = self._build_employee_name(
                        row.employee_id,
                        employee_name,
                        employee_lastname,
                    )
                    items.append(
                        ServiceReviewPendingItemDTO(
                            id=row.doc_id,
                            fo_type=fo_type,
                            fo_type_display=display_name,
                            date=date_value,
                            employee=ServiceReviewPendingEmployeeDTO(
                                employee_id=row.employee_id,
                                employee_name=employee_name,
                                employee_lastname=employee_lastname,
                                employee_full_name=employee_full_name,
                            ),
                            client=ServiceReviewPendingClientDTO(
                                client_id=row.client_id,
                                client_name=row.client_name,
                            ),
                        )
                    )

            items.sort(
                key=lambda item: (
                    self._format_order.get(item.fo_type, len(self._format_order)),
                    item.date,
                    item.fo_type,
                    item.id,
                )
            )

            return ServiceReviewPendingResultDTO(
                totalPending=len(items),
                items=items,
            )
        except ValueError:
            raise
        except Exception as exc:
            raise Exception(f"Error al obtener service reviews pendientes: {exc}")