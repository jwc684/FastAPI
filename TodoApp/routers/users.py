from fastapi import HTTPException, status, Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..models import Users
from ..database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRequest(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=100)
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    is_active: bool
    role: str = Field(min_length=3, max_length=100)
    phone_number: str = Field(min_length=3, max_length=100)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: user_dependency,
                      db: db_dependency,
                      user_request: UserRequest,
                      user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentification Failed')

    user_model = db.query(Users).filter(Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')

    user_model.email = user_request.email
    user_model.username = user_request.username
    user_model.last_name = user_request.last_name
    user_model.first_name = user_request.first_name
    user_model.is_active = user_request.is_active
    user_model.role = user_request.role
    user_model.phone_number = user_request.phone_number

    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency, db: db_dependency, phone_number: str):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentification Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()





