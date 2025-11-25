from fastapi import APIRouter, status, HTTPException, Depends

from dependencies import SessionDep, Hasher, get_current_user
from jwt_auth import sign_jwt
from models.user import User
from schemas.auth import ChangePasswordInput
from schemas.user import RegisterOutput, RegisterInput

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(data: RegisterInput, session: SessionDep):
    instance = User.model_validate(data)
    password_hash = Hasher.get_password_hash(instance.password)
    instance.password = password_hash
    session.add(instance)
    session.commit()
    session.refresh(instance)
    access_token = sign_jwt(instance.id)
    return access_token


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(data: RegisterInput, session: SessionDep):
    instance = session.query(User).filter(User.username == data.username).first()
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hasher.verify_password(data.password, instance.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    access_token = sign_jwt(instance.id)
    return access_token


@router.post("/change_password", status_code=status.HTTP_200_OK)
def change_password(
        data: ChangePasswordInput,
        session: SessionDep,
        current_user: User = Depends(get_current_user),
):
    if not Hasher.verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password")

    if Hasher.verify_password(data.new_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="New password cannot be the same as the old password")

    current_user.password = Hasher.get_password_hash(data.new_password)

    session.commit()
    session.refresh(current_user)

    return {"message": "Password changed successfully"}
