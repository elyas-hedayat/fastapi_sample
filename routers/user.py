from fastapi import APIRouter, status, HTTPException

from dependencies import SessionDep, Hasher
from models.user import User
from schemas.user import RegisterOutput, RegisterInput

router = APIRouter()


@router.post("/register", response_model=RegisterOutput, status_code=status.HTTP_201_CREATED)
def register_user(data: RegisterInput, session: SessionDep):
    instance = User.model_validate(data)
    password_hash = Hasher.get_password_hash(instance.password)
    instance.password = password_hash
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


@router.post("/login", response_model=RegisterOutput, status_code=status.HTTP_200_OK)
def login_user(data: RegisterInput, session: SessionDep):
    instance = session.query(User).filter(User.username == data.username).first()
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hasher.verify_password(data.password, instance.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return instance
