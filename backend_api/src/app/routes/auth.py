from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from src.app.db import get_session
from src.app.models import User
from src.app.schemas import LoginRequest, MeResponse, RegisterRequest, TokenResponse
from src.app.services.auth import create_jwt, get_current_user, hash_password, verify_password

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/register", response_model=MeResponse, summary="Register a new user")
def register(payload: RegisterRequest, session=Depends(get_session)):
    """
    Register a new user with email and password.

    Parameters:
    - email: Email address
    - password: Password (min 6 chars)
    - full_name: Optional full name

    Returns:
    - MeResponse: Created user details (without sensitive info)
    """
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return MeResponse(id=user.id, email=user.email, full_name=user.full_name)

# PUBLIC_INTERFACE
@router.post("/login", response_model=TokenResponse, summary="Login and get JWT")
def login(payload: LoginRequest, session=Depends(get_session)):
    """
    Login with email and password to receive a JWT.

    Returns:
    - TokenResponse: access_token and token_type
    """
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_jwt({"sub": user.id})
    return TokenResponse(access_token=token, token_type="bearer")

# PUBLIC_INTERFACE
@router.get("/me", response_model=MeResponse, summary="Get current user")
def me(current=Depends(get_current_user)):
    """
    Retrieve the current authenticated user.

    Authorization:
    - Bearer token (JWT) required

    Returns:
    - MeResponse: Authenticated user details
    """
    return MeResponse(id=current.id, email=current.email, full_name=current.full_name)
