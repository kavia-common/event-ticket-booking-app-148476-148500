from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """User model with basic fields for authentication."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    full_name: Optional[str] = None


class Event(SQLModel, table=True):
    """Event model for listing and details."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: str  # ISO date string for simplicity
    venue: str
    price_from: float
