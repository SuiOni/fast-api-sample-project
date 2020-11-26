from sqlalchemy.orm import Session

from app.db import base  # noqa: F401
from app.db import session


def init_db(db: Session) -> None:
    base.Base.metadata.create_all(bind=session.engine)
