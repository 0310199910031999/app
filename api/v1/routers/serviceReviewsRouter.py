from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel
from api.v1.schemas.service_review import (
    ServiceReviewCreateSchema,
    ServiceReviewSchema,
    ServiceReviewSummaryFilterSchema,
    ServiceReviewSummarySchema,
    ServiceReviewUpdateSchema,
)
from mainContext.application.dtos.service_review_dto import (
    ServiceReviewCreateDTO,
    ServiceReviewSummaryFilterDTO,
    ServiceReviewUpdateDTO,
)
from mainContext.application.use_cases.service_review_use_cases import (
    CreateServiceReview,
    DeleteServiceReview,
    GetAllServiceReviews,
    GetServiceReviewById,
    GetServiceReviewByTarget,
    GetServiceReviewsSummary,
    UpdateServiceReview,
)
from mainContext.infrastructure.adapters.ServiceReviewRepo import ServiceReviewRepoImpl
from mainContext.infrastructure.dependencies import get_service_review_repo


ServiceReviewsRouter = APIRouter(prefix="/service-reviews", tags=["Service Reviews"])


@ServiceReviewsRouter.post("/create", response_model=ResponseIntModel)
def create_service_review(
    dto: ServiceReviewCreateSchema,
    repo: ServiceReviewRepoImpl = Depends(get_service_review_repo),
):
    use_case = CreateServiceReview(repo)
    try:
        review_id = use_case.execute(ServiceReviewCreateDTO(**dto.model_dump()))
        return ResponseIntModel(result=review_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@ServiceReviewsRouter.get("/get/{review_id}", response_model=ServiceReviewSchema)
def get_service_review_by_id(
    review_id: int,
    repo: ServiceReviewRepoImpl = Depends(get_service_review_repo),
):
    use_case = GetServiceReviewById(repo)
    review = use_case.execute(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Service review no encontrado")
    return review


@ServiceReviewsRouter.get("/target/{fo_type}/{fo_id}", response_model=ServiceReviewSchema)
def get_service_review_by_target(
    fo_type: str,
    fo_id: int,
    repo: ServiceReviewRepoImpl = Depends(get_service_review_repo),
):
    use_case = GetServiceReviewByTarget(repo)
    try:
        review = use_case.execute(fo_type, fo_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not review:
        raise HTTPException(status_code=404, detail="Service review no encontrado")
    return review


@ServiceReviewsRouter.get("/get_all", response_model=List[ServiceReviewSchema])
def get_all_service_reviews(
    repo: ServiceReviewRepoImpl = Depends(get_service_review_repo),
):
    use_case = GetAllServiceReviews(repo)
    return use_case.execute()


@ServiceReviewsRouter.put("/update/{review_id}", response_model=ResponseBoolModel)
def update_service_review(
    review_id: int,
    dto: ServiceReviewUpdateSchema,
    repo: ServiceReviewRepoImpl = Depends(get_service_review_repo),
):
    use_case = UpdateServiceReview(repo)
    try:
        updated = use_case.execute(
            review_id,
            ServiceReviewUpdateDTO(**dto.model_dump(exclude_none=True)),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not updated:
        raise HTTPException(status_code=404, detail="Service review no encontrado")
    return ResponseBoolModel(result=updated)


@ServiceReviewsRouter.delete("/delete/{review_id}", response_model=ResponseBoolModel)
def delete_service_review(
    review_id: int,
    repo: ServiceReviewRepoImpl = Depends(get_service_review_repo),
):
    use_case = DeleteServiceReview(repo)
    deleted = use_case.execute(review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service review no encontrado")
    return ResponseBoolModel(result=deleted)


@ServiceReviewsRouter.post("/summary", response_model=ServiceReviewSummarySchema)
def get_service_reviews_summary(
    filters: ServiceReviewSummaryFilterSchema,
    repo: ServiceReviewRepoImpl = Depends(get_service_review_repo),
):
    use_case = GetServiceReviewsSummary(repo)
    try:
        return use_case.execute(ServiceReviewSummaryFilterDTO(**filters.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc