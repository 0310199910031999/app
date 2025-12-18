from mainContext.application.ports.AppUserRepo import AppUserRepo
from mainContext.application.dtos.app_user_dto import (
    AppUserDTO,
    AppUserCreateDTO,
    AppUserUpdateDTO,
    AuthAppUserDTO,
    AppUserAuthResponseDTO,
    ClientDTO,
)
from mainContext.infrastructure.models import AppUsers as AppUserModel, Clients as ClientModel
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

class AppUserRepoImpl(AppUserRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_app_user(self, dto: AppUserCreateDTO) -> int:
        try:
            model = AppUserModel(
                client_id=dto.client_id,
                name=dto.name,
                lastname=dto.lastname,
                email=dto.email,
                password=dto.password,
                phone_number=dto.phone_number,
                token_fcm=dto.token_fcm
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar usuario en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear usuario: {str(e)}")

    def get_app_user_by_id(self, id: int) -> Optional[AppUserDTO]:
        try:
            model = (
                self.db.query(AppUserModel)
                .filter_by(id=id)
                .first()
            )
            
            if not model:
                return None
            
            
            return AppUserDTO(
                id=model.id,
                client_id=model.client_id,
                name=model.name,
                lastname=model.lastname,
                email=model.email,
                password=model.password,
                phone_number=model.phone_number,
                token_fcm=model.token_fcm
            )
        except Exception as e:
            raise Exception(f"Error al obtener usuario: {str(e)}")

    def get_all_app_users(self) -> List[AppUserDTO]:
        try:
            models = (
                self.db.query(AppUserModel)
                .all()
            )
            
            result = []
            for model in models:
                        
                
                result.append(AppUserDTO(
                    id=model.id,
                    client_id=model.client_id,
                    name=model.name,
                    lastname=model.lastname,
                    email=model.email,
                    password=model.password,
                    phone_number=model.phone_number,
                    token_fcm=model.token_fcm,
                ))
            
            return result
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")

    def get_app_users_by_client(self, client_id: int) -> List[AppUserDTO]:
        try:
            models = (
                self.db.query(AppUserModel)
                .filter_by(client_id=client_id)
                .all()
            )
            
            result = []
            for model in models:
                
                result.append(AppUserDTO(
                    id=model.id,
                    client_id=model.client_id,
                    name=model.name,
                    lastname=model.lastname,
                    email=model.email,
                    password=model.password,
                    phone_number=model.phone_number,
                    token_fcm=model.token_fcm,
                ))
            
            return result
        except Exception as e:
            raise Exception(f"Error al obtener usuarios por cliente: {str(e)}")

    def update_app_user(self, id: int, dto: AppUserUpdateDTO) -> bool:
        try:
            model = self.db.query(AppUserModel).filter_by(id=id).first()
            
            if not model:
                return False
            
            update_data = dto.model_dump(exclude_none=True)
            
            for key, value in update_data.items():
                setattr(model, key, value)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar usuario: {str(e)}")

    def delete_app_user(self, id: int) -> bool:
        try:
            model = self.db.query(AppUserModel).filter_by(id=id).first()
            
            if not model:
                return False
            
            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar usuario: {str(e)}")

    def auth_app_user(self, auth_dto: AuthAppUserDTO) -> Optional[AppUserAuthResponseDTO]:
        try:
            model = (
                self.db.query(AppUserModel)
                .options(joinedload(AppUserModel.client))
                .filter_by(email=auth_dto.email, password=auth_dto.password)
                .first()
            )

            if not model:
                return None

            client_name = model.client.name if model.client else None

            return AppUserAuthResponseDTO(
                id=model.id,
                client_id=model.client_id,
                client_name=client_name,
                name=model.name,
                lastname=model.lastname,
                email=model.email,
                phone_number=model.phone_number,
                token_fcm=model.token_fcm,
            )
        except Exception as e:
            raise Exception(f"Error al autenticar usuario: {str(e)}")

    def listWithClientName(self) -> List[dict]:
        try:
            result = (
                self.db.query(
                    AppUserModel.id,
                    AppUserModel.name,
                    AppUserModel.lastname,
                    AppUserModel.email,
                    AppUserModel.phone_number,
                    ClientModel.name.label('client_name')
                )
                .join(ClientModel, AppUserModel.client_id == ClientModel.id, isouter=True)
                .all()
            )
            
            return [
                {
                    "id": row.id,
                    "name": row.name,
                    "lastname": row.lastname,
                    "email": row.email,
                    "phone_number": row.phone_number,
                    "client_name": row.client_name
                }
                for row in result
            ]
        except Exception as e:
            raise Exception(f"Error al listar usuarios con cliente: {str(e)}")