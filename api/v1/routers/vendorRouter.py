from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.vendor_dto import VendorCreateDTO, VendorUpdateDTO
from mainContext.application.use_cases.vendor_use_cases import (
    CreateVendor,
    GetVendorById,
    GetAllVendors,
    UpdateVendor,
    DeleteVendor
)
from mainContext.infrastructure.adapters.VendorRepo import VendorRepoImpl

from api.v1.schemas.vendor import VendorSchema, VendorCreateSchema, VendorUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

VendorRouter = APIRouter(prefix="/vendors", tags=["Vendors"])


@VendorRouter.post("/create", response_model=ResponseIntModel)
def create_vendor(dto: VendorCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo vendor (proveedor)
    
    Campo requerido:
    - name: Nombre del vendor
    
    Campos opcionales:
    - rfc: RFC del vendor
    - contact_person: Persona de contacto
    - phone_number: Número de teléfono
    - email: Correo electrónico
    - address: Dirección
    """
    repo = VendorRepoImpl(db)
    use_case = CreateVendor(repo)
    vendor_id = use_case.execute(VendorCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=vendor_id)


@VendorRouter.get("/get/{id}", response_model=VendorSchema)
def get_vendor_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un vendor por su ID
    """
    repo = VendorRepoImpl(db)
    use_case = GetVendorById(repo)
    vendor = use_case.execute(id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@VendorRouter.get("/get_all", response_model=List[VendorSchema])
def get_all_vendors(db: Session = Depends(get_db)):
    """
    Obtiene todos los vendors (proveedores)
    
    Retorna la lista completa de vendors con todos sus datos:
    - id: ID del vendor
    - name: Nombre del vendor
    - rfc: RFC
    - contact_person: Persona de contacto
    - phone_number: Número de teléfono
    - email: Correo electrónico
    - address: Dirección
    """
    repo = VendorRepoImpl(db)
    use_case = GetAllVendors(repo)
    return use_case.execute()


@VendorRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_vendor(id: int, dto: VendorUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un vendor
    
    Campos actualizables:
    - name: Nombre del vendor
    - rfc: RFC
    - contact_person: Persona de contacto
    - phone_number: Número de teléfono
    - email: Correo electrónico
    - address: Dirección
    """
    repo = VendorRepoImpl(db)
    use_case = UpdateVendor(repo)
    updated = use_case.execute(id, VendorUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return ResponseBoolModel(result=updated)


@VendorRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_vendor(id: int, db: Session = Depends(get_db)):
    """
    Elimina un vendor
    """
    repo = VendorRepoImpl(db)
    use_case = DeleteVendor(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return ResponseBoolModel(result=deleted)
