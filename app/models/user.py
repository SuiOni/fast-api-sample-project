
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String
from sqlalchemy_utils import URLType, UUIDType
from sqlalchemy.orm import relationship

import uuid

from app.core.config import settings
# from furl import furl

from app.db.base_class import Base

if TYPE_CHECKING:
    from .idea import Idea  # noqa: F401


class User(Base):
    id = Column(UUIDType, primary_key=True, index=True,
                default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar_url = Column(URLType, nullable=True, default=settings.GRAVATAR_DEFAULT_URL)
    is_active = Column(Boolean(), default=True)
    ideas = relationship("Idea", back_populates="owner")
