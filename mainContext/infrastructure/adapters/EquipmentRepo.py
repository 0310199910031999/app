from mainContext.domain.models.Equipment import Equipment, EquipmentBrand, EquipmentType
from mainContext.application.ports.equipment_repo import EquipmentRepo
from mainContext.infrastructure.models import Equipment as EquipmentModel, EquipmentTypes, EquipmentBrands
from mainContext.application.dtos.Equipment.brands_types_dto import BrandsTypesDTO, BrandDTO, TypeDTO
from typing import List
from sqlalchemy.orm import Session

class EquipmentRepoImpl(EquipmentRepo):
    def __init__(self, db: Session):
        self.db = db
        
    def list_by_client_id(self, client_id: str) -> List[EquipmentModel]:
        query = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.client_id == client_id)
            .join(EquipmentModel.type)
            .join(EquipmentModel.brand)
            .all()
        )
        return [
            Equipment(
                id=eq.id,
                client_id=eq.client_id,
                type=EquipmentType(id=eq.type.id, name=eq.type.name),
                brand=EquipmentBrand(id=eq.brand.id, name=eq.brand.name, img_path=eq.brand.img_path),
                model=eq.model,
                mast=eq.mast,
                serial_number=eq.serial_number,
                hourometer=eq.hourometer,
                doh=eq.doh,
                economic_number=eq.economic_number,
                capacity=eq.capacity,
                addition=eq.addition,
                motor=eq.motor,
                property=eq.property
            )
            for eq in query
        ]

    def get_equipment_by_id(self, equipment_id: int) -> Equipment:
        query = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.id == equipment_id)
            .join(EquipmentModel.type)
            .join(EquipmentModel.brand)
            .first()
        )
        if not query:
            return None
        return Equipment(
            id=query.id,
            client_id=query.client_id,
            type=EquipmentType(id=query.type.id, name=query.type.name),
            brand=EquipmentBrand(id=query.brand.id, name=query.brand.name, img_path=query.brand.img_path),
            model=query.model,
            mast=query.mast,
            serial_number=query.serial_number,
            hourometer=query.hourometer,
            doh=query.doh,
            economic_number=query.economic_number,
            capacity=query.capacity,
            addition=query.addition,
            motor=query.motor,
            property=query.property
        )

    def create_equipment(self, equipment: Equipment) -> Equipment:
        new_equipment = EquipmentModel(
            client_id=equipment.client_id,
            type_id=equipment.type.id,
            brand_id=equipment.brand.id,
            model=equipment.model,
            mast=equipment.mast,
            serial_number=equipment.serial_number,
            hourometer=equipment.hourometer,
            doh=equipment.doh,
            economic_number=equipment.economic_number,
            capacity=equipment.capacity,
            addition=equipment.addition,
            motor=equipment.motor,
            property=equipment.property
        )
        self.db.add(new_equipment)
        self.db.commit()
        self.db.refresh(new_equipment)
        equipment.id = new_equipment.id
        return Equipment(
            id=new_equipment.id,
            client_id=new_equipment.client_id,
            type=EquipmentType(id=new_equipment.type.id, name=new_equipment.type.name),
            brand=EquipmentBrand(id=new_equipment.brand.id, name=new_equipment.brand.name, img_path=new_equipment.brand.img_path),
            model=new_equipment.model,
            mast=new_equipment.mast,
            serial_number=new_equipment.serial_number,
            hourometer=new_equipment.hourometer,
            doh=new_equipment.doh,
            economic_number=new_equipment.economic_number,
            capacity=new_equipment.capacity,
            addition=new_equipment.addition,
            motor=new_equipment.motor,
            property=new_equipment.property
        )
    
    def delete_equipment(self, equipment_id: int) -> bool:
        equipment = self.db.query(EquipmentModel).filter(EquipmentModel.id == equipment_id).first()
        if not equipment:
            return False
        self.db.delete(equipment)
        self.db.commit()
        return True
    
    def update_equipment(self, equipment_id: int, equipment: Equipment) -> Equipment:
        existing = self.db.query(EquipmentModel).filter(EquipmentModel.id == equipment_id).first()
        if not existing:
            return None
        existing.client_id = equipment.client_id
        existing.type_id = equipment.type.id
        existing.brand_id = equipment.brand.id
        existing.model = equipment.model
        existing.mast = equipment.mast
        existing.serial_number = equipment.serial_number
        existing.hourometer = equipment.hourometer
        existing.doh = equipment.doh
        existing.economic_number = equipment.economic_number
        existing.capacity = equipment.capacity
        existing.addition = equipment.addition
        existing.motor = equipment.motor
        existing.property = equipment.property
        
        self.db.commit()
        self.db.refresh(existing)
        
        return Equipment(
            id=existing.id,
            client_id=existing.client_id,
            type=EquipmentType(id=existing.type.id, name=existing.type.name),
            brand=EquipmentBrand(id=existing.brand.id, name=existing.brand.name, img_path=existing.brand.img_path),
            model=existing.model,
            mast=existing.mast,
            serial_number=existing.serial_number,
            hourometer=existing.hourometer,
            doh=existing.doh,
            economic_number=existing.economic_number,
            capacity=existing.capacity,
            addition=existing.addition,
            motor=existing.motor,
            property=existing.property
        )
    
    def get_brands_and_types(self):
        brands_db = self.db.query(EquipmentBrands).all()
        types_db = self.db.query(EquipmentTypes).all()

        brands_dto = [BrandDTO(id=brand.id, name=brand.name) for brand in brands_db]
        types_dto = [TypeDTO(id=type.id, name=type.name) for type in types_db]

        return BrandsTypesDTO(brands=brands_dto, types=types_dto)
    
    def get_equipment_by_property(self, property: str) -> List[EquipmentModel]:
        query = (
            self.db.query(EquipmentModel)
            .filter(EquipmentModel.property == property)
            .join(EquipmentModel.type)
            .join(EquipmentModel.brand)
            .all()
        )
        return [
            Equipment(
                id=eq.id,
                client_id=eq.client_id,
                type=EquipmentType(id=eq.type.id, name=eq.type.name),
                brand=EquipmentBrand(id=eq.brand.id, name=eq.brand.name, img_path=eq.brand.img_path),
                model=eq.model,
                mast=eq.mast,
                serial_number=eq.serial_number,
                hourometer=eq.hourometer,
                doh=eq.doh,
                economic_number=eq.economic_number,
                capacity=eq.capacity,
                addition=eq.addition,
                motor=eq.motor,
                property=eq.property
            )
            for eq in query
        ]
        
        
