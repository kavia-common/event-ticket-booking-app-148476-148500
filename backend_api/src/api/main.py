from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.db import init_db
from src.app.routes import auth as auth_routes
from src.app.routes import events as events_routes

# Create FastAPI app with metadata for OpenAPI docs
app = FastAPI(
    title="Event Ticket Booking API",
    description="Backend API for authentication, event listing, seat selection, and payments (stubs).",
    version="0.1.0",
    contact={"name": "Event Ticket Booking"},
    license_info={"name": "MIT"},
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS for mobile frontend and dev wildcard
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*",  # dev wildcard
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with tags
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(events_routes.router, prefix="/events", tags=["Events"])

# PUBLIC_INTERFACE
@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    """Simple health endpoint to verify the service is running."""
    return {"message": "Healthy"}

# Init DB on startup
@app.on_event("startup")
async def on_startup():
    """Initialize database and create tables on app startup."""
    init_db()
