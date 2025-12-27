import base64
import os
import re
from typing import List, Optional

from sqlalchemy.orm import Session

from mainContext.application.ports.EquipmentBrandRepo import EquipmentBrandRepo
from mainContext.application.dtos.equipment_brand_dto import EquipmentBrandDTO, EquipmentBrandCreateDTO, EquipmentBrandUpdateDTO
from mainContext.infrastructure.models import EquipmentBrands as EquipmentBrandModel


CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE_DIR))
BRAND_IMG_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "brands")
BRAND_IMG_URL_BASE = "/static/img/brands"
os.makedirs(BRAND_IMG_DIR, exist_ok=True)

class EquipmentBrandRepoImpl(EquipmentBrandRepo):
    def __init__(self, db: Session):
        self.db = db

    def _sanitize_filename(self, name: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", (name or "").strip())
        cleaned = cleaned.strip("_")
        return cleaned or "brand"

    def _save_base64_image(self, base64_string: str, brand_name: str) -> str:
        header = ""
        data = base64_string
        if "," in base64_string:
            header, data = base64_string.split(",", 1)

        image_data = base64.b64decode(data)

        ext = ".png"
        header_lower = header.lower()
        if "image/jpeg" in header_lower or "image/jpg" in header_lower:
            ext = ".jpg"
        elif "image/png" in header_lower:
            ext = ".png"

        filename = f"{self._sanitize_filename(brand_name)}{ext}"
        save_path = os.path.join(BRAND_IMG_DIR, filename)

        if os.path.exists(save_path):
            os.remove(save_path)

        with open(save_path, "wb") as f:
            f.write(image_data)

        return f"{BRAND_IMG_URL_BASE}/{filename}"

    def _delete_existing_image(self, img_url: Optional[str]):
        if not img_url:
            return
        file_path = os.path.join(BRAND_IMG_DIR, os.path.basename(img_url))
        if os.path.exists(file_path):
            os.remove(file_path)

    def _rename_image_to_brand(self, img_url: str, brand_name: str) -> str:
        if not img_url:
            return img_url

        current_filename = os.path.basename(img_url)
        _, ext = os.path.splitext(current_filename)
        target_filename = f"{self._sanitize_filename(brand_name)}{ext}"

        if current_filename == target_filename:
            return img_url

        current_path = os.path.join(BRAND_IMG_DIR, current_filename)
        target_path = os.path.join(BRAND_IMG_DIR, target_filename)

        if os.path.exists(current_path):
            if os.path.exists(target_path):
                os.remove(target_path)
            os.rename(current_path, target_path)
            return f"{BRAND_IMG_URL_BASE}/{target_filename}"

        return img_url

    def create_equipment_brand(self, dto: EquipmentBrandCreateDTO) -> int:
        saved_img_url: Optional[str] = None
        try:
            img_url = None
            if dto.img_base64:
                img_url = self._save_base64_image(dto.img_base64, dto.name)
                saved_img_url = img_url

            model = EquipmentBrandModel(
                name=dto.name,
                img_path=img_url
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar marca de equipo en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            if saved_img_url:
                self._delete_existing_image(saved_img_url)
            raise Exception(f"Error al crear marca de equipo: {str(e)}")

    def get_equipment_brand_by_id(self, id: int) -> Optional[EquipmentBrandDTO]:
        try:
            model = self.db.query(EquipmentBrandModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return EquipmentBrandDTO(
                id=model.id,
                name=model.name,
                img_path=model.img_path
            )
        except Exception as e:
            raise Exception(f"Error al obtener marca de equipo: {str(e)}")

    def get_all_equipment_brands(self) -> List[EquipmentBrandDTO]:
        try:
            models = self.db.query(EquipmentBrandModel).all()
            
            return [
                EquipmentBrandDTO(
                    id=model.id,
                    name=model.name,
                    img_path=model.img_path
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener marcas de equipo: {str(e)}")

    def update_equipment_brand(self, id: int, dto: EquipmentBrandUpdateDTO) -> bool:
        saved_img_url: Optional[str] = None
        model: Optional[EquipmentBrandModel] = None
        try:
            model = self.db.query(EquipmentBrandModel).filter_by(id=id).first()
            if not model:
                return False

            new_brand_name = dto.name if dto.name is not None else (model.name or "")

            if dto.img_base64 is not None:
                new_img_url = self._save_base64_image(dto.img_base64, new_brand_name)
                saved_img_url = new_img_url
                if model.img_path and model.img_path != new_img_url:
                    self._delete_existing_image(model.img_path)
                model.img_path = new_img_url
            elif dto.name is not None and model.img_path:
                model.img_path = self._rename_image_to_brand(model.img_path, new_brand_name)

            if dto.name is not None:
                model.name = new_brand_name

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            if saved_img_url:
                self._delete_existing_image(saved_img_url)
            raise Exception(f"Error al actualizar marca de equipo: {str(e)}")

    def delete_equipment_brand(self, id: int) -> bool:
        try:
            model = self.db.query(EquipmentBrandModel).filter_by(id=id).first()
            if not model:
                return False

            self._delete_existing_image(model.img_path)
            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar marca de equipo: {str(e)}")
