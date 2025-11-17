# event-ticket-booking-app-148476-148500

Backend (FastAPI) quick start

- From the backend_api directory:
  - Create/activate your venv as needed.
  - Install deps: pip install -r requirements.txt
  - Run dev server: uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

OpenAPI docs: http://localhost:3001/docs

Endpoints
- GET /             Health
- POST /auth/register  {email, password, full_name?}
- POST /auth/login     {email, password} -> {access_token}
- GET /auth/me         (Bearer token) -> current user
- GET /events          List events [{id,title,date,venue,priceFrom}]
- GET /events/{id}     Event details + seatingSummary
- GET /events/{id}/seats  Sample 10x12 grid of seat availability

Notes
- SQLite (app.db) auto-created on startup; schema is auto-managed with SQLModel.
- CORS allows http://localhost:3000 and dev wildcard.
- No external services or env variables required.