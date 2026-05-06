from fastapi import APIRouter, Depends, HTTPException
from typing import List
from mainContext.infrastructure.dependencies import get_app_user_repo
from mainContext.infrastructure.adapters.AppUserRepo import AppUserRepoImpl
from mainContext.application.use_cases.app_user_use_cases import (
    CreateAppUser,
    GetAppUserById,
    GetAllAppUsers,
    GetAppUsersByClient,
    UpdateAppUser,
    GetAppUserFcmToken,
    UpsertAppUserFcmToken,
    ClearAppUserFcmToken,
    DeleteAppUser,
    AuthAppUser,
)
from mainContext.application.dtos.app_user_dto import (
    AppUserCreateDTO,
    AppUserUpdateDTO,
    AppUserFcmTokenUpsertDTO,
    AuthAppUserDTO,
)
from api.v1.schemas.app_user import (
    AppUserSchema,
    AppUserCreateSchema,
    AppUserUpdateSchema,
    AppUserFcmTokenSchema,
    AppUserUpsertFcmTokenSchema,
    AppUserTableRowSchema,
    AuthAppUserSchema,
    AppUserAuthResponseSchema,
)
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

AppUserRouter = APIRouter(prefix="/appUsers", tags=["AppUsers"])


@AppUserRouter.post("/create", response_model=ResponseIntModel)
def create_app_user(dto: AppUserCreateSchema, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Crea un nuevo usuario de aplicación
    
    Campos requeridos:
    - client_id: ID del cliente
    - name: Nombre
    - lastname: Apellido
    - email: Correo electrónico
    - password: Contraseña
    - phone_number (opcional): Número de teléfono
    """
    use_case = CreateAppUser(repo)
    app_user_id = use_case.execute(AppUserCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=app_user_id)


@AppUserRouter.get("/get/{id}", response_model=AppUserSchema)
def get_app_user_by_id(id: int, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Obtiene un usuario de aplicación por su ID
    """
    use_case = GetAppUserById(repo)
    app_user = use_case.execute(id)
    if not app_user:
        raise HTTPException(status_code=404, detail="App user not found")
    return app_user


@AppUserRouter.get("/get_all", response_model=List[AppUserSchema])
def get_all_app_users(repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Obtiene todos los usuarios de aplicación con sus clientes
    """
    use_case = GetAllAppUsers(repo)
    return use_case.execute()


@AppUserRouter.get("/get_table", response_model=List[AppUserTableRowSchema])
def get_app_users_table(repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Obtiene todos los usuarios en formato tabla (simplificado para grids/tablas)
    
    Devuelve información resumida de usuarios con nombre de cliente
    """
    users = repo.listWithClientName()
    return users


@AppUserRouter.get("/by_client/{client_id}", response_model=List[AppUserSchema])
def get_app_users_by_client(client_id: int, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Obtiene todos los usuarios de aplicación de un cliente específico
    """
    use_case = GetAppUsersByClient(repo)
    return use_case.execute(client_id)


@AppUserRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_app_user(id: int, dto: AppUserUpdateSchema, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Actualiza los datos de un usuario de aplicación
    
    Campos actualizables:
    - client_id: ID del cliente
    - name: Nombre
    - lastname: Apellido
    - email: Correo electrónico
    - password: Contraseña
    - phone_number: Número de teléfono
    """
    use_case = UpdateAppUser(repo)
    updated = use_case.execute(id, AppUserUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="App user not found")
    return ResponseBoolModel(result=updated)


@AppUserRouter.get("/{id}/token-fcm", response_model=AppUserFcmTokenSchema)
def get_app_user_token_fcm(id: int, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Obtiene el token FCM dedicado de un usuario de aplicación.
    """
    use_case = GetAppUserFcmToken(repo)
    app_user_token = use_case.execute(id)
    if not app_user_token:
        raise HTTPException(status_code=404, detail="App user not found")
    return app_user_token


@AppUserRouter.put("/{id}/token-fcm", response_model=ResponseBoolModel)
def upsert_app_user_token_fcm(
    id: int,
    dto: AppUserUpsertFcmTokenSchema,
    repo: AppUserRepoImpl = Depends(get_app_user_repo),
):
    """
    Registra o reemplaza el token FCM de un usuario de aplicación.
    """
    use_case = UpsertAppUserFcmToken(repo)
    updated = use_case.execute(id, AppUserFcmTokenUpsertDTO(**dto.model_dump()))
    if not updated:
        raise HTTPException(status_code=404, detail="App user not found")
    return ResponseBoolModel(result=updated)


@AppUserRouter.delete("/{id}/token-fcm", response_model=ResponseBoolModel)
def clear_app_user_token_fcm(id: int, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Elimina el token FCM de un usuario de aplicación para el flujo de logout.
    """
    use_case = ClearAppUserFcmToken(repo)
    cleared = use_case.execute(id)
    if not cleared:
        raise HTTPException(status_code=404, detail="App user not found")
    return ResponseBoolModel(result=cleared)


@AppUserRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_app_user(id: int, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Elimina un usuario de aplicación
    """
    use_case = DeleteAppUser(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="App user not found")
    return ResponseBoolModel(result=deleted)


@AppUserRouter.get("/withClient", response_model=List[dict])
def list_app_users_with_client(repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Lista usuarios de aplicación con nombre de cliente (endpoint legacy)
    """
    return repo.listWithClientName()


@AppUserRouter.post("/auth", response_model=AppUserAuthResponseSchema)
def auth_app_user(dto: AuthAppUserSchema, repo: AppUserRepoImpl = Depends(get_app_user_repo)):
    """
    Autentica a un usuario de la aplicación por email y contraseña.
    """
    use_case = AuthAppUser(repo)
    app_user = use_case.execute(AuthAppUserDTO(**dto.model_dump()))
    if not app_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return app_user
