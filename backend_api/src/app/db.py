from contextlib import contextmanager
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine

# SQLite file DB for simplicity. No env vars required as per task constraints.
SQLITE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLITE_URL, echo=False, connect_args={"check_same_thread": False}
)

def init_db() -> None:
    """Create database tables. Seed sample data if needed."""
    from src.app import models  # noqa: F401 - ensure models are imported for table creation
    SQLModel.metadata.create_all(engine)
    _seed_if_empty()

@contextmanager
def get_session() -> Iterator[Session]:
    """Yield a SQLModel session."""
    with Session(engine) as session:
        yield session

def _seed_if_empty() -> None:
    """Seed initial events if the table is empty."""
    from sqlmodel import select
    from src.app.models import Event
    with Session(engine) as session:
        count = session.exec(select(Event)).first()
        if count is None:
            events = [
                Event(
                    title="Rock Fest 2025",
                    description="Annual rock music festival featuring top bands.",
                    date="2025-12-20",
                    venue="City Arena",
                    price_from=49.99,
                ),
                Event(
                    title="Tech Conference",
                    description="Talks and workshops on emerging technologies.",
                    date="2025-11-15",
                    venue="Convention Center",
                    price_from=99.00,
                ),
                Event(
                    title="Stand-up Night",
                    description="Comedy night with renowned comedians.",
                    date="2025-10-05",
                    venue="Downtown Theater",
                    price_from=25.00,
                ),
            ]
            for e in events:
                session.add(e)
            session.commit()
