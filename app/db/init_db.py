from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base, session  # noqa: F401

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    base.Base.metadata.create_all(bind=session.engine)

   