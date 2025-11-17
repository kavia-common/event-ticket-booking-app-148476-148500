import base64
import hashlib
import hmac
import json
import time
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.app.db import get_session
from src.app.models import User

# Simple secret for demo (no env vars per constraints)
JWT_SECRET = "demo_secret_change_me"
JWT_ALG = "HS256"
JWT_EXP_SECONDS = 60 * 60 * 24  # 24h

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def hash_password(password: str) -> str:
    """Hash password using SHA256 for quick start (replace with bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password by comparing SHA256 hashes."""
    return hash_password(password) == password_hash

def _sign(data: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode(), data, hashlib.sha256).digest()
    return _b64url_encode(sig)

def create_jwt(payload: dict, secret: str = JWT_SECRET, exp_seconds: int = JWT_EXP_SECONDS) -> str:
    """Create a minimal HS256 JWT token."""
    header = {"alg": JWT_ALG, "typ": "JWT"}
    payload = payload.copy()
    payload["exp"] = int(time.time()) + exp_seconds
    encoded_header = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{encoded_header}.{encoded_payload}".encode()
    signature = _sign(signing_input, secret)
    return f"{encoded_header}.{encoded_payload}.{signature}"

def decode_jwt(token: str, secret: str = JWT_SECRET) -> Optional[dict]:
    """Decode and verify a minimal HS256 JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig = parts
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = _sign(signing_input, secret)
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = json.loads(_b64url_decode(payload_b64))
        if "exp" in payload and int(time.time()) > int(payload["exp"]):
            return None
        return payload
    except Exception:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)) -> User:
    """FastAPI dependency to get the current user from JWT token."""
    payload = decode_jwt(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload["sub"]
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
