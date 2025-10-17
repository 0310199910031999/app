from mainContext.domain.models.Equipment import Equipment, EquipmentType, EquipmentBrand
from mainContext.application.dtos.Equipment.create_equipment_dto import CreateEquipmentDTO
from mainContext.application.dtos.Equipment.update_equipment_dto import UpdateEquipmentDTO


def dto_to_equipment(dto: CreateEquipmentDTO) -> Equipment:
    return Equipment(
        id=0,  # se ignora en creación
        client_id=dto.client_id,
        type=EquipmentType(id=dto.type_id, name=""),  # name se rellena en repo
        brand=EquipmentBrand(id=dto.brand_id, name="", img_path=""),
        model=dto.model,
        mast=dto.mast,
        serial_number=dto.serial_number,
        hourometer=dto.hourometer,
        doh=dto.doh,
        economic_number=dto.economic_number,
        capacity=dto.capacity,
        addition=dto.addition,
        motor=dto.motor,
        property=dto.property
    )
def dto_to_updated_equipment(dto: UpdateEquipmentDTO, existing: Equipment) -> Equipment:
    return Equipment(
        id=existing.id,
        client_id=existing.client_id,
        type=EquipmentType(id=dto.type_id, name=""),
        brand=EquipmentBrand(id=dto.brand_id, name="", img_path=""),
        model=dto.model,
        mast=dto.mast,
        serial_number=dto.serial_number,
        hourometer=dto.hourometer,
        doh=dto.doh,
        economic_number=dto.economic_number,
        capacity=dto.capacity,
        addition=dto.addition,
        motor=dto.motor,
        property=dto.property
    )
