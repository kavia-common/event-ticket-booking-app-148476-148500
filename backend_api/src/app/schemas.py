from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# AUTH SCHEMAS

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")
    full_name: Optional[str] = Field(None, description="Full name")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class MeResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]


# EVENT SCHEMAS

class EventItem(BaseModel):
    id: int
    title: str
    date: str
    venue: str
    priceFrom: float


class EventDetails(BaseModel):
    id: int
    title: str
    description: str
    date: str
    venue: str
    priceFrom: float
    seatingSummary: str


class SeatCell(BaseModel):
    row: int
    col: int
    available: bool
    price: float


class SeatsGrid(BaseModel):
    rows: int
    cols: int
    seats: List[SeatCell]
