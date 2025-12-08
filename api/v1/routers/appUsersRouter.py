from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from shared.db import get_db 
from mainContext.infrastructure.adapters.AppUserRepo import AppUserRepoImpl
from mainContext.application.use_cases.app_user_use_cases import (
    CreateAppUser,
    GetAppUserById,
    GetAllAppUsers,
    GetAppUsersByClient,
    UpdateAppUser,
    DeleteAppUser
)
from mainContext.application.dtos.app_user_dto import AppUserCreateDTO, AppUserUpdateDTO
from api.v1.schemas.app_user import AppUserSchema, AppUserCreateSchema, AppUserUpdateSchema, AppUserTableRowSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

AppUserRouter = APIRouter(prefix="/appUsers", tags=["AppUsers"])


@AppUserRouter.post("/create", response_model=ResponseIntModel)
def create_app_user(dto: AppUserCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario de aplicación
    
    Campos requeridos:
    - client_id: ID del cliente
    - name: Nombre
    - lastname: Apellido
    - email: Correo electrónico
    - password: Contraseña
    - phone_number (opcional): Número de teléfono
    - token_fcm (opcional): Token FCM para notificaciones
    """
    repo = AppUserRepoImpl(db)
    use_case = CreateAppUser(repo)
    app_user_id = use_case.execute(AppUserCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=app_user_id)


@AppUserRouter.get("/get/{id}", response_model=AppUserSchema)
def get_app_user_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un usuario de aplicación por su ID
    """
    repo = AppUserRepoImpl(db)
    use_case = GetAppUserById(repo)
    app_user = use_case.execute(id)
    if not app_user:
        raise HTTPException(status_code=404, detail="App user not found")
    return app_user


@AppUserRouter.get("/get_all", response_model=List[AppUserSchema])
def get_all_app_users(db: Session = Depends(get_db)):
    """
    Obtiene todos los usuarios de aplicación con sus clientes
    """
    repo = AppUserRepoImpl(db)
    use_case = GetAllAppUsers(repo)
    return use_case.execute()


@AppUserRouter.get("/get_table", response_model=List[AppUserTableRowSchema])
def get_app_users_table(db: Session = Depends(get_db)):
    """
    Obtiene todos los usuarios en formato tabla (simplificado para grids/tablas)
    
    Devuelve información resumida de usuarios con nombre de cliente
    """
    repo = AppUserRepoImpl(db)
    users = repo.listWithClientName()
    return users


@AppUserRouter.get("/by_client/{client_id}", response_model=List[AppUserSchema])
def get_app_users_by_client(client_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los usuarios de aplicación de un cliente específico
    """
    repo = AppUserRepoImpl(db)
    use_case = GetAppUsersByClient(repo)
    return use_case.execute(client_id)


@AppUserRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_app_user(id: int, dto: AppUserUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un usuario de aplicación
    
    Campos actualizables:
    - client_id: ID del cliente
    - name: Nombre
    - lastname: Apellido
    - email: Correo electrónico
    - password: Contraseña
    - phone_number: Número de teléfono
    - token_fcm: Token FCM
    """
    repo = AppUserRepoImpl(db)
    use_case = UpdateAppUser(repo)
    updated = use_case.execute(id, AppUserUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="App user not found")
    return ResponseBoolModel(result=updated)


@AppUserRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_app_user(id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario de aplicación
    """
    repo = AppUserRepoImpl(db)
    use_case = DeleteAppUser(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="App user not found")
    return ResponseBoolModel(result=deleted)


@AppUserRouter.get("/withClient", response_model=List[dict])
def list_app_users_with_client(db: Session = Depends(get_db)):
    """
    Lista usuarios de aplicación con nombre de cliente (endpoint legacy)
    """
    repo = AppUserRepoImpl(db)
    return repo.listWithClientName()
