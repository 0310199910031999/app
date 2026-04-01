from typing import List

from fastapi import APIRouter, Depends, HTTPException

from mainContext.application.dtos.spare_part_category_dto import (
    SparePartCategoryCreateDTO,
    SparePartCategoryUpdateDTO,
)
from mainContext.application.use_cases.spare_part_category_use_cases import (
    CreateSparePartCategory,
    GetSparePartCategoryById,
    GetAllSparePartCategories,
    UpdateSparePartCategory,
    DeleteSparePartCategory,
)
from mainContext.infrastructure.dependencies import get_spare_part_category_repo
from mainContext.infrastructure.adapters.SparePartCategoryRepo import SparePartCategoryRepoImpl
from api.v1.schemas.spare_part_category import (
    SparePartCategorySchema,
    SparePartCategoryCreateSchema,
    SparePartCategoryUpdateSchema,
)
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

SparePartCategoryRouter = APIRouter(prefix="/spare-part-categories", tags=["Spare Part Categories"])


@SparePartCategoryRouter.post("/create", response_model=ResponseIntModel)
def create_spare_part_category(dto: SparePartCategoryCreateSchema, repo: SparePartCategoryRepoImpl = Depends(get_spare_part_category_repo)):
    use_case = CreateSparePartCategory(repo)
    category_id = use_case.execute(SparePartCategoryCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=category_id)


@SparePartCategoryRouter.get("/get/{id}", response_model=SparePartCategorySchema)
def get_spare_part_category_by_id(id: int, repo: SparePartCategoryRepoImpl = Depends(get_spare_part_category_repo)):
    use_case = GetSparePartCategoryById(repo)
    category = use_case.execute(id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría de refacciones no encontrada")
    return category


@SparePartCategoryRouter.get("/get_all", response_model=List[SparePartCategorySchema])
def get_all_spare_part_categories(repo: SparePartCategoryRepoImpl = Depends(get_spare_part_category_repo)):
    use_case = GetAllSparePartCategories(repo)
    return use_case.execute()


@SparePartCategoryRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_spare_part_category(id: int, dto: SparePartCategoryUpdateSchema, repo: SparePartCategoryRepoImpl = Depends(get_spare_part_category_repo)):
    use_case = UpdateSparePartCategory(repo)
    updated = use_case.execute(id, SparePartCategoryUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Categoría de refacciones no encontrada")
    return ResponseBoolModel(result=updated)


@SparePartCategoryRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_spare_part_category(id: int, repo: SparePartCategoryRepoImpl = Depends(get_spare_part_category_repo)):
    use_case = DeleteSparePartCategory(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoría de refacciones no encontrada")
    return ResponseBoolModel(result=deleted)
