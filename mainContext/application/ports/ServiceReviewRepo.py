from abc import ABC, abstractmethod
from typing import List, Optional

from mainContext.application.dtos.service_review_dto import (
    ServiceReviewCreateDTO,
    ServiceReviewDTO,
    ServiceReviewSummaryDTO,
    ServiceReviewSummaryFilterDTO,
    ServiceReviewUpdateDTO,
)


class ServiceReviewRepo(ABC):
    @abstractmethod
    def create_service_review(self, dto: ServiceReviewCreateDTO) -> int:
        pass

    @abstractmethod
    def get_service_review_by_id(self, review_id: int) -> Optional[ServiceReviewDTO]:
        pass

    @abstractmethod
    def get_service_review_by_target(self, fo_type: str, fo_id: int) -> Optional[ServiceReviewDTO]:
        pass

    @abstractmethod
    def get_all_service_reviews(self) -> List[ServiceReviewDTO]:
        pass

    @abstractmethod
    def update_service_review(self, review_id: int, dto: ServiceReviewUpdateDTO) -> bool:
        pass

    @abstractmethod
    def delete_service_review(self, review_id: int) -> bool:
        pass

    @abstractmethod
    def get_service_reviews_summary(self, filters: ServiceReviewSummaryFilterDTO) -> ServiceReviewSummaryDTO:
        pass