from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_pp_02_dto import (
    FOPP02CreateDTO,
    FOPP02UpdateDTO,
    FOPP02SignatureDTO,
    FOPP02TableRowDTO,
    GetFOPP02ByFOPCDTO,
    FOPP02ByFOPCResponseDTO
)
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_pp_02 import (
    CreateFOPP02,
    UpdateFOPP02,
    GetFOPP02ById,
    GetListFOPP02ByFOPCId,
    DeleteFOPP02,
    SignFOPP02Departure,
    SignFOPP02Delivery,
    GetListFOPP02Table,
    GetFOPP02ByFOPC
)
from mainContext.application.use_cases.vendor_use_cases import GetAllVendors

# Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_pp_02_repo import FOPP02RepoImpl
from mainContext.infrastructure.adapters.VendorRepo import VendorRepoImpl

# Importing Schemas
from api.v1.schemas.Formats.fo_pp_02 import (
    FOPP02UpdateSchema,
    FOPP02Schema,
    FOPP02TableRowSchema,
    FOPP02CreateSchema,
    FOPP02SignatureSchema,
    GetFOPP02ByFOPCSchema,
    FOPP02ByFOPCResponseSchema
)
from api.v1.schemas.vendor import VendorSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel


FOPP02Router = APIRouter(prefix="/fopp02", tags=["FOPP02"])


@FOPP02Router.post("/create", response_model=ResponseIntModel)
def create_fopp02(dto: FOPP02CreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro FOPP02 (Préstamo de Propiedad)
    
    Requiere:
    - employee_id: ID del empleado responsable
    - fopc_id: ID del FOPC02 relacionado
    - property_id: ID de la propiedad del equipo
    - status: Estado inicial (default: "Abierto")
    - file_id: ID del file (opcional, se obtiene del FOPC02 si existe)
    """
    repo = FOPP02RepoImpl(db)
    use_case = CreateFOPP02(repo)
    created = use_case.execute(FOPP02CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)


@FOPP02Router.get("/get_by_id/{id}", response_model=FOPP02Schema)
def get_fopp02_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un FOPP02 por su ID con todas sus relaciones cargadas
    
    Incluye:
    - Empleado responsable
    - FOPC02 relacionado
    - Propiedad del equipo
    - Vendedor (si aplica)
    """
    repo = FOPP02RepoImpl(db)
    use_case = GetFOPP02ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOPP02 not found")
    return get


@FOPP02Router.get("/get_table/{fopc_id}", response_model=List[FOPP02TableRowSchema])
def get_list_fopp02_table(fopc_id: int, db: Session = Depends(get_db)):
    """
    Obtiene la lista de FOPP02 en formato tabla para un FOPC02 específico
    
    Retorna:
    - id: ID del FOPP02
    - status: Estado del documento
    - file: ID del file
    - equipment_name: Nombre del equipo (marca + modelo)
    - employee_name: Nombre completo del empleado
    - date_created: Fecha de creación
    """
    repo = FOPP02RepoImpl(db)
    use_case = GetListFOPP02Table(repo)
    return use_case.execute(fopc_id)


@FOPP02Router.put("/update/{fopp02_id}", response_model=ResponseBoolModel)
def update_fopp02(fopp02_id: int, dto: FOPP02UpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un FOPP02
    
    Campos actualizables:
    - departure_date: Fecha de salida
    - departure_description: Descripción de salida
    - delivery_date: Fecha de entrega
    - delivery_description: Descripción de entrega
    - name_auth_departure: Nombre del autorizador de salida
    - name_delivery: Nombre quien recibe
    - observations: Observaciones generales
    """
    repo = FOPP02RepoImpl(db)
    use_case = UpdateFOPP02(repo)
    updated = use_case.execute(fopp02_id, FOPP02UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOPP02 not found")
    return ResponseBoolModel(result=updated)


@FOPP02Router.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_fopp02(id: int, db: Session = Depends(get_db)):
    """
    Elimina un FOPP02 y todas sus firmas asociadas
    """
    repo = FOPP02RepoImpl(db)
    use_case = DeleteFOPP02(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="FOPP02 not found")
    return ResponseBoolModel(result=deleted)


@FOPP02Router.post("/sign_departure/{id}", response_model=ResponseBoolModel)
def sign_fopp02_departure(id: int, dto: FOPP02SignatureSchema, db: Session = Depends(get_db)):
    """
    Firma de salida (departure) del FOPP02
    
    Tipos de firma:
    - is_employee=True: Firma del técnico en salida (TecDep)
    - is_employee=False: Firma del cliente en salida (CliDep)
    
    Cierre automático:
    - Si todas las firmas (departure + delivery, técnico + cliente) están completas,
      el status cambia a "Cerrado"
    - Si el file asociado tiene todos sus documentos cerrados, también se cierra
    """
    repo = FOPP02RepoImpl(db)
    use_case = SignFOPP02Departure(repo)
    signed = use_case.execute(id, FOPP02SignatureDTO(**dto.model_dump()))
    if not signed:
        raise HTTPException(status_code=404, detail="FOPP02 not found or signature failed")
    return ResponseBoolModel(result=signed)


@FOPP02Router.post("/sign_delivery/{id}", response_model=ResponseBoolModel)
def sign_fopp02_delivery(id: int, dto: FOPP02SignatureSchema, db: Session = Depends(get_db)):
    """
    Firma de entrega (delivery) del FOPP02
    
    Tipos de firma:
    - is_employee=True: Firma del técnico en entrega (TecDel)
    - is_employee=False: Firma del cliente en entrega (CliDel)
    
    Cierre automático:
    - Si todas las firmas (departure + delivery, técnico + cliente) están completas,
      el status cambia a "Cerrado"
    - Si el file asociado tiene todos sus documentos cerrados, también se cierra
    """
    repo = FOPP02RepoImpl(db)
    use_case = SignFOPP02Delivery(repo)
    signed = use_case.execute(id, FOPP02SignatureDTO(**dto.model_dump()))
    if not signed:
        raise HTTPException(status_code=404, detail="FOPP02 not found or signature failed")
    return ResponseBoolModel(result=signed)


@FOPP02Router.get("/get_fopp02_by_fopc/{fopc_id}", response_model=List[FOPP02ByFOPCResponseSchema])
def get_fopp02_by_fopc(fopc_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los FOPP02 asociados a un FOPC02
    
    Útil para verificar si un FOPC02 tiene préstamos de propiedades asociados
    
    Retorna:
    - id: ID del FOPP02
    - date_created: Fecha de creación
    - status: Estado del documento
    - file_id: ID del file asociado
    """
    repo = FOPP02RepoImpl(db)
    use_case = GetFOPP02ByFOPC(repo)
    result = use_case.execute(GetFOPP02ByFOPCDTO(fopc_id=fopc_id))
    return result


@FOPP02Router.get("/vendors", response_model=List[VendorSchema])
def get_all_vendors(db: Session = Depends(get_db)):
    """
    Obtiene todos los vendors (proveedores)
    
    Retorna la lista completa de vendors con todos sus datos:
    - id: ID del vendor
    - name: Nombre del proveedor
    - rfc: RFC del proveedor
    - contact_person: Persona de contacto
    - phone_number: Número de teléfono
    - email: Correo electrónico
    """
    repo = VendorRepoImpl(db)
    use_case = GetAllVendors(repo)
    result = use_case.execute()
    return result
