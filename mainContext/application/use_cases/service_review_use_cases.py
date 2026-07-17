from typing import List, Optional

from mainContext.application.dtos.service_review_dto import (
    ServiceReviewCreateDTO,
    ServiceReviewDTO,
    ServiceReviewPendingFilterDTO,
    ServiceReviewPendingResultDTO,
    ServiceReviewSummaryDTO,
    ServiceReviewSummaryFilterDTO,
    ServiceReviewUpdateDTO,
)
from mainContext.application.ports.ServiceReviewRepo import ServiceReviewRepo


class CreateServiceReview:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self, dto: ServiceReviewCreateDTO) -> int:
        return self.repo.create_service_review(dto)


class GetServiceReviewById:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self, review_id: int) -> Optional[ServiceReviewDTO]:
        return self.repo.get_service_review_by_id(review_id)


class GetServiceReviewByTarget:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self, fo_type: str, fo_id: int) -> Optional[ServiceReviewDTO]:
        return self.repo.get_service_review_by_target(fo_type, fo_id)


class GetAllServiceReviews:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self) -> List[ServiceReviewDTO]:
        return self.repo.get_all_service_reviews()


class UpdateServiceReview:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self, review_id: int, dto: ServiceReviewUpdateDTO) -> bool:
        return self.repo.update_service_review(review_id, dto)


class DeleteServiceReview:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self, review_id: int) -> bool:
        return self.repo.delete_service_review(review_id)


class GetServiceReviewsSummary:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self, filters: ServiceReviewSummaryFilterDTO) -> ServiceReviewSummaryDTO:
        return self.repo.get_service_reviews_summary(filters)


class GetPendingServiceReviews:
    def __init__(self, repo: ServiceReviewRepo):
        self.repo = repo

    def execute(self, filters: ServiceReviewPendingFilterDTO) -> ServiceReviewPendingResultDTO:
        return self.repo.get_pending_service_reviews(filters)